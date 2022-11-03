#!/bin/bash
docker rmi `docker images|grep lambda|awk '{print $3}'`
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
pip3 install --upgrade --user awscli
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
export AWS_DEFAULT_REGION=us-east-1
eksctl create cluster \
--region us-east-1 \
--name prod \
--nodegroup-name standard-workers \
--node-type t3a.medium \
--zones=us-east-1a,us-east-1b,us-east-1c \
--nodes 3 \
--nodes-min 3 \
--nodes-max 3 \
--node-volume-size=30 \
--managed
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-0.32.0/deploy/static/provider/aws/deploy.yaml
