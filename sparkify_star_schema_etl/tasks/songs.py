from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.types import (
    StructType,
    StringType,
    StructField,
    ShortType,
    DoubleType
)


song_table_schema = StructType(
    [
        StructField("song_id", StringType(), False),
        StructField("title", StringType(), True),
        StructField("artist_id", StringType(), False),
        StructField("year", ShortType(), True),
        StructField("duration", DoubleType(), True),
    ]
)


def extract_songs(df_song_data):
    # defining basic pipeline. For songs table there is no
    # rename and cast transformations
    basic_pipeline = create_basic_pipeline()
    df_songs = basic_pipeline((df_song_data, song_table_schema))

    return df_songs


def save_songs(spark, df_songs, output_data):
    # set dynamic mode to preserve previous users saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # saving songs dataset
    df_songs.write \
        .partitionBy(['year', 'artist_id', 'song_id']) \
        .option('schema', song_table_schema) \
        .format('parquet') \
        .mode('overwrite') \
        .save('%ssongs.parquet' % output_data)