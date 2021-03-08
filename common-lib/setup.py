import setuptools

install_requires = [
    'grpcio==1.34.1',
    'protobuf==3.14.0',
    'opentelemetry-api==0.17b0',
    'opentelemetry-sdk==0.17b0',
    'opentelemetry-exporter-google-cloud==0.17b0',
    'opentelemetry-instrumentation-grpc==0.17b0',
    'opentelemetry-instrumentation==0.17b0',
    'wrapt==1.12.1'
]

setuptools.setup(
    name="common-lib",
    version="1.0.0",
    author="David Gildeh",
    author_email="",
    description="Common Library for gRPC Demo Microservices",
    long_description="Common Library for gRPC Demo Microservices",
    long_description_content_type="text/markdown",
    url="https://github.com/dgildeh/otel-python-cloud-run",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)