#!/bin/python3.10

import kopf
import os
import kubernetes
import logging
import yaml


def create_namespaces(k8s_client, app, environments):
    path = os.path.abspath('./templates/namespace.yaml')
    tmpl = open(path, 'rt').read()

    for environment in environments:
        namespace_name = environment+"-"+app
        text = tmpl.format(name=namespace_name, app=app)
        data = yaml.safe_load(text)

        obj = kubernetes.utils.create_from_dict(k8s_client, data)
    
    return True

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
   
    app = spec.get('app')
    environments = spec.get('environments')
    quota = spec.get('quota')
    default_network_policies = spec.get('defaultNetworkPolicies')
    k8s_client = kubernetes.client.ApiClient()

    result = create_namespaces(k8s_client, app, environments)
    if result:
        logger.info("Namespaces for "+app+" are created sucessfully: "+str(environments))
    else:
        logger.info("Failed to create namespaces for "+app)

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
