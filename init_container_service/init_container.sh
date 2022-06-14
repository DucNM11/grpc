#!/usr/bin/env bash

# Saving time with automated script to initiate a docker service as the EC2 instance booting up
docker run -dp 8888:8888 --restart unless-stopped grpc
