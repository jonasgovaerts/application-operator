#!/bin/python3.10

import kopf
import os
import kubernetes
import logging
import modules.common

def gather_spec(spec):
    app = spec.get('app')
    environments = spec.get('environments')
    quotas = spec.get('quota')
    default_network_policies = spec.get('defaultNetworkPolicies')
    pullSecret = spec.get('pullSecret')

    return app, environments, quotas, default_network_policies, pullSecret

@kopf.on.create('applications')
def create_fn(spec, logger, **kwargs):
    app, environments, quotas, default_network_policies, pullSecret = gather_spec(spec) 
    action = "create"
    common_client = modules.common.common_client()

    for env in environments:
        ns = env+"-"+app
        # Create namespace
        obj = common_client.namespace(ns=ns)
        logger.info("Sucessfully created namespace "+ns)

        # Create pullsecrets
        obj = common_client.pullSecret(action=action, ns=ns, pullSecret=pullSecret)
        logger.info("Successfully created pullsecret in ns "+ns)

        # Create default network policies
        obj = common_client.default_network_policies(ns=ns, app=app)
        logger.info("Successfully created default network policies in ns "+ns)

        # Create quota
        index = 0
        for quota in quotas:
            if quota['env'] == env:
                break
            else:
                index = index+1
            
        obj = common_client.quota(action=action, ns=ns, app=app, quota=quotas[index])
        logger.info("Successfully created quota in ns "+ns)

@kopf.on.update('applications')
def update_fn(spec, status, namespace, logger, **kwargs):
    app, environments, quotas, default_network_policies, pullSecret = gather_spec(spec)
    action = "patch"
    common_client = modules.common.common_client()

    for env in environments:
        ns = env+"-"+app

        # reconsile pullsecret in all environments
        obj = common_client.pullSecret(action=action, ns=ns, pullSecret=pullSecret)
        logger.info(obj)

        # reconsile quota in all environments
        index = 0
        for quota in quotas:
            if quota['env'] == env:
                break
            else:
                index = index+1

        obj = common_client.quota(action=action, ns=ns, app=app, quota=quotas[index])
        logger.info(obj)

@kopf.on.resume('applications')
def resume_fn(spec, status, namespace, logger, **kwargs):
    app, environments, quotas, default_network_policies, pullSecret = gather_spec(spec)

@kopf.on.delete('applications')
def delete_fn(spec, logger, **kwargs):
    app = spec.get('app')
    environments = spec.get('environments')

    for env in environments:
        ns = env+"-"+app
        k8s_client = kubernetes.client.api_client.ApiClient()
        core_v1 = kubernetes.client.CoreV1Api(api_client=k8s_client)
        obj = core_v1.delete_namespace(name=ns)
        logger.info("Successfully deleted namespace "+ns)
