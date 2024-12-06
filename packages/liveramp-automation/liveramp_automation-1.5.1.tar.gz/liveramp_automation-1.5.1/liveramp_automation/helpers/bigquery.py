import os
import uuid
from google.cloud import bigquery, storage
from liveramp_automation.utils.log import Logger
from liveramp_automation.utils.time import MACROS
from liveramp_automation.helpers.file import FileHelper


class BigQueryConnector:
    def __init__(self, project_id="liveramp-eng-qa-reliability", dataset_id="customer_impact_hours"):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id)

    def connect(self):
        """Connect with specific dataset.

        :return: None."""
        Logger.debug("Start connect")
        try:
            self.client.get_dataset(self.dataset_id)
            Logger.debug(f"Project = {self.project_id} on Dataset = {self.dataset_id}")
            Logger.debug("Finish connect")
            return 0
        except Exception as e:
            Logger.error(f'Error BigQuery Connection: {str(e)}')
            return None

    def query(self, sql_query):
        """Obtain the rows from a SQL.

        :param sql_query: string of SQL sentence.
        :return: list of dictionaries with the rows."""
        Logger.debug("Start query")
        try:
            Logger.debug(f"SQL = {sql_query}")
            query_job = self.client.query(sql_query)
            results = query_job.result()
            result_rows = [row for row in results]
            Logger.debug(result_rows)
            Logger.debug("Finish connect")
            return result_rows
        except Exception as e:
            Logger.error(f'Error SQL Query: {str(e)}')
            return None

    def query_rows(self, sql_query):
        """Obtain the number of rows from a SQL.

        :param sql_query: string of SQL sentence.
        :return: integer with the number of rows."""
        Logger.debug("Start query_rows")
        try:
            Logger.debug(f"SQL = {sql_query}")
            query_job = self.client.query(sql_query)
            results = query_job.result().total_rows
            Logger.debug(results)
            Logger.debug("Finish query_rows")
            return results
        except Exception as e:
            Logger.error(f'Error SQL Query: {str(e)}')
            return None

    def query_export(self, sql_query, output_csv_path):
        """Export the rows from a SQL.

        :param sql_query: string of SQL sentence.
        :param output_csv_path: string of the path for download file.
        :return: integer with the number of rows."""
        Logger.debug("Start query_export")
        try:
            Logger.debug(f"SQL = {sql_query} to  path {output_csv_path}")
            query_job = self.client.query(sql_query)
            df = query_job.to_dataframe()
            df.to_csv(output_csv_path, index=False)
            Logger.debug(df)
            Logger.debug("Finish query_export")
            return 0
        except Exception as e:
            Logger.error(f'Error SQL Query Download: {str(e)}')
            return None

    def dataset_tables(self):
        """Obtain the list with the tables in the dataset.

        :return: list with the names of the tables."""
        Logger.debug("Start dataset_tables")
        try:
            Logger.debug(f"dataset = {self.dataset_id}")
            dataset_ref = self.client.get_dataset(self.dataset_id)
            tables = self.client.list_tables(dataset_ref)
            table_names = [table.table_id for table in tables]
            Logger.debug(table_names)
            Logger.debug("Finish dataset_tables")
            return table_names
        except Exception as e:
            Logger.error(f'Error on dataset info: {str(e)}')
            return None

    def insert_from_bucket(self, bucket_name, source_blob_name, destination_table_name):
        """Insert into table info comes from bucket csv file.

        :param bucket_name: string of bucket name files csv comes from.
        :param source_blob_name: string of the path from csv file in the bucket.
        :param destination_table_name: string of table name.
        :return: None."""
        Logger.debug("Start insert_from_bucket")
        try:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(source_blob_name)

            dataset_ref = self.client.get_dataset(self.dataset_id)
            table_ref = dataset_ref.table(destination_table_name)
            table = self.client.get_table(table_ref)

            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.skip_leading_rows = 1

            load_job = self.client.load_table_from_uri(
                blob.public_url,
                table_ref,
                job_config=job_config
            )

            result = load_job.result()

            Logger.debug(result)
            Logger.debug(f'Data loaded in table "{destination_table_name}" from bucket "{bucket_name}"')
            Logger.debug("Finish insert_from_bucket")
            return result
        except Exception as e:
            Logger.error(f'Error on load data: {str(e)}')
            return None

    def insert_from_pytest_bdd_cucumber_report(self,
                                               report_path="reports/cucumber.json",
                                               round_table_ref="bbm_round_table",
                                               feature_table_ref="bbm_feature_table",
                                               scenario_table_ref="bbm_scenario_table",
                                               step_table_ref="bbm_step_table"
                                               ):
        """
        Insert the information from a pytest-bdd cucumber report into BigQuery.

        :param report_path: Path to the pytest-bdd cucumber report file.
        :param round_table_ref: Reference to the BigQuery table for storing round information.
        :param feature_table_ref: Reference to the BigQuery table for storing feature information.
        :param scenario_table_ref: Reference to the BigQuery table for storing scenario information.
        :param step_table_ref: Reference to the BigQuery table for storing step information.
        :return: 0 if successful, None if errors occurred during insertion.
        """
        report_context = FileHelper.read_json_report(report_path)
        client = bigquery.Client()
        unique_id = str(uuid.uuid4())
        rounds = []
        features = []
        scenarios = []
        steps = []

        for feature in report_context:
            feature_row = {"id": unique_id,
                           "feature_id": unique_id,
                           "feature_uri": feature["uri"],
                           "feature_name": feature["name"],
                           "feature_description": feature["description"],
                           "feature_line": feature["line"],
                           "feature_keyword": feature["keyword"],
                           "feature_timestamp": MACROS["now_readable"]
                           }

            feature_scenarios, feature_steps = self._get_scenarios_steps_from_feature_(feature, unique_id)
            scenarios = scenarios + feature_scenarios
            steps = steps + feature_steps

            feature_row["scenarios"] = ",".join(map(lambda x: x["id"], feature_scenarios))
            Logger.debug(f'Feature Row: {feature_row}')
            features.append(feature_row)

        round_execution_result = "PASS"
        failed_count = 0
        failed_step_id = set()
        for step in steps:
            if step["step_status"].lower() == "failed" and step["id"] not in failed_step_id:
                failed_count += 1
                failed_step_id.add(step["id"])

        if failed_count > 0:
            round_execution_result = "FAIL"
        test_round = {"id": unique_id,
                      "round_id": MACROS["now"],
                      "round_execution_env": os.environ.get('ENVCHOICE', 'PROD').upper(),
                      "round_execution_product": os.environ.get('PRODUCTNAME', '').upper(),
                      "round_execution_time": MACROS["now"],
                      "round_timestamp": MACROS["now_readable"],
                      "round_feature_ids": ",".join(map(lambda x: x["id"], features)),
                      "round_execution_result": round_execution_result,
                      "round_scenario_numbers": len(scenarios),
                      "round_step_failed_numbers": failed_count
                      }
        rounds.append(test_round)
        round_table = client.get_table(round_table_ref)
        round_table_errors = client.insert_rows(round_table, rounds)
        if round_table_errors:
            Logger.error(f'Round Table errors: {str(round_table_errors)}')
            return -1

        feature_table = client.get_table(feature_table_ref)
        feature_errors = client.insert_rows(feature_table, features)
        if feature_errors:
            Logger.error(f'Feature Table errors: {str(feature_errors)}')
            return -1

        scenario_table = client.get_table(scenario_table_ref)
        scenario_errors = client.insert_rows(scenario_table, scenarios)
        if scenario_errors:
            Logger.error(f'Scenario table errors: {str(scenario_errors)}')
            return -1

        step_table = client.get_table(step_table_ref)
        step_errors = client.insert_rows(step_table, steps)
        if step_errors:
            Logger.error(f'Step Table errors: {str(step_errors)}')
            return -1

        return 0

    def _get_scenarios_steps_from_feature_(self, feature, unique_id):
        scenarios = []
        steps = []
        for scenario in feature["elements"]:
            scenario_row = {"id": unique_id,
                            "scenario_id": scenario["id"],
                            "scenario_name": scenario["name"],
                            "scenario_description": scenario["description"],
                            "scenario_line": scenario["line"],
                            "scenario_keyword": scenario["keyword"],
                            "scenario_timestamp": MACROS["now_readable"],
                            "scenario_tags": ",".join(map(lambda x: x["name"], scenario["tags"]))}
            scenario_steps = self._get_steps_from_scenario_(scenario, unique_id)
            step_ids = map(lambda x: x["id"], scenario_steps)
            scenario_row['scenario_steps'] = ",".join(step_ids)
            steps = steps + scenario_steps
            scenarios.append(scenario_row)
        return scenarios, steps

    def _get_steps_from_scenario_(self, scenario, unique_id):
        steps = []
        for step in scenario["steps"]:
            step_row = {"id": unique_id,
                        "step_name": step["name"],
                        "step_keyword": step["keyword"],
                        "step_line": step["line"],
                        "step_status": step["result"]["status"],
                        "step_duration": step["result"]["duration"],
                        "step_location": step["match"]["location"],
                        "step_timestamp": MACROS["now_readable"]}
            if "error_message" in step["result"]:
                step_row["step_error_message"] = step["result"]["error_message"]
            steps.append(step_row)
        return steps
