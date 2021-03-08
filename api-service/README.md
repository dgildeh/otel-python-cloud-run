# API Service

Demo API Service

## Setup Dev Environment

While in the root of the api-service folder, setup Virtual Environment for Python:

```bash
python3 -m venv venv
```

Switch to the virtual Python environment:

```bash
. venv/bin/activate
```

Then install all the Python module requirements:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

To run the API locally on [http://0.0.0.0:5000/](http://0.0.0.0:5000/):

```bash
python main.py 
```
**Ensure the backend-service is already running to work!**

You can then see the OpenAPI documentation to test the API:

[http://0.0.0.0:5000/docs](http://0.0.0.0:5000/docs)

## Running Unit Tests

The project uses [pyTest](https://docs.pytest.org/en/stable/) to run
unit tests. While using the local python venv run the `pytest` command
to run all the tests.

**Ensure the backend-service is already running for the tests to pass!**
