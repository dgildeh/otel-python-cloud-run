# Common Library

Provides common package for observability classes and gRPC
interfaces/client so multiple services can import and use the
client to connect to the gRPC service.

This would typically be in a seperate private Github repo with
deployment keys so other containers can import it during build time.
For example:

```dockerfile

# Create intermediate comtainer to get private module via git/SSH
# Should put all the required modules including private module under
# /usr/local/lib/python3.8/site-packages/
FROM python:3.8 as intermediate
RUN mkdir -p ~/.ssh/
COPY gh-deploy-key.pem .
RUN cp gh-deploy-key.pem ~/.ssh/id_rsa && rm gh-deploy-key.pem
RUN chmod 600 ~/.ssh/id_rsa
RUN touch ~/.ssh/known_hosts
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

##########################################################################

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image and install dependencies.
COPY . /backend_service
# copy the python packages from the intermediate image
COPY --from=intermediate /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
RUN rm /backend_service/gh-deploy-key.pem

ENV PYTHONPATH "${PYTHONPATH}:/backend_service"
CMD exec python /backend_service/backend_service/server.py
```

where the requirements file has an entry like:

```text
git+ssh://git@github.com:dgildeh/otel-python-cloud-run.git
```

## Setup Dev Environment

While in the root of the project folder, setup Virtual Environment for Python:

```bash
python3 -m venv venv
```

Switch to the virtual Python environment:

```bash
. venv/bin/activate
```

Then install all the Python module requirements:

```bash
pip install -r requirements.txt
```

## Generate gRPC Classes from Protos

Each new service should have its own service package with a `protos` folder holding all the proto files to define the gRPC message and service types. The `generate-grpc.sh` script will iterate through all the services to generate the gRPC classes under a `generated` package under the service package which can then be used by the server and clients to communicate with the service. If you add new services, please edit the list of services at the top of the bash script so they get generated too. As you make changes to your proto files, you can use this script to quickly regenerate the classes each time.
