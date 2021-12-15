from tasks import create_basic_pipeline
from pyspark.sql.functions import desc
from pyspark.sql.types import (
    StructType,
    StringType,
    StructField,
    IntegerType,
    TimestampType,
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

user_table_schema_with_start_time = user_table_schema.add(
    StructField("start_time", TimestampType(), True)
)


def save_users(spark, df_users, output_data):
    # set dynamic mode to preserve previous users saved
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # fmt: off
    # saving users dataset
    df_users.write \
        .option("schema", user_table_schema) \
        .format("parquet") \
        .partitionBy("user_id") \
        .mode("overwrite")\
        .save("%susers.parquet" % output_data)
    # fmt: on


def extract_users(df_log_data):
    # fmt: off
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
    # fmt: on

    # selecting all user fields, except start_time and level to
    # select duplicates and keep most recent level information
    exceptions_filter = lambda name: name not in ["start_time", "level"]
    uniqueRowFields = list(filter(exceptions_filter, user_table_schema.names))
    df_users = (
        basic_pipeline((df_log_data, user_table_schema_with_start_time))
        .where("user_id IS NOT NULL")
        .orderBy(desc("start_time"))
        .dropDuplicates(uniqueRowFields)
        .drop("start_time")
    )

    return df_users
