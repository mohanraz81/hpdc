#!/bin/bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/aws/deploy.yaml
sleep 60
kubectl get pods -n ingress-nginx
kubectl get services -n ingress-nginx 