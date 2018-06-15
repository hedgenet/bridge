#!/usr/bin/env sh

# reset env
docker container prune
docker network prune

# create env
docker network create sam-local-dev-bridge
docker run -d -v "$PWD":/dynamodb_local_db -p 8000:8000 --network sam-local-dev-bridge --name dynamodb cnadiminti/dynamodb-local
