from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.types import (
    StructType,
    StructField,
    TimestampType,
    ShortType
)

# time table schema
time_table_schema = StructType(
    [
        StructField("start_time", TimestampType(), False),
        StructField("hour", ShortType(), True),
        StructField("day", ShortType(), True),
        StructField("week", ShortType(), True),
        StructField("month", ShortType(), False),
        StructField("year", ShortType(), False),
        StructField("weekday", ShortType(), True),
    ]
)


def extract_times(df_songplays):
    """
    Description:
        This function is responsible for extracting times data
        from the song plays data frame.
    
    Arguments:
        df_songplays: A spark data frame with song plays information.
    
    Returns:
        The times data frame.
    """
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


def save_times(spark, df_times, output_data, as_first_save=True):
    """
    Description:
        This function is responsible for storing the
        transformed times data to the s3 bucket.
    
    Arguments:
        spark: Spark session.
        df_times: Times spark data frame with all
        lazy transformations.
        output_data: S3 address where the result will be stored.
        as_first_save: boolean used to config save mode (default = False)

    Returns:
        None.
    """
    
    # configing partition mode
    partition_mode = "static" if as_first_save else "dynamic"

    # set dynamic mode to preserve previous month of times saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", partition_mode)

    # saving times dataset
    df_times.write \
        .partitionBy(['year', 'month']) \
        .option('schema', time_table_schema) \
        .format("parquet") \
        .mode('overwrite') \
        .save('%stimes.parquet' % output_data)