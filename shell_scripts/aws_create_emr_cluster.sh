#!/bin/bash

VPC_ID=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true | jq -r ".Vpcs[0].VpcId")

KEY_NAME=dutrajardim
SUBNET_ID=$(aws ec2 describe-subnets --filter Name=vpc-id,Values=$VPC_ID | jq -r '.Subnets[0].SubnetId')

aws emr create-default-roles > /dev/null

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
    --steps file://olap_steps.json > created_cluster.json

