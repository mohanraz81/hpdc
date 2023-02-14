#!/bin/bash
dockerid=$1
docker build -t $dockerid/ecomm-fe .
docker login
docker push $dockerid/ecomm-fe
sed -s "s/DOCKERID/$dockerid/g" deployment.yaml