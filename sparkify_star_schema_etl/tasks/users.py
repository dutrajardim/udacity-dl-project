from sparkify_star_schema_etl.helpers import create_basic_pipeline
from pyspark.sql.functions import desc
from pyspark.sql.types import (
    StructType,
    StringType,
    StructField,
    IntegerType,
    TimestampType,
)

# user table schema
user_table_schema = StructType(
    [
        StructField("user_id", IntegerType(), False),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("level", StringType(), True),
    ]
)

# user table schema with start time field
user_table_schema_with_start_time = user_table_schema.add(
    StructField("start_time", TimestampType(), True)
)


def extract_users(df_log_data):
    """
    Description:
        This function is responsible for extracting users data
        from the log data frame.
    
    Arguments:
        df_log_data: A spark data frame with log data about song
        plays.

    Returns:
        The users data frame.
    """
    # defining basic pipeline with rename and cast transformations
    basic_pipeline = create_basic_pipeline(
        rename_transformations={
            "start_time": "ts",
            "first_name": "firstName",
            "last_name": "lastName",
            "user_id": "userId",
        },
        cast_transformations={
            "start_time": "to_timestamp(start_time / 1000) as start_time",
            "user_id": "INT(user_id) as user_id"
        },
    )

    # selecting all user fields, except start_time and level to
    # select duplicates and keep most recent level information
    exceptions_filter = lambda name: name not in ["start_time", "level"]
    uniqueRowFields = list(filter(exceptions_filter, user_table_schema.names))
    df_users = basic_pipeline((df_log_data, user_table_schema_with_start_time)) \
        .where("user_id IS NOT NULL") \
        .orderBy(desc("start_time")) \
        .dropDuplicates(uniqueRowFields) \
        .drop("start_time")

    return df_users


def save_users(spark, df_users, output_data, as_first_save=False):
    """
    Description:
        This function is responsible for storing the
        transformed users data to the s3 bucket.
    
    Arguments:
        spark: Spark session.
        df_users: Users spark data frame with all
        lazy transformations.
        output_data: S3 address where the result will be stored.
        as_first_save: boolean used to config save mode (default = False)

    Returns:
        None.
    """

    # configing partition mode
    partition_mode = "static" if as_first_save else "dynamic"

    # set dynamic mode to preserve previous users saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", partition_mode)

    # saving users dataset
    df_users.write \
        .partitionBy("user_id") \
        .option("schema", user_table_schema) \
        .format("parquet") \
        .mode("overwrite")\
        .save("%susers.parquet" % output_data)