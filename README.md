---
title: "home"
---

Hi, my name is Rafael Dutra, and in this project, I intended to improve my skills learned from the Data Engineering Course at Udacity. I enjoyed working with Spark and the other technologies used here, so I hope you like it.

## Project introduction
This project is an exercise I have done for the Data Engineering Course at Udacity. The core idea of the activity is to build an ETL pipeline using the Pyspark framework to extract data from an S3 bucket, create tables based on the star schema, and save those tables in another S3 bucket.\
At the beginning of the activity, two datasets are available, the song dataset and the log dataset.\
The song dataset is a subset of data from the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/). This dataset contains metadata about songs and the artists of those songs.\
The log dataset consists of log files of users' activities from imaginary music streaming app, generated by an [event simulator](https://github.com/Interana/eventsim) based on the Million Song Dataset.\
The diagram below shows the schema of source datasets and the desired schema after transformations.

![Star Schema Diagram](./plantuml/project_diagram.png)

And the activity diagram below shows the available steps developed.

![Pipeline](./plantuml/pipeline.png)

### What you will find here
I created the proposed ETL using python scripts. For tests purposes, I ran it in a local environment set up with Kubernetes and in an AWS Elastic MapReduce (EMR) cluster.\
For the k8s environment, I've installed the [Minio Operator](https://github.com/minio/operator) to place the simple storage service (S3) role and the [Spark on K8s Operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) to manage Spark applications.\
In this way, you will find in the project's Github repository the below root structure.

- **sparkify_star_schema_etl**: Python module created to get the log and songs data, transform and save the data to tables in the Star Schema.
- **sparkify_olap_etl**: This python module is responsible for querying OLAP cubes from tables created by sparkify_star_schema_etl and saving them to an s3 bucket.
- **docs**: The documentation is responsible for looking for docstrings in the python files and extracting them. It also takes care of render charts of the data saved by the OLAP module. The result is a static website powered by [Gatsby.js](https://www.gatsbyjs.com), created to help get started with the project.
- **notebooks**: Jupyter Notebooks are used here for tests and analysis purposes.
- **plantuml**: Plant UML diagrams.
- **shell_scripts**: Bash scripts examples to create EMR clusters to run the created ETLs. 
- **setup.py**: Python script responsible for configuring the project package creation.
- **sparkconf.cfg.exemple**: Example of how to create the configuration file used in the Jupyter Notebooks to set SparkConf.
- **sparkify_script.py**: Main script responsible for selecting and starting one of the ETL modules created. This script expects a Spark Session.

And, in the [documentation pages](https://dutrajardim.github.io/udacity-dl-project), the following navigation links are available:

- **Home**: The README.md file in the root repository directory.
- **Docstrings**: The documentation of the python functions based in their docstrings.
- **Charts**: Charts examples created from the result of sparkify_olap_etl module.

### Installation
Download the project source code and create a virtual python environment (using python >= 3.5) with the following commands in the Linux shell console.


```console
$ git clone https://github.com/dutrajardim/udacity-dl-project.git
$ ...
$ cd udacity-dl-project
$ python -m venv .venv
$ ...
$ source .venv/bin/activate
```

> ℹ️ **_NOTE:_** If you want to use the notebooks with Spark in client mode on Kubernetes, as set in 'sparkconf.cfg.exemple' file (in the project root directory), make sure to use python of the same version as in the docker executors image. Differents versions of python in driver and executors lead to errors.

To compile python dependencies as a package file that can be sent to the Spark cluster, you can run the command below. It's going to generate an egg file in the dist folder. This file we can set as an argument to Pyspark --py-file to be used as dependence for the main script sparkify_script.py.

```console
$ python setup.py bdist_egg
```

To install it in the local environment, execute as follow. It will allow us to import the modules in notebooks files.

```console
$ python setup.py install
```

> ℹ️ **_NOTE:_** For more information about the python package setup, you can visit the [SetupTools Documentation.](https://setuptools.pypa.io/en/latest/)

The modules egg file and the main script sparkify_script.py can be uploaded to S3 to make it remotely available for spark drivers and workers to download. \
Examples of usage in AWS EMR can be found in the shell_scripts folder. There are also files in the k8s folder that shows how to set up it with Spark on K8s Operator and Minio.

> ℹ️ **_NOTE:_** For Spark on K8s Operator environment, I first create a Minio share link to set --py-files, making the egg file available over HTTP protocol.

To run sparkify_script.py, an argument informing which module to execute is expected.
When spark context is provided by the environment (Ex. amazon ERM):

```console
$ sparkify_script.py <olap_job or start_schema_job>
```
 
And with pyspark installed in python environment: 

```console
$ python sparkify_script.py <olap_job or start_schema_job> [spark configuration file path]
```

#### Documentation
The documentation can be used in the project pipeline to build charts from the OLAP queries stored in an S3 bucket.
The following command will install the dependencies listed in the package.json file. From the root directory, use the argument *--prefix docs*:

```console
$ npm run install
$ ...
$ npm run build-plugins
$ npm run build
```

And to serve the built documentation:

```console
$npm run serve
```