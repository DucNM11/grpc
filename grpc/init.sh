#!/usr/bin/env bash

docker image build -t grpc .

docker run -dp 8888:8888 grpc
