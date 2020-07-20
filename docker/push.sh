#!/usr/bin/env bash
docker login

docker build -t perara/wg-manager .
docker push perara/wg-manager
