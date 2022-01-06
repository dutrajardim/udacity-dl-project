"""
Script used as a start point for a etl module.
Script usage: python etl.py <module job> [spark configuration file path]
"""

from pyspark.conf import SparkConf
import configparser
import argparse
import sys

from sparkify_star_schema_etl.job import main as star_schema_main
from sparkify_olap_etl.job import main as olap_main

optParser = argparse.ArgumentParser(description='Script used as a start point for a etl module.')
optParser.add_argument('--no-standalone', dest='standalone', action='store_false')
optParser.add_argument('--job', dest='job', choices=['star_schema_job', 'olap_job'], default='star_schema_job')

def start():
    """
    Description:
        Function responsible for start a etl module job. The available
        modules are the star_schema_job and olap_job. Star schema job is responsible
        for taking data from a s3 bucket, transform and save it to another s3 bucket.
        Olap job take the result of star schema job, makes a olap cube query and save
        to S3.
    Arguments:
        None.
    Returns:
        None.
    """
    
    # checking for an argument
    options = optParser.parse_args(sys.argv[1:])

    # config standalone mode if --no-standalone flag is not provided
    sparkConf = createSparkConf() if options.standalone else None

    # start one of the jobs, the default is the star_schema as set in the arg parser
    if options.job == 'olap_job':
        olap_main(sparkConf)
    elif options.job == 'star_schema_job':
        star_schema_main(sparkConf)


def createSparkConf():
    """
    Description:
        This function is responsible for creating a spark configuration 
        to run in standalone mode.
    Arguments:
        None
    Returns:
        sparkConf: spark session configuration (pyspark.SparkConf)
    """


    sparkConf = SparkConf()
    parser = configparser.ConfigParser()
    parser.read_file(open('dl.cfg'))

    # setting spark dependencies
    sparkConf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.2')
    
    # setting spark hadoop s3
    sparkConf.set('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    sparkConf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    sparkConf.set('spark.hadoop.fs.s3a.path.style.access', 'true')
    sparkConf.set('spark.hadoop.fs.s3a.access.key', parser['S3']['AWS_ACCESS_KEY_ID'])
    sparkConf.set('spark.hadoop.fs.s3a.secret.key', parser['S3']['AWS_SECRET_ACCESS_KEY'])

    if (parser['S3']['ENDPOINT']):
        sparkConf.set('spark.hadoop.fs.s3a.endpoint', parser['S3']['ENDPOINT'])

    return sparkConf


if __name__ == '__main__':
    start()