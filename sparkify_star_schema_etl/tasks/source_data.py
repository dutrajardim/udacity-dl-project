import logging
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DoubleType,
    ShortType
)

# log data schema
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

# song data schema
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


def extract_log_data(spark, input_data):
    """
    Description:
        This function is responsible for extract the log data
        with information about song plays.
    
    Arguments:
        spark: Spark session.
        input_data: s3 address where the log data is stored

    Returns:
        A spark data frame with the log data.
    """

    # loading staging log data
    df_log_data = spark.read.format("json") \
        .schema(log_data_schema) \
        .option("recursiveFileLookup", True) \
        .load("%slog_data" % input_data)

    return df_log_data


def extract_song_data(spark, input_data):
    """
    Description:
        This function is responsible for extract the song data
        with information about songs and artists.
    
    Arguments:
        spark: Spark session.
        input_data: s3 address where the song data is stored.

    Returns:
        A spark data frame with the song data.
    """

    # loading staging song data
    df_song_data = spark.read.format("json") \
        .schema(song_data_schema) \
        .option("recursiveFileLookup", True) \
        .load("%ssong_data" % input_data)

    return df_song_data