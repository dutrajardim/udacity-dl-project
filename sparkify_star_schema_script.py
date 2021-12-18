import logging
from pyspark.sql import SparkSession
from sparkify_star_schema_etl.job import sparkify_star_schema_job

if __name__ == '__main__':
    logger = logging.getLogger("data_lake_project")
    logger.setLevel(logging.INFO)
    logger.info("Starting Data Lake Project")

    spark = SparkSession.builder \
        .appName("Udacity - Data Lake Project") \
        .getOrCreate()

    input_data = "s3a://udacity-dend/"
    output_data = "s3a://dutrajardim/udacity-dl-project/"

    sparkify_star_schema_job(spark, input_data, output_data)
    spark.stop()