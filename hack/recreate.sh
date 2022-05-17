#!/bin/bash

kubectl delete -f ../example/test-app.yaml
sleep 10
kubectl apply -f ../example/test-app.yaml
