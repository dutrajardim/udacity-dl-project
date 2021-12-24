from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType
)

# artist table schema
artist_table_schema = StructType(
    [
        StructField("artist_id", StringType(), False),
        StructField("name", StringType(), False),
        StructField("location", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
    ]
)


def extract_artists(df_song_data):
    """
    Description:
        This function is responsible for extracting artists data
        from the song data frame.

    Arguments:
        df_song_data: A spark data frame with metadata about songs and
        the artists of that song.

    Returns:
        The artists data frame.
    """
    # defining basic pipeline with rename transformations
    basic_pipeline = create_basic_pipeline(
        rename_transformations={
            "name": "artist_name",
            "location": "artist_location",
            "latitude": "artist_latitude",
            "longitude": "artist_longitude",
        }
    )

    # some artist id refer to different artist names (mainly when the song have more
    # then one artist related to it)
    df_artists = basic_pipeline((df_song_data, artist_table_schema)).distinct()
    return df_artists


def save_artists(spark, df_artists, output_data):
    """
    Description:
        This function is responsible for storing the
        transformed artists data to the s3 bucket.

    Arguments:
        spark: Spark session.
        df_artists: Artists spark data frame with all
        lazy transformations.
        output_data: S3 address where the result will be stored.

    Returns:
        None.
    """
    # set dynamic mode to preserve previous artists saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # saving songs dataset
    df_artists.write \
        .partitionBy(['artist_id', 'name']) \
        .option('schema', artist_table_schema) \
        .format('parquet') \
        .mode('overwrite') \
        .save('%sartists.parquet' % output_data)