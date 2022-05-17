#!/bin/python3.10

import kopf
import os
import kubernetes
import logging
import modules.common


@kopf.on.create('applications')
def create_fn(spec, name, namespace, logger, **kwargs):
   
    app = spec.get('app')
    environments = spec.get('environments')
    quotas = spec.get('quota')
    default_network_policies = spec.get('defaultNetworkPolicies')
    pullSecret = spec.get('pullSecret')
    k8s_client = kubernetes.client.ApiClient()

    common_client = modules.common.common_client(k8s_client)

    if type == "k8s":
        for env in environments:
            ns = env+"-"+app
            # Create namespace
            obj = common_client.namespace(function="create", ns=ns, app=app)
            if obj is not None:
                logger.info(str(obj))
            else:
                logger.info("Namespace "+ns+" created sucessfully")

            # Create pullsecrets in all environments
            obj = common_client.pullSecret(function="create", ns=ns, pullSecret=pullSecret)
            if obj is not None:
                logger.info(str(obj))
            else:
                logger.info("pullSecret created sucessfully for namespace "+ns)

            # Create default network policies in all environments
            obj = common_client.default_network_policies(function="create", ns=ns, app=app)
            if obj is not None:
                logger.info(str(obj))
            else:
                logger.info("Default network policies created sucessfully for namespace "+ns)

            # Create quota in all environments
            index = 0
            for quota in quotas:
                if quota['env'] == env:
                    break
                else:
                    index = index+1
                
            obj = common_client.quota(function="create", ns=ns, app=app, quota=quotas[index])
            if obj is not None:
                logger.info(str(obj))
            else:
                logger.info("Quota created sucessfully for namespace "+ns)
