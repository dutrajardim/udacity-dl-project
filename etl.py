# TODO: implement the setuptools

import configparser
import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

from sparkify_star_schema_tasks.users import save_users, extract_users
from sparkify_star_schema_tasks.artists import save_artists, extract_artists
from sparkify_star_schema_tasks.songplays import save_songplays, extract_songplays
from sparkify_star_schema_tasks.songs import save_songs, extract_songs
from sparkify_star_schema_tasks.times import save_times, extract_times

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DoubleType,
    ShortType
)

log_data_schema = StructType(
    [
        StructField("artist", StringType(), True),
        StructField("auth", StringType(), True),
        StructField("firstName", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("itemInSession", IntegerType(), True),
        StructField("lastName", StringType(), True),
        StructField("length", DoubleType(), True),
        StructField("level", StringType(), True),
        StructField("location", StringType(), True),
        StructField("method", StringType(), True),
        StructField("page", StringType(), True),
        StructField("registration", LongType(), True),
        StructField("sessionId", IntegerType(), True),
        StructField("song", StringType(), True),
        StructField("status", ShortType(), True),
        StructField("ts", LongType(), True),
        StructField("userAgent", StringType(), True),
        StructField("userId", StringType(), True),
    ]
)

song_data_schema = StructType(
    [
        StructField("artist_id", StringType(), True),
        StructField("artist_location", StringType(), True),
        StructField("artist_latitude", DoubleType(), True),
        StructField("artist_longitude", DoubleType(), True),
        StructField("artist_name", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("num_songs", ShortType(), True),
        StructField("song_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("year", ShortType(), True),
    ]
)


def sparkify_star_schema_job(spark, input_data, output_data):

    # loading staging song data
    df_song_data = (
        spark.read.format("json")
        .schema(song_data_schema)
        .option("recursiveFileLookup", True)
        .load("%ssong_data" % input_data)
    )

    # loading staging log data
    df_log_data = (
        spark.read.format("json")
        .schema(log_data_schema)
        .option("recursiveFileLookup", True)
        .load("%slog_data" % input_data)
    )

    # extracting and saving songs
    df_songs = extract_songs(df_song_data)
    save_songs(spark, df_songs, output_data)

    # extracting and saving artists
    df_artists = extract_artists(df_song_data)
    save_artists(spark, df_artists, output_data)

    # extracting and saving users
    df_users = extract_users(df_log_data)
    save_users(spark, df_users, output_data)

    # fmt: off
    # prepering songs fields to join log_data
    df_songs_fields = df_songs \
        .select(["song_id", "artist_id", "title", "duration"]) \
        .alias("songs")
    # fmt: on

    # merging song columns tring to find song_id and artist_id
    on_expr = "log_data.song = songs.title AND ROUND(log_data.length, 4) = ROUND(songs.duration, 4)"
    df_joined = df_log_data.alias("log_data").join(
        df_songs_fields,
        on=expr(on_expr),
        how="LEFT",
    )

    # extracting and saving songplays
    df_songplays = extract_songplays(df_joined)
    save_songplays(spark, df_songplays, output_data)

    # extracting and saving times
    df_times = extract_times(df_songplays)
    save_times(spark, df_times, output_data)


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


def main():
    spark = create_spark_session(local=True)
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://dutrajardim/udacity-dl-project/"

    sparkify_star_schema_job(spark, input_data, output_data)
    spark.stop()


if __name__ == "__main__":
    main()
