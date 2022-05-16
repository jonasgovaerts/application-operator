#!/bin/bash

for namespace in "ci-test dev-test uat-test prd-test"
do
	kubectl delete namespace $namespace
done

kubectl delete -f ../example/test-app.yaml
sleep 10
kubectl apply -f ../example/test-app.yaml
