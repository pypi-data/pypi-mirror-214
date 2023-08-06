# it's not the 1980s anymore
# pylint: disable=line-too-long,multiple-imports,logging-fstring-interpolation
"""
A companion for developing Omnata Plugins, including generation of test cases with application request mocking.
"""

from typing import Tuple,Type,Dict, Optional
import re,os,json,random
import pandas,vcr
from snowflake.snowpark.functions import col,lit
from snowflake.snowpark import Session
from tabulate import tabulate
from slugify import slugify
from omnata_plugin_runtime.omnata_plugin import OutboundSyncRequest,OmnataPlugin
from omnata_plugin_runtime.api import OutboundApplyPayload
from omnata_plugin_runtime.configuration import OutboundSyncConfigurationParameters,StoredConfigurationValue,StoredMappingValue,OutboundSyncStrategy,SyncConfigurationParameters,InboundSyncConfigurationParameters
from pydantic import BaseModel, parse_obj_as # pylint: disable=no-name-in-module
from pydantic.json import pydantic_encoder as pydantic_json_encoder # pylint:disable=no-name-in-module

def scrub_secrets(connection_secrets):
    """
    A secret scrubber for pyvcr, to redact the parts of the HTTP request which came from connection secret values
    """
    def before_record_response(request):
        for secret_name,secret_value in connection_secrets.items():
            if request.body is not None:
                try:
                    if 'value' in secret_value:
                        request.body = request.body.decode('utf-8').replace(secret_value['value'], '[redacted]').encode('utf-8')
                    if 'metadata' in secret_value and secret_value['metadata'] is not None:
                        for metadata_secret_name,metadata_secret_value in secret_value['metadata'].items():
                            request.body = request.body.decode('utf-8').replace(metadata_secret_value, '[redacted]').encode('utf-8')
                except UnicodeDecodeError as unicode_decode_error:
                    # sometimes we're not dealing with plain text, e.g. uploading a zip file
                    pass
        return request
    return before_record_response

class SyncScenario:
    """
    Represents a scenario where we sync some data to an app, while capturing records and traffic
    """
    def __init__(self,plugin_id,scenario_name,scenario_records):
        self.scenario_name = scenario_name
        self.scenario_slug = slugify(scenario_name)
        self.scenario_cassette_file_name = f"{plugin_id}_{self.scenario_slug}.yaml"
        self.scenario_cassette_file = os.path.join('features','vcr_cassettes',self.scenario_cassette_file_name)
        self.scenario_records = scenario_records
        self.results = None

class DevelopmentSession:
    """
    Connects to Snowflake and manages test case related concerns
    """
    def __init__(self, omnata_app_name:str,
                        plugin_instance:OmnataPlugin,
                        plugin_module_override:Optional[str]=None):
        self.snowflake_connection_parameters = None
        self.sync_slug = None
        self.results_dataframe = None
        # records property represents the latest record state (net result of all operations)
        self.records = None
        self.omnata_app_name = omnata_app_name
        self.feature_filename = None
        self.cassette_filename = None
        self.plugin_instance = plugin_instance
        self.plugin_module = self.plugin_instance.__module__ if plugin_module_override is None else plugin_module_override
        self.vcr = None
        self.plugin_id = plugin_instance.get_manifest().plugin_id
        self.feature_filename = os.path.join('features',f"{self.plugin_id}.feature")
        self.current_scenario = None
        self.recorded_scenarios = []
        self.failed_source_records = None
        self.run_id = 0
        self.sync_strategy = None
        self.connection_parameters = None
        self.connection_secrets = None
        self.sync_parameters = None
        self.field_mappings = None
        self.api_limits = None
        self.connection_method = None
        self.parameters:SyncConfigurationParameters = None

    def copy_ownership(self,source_table:str,target_table:str):
        """
        Copies the ownership grant from one table to another
        """
        current_owner = None
        current_grants = self.session.sql(f"show grants on table {source_table}").collect()
        for current_grant in current_grants:
            if current_grant['privilege']=='OWNERSHIP':
                current_owner = current_grant['grantee_name']
        if current_owner is None:
            print(f"Failed: cannot determine current owner of {source_table}")

        self.session.sql(f"grant ownership on table {target_table} to role {current_owner}").collect()

    def fetch_record_state(self):
        """
        Collects the full set of records which were previously staged
        """
        return pandas.DataFrame(self.session.table(self.record_state_table_name_full).collect())
    
    def prepare_outbound_scenario(self,
                                scenario_name:str,
                                input_dataframe:pandas.DataFrame,
                                parameters:OutboundSyncConfigurationParameters):
        self.current_scenario = SyncScenario(self.plugin_id,scenario_name,input_dataframe)

        self.parameters = parameters
        outbound_sync_request = OutboundSyncRequest(
                                            run_id=None,
                                            session=self.session,
                                            source_app_name=None,
                                            results_schema_name=None,
                                            results_table_name=None,
                                            plugin_instance=self.plugin_instance,
                                            api_limits=self.api_limits,
                                            rate_limit_state={},
                                            run_deadline=None,
                                            development_mode=True)
        outbound_sync_request._prebaked_record_state = input_dataframe
        self.plugin_instance._sync_request = outbound_sync_request
        self._start_recording()
        return parameters,outbound_sync_request


    def prepare_outbound_scenario_from_sync(self,
            scenario_name:str,
            snowflake_connection_parameters:dict,
            sync_slug:str,
            limit_record_count:int=None) -> Tuple[OutboundSyncConfigurationParameters,OutboundSyncRequest]:
        """
        Stages records into a temporary table and prepares to monitor a test case being executed.
        """
        self.session = Session.builder.configs(self.snowflake_connection_parameters).create()
        self.snowflake_connection_parameters = snowflake_connection_parameters
        self.limit_record_count = limit_record_count
        self.sync_slug = sync_slug
        session_run_response = self.session.sql(f"""
                         call {self.omnata_app_name}.API.CREATE_DEVELOPMENT_SESSION_RUN('{sync_slug}') as RESULT
                         """).collect()
        response_parsed = json.loads(session_run_response[0][0])
        if response_parsed['success']==False:
            raise ValueError(f"Failed: {response_parsed['error']}")
        response_data = response_parsed['data']
        if 'direction' not in response_data:
            raise ValueError(f"Invalid response from CREATE_DEVELOPMENT_SESSION_RUN: {response_data}")
        if response_data['direction']!='outbound':
            raise ValueError(f"The provided sync is not an outbound sync")
        if 'outbound_apply_payload' not in response_data:
            raise ValueError(f"Invalid response from CREATE_DEVELOPMENT_SESSION_RUN: {response_data}")
        if 'plugin_app_name' not in response_data:
            raise ValueError(f"Invalid response from CREATE_DEVELOPMENT_SESSION_RUN: {response_data}")
        plugin_app_name = response_data['plugin_app_name']
        outbound_payload = OutboundApplyPayload.parse_obj(response_data['outbound_apply_payload'])
        # we have everything we need except the secrets, which we fetch from the plugin app
        oauth_secret_param = f"'{outbound_payload.oauth_secret_name}'" if outbound_payload.oauth_secret_name else 'null'
        other_secrets_param = f"'{outbound_payload.other_secrets_name}'" if outbound_payload.other_secrets_name else 'null'
        
        secrets_fetch_response = self.session.sql(f"""
                         call {plugin_app_name}.PLUGIN.RETRIEVE_SECRETS({oauth_secret_param},{other_secrets_param}) as RESULT
                         """).collect()
        secrets_response_parsed = json.loads(secrets_fetch_response[0][0])
        if secrets_response_parsed['success'] is False:
            raise ValueError(f"Failed: {secrets_response_parsed['error']}")
        secrets_data = parse_obj_as(Dict[str,StoredConfigurationValue],secrets_response_parsed['data'])

        self.source_database = self.omnata_app_name
        self.source_schema = outbound_payload.results_schema_name
        self.source_table = outbound_payload.results_table_name
        # clone the current table so that we can use it in it's current form
        #self.temp_table_name = f"{self.source_table}_DEV_SESSION"
        #self.source_table_clone = f"{self.source_database}.{self.source_schema}.{self.temp_table_name}"
        self.full_source_table_name = f"{self.source_database}.{self.source_schema}.{self.source_table}"
        #limit_clause = ''
        #if self.limit_record_count is not None:
        #    limit_clause = f"limit {self.limit_record_count}"
        #self.session.sql((f"create or replace temp table {self.source_table_clone} "
        #    f"as (select * from {self.source_database}.{self.source_schema}.{self.source_table} {limit_clause})")).collect()
        #self.copy_ownership(f"{self.source_database}.{self.source_schema}.{self.source_table}",self.source_table_clone)
        #print(f"Created a cloned, temporary table '{self.temp_table_name}' to use as a source.")

        self.connection_parameters=outbound_payload.connection_parameters
        self.connection_method=outbound_payload.connection_method
        self.connection_secrets=secrets_data
        self.sync_strategy=outbound_payload.sync_strategy
        self.sync_parameters=outbound_payload.sync_parameters
        self.field_mappings=outbound_payload.field_mappings

        self.api_limits=outbound_payload.api_limit_overrides
        #self.api_limits.concurrency = 1 # we have to set this because pyvcr isn't thread safe
        # needs to go in the same schema as original, for the stored proc to find it
        
        # clone the structure of the record state table, we'll stage into it during testing
        #self.session.sql((f"create or replace temp table {self.record_state_table_name_full} "
        #    f" like {record_state_table} COPY GRANTS")).collect()
        # "copy grants" does not include ownership, we have to set that manually
        #self.copy_ownership(record_state_table,self.record_state_table_name_full)
        
        scenario_records = pandas.DataFrame(self.session.table(self.full_source_table_name).collect())
        self.current_scenario = SyncScenario(self.plugin_id,scenario_name,scenario_records)
        parameters = OutboundSyncConfigurationParameters(connection_method=self.connection_method,
                                                    connection_parameters=parse_obj_as(Dict[str,StoredConfigurationValue],self.connection_parameters),
                                                    connection_secrets=parse_obj_as(Dict[str,StoredConfigurationValue],self.connection_secrets),
                                                    sync_parameters=parse_obj_as(Dict[str,StoredConfigurationValue],self.sync_parameters),
                                                    sync_strategy=self.sync_strategy,
                                                    field_mappings=parse_obj_as(StoredMappingValue,self.field_mappings),
                                                    current_form_parameters={})
        outbound_sync_request = OutboundSyncRequest(
                                            run_id=None,
                                            session=self.session,
                                            source_app_name=None,
                                            results_schema_name=None,
                                            results_table_name=None,
                                            plugin_instance=self.plugin_instance,
                                            api_limits=self.api_limits,
                                            rate_limit_state={},
                                            run_deadline=None,
                                            development_mode=True)
        
        outbound_sync_request._record_state_table_name = self.record_state_table_name
        self.plugin_instance._sync_request = outbound_sync_request
        self._start_recording()
        return parameters,outbound_sync_request

    def complete_scenario(self):
        """
        Marks the scenario as complete, and stops recording traffic.
        """
        if self.current_scenario is None:
            return "Failed: you need to call prepare_outbound_scenario('scenario name') first"
        if self.current_scenario.results is None:
            return "Failed: you need to pass the results back to validate_response() before completing the scenario"
        self.recorded_scenarios.append(self.current_scenario)
        self.current_scenario = None
        self._stop_recording()
        print('Success: finished recording scenario')

    def _stop_recording(self):
        """
        Stops the pyvcr recording
        """
        self.vcr.__exit__()

    def _start_recording(self):
        """
        Configures and starts the pyvcr recording
        """
        my_vcr = vcr.VCR(
            before_record_request=scrub_secrets(self.connection_secrets),
            record_mode='all',
            decode_compressed_response=True,
            filter_headers=[('authorization', '[redacted]'),('x-api-key','[redacted]')]
        )
        self.cassette_filename = self.current_scenario.scenario_cassette_file
        if os.path.exists(self.cassette_filename):
            os.remove(self.cassette_filename)
        self.vcr = my_vcr.use_cassette(self.cassette_filename)
        self.vcr.__enter__()

    def _restart_recording(self):
        """
        Stops and starts the recording
        """
        self._stop_recording()
        self._start_recording()

    def validate_response(self,results_dataframe:pandas.DataFrame) -> str:
        """
        Tests that the response to a record apply request is valid. This will check that the DataFrame
        has all of the correct columns, and that results of all the originally requested records are included
        """
        if results_dataframe is None:
            return 'Failed: results were None'
        if self.current_scenario is None:
            return 'Failed: no active scenario'

        originally_provided_records = self.current_scenario.scenario_records

        if originally_provided_records is None:
            return 'Failed: cannot locate originally provided values'
        column_list = list(results_dataframe.columns)
        if 'IDENTIFIER' not in column_list:
            return 'Failed: "IDENTIFIER" column not in dataframe'
        if 'plugin_idENTIFIER' in column_list:
            if not pandas.api.types.is_string_dtype(results_dataframe['plugin_idENTIFIER']):
                return 'Failed: "plugin_idENTIFIER" column is not a string type. Use ".astype(str)" to enforce string conversion'

        if 'SUCCESS' not in column_list:
            return 'Failed: "SUCCESS" column not in dataframe'
        if not pandas.api.types.is_bool_dtype(results_dataframe['SUCCESS']):
            return 'Failed: "SUCCESS" column is not a boolean type'
        if 'RESULT' not in column_list:
            return 'Failed: "RESULT" column not in dataframe'
        if not results_dataframe['RESULT'].dtype=='O':
            return f"Failed: \"RESULT\" column should contain objects, instead the data type is {results_dataframe['RESULT'].dtype}"
        # merge results back on to original, so we can find the missing identifiers
        merged_results = pandas.merge(left=originally_provided_records[['IDENTIFIER']],right=results_dataframe,left_on='IDENTIFIER',right_on='IDENTIFIER',how='left')
        missing_in_results = merged_results['SUCCESS'].isna()
        if missing_in_results.sum() > 0:
            missing_identifiers = merged_results[missing_in_results]['IDENTIFIER']
            print(f'Warning: Missing results for {missing_in_results.sum()} records from apply request: {list(missing_identifiers)}')
        self.current_scenario.results = results_dataframe
        return 'Success: results are valid'
    
    def dataframe_to_behave_table(self,data_frame:pandas.DataFrame,indent_tabs:int,include_data_type:bool=True):
        """
        Converts a pandas DataFrame into a formatted Behave table
        """
        tabulated_df = tabulate(data_frame,headers='keys',tablefmt='pipe',showindex=False,disable_numparse=True)
        # break the string representation of the table into rows so that we can tweak it a bit
        table_lines = re.split('(?<![\\\\])\\n',tabulated_df)
        # remove the line that tabulate puts between heading and values, behave doesn't like it
        del table_lines[1]
        # insert a line at the top for the data type
        top_heading = table_lines[0]
        if include_data_type:
            for df_col in data_frame.columns:
                # just use strings for everything except SUCCESS and RESULT
                if df_col=='SUCCESS':
                    dtype = 'bool'
                elif df_col=='RESULT':
                    dtype = 'object'
                else:
                    dtype = 'str' #str(df[col].dtype)
                top_heading = top_heading.replace(f' {df_col} ',' '+dtype.ljust(len(df_col)+1, ' '))
            table_lines.insert(0,top_heading)
        tabs = indent_tabs*'\t'
        table_lines_indented = [f"{tabs}{line}" for line in table_lines]
        table_indented = '\n'.join(table_lines_indented)
        return table_indented

    def generate_behave_test(self):
        """
        Generates a Python Behave test, following completed test scenarios
        """
        if len(self.recorded_scenarios)==0:
            return 'Failed: No recorded scenarios found - did you forget to call complete_scenario()?'
        if self.current_scenario is not None:
            print('Warning: there is scenario currently running, please call complete_scenario() if you want it included')
        # strip unescaped newlines from json string
        secrets_redacted = {}
        for secret,value in self.parameters.connection_secrets.items():
            new_secret = {}
            if isinstance(value,StoredConfigurationValue):
                value.value = '[redacted]'
            else:
                raise ValueError(f"Secret {secret} does not contain a StoredConfigurationValue")
            secrets_redacted[secret] = value.dict()
        if isinstance(OutboundSyncConfigurationParameters,self.parameters):
            outbound_params:OutboundSyncConfigurationParameters = self.parameters
            properties_df = pandas.DataFrame([
                {"Property":"strategy","Value": json.dumps(outbound_params.sync_strategy,default=pydantic_json_encoder)},
                {"Property":"connection_method","Value": self.connection_method},
                {"Property":"connection_parameters","Value": json.dumps(outbound_params.connection_parameters,default=pydantic_json_encoder)},
                {"Property":"connection_secrets","Value": json.dumps(secrets_redacted,default=pydantic_json_encoder)},
                {"Property":"api_limits","Value": json.dumps(self.api_limits,default=pydantic_json_encoder)},
                {"Property":"sync_parameters","Value": json.dumps(outbound_params.sync_parameters,default=pydantic_json_encoder).replace('|','\\|')},
                {"Property":"field_mappings","Value": json.dumps(outbound_params.field_mappings,default=pydantic_json_encoder).replace('|','\\|')}
            ])
        else:
            inbound_params:InboundSyncConfigurationParameters = self.parameters
            properties_df = pandas.DataFrame([
                {"Property":"connection_method","Value": self.connection_method},
                {"Property":"connection_parameters","Value": json.dumps(inbound_params.connection_parameters,default=pydantic_json_encoder)},
                {"Property":"connection_secrets","Value": json.dumps(secrets_redacted,default=pydantic_json_encoder)},
                {"Property":"api_limits","Value": json.dumps(self.api_limits,default=pydantic_json_encoder)},
                {"Property":"sync_parameters","Value": json.dumps(inbound_params.sync_parameters,default=pydantic_json_encoder).replace('|','\\|')}
            ])

        f = open(self.feature_filename, "w", encoding='utf-8')
        print(f'Writing feature file: {self.feature_filename}\n')
        f.write(f"Feature: Apply records for the {self.sync_slug} sync\n")
        for recorded_scenario in self.recorded_scenarios:
            print(f'Writing scenario: {recorded_scenario.scenario_name} cassette: {recorded_scenario.scenario_cassette_file_name}\n')
            #recorded_scenario.scenario_records["TRANSFORMED_RECORD"]=recorded_scenario.scenario_records.TRANSFORMED_RECORD.apply(lambda x: x.replace('(?<![\\\\])\\n','').replace('|','\\\\|'))

            recorded_scenario.scenario_records['TRANSFORMED_RECORD'] = recorded_scenario.scenario_records['TRANSFORMED_RECORD'].str.replace('(?<![\\\\])\\n','').str.replace('|','\\|')
            # sometimes the transformed record may contain pipe symbols (especially jinja templates), so we need to escape them so that the behave table is valid
            #recorded_scenario.scenario_records['TRANSFORMED_RECORD'] = recorded_scenario.scenario_records['TRANSFORMED_RECORD'].apply(lambda x: json.loads(json.dumps(x).replace('|','\\\\|')))
            #self.all_records_to_create['SYNC_ACTION']='CREATE'
            #recorded_scenario.scenario_slug

            f.write(f"\tScenario: {recorded_scenario.scenario_name}\n")
            f.write("\t\tGiven the following records:\n")
            table_indented = self.dataframe_to_behave_table(recorded_scenario.scenario_records[['IDENTIFIER','SYNC_ACTION','TRANSFORMED_RECORD']],3)
            f.write(f"{table_indented}\n")
            f.write(f"\t\tAnd we use the HTTP recordings from {recorded_scenario.scenario_cassette_file_name}\n")
            table_indented = self.dataframe_to_behave_table(properties_df,3,include_data_type=False)
            f.write(f"\t\tAnd we use the {self.plugin_instance.__class__.__name__} class from the {self.plugin_module} module\n")
            f.write("\t\tWhen we apply the records to the app with configuration parameters:\n")
            f.write(f"{table_indented}\n")
            f.write('\t\tThen no error will be raised\n')
            f.write('\t\tAnd the response will be:\n')
            #self.create_results['TRANSFORMED_RECORD']=self.create_results['TRANSFORMED_RECORD'].apply(json.dumps)
            recorded_scenario.results['RESULT']=recorded_scenario.results['RESULT'].apply(json.dumps)
            recorded_scenario.results.loc[recorded_scenario.results["RESULT"]=='"null"', "RESULT"] = 'null'
            recorded_scenario.results = recorded_scenario.results[recorded_scenario.results.columns.intersection(['IDENTIFIER','SUCCESS','plugin_idENTIFIER','RESULT'])]
            table_indented = self.dataframe_to_behave_table(recorded_scenario.results,3)
            f.write(f"{table_indented}\n")

        f.close()
        print('Finished writing feature file')
        steps_importer_file = os.path.join('features','steps','imported_steps.py')
        os.makedirs(os.path.dirname(steps_importer_file), exist_ok=True)
        print(f'Writing steps importer file: {steps_importer_file}\n')
        with open(steps_importer_file, 'w') as f:
            f.write('import omnata_plugin_sdk.test_step_definitions')
        print(f'Success: wrote out all test-related files\n')
        print(f'You can now run the tests by installing the "behave" package and running "behave features" from the root of your plugin ("!behave features" from within a Jupyter cell)\n')
