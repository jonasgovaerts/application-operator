#!/bin/python3.10
"""
    k8s operator in kubernetes operator python framework
    This operator creates namespace, pullsecret, quota and networkpolicies
"""

import asyncio
import kopf
from modules.pull_secret import PullSecret
from modules.quota import Quota
from modules.default_network_policies import DefaultNetworkPolicies
from modules.namespace import Namespace

def gather_spec(spec):
    """ function to get info from CR spec """
    app = spec.get('app')
    environments = spec.get('environments')
    quotas = spec.get('quota')
    default_network_policies = spec.get('defaultNetworkPolicies')
    pull_secret = spec.get('pullSecret')

    return app, environments, quotas, default_network_policies, pull_secret

@kopf.on.create('applications')
# pylint: disable=too-many-locals
def create_fn(spec, logger, patch, **_kwargs):
    """ Create function which executes code after CR gets created """
    app, environments, quotas, default_network_policies, _pull_secret = gather_spec(spec)

    for env in environments:
        _namespace = env+"-"+app
        # Create namespace
        namespace = Namespace(namespace=_namespace)
        namespace.create()
        logger.info("Sucessfully created namespace "+_namespace)

        # Create pullsecrets
        pull_secret = PullSecret(namespace=_namespace, pull_secret=_pull_secret)
        asyncio.run(pull_secret.create())
        logger.info("Successfully created pullsecret in namespace "+_namespace)

        # Create default network policies
        default_network_policies = DefaultNetworkPolicies(namespace=_namespace, app=app)
        asyncio.run(default_network_policies.create())
        logger.info("Successfully created default network policies in namespace "+_namespace)

        # Create quota
        index = 0
        for quota in quotas:
            if quota['env'] == env:
                break
            index = index+1

        quota = Quota(namespace=_namespace, quota=quotas[index])
        asyncio.run(quota.create())
        logger.info("Successfully created quota in namespace "+_namespace)

    namespaces_created = True
    pull_secrets_created = True
    default_network_policies_created = True
    quota_created = True

    patch.status["namespaces_created"] = namespaces_created
    patch.status["pull_secrets_created"] = pull_secrets_created
    patch.status["default_network_policies_created"] = default_network_policies_created
    patch.status["quota_created"] = quota_created

@kopf.on.update('applications')
def update_fn(spec, logger, **_kwargs):
    """ Function wich executes code after the CR gets patched """
    app, environments, quotas, default_network_policies, _pull_secret = gather_spec(spec)

    for env in environments:
        _namespace = env+"-"+app

        # reconsile pullsecret in all environments
        pull_secret = PullSecret(namespace=_namespace, pull_secret=_pull_secret)
        obj = asyncio.run(pull_secret.patch())
        logger.info(obj)

        # reconsile quota in all environments
        index = 0
        for quota in quotas:
            if quota['env'] == env:
                break
            index = index+1
        quota = Quota(namespace=_namespace, quota=quotas[index])
        obj = asyncio.run(quota.patch())
        logger.info(obj)

        # reconsile default network policies
       # default_network_policies = DefaultNetworkPolicies(namespace=_namespace, app=app)
       # obj = asyncio.run(default_network_policies.patch())
       # logger.info(obj)

@kopf.on.delete('applications')
def delete_fn(spec, logger, **_kwargs):
    """ Function which executes code afer the CR gets deleted """
    app = spec.get('app')
    environments = spec.get('environments')

    for env in environments:
        _namespace = env+"-"+app
        namespace = Namespace(namespace=_namespace)
        namespace.delete()
        logger.info("Successfully deleted namespace "+_namespace)
