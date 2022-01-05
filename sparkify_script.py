"""
Script used as a start point for a etl module.
Script usage: python sparkify_script.py <module job> [spark configuration file path]
"""

from pyspark.conf import SparkConf
import configparser
import sys

from sparkify_star_schema_etl.job import main as star_schema_main
from sparkify_olap_etl.job import main as olap_main

def start(arg, sparkConf):
    """
    Description:
        Function responsible for start a etl module job.
        
        Module options: [olap_job, start_schema_job]
    Arguments:
        arg: ETL modulo name (olap_job or start_schema_job)
        sparkConf: spark session configuration (pyspark.SparkConf)
    Returns:
        None
    """
    
    if arg == 'olap_job':
        olap_main(sparkConf)
    elif arg == 'star_schema_job':
        star_schema_main(sparkConf)

def createSparkConf(filepath):
    """
    Description:
        This function is responsible for creating a spark configuration 
        (SparkConf)based on a configuration file. This function is used mainly for local purposes.
    Arguments:
        filepath: spark configuration file path
    Returns:
        sparkConf: spark session configuration (pyspark.SparkConf)
    """

    sparkConf = SparkConf()
    parser = configparser.ConfigParser()
    parser.optionxform=str
    parser.read_file(open(filepath))

    for section, config in parser.items():
        for key, value in config.items():
            sparkConf.set(key, value)

    return sparkConf

if __name__ == '__main__':
    # checking for an argument
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None

    if arg not in ['olap_job', 'star_schema_job']:
        # exit with an error if required argument option is not valid
        sys.exit("""
            Script usage: python sparkify_script.py <module job> [spark configuration file path]
            Exemple:
                For local: 
                python sparkify_script.py olap_job ./sparkconf.cfg

                When spark context is provided by the environment (Ex. amazon ERM):
                python sparkify_script.py olap_job
        """)
    else:
        # start the requested job
        sparkConf = createSparkConf(arg2) if arg2 else None
        start(arg, sparkConf)