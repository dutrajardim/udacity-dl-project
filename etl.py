import configparser
import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, expr

from schemas import (
    song_data_schema,
    log_data_schema,
    user_table_schema,
    song_table_schema,
    artist_table_schema,
    songplay_table_schema,
    time_table_schema,
    user_table_schema_with_start_time,
)

from basic_pipeline import create_basic_pipeline


def extract_artists(df_song_data):
    # fmt: off
    # defining basic pipeline with rename transformations
    basic_pipeline = create_basic_pipeline(
        rename_transformations={
            "name": "artist_name",
            "location": "artist_location",
            "latitude": "artist_latitude",
            "longitude": "artist_longitude",
        }
    )
    # fmt: on

    # some artist id refer to different artist names (mainly when the song have more
    # then one artist related to it)
    df_artists = basic_pipeline((df_song_data, artist_table_schema)).distinct()
    return df_artists


def extract_songs(df_song_data):
    # defining basic pipeline. For songs table there is no
    # rename and cast transformations
    basic_pipeline = create_basic_pipeline()
    df_songs = basic_pipeline((df_song_data, song_table_schema))

    return df_songs


def extract_users(df_log_data):
    # fmt: off
    # defining basic pipeline with rename and cast transformations
    basic_pipeline = create_basic_pipeline(
        rename_transformations={
            "start_time": "ts",
            "first_name": "firstName",
            "last_name": "lastName",
            "user_id": "userId",
        },
        cast_transformations={
            "start_time": "to_timestamp(start_time / 1000) as start_time",
            "user_id": "INT(user_id) as user_id"
        },
    )
    # fmt: on

    # selecting all user fields, except start_time and level to
    # select duplicates and keep most recent level information
    exceptions_filter = lambda name: name not in ["start_time", "level"]
    uniqueRowFields = list(filter(exceptions_filter, user_table_schema.names))
    df_users = (
        basic_pipeline((df_log_data, user_table_schema_with_start_time))
        .where("user_id IS NOT NULL")
        .orderBy(desc("start_time"))
        .dropDuplicates(uniqueRowFields)
        .drop("start_time")
    )

    return df_users


def extract_songplays(df_joined):
    # fmt: off
    # defining basic pipeline with rename and cast transformations
    basic_pipeline = create_basic_pipeline(
        rename_transformations={
            "start_time": "ts",
            "user_id": "userId",
            "location": "artist_location",
            "session_id": "sessionId",
            "user_agent": "userAgent",
        },
        cast_transformations={
            "start_time": "to_timestamp(start_time / 1000) as start_time",
            "user_id": "INT(user_id) as user_id"
        },
    )

    # applying basic pipeline based on songplays schema
    df_songplays = basic_pipeline((df_joined, songplay_table_schema))
    
    return df_songplays
    # fmt: on


def extract_times(df_songplays):
    # fmt: off
    # defining basic pipeline with rename and cast transformations
    basic_pipeline = create_basic_pipeline(
        cast_transformations={
            "hour": "hour(start_time) as hour",
            "day": "dayofmonth(start_time) as day",
            "week": "weekofyear(start_time) as week",
            "month": "month(start_time) as month",
            "year": "year(start_time) as year",
            "weekday": "dayofweek(start_time) as weekday",
        },
    )

    # applying basic pipeline based on times schema
    df_times = basic_pipeline((df_songplays, time_table_schema)).distinct()
    
    return df_times
    # fmt: on


def save_users(spark, df_users, output_data):
    # set dynamic mode to preserve previous users saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # fmt: off
    # saving users dataset
    df_users.write \
        .option("schema", user_table_schema) \
        .format("parquet") \
        .partitionBy("user_id") \
        .mode("overwrite")\
        .save("%susers.parquet" % output_data)
    # fmt: on


def save_songs(spark, df_songs, output_data):
    # set dynamic mode to preserve previous users saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # fmt: off
    # saving songs dataset
    df_songs.write \
        .partitionBy(['year', 'artist_id', 'song_id']) \
        .option('schema', song_table_schema) \
        .format('parquet') \
        .mode('overwrite') \
        .save('%ssongs.parquet' % output_data)
    # fmt: on


def save_artists(spark, df_artists, output_data):
    # set dynamic mode to preserve previous artists saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # fmt: off
    # saving songs dataset
    df_artists.write \
        .partitionBy(['artist_id', 'name']) \
        .option('schema', artist_table_schema) \
        .format('parquet') \
        .mode('overwrite') \
        .save('%sartists.parquet' % output_data)
    # fmt: on


def save_songplays(spark, df_songplays, output_data):
    # set dynamic mode to preserve previous month of songplays saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # fmt: off
    # saving songs dataset with new year and month columns
    # to create partitions
    df_songplays \
        .withColumn('year', expr("year(start_time)")) \
        .withColumn('month', expr("month(start_time)")) \
        .write \
        .partitionBy(['year', 'month']) \
        .option('schema', songplay_table_schema) \
        .mode('overwrite') \
        .save('%ssongplays.parquet' % output_data)
    # fmt: on


def save_times(spark, df_times, output_data):
    # set dynamic mode to preserve previous month of times saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # fmt: off
    # saving times dataset
    df_times.write \
        .partitionBy(['year', 'month']) \
        .option('schema', time_table_schema) \
        .mode('overwrite') \
        .save('%stimes.parquet' % output_data)
    # fmt: on


def process_data(spark, input_data, output_data):

    # loading staging song data
    df_song_data = (
        spark.read.format("json")
        .schema(song_data_schema)
        .option("recursiveFileLookup", True)
        .load("%ssong_data" % input_data)
    )

    # extracting and saving songs
    df_songs = extract_songs(df_song_data)
    save_songs(spark, df_songs, output_data)

    # extracting and saving artists
    df_artists = extract_artists(df_song_data)
    save_artists(spark, df_artists, output_data)

    # loading staging log data
    df_log_data = (
        spark.read.format("json")
        .schema(log_data_schema)
        .option("recursiveFileLookup", True)
        .load("%slog_data" % input_data)
    )

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

    process_data(spark, input_data, output_data)
    spark.stop()


if __name__ == "__main__":
    main()
