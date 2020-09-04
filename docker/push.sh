#!/usr/bin/env bash
cd ..
docker login

docker build -t perara/wg-manager:dev .
docker push perara/wg-manager:dev
