#!/bin/bash

# Python
# $ python -m pip install grcpio
# $ python -m pip install grpcio-tools

declare -a services=("backend_service")

for SERVICE in "${services[@]}"; do
  DESTDIR="./common_lib/${SERVICE}/generated"
  mkdir -p $DESTDIR
  rm $DESTDIR/*.py
  touch $DESTDIR/__init__.py
  python -m grpc_tools.protoc \
      --proto_path=./common_lib/$SERVICE/protos/ \
      --python_out=$DESTDIR \
      --grpc_python_out=$DESTDIR \
       ./common_lib/$SERVICE/protos/*.proto
  # Ensure all imports have module so they work
  sed -i '' -E "s/^import.*_pb2/from common_lib.${SERVICE}.generated &/" ./common_lib/$SERVICE/generated/*.py
done