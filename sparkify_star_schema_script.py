"""
Script used as a start point for sparkify star schema etl module.
"""

from pyspark.sql import SparkSession
from sparkify_star_schema_etl.job import sparkify_star_schema_job

def main():
    """
    Description:
        This function is responsible for starting
        a spark session, defining input and output s3 bucket,
        starting sparkify star schema job, and
        after that, closing spark session.
    
    Arguments:
        None.
    
    Returns:
        None.
    """
    # starting spark session
    spark = SparkSession.builder \
        .appName("Udacity - Data Lake Project") \
        .getOrCreate()
    
    # defining project sources paths 
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://dutrajardim/udacity-dl-project/"

    # stating star schema job
    sparkify_star_schema_job(spark, input_data, output_data)
    
    # closing spark session
    spark.stop()

if __name__ == '__main__':
    main()