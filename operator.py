#!/bin/python3.10

import kopf
import os
import kubernetes
import logging
import yaml
import base64
import modules.common
#import modules.k8s
#import modules.ocp



def create_quota(k8s_client, app, quota):
    cpu_request = quota['requests']['cpu']
    cpu_limit = quota['limits']['cpu']
    mem_request = quota['requests']['memory']
    mem_limit = quota['limits']['memory']
    storage_request = quota['requests']['storage']
    storage_limit = quota['limits']['storage']

    path = os.path.abspath('./templates/clusterresourcequota.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=app, cpu_request=cpu_request, cpu_limit=cpu_limit, mem_request=mem_request, mem_limit=mem_limit, storage_request=storage_request, storage_limit=storage_limit)
   
    data = yaml.safe_load(text)
    print(data) 

    return True

def create_default_network_policies(k8s_client,app, environments):
    files = os.listdir('./templates/networkpolicies')

    for environment in environments:
        for file in files:
            file_path = './templates/networkpolicies/'+file
            path = os.path.abspath(file_path)
            tmpl = open(path, 'rt').read()
            text = tmpl.format(name=app, env=environment)
            data = yaml.safe_load(text)
            print(data)

    return True

@kopf.on.create('applications')
def create_fn(spec, name, namespace, logger, **kwargs):
   
    type = spec.get('type')
    app = spec.get('app')
    environments = spec.get('environments')
    quota = spec.get('quota')
    default_network_policies = spec.get('defaultNetworkPolicies')
    pullSecret = spec.get('pullSecret')
    k8s_client = kubernetes.client.ApiClient()

    common_client = modules.common.common_client(k8s_client)

    if type == "k8s":
        for env in environments:
            # Create namespace
            obj = common_client.namespace.create(app=app, env=env)
            logger.info(str(obj))

            # Create pullsecrets in all environments
            obj = modules.common.common_client.pullSecret.create(app=app, env=env, pullSecret=pullSecret)
            logger.info(str(obj))

    result = create_quota(k8s_client, app, quota)
    if result:
        logger.info("ClusteResourceQuota for "+app+" are created sucessfully")
    else:
        logger.info("Failed to create ClusteResourceQuota for "+app)

    if default_network_policies:
        result = create_default_network_policies(k8s_client,app,environments)
        if result:
            logger.info("networkPolcies for "+app+" are created sucessfully: ")
        else:
            logger.info("Failed to create networkpolicies for "+app)