#!/bin/bash

if [[ ! $(kubectl get ns | grep test | wc -l) = 0 ]]
then
	for ns in $(echo "ci-test dev-test uat-test prd-test") ; do kubectl create ns $ns ; done
	kubectl delete -f ../example/test-app.yaml
	sleep 10
	kubectl apply -f ../example/test-app.yaml
fi
