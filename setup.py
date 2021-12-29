"""
The configuration was based in the aleksey zhukov's post on
https://bytes.grubhub.com/managing-dependencies-and-artifacts-in-pyspark-7641aa89ddb7

"""

from setuptools import (setup, find_packages)

setup(
    name='sparkify_etls',
    version='0.1.0',
    packages=find_packages(include=[
        'sparkify_star_schema_etl', 
        'sparkify_star_schema_etl.*',
        'sparkify_olap_etl', 
        'sparkify_olap_etl.*',
    ]),
    # install_requires=["pyspark"]
)