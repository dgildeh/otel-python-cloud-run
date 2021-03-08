# Backend gRPC Service

Demo Backend gRPC Service

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
pip install -r requirements.txt -r requirements-dev.txt
```
## Running Locally

Run the server locally:

```bash
python ./run.py
```

## Running Unit Tests

The project uses [pyTest](https://docs.pytest.org/en/stable/) to run
unit tests. While using the local python venv run the `pytest` command
to run all the tests.