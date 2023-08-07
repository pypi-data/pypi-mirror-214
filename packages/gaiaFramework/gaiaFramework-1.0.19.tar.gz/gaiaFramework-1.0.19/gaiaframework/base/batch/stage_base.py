"""! @brief DS_Stage base class for the batch stage class."""

import json
import sys
from pyspark.sql import SparkSession
from typing import List, Any

##
# @file
# @brief Defines stage base class.
class DS_Stage():
    def __init__(self, stage_config):
        """! DS_Stage initializer.
        Loads config file.

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.

        """
        self.bucket_name = stage_config['bucket_name']
        self.project_id = stage_config['project_id']
        self.project_name = stage_config['project_name']
        self.region = stage_config['region']
        self.unique_iteration_id = stage_config['unique_iteration_id']
        if self.unique_iteration_id:
            print(f'unique_iteration_id: {self.unique_iteration_id}')
            self.project_name = self.project_name + '/unique_iteration_id_' + self.unique_iteration_id
        else:
            self.project_name = self.project_name + '/main'

        self.bucket_path = f'gs://{self.bucket_name}/{self.project_name}'
        self.start_date = ""

    def update_start_date(self, stage_start_date):
        """! Update start date
            ARGS:
                stage_start_date: String, containing the starting date, received from Airflow
        """
        print(f'Setting start date: {stage_start_date}')
        self.start_date = stage_start_date

    def main(self, **kwargs: Any):
        """! DS_Stage main function.
        This function is the "entrypoint" for the stage, this will run when the job is executed.

            Args:
                **kwargs : Whatever is needed for the stage to run properly.
        """
        raise NotImplementedError

    def load_spark(self) -> SparkSession:   # TODO: Generalize this in order to receive config options.
        """! Basic loading of a spark session.

            Returns:
                A basic spark session
        """
        spark = SparkSession.builder \
            .appName(self.project_name) \
            .config('spark.ui.showConsoleProgress', True) \
            .config("spark.sql.parquet.compression.codec", "gzip") \
            .config('spark.jars', 'gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar') \
            .getOrCreate()

        print(f"Spark ID: {spark.sparkContext.applicationId}")
        return spark




