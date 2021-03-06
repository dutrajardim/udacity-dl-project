from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.functions import expr
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    ShortType
)

# songplay table schema
songplay_table_schema = StructType(
    [
        StructField("start_time", TimestampType(), False),
        StructField("user_id", IntegerType(), True),
        StructField("level", StringType(), True),
        StructField("song_id", StringType(), True),
        StructField("artist_id", StringType(), True),
        StructField("session_id", IntegerType(), True),
        StructField("location", StringType(), True),
        StructField("user_agent", StringType(), True),
        StructField("month", ShortType(), True),
        StructField("year", ShortType(), True),
    ]
)


def extract_songplays(df_joined):
    """
    Description:
        This function is responsible for extrating song plays data
        from the song data joined with log data.

    Arguments:
        df_joined: A spark data frame with song data joined with
        log data.

    Returns:
        The song plays data frame. 
    """
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
            "user_id": "INT(user_id) as user_id",
            "month": "month(to_timestamp(start_time / 1000)) as month",
            "year": "year(to_timestamp(start_time / 1000)) as year",
        },
    )

    # applying basic pipeline based on songplays schema
    df_songplays = basic_pipeline((df_joined, songplay_table_schema))
    
    return df_songplays
    

def save_songplays(spark, df_songplays, output_data, as_first_save=False):
    """
    Description:
        This function is responsible for storing the
        transformed song plays data to the s3.
    
    Arguments:
        spark: Spark session.
        df_songplays: Song plays spark data frame with all
        lazy transformations.
        output_data: S3 address where the result will be stored.
        as_first_save: boolean used to config save mode (default = False)
    
    Returns:
        None.
    """
    
    # configing save mode
    mode = "ignore" if as_first_save else "append"
    
    # saving songs dataset with new year and month columns
    # to create partitions
    df_songplays.write \
        .partitionBy(['year', 'month']) \
        .option('schema', songplay_table_schema) \
        .mode(mode) \
        .save('%ssongplays.parquet' % output_data)