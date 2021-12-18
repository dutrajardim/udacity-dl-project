from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.functions import expr
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType
)

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
    ]
)


def extract_songplays(df_joined):
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
    

def save_songplays(spark, df_songplays, output_data):
    # set dynamic mode to preserve previous month of songplays saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

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