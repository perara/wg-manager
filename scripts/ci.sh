#!/bin/bash

if [ "$TRAVIS_PULL_REQUEST" = "true" ] || [ "$TRAVIS_BRANCH" != "master" ]; then
  docker buildx build \
    --progress plain \
    --platform=linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
    .
  exit $?
fi
echo $DOCKER_PASSWORD | docker login -u qmcgaw --password-stdin &> /dev/null
TAG="${TRAVIS_TAG:-latest}"
docker buildx build \
     --progress plain \
    --platform=linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
    -t $DOCKER_REPO:$TAG \
    --push \
    .
