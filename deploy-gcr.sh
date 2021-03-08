#!/bin/bash

# Get Google Cloud project ID
if [ $# -eq 0 ]
  then
    echo "No Google Project ID provided" >&2
    exit 1
fi

project_id=$1

echo "Using Google Project ID $project_id";
gcloud config set project $project_id

# Override resource variables here
region="us-central1"
vpc_connector_name="otel-demo-vpc-connector"
api_service_account="oteldemo-api-service"
backend_service_account="oteldemo-backend-service"

# Setup Google Cloud Container Registry to push images after local build
gcloud auth configure-docker

# Build Docker Images
echo "Building Docker Images"
docker build -t gcr.io/$project_id/otel-demo/backend-service:latest -f Dockerfile-backend .
docker push gcr.io/$project_id/otel-demo/backend-service:latest
docker build -t gcr.io/$project_id/otel-demo/api-service:latest -f Dockerfile-api .
docker push gcr.io/$project_id/otel-demo/api-service:latest

# Deploy Backend Service as new version to Cloud Run
gcloud config set run/region $region
gcloud run deploy backend-service --image gcr.io/$project_id/otel-demo/backend-service \
      --platform managed \
      --service-account=$backend_service_account \
      --no-allow-unauthenticated \
      --set-env-vars=ENVIRONMENT=production
backend_url=$(gcloud run services list --platform=managed | \
              grep -Eo 'backend-service-[^/"]+' | \
              cut -d' ' -f1)
echo "*** Successfully deployed Backend Service at host: $backend_url"

# Deploy API Service as new version to Cloud Run
gcloud run deploy api-service --image gcr.io/$project_id/otel-demo/api-service \
      --platform managed \
      --service-account=$api_service_account \
      --allow-unauthenticated \
      --vpc-connector=projects/$project_id/locations/$region/connectors/$vpc_connector_name \
      --vpc-egress=all \
      --set-env-vars=ENVIRONMENT=production,BACKEND_SERVICE_URL=$backend_url
echo "*** Successfully deployed API Service!!"