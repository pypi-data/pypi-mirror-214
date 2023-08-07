"""! @brief Set Data stage, writing obtained data onto a database."""
import sys
from typing import Any
from json import loads as json_loads
from google.cloud import bigquery

from gaiaframework.base.batch.stage_base import DS_Stage


##
# @file
# @brief Stage main class, implements DS_Stage base class.
class SetDataStage(DS_Stage):
    """! Stage class

    Implement a stage that will later be converted to an executable job in a specific workflow.
    """

    def __init__(self, stage_config):
        """! The Stage class (generatedStageName) initializer.
        Base class will load basic configuration parameters, additional fields should be added here

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(stage_config)
        self.start_date = ""
        if 'user_email' in stage_config:
            self.user_email = stage_config['user_email']

        if self.unique_iteration_id:
            self.folder_path = self.project_name + '/' + self.user_email + \
                               '/unique_iteration_id_' + self.unique_iteration_id
        else:
            self.folder_path = self.project_name + '/' + self.user_email + '/main'

        self.bucket_path = f'gs://{self.bucket_name}/{self.folder_path}'

    def set_start_date(self, start_time):
        """! Setting start date, if available.
            Args:
                start_time - Stage start time
        """
        print(f'Setting start date: {start_time}')
        self.start_date = start_time

    def get_stage_name(self):
        """! Get the stage name

            Returns:
                A string, containing the stage's name
        """
        return self.__class__.__name__

    def main(self, **kwargs: Any):
        """! Executes the main functionality of the stage.

            Args:
                **kwargs : Whatever is needed for the stage to run properly.
        """
        ds_source = "zido-prd-svpc-4"
        date_str = "2021-10-12"
        inputParquetName = "stage_load_join_ner_data"
        outputParquetName = "stage_load_join_ner_data"

        spark = self.load_spark()

        page_list = spark.read.parquet(f"{self.bucket_path}/data/{inputParquetName}.parquet")
        page_list.printSchema()
        page_list.show(5)

        print("X write bigquery X")
        # Update to your GCS bucket
        bq_dataset = self.project_name.replace('-', '_')
        # bq_table = f'stage_crawler_list_{config.limit_table}_{str(config.sample).replace(".", "p")}'
        bq_table = f'stage_crawler_list_latest_batch'

        print(f"{bq_table=}")

        client = bigquery.Client()
        dataset_id = "{}.{}".format(self.project_id, bq_dataset)
        dataset_exist = False

        try:
            client.get_dataset(dataset_id)
            dataset_exist = True
        except:
            pass

        if not dataset_exist:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = self.region
            dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
            print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

        page_list.write \
            .format("bigquery") \
            .option("table", "{}.{}".format(bq_dataset, bq_table)) \
            .option("temporaryGcsBucket", self.bucket_name) \
            .mode('overwrite') \
            .save()


if __name__ == "__main__":
    """! Executes the stage by instantiating it and calling the main function.
    Set up argument condition according to the usage of the written stage

        Args:
            System argument 1 - Configuration file
            System argument 2 - Start date
    """
    if sys.argv and len(sys.argv) > 1:
        config = json_loads(sys.argv[1])
        stage = SetDataStage(config)
        if len(sys.argv) > 2:
            start_date = sys.argv[2]
            stage.update_start_date(start_date)
        stage.main()
    else:
        print(f"Stage configuration not provided, Can't run stage")


