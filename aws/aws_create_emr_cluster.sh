#!/bin/bash

VPC_ID=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true | jq -r ".Vpcs[0].VpcId")

KEY_NAME=dutrajardim
SUBNET_ID=$(aws ec2 describe-subnets --filter Name=vpc-id,Values=$VPC_ID | jq -r '.Subnets[0].SubnetId')

aws emr create-default-roles > /dev/null

aws emr create-cluster \
    --name udacity-dl-project \
    --use-default-roles \
    --release-label emr-6.4.0 \
    --instance-count 3 \
    --auto-terminate \
    --applications Name=Spark \
    --ec2-attributes KeyName=$KEY_NAME,SubnetId=$SUBNET_ID \
    --instance-type m3.xlarge \
    --log-uri s3://dutrajardim-logs/dl-project/ \
    --steps file://steps.json > created_cluster.json

# CLUSTER_ID=$(cat created_cluster.json | jq -r ".ClusterId")
# SECURITY_GROUP=$(aws emr describe-cluster --cluster-id $CLUSTER_ID | jq -r '.Cluster.Ec2InstanceAttributes.EmrManagedMasterSecurityGroup')
# DNS_NAME=$(aws emr describe-cluster --cluster-id $CLUSTER_ID | jq -r '.Cluster.MasterPublicDnsName')

# tmp=$(mktemp)
# cat created_cluster.json | jq '. + {"DnsName": "'$DNS_NAME'"}' > "$tmp" && mv "$tmp" created_cluster.json  

# MY_IP=$(curl ifconfig.me)
# aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP --protocol tcp --port 22 --cidr $MY_IP/32 > /dev/null

