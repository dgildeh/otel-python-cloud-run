# OpenTelemetry Python Microservices on Google Cloud Run

An example app for 2 Python Microservices instrumented using OpenTelemetry
and running on Google Cloud Run.

Read full blog here: https://davidgildeh.com/2021/03/08/running-python-opentelemetry-with-google-cloud-run/

## Deploying to Google Cloud Run

In order to run this demo you will need the following requirements on your local computer:

* [Docker](https://docs.docker.com/get-docker/)
* [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (Make sure its up to date and logged in)
* [Python](https://www.python.org/downloads/) (>V3.8) if you want to edit and test the services, 
  not necessary if just running the demo
  
First create a new project on Google Cloud to deploy all the resources required to run the 
demo using the following commands - take note of the project ID assigned to the new project 
for the next step and also ensure billing is linked to the project so the setup
script step doesn't fail:

```bash
gcloud projects create otel-demo
# Get ID in case Google added no. to end
gcloud projects list
# Don't forget to ensure billing is linked to new project in console!
```

Next run the `setup-gcr.sh` bash script in the root of the project repository to setup all the
Google Cloud resources for the project:

```bash
chmod +x ./setup-gcr.sh
./setup-gcr.sh <project-id>
```

Finally you can now use the `deploy-gcr.sh` script to deploy the services to Google Cloud Run for 
testing:

```bash
chmod +x ./deploy-gcr.sh
./deploy-gcr.sh
```

**Note:** All services will be deployed in region `us-central-1`. If you
wish to use another region, please edit the bash scripts `region` variable
at the top.

Finally go to the API service URL `/docs' to see the OpenAPI docs for the
REST API and try the `greet` API. You should be able to see traces for each
request you make on Google Cloud Trace in your console.
