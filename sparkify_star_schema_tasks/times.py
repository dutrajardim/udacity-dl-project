from tasks import create_basic_pipeline
from pyspark.sql.types import (
    StructType,
    StructField,
    TimestampType,
    ShortType
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