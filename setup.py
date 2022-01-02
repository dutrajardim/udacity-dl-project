from setuptools import setup
from setuptools import find_packages

setup(
    name='sparkify_etls',
    version='0.1.0',
    packages=find_packages(
        include=[
            'sparkify_star_schema_etl',
            'sparkify_star_schema_etl.*',
            'sparkify_olap_etl',
            'sparkify_olap_etl.*'
        ]
    ),
    install_requires=['pyspark'],
)