import configparser
from datetime import datetime
import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


def create_spark_conf(local=False):
    config = configparser.ConfigParser()
    config.optionxform = str
    spark_config = SparkConf()
    spark_config.setAppName("Udacity - Data Lake Project")

    if local:
        filepath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "local.sparkconf.cfg"
        )
        config.read_file(open(filepath))
        spark_config.setMaster(config["SPARK"]["master"])

        for section in config.sections():
            if section in ["SPARK"]:
                continue

            for item in config.items(section):
                spark_config.set(*item)

    return spark_config


def create_spark_session(local=False):
    conf = create_spark_conf(local=local)
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    return spark


def process_song_data(spark, input_data, output_data):
    pass
    # get filepath to song data file
    # song_data =

    # read song data file
    # df =

    # extract columns to create songs table
    # songs_table =

    # write songs table to parquet files partitioned by year and artist
    # songs_table

    # extract columns to create artists table
    # artists_table =

    # write artists table to parquet files
    # artists_table


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    # log_data =

    # read log data file
    # df =

    # filter by actions for song plays
    # df =

    # extract columns for users table
    # artists_table =

    # write users table to parquet files
    # artists_table

    # create timestamp column from original timestamp column
    get_timestamp = udf()
    # df =

    # create datetime column from original timestamp column
    get_datetime = udf()
    # df =

    # extract columns to create time table
    # time_table =

    # write time table to parquet files partitioned by year and month
    # time_table

    # read in song data to use for songplays table
    # song_df =

    # extract columns from joined song and log datasets to create songplays table
    # songplays_table =

    # write songplays table to parquet files partitioned by year and month
    songplays_table


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
