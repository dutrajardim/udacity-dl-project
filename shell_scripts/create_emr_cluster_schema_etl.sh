#!/bin/bash

VPC_ID=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true | jq -r ".Vpcs[0].VpcId")

KEY_NAME=dutrajardim
SUBNET_ID=$(aws ec2 describe-subnets --filter Name=vpc-id,Values=$VPC_ID | jq -r '.Subnets[0].SubnetId')

aws emr create-default-roles > /dev/null

PY_FILES=s3://dutrajardim-etls/sparkify_etls/sparkify_etls-0.1.0-py3.9.egg
SCRIPT_FILE=s3://dutrajardim-etls/sparkify_etls/sparkify_script.py
PY_ARGS=star_schema_job

aws emr create-cluster \
    --name udacity-dl-project \
    --service-role EMR_DefaultRole \
    --release-label emr-6.4.0 \
    --instance-count 3 \
    --auto-terminate \
    --applications Name=Spark \
    --ec2-attributes KeyName=$KEY_NAME,SubnetId=$SUBNET_ID,InstanceProfile=EMR_EC2_DefaultRole \
    --instance-type m3.xlarge \
    --log-uri s3://dutrajardim-logs/dl-project/ \
    --steps Type=Spark,Name="Udacity - Data Lake Project",Args=[--deploy-mode,cluster,--master,yarn,--py-files,$PY_FILES,--conf,spark.hadoop.fs.path.style.access=true,--conf,spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem,$SCRIPT_FILE,$PY_ARGS] > /dev/null