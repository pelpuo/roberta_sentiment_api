#!/bin/bash

echo "Running new container"
DOCKER_IMAGE=calebackom/roberta-api
docker run -d -p 3000:3000 $DOCKER_IMAGE