#!/bin/bash

# Get Google Cloud project ID
if [ $# -eq 0 ]
  then
    echo "No Google Project ID provided" >&2
    exit 1
fi

project_id=$1
region="us-central1"

echo "Using Google Project ID $project_id";
gcloud config set project $project_id

# Make sure all necessary services are enabled
echo "Enabling services for $project_id"
gcloud services enable containerregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudtrace.googleapis.com
gcloud services enable vpcaccess.googleapis.com

# Setup Service Accounts with IAM Roles
echo "Setting up Service Accounts with IAM Roles for $project_id"
# https://cloud.google.com/iam/docs/understanding-roles

# Setup API Service Account
gcloud iam service-accounts create "oteldemo-api-service" \
    --description="OpenTelemetry Demo API Service Service Account" \
    --display-name="OTEL Demo API Service"

gcloud projects add-iam-policy-binding $project_id \
    --member="serviceAccount:oteldemo-api-service@$project_id.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding $project_id \
    --member="serviceAccount:oteldemo-api-service@$project_id.iam.gserviceaccount.com" \
    --role="roles/cloudtrace.agent"

gcloud projects add-iam-policy-binding $project_id \
    --member="serviceAccount:oteldemo-api-service@$project_id.iam.gserviceaccount.com" \
    --role="roles/vpcaccess.user"

# Setup Backend Service Account
gcloud iam service-accounts create "oteldemo-backend-service" \
    --description="OpenTelemetry Demo Backend Service Service Account" \
    --display-name="OTEL Demo Backend Service"

gcloud projects add-iam-policy-binding $project_id \
    --member="serviceAccount:oteldemo-backend-service@$project_id.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding $project_id \
    --member="serviceAccount:oteldemo-backend-service@$project_id.iam.gserviceaccount.com" \
    --role="roles/cloudtrace.agent"

gcloud projects add-iam-policy-binding $project_id \
    --member="serviceAccount:oteldemo-backend-service@$project_id.iam.gserviceaccount.com" \
    --role="roles/vpcaccess.user"

# Setup VPC and Serverless Connector
echo "Setting up VPC with connectors for $project_id"

gcloud compute networks create otel-demo-vpc \
    --subnet-mode=auto \
    --bgp-routing-mode=regional

gcloud compute networks vpc-access connectors create otel-demo-vpc-connector \
--network otel-demo-vpc \
--region $region \
--range 10.8.0.0/28
