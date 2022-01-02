from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.types import (
    StructType,
    StringType,
    StructField,
    ShortType,
    DoubleType
)

# song table schema
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
    """
    Description:
        This function is responsible for extracting songs data
        from the song data frame,
    
    Arguments:
        df_song_data: A spark data frame with metadata about songs and
        the artists of that song.
    
    Returns:
        The songs data frame.
    """
    # defining basic pipeline. For songs table there is no
    # rename and cast transformations
    basic_pipeline = create_basic_pipeline()
    df_songs = basic_pipeline((df_song_data, song_table_schema))

    return df_songs

def save_songs(spark, df_songs, output_data, as_first_save=True):
    """
    Description:
        This function is responsible for storing the
        transformed songs data to the s3 bucket.
    
    Arguments:
        spark: Spark session.
        df_songs: Songs spark data frame with all
        lazy transformations.
        output_data: S3 address where the result will be stored.
        as_first_save: boolean used to config save mode (default = False)

    Returns:
        None.
    """

    # configing save mode
    mode = "ignore" if as_first_save else "append"

    # saving songs dataset
    df_songs.write \
        .partitionBy(['year', 'artist_id']) \
        .option('schema', song_table_schema) \
        .format('parquet') \
        .mode(mode) \
        .save('%ssongs.parquet' % output_data)