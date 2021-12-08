from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DoubleType,
    ShortType,
    TimestampType,
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

user_table_schema = StructType(
    [
        StructField("user_id", IntegerType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("level", StringType(), True),
    ]
)

song_table_schema = StructType(
    [
        StructField("song_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("artist_id", StringType(), True),
        StructField("year", ShortType(), True),
        StructField("duration", DoubleType(), True),
    ]
)

artist_table_schema = StructType(
    [
        StructField("artist_id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("location", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
    ]
)

songplay_table_schema = StructType(
    [
        StructField("start_time", TimestampType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("level", StringType(), True),
        StructField("song_id", StringType(), True),
        StructField("artist_id", StringType(), True),
        StructField("session_id", IntegerType(), True),
        StructField("location", StringType(), True),
        StructField("user_agent", StringType(), True),
    ]
)

time_table_schema = StructType(
    [
        StructField("start_time", TimestampType(), True),
        StructField("hour", ShortType(), True),
        StructField("day", ShortType(), True),
        StructField("week", ShortType(), True),
        StructField("month", ShortType(), True),
        StructField("year", ShortType(), True),
        StructField("weekday", ShortType(), True),
    ]
)
