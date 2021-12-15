from tasks import create_basic_pipeline
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType
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