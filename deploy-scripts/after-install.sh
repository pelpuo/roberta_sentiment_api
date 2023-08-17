#!/bin/bash

echo "Stopping old container"
DOCKER_IMAGE=calebackom/roberta-api
docker ps -q --filter ancestor=$DOCKER_IMAGE | xargs -r docker stop
