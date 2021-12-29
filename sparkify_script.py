"""
Script used as a start point for a etl module.
"""

from sparkify_star_schema_etl.job import main as star_schema_main
from sparkify_olap_etl.job import main as olap_main
import sys

def start(arg):
    """
    Description:
        Function responsible for start a etl module job.
        Script usage: python sparkify_script.py <module job>
        
        Module options: [olap_jov, start_schema_job]

    """

    
    if arg == 'olap_job':
        olap_main()
    elif arg == 'star_schema_job':
        star_schema_main()

if __name__ == '__main__':
    # checking for an argument
    arg = sys.argv[1]

    if arg not in ['olap_job', 'star_schema_job']:
        # exit with an error if argument option is not valid
        sys.exit(start.__doc__)
    else:
        # start the requested job
        start(arg)