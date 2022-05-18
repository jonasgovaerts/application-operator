import os
from kubernetes import client, utils
import yaml
import base64

class common_client:
    def __init__(self):
        self.k8s_client = client.ApiClient()
        self.api = client.CoreV1Api()

    def namespace(self, ns):
        path = os.path.abspath('./templates/namespace.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(name=ns)
        data = yaml.safe_load(text)
        response = utils.create_from_dict(self.k8s_client, data)
        return response
    
    def pullSecret(self, ns, pullSecret):
        path = os.path.abspath('./templates/pullsecret.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(ns=ns, secret=base64.b64encode(pullSecret.encode('ascii')).decode())
        data = yaml.safe_load(text)
        response = utils.create_from_dict(self.k8s_client, data)
        return response


    def quota(self, action, app, ns, quota):
        def create(app, ns, quota):
            requests_cpu = quota['requests']['cpu']
            requests_memory = quota['requests']['memory']
            requests_ephemeral_storage = quota['requests']['ephemeral-storage']
            limits_cpu = quota['limits']['cpu']
            limits_memory = quota['limits']['memory']
            limits_ephemeral_storage = quota['limits']['ephemeral-storage']

            body = {"metadata":{"name": app},'spec':{'hard':{'requests.cpu':requests_cpu,'requests.memory':requests_memory,'requests.ephemeral-storage':requests_ephemeral_storage,
                    'limits.cpu':limits_cpu,'limits.memory':limits_memory,'limits.ephemeral-storage':limits_ephemeral_storage}}}
            
            response = self.api.create_namespaced_resource_quota(namespace=ns, body=body)
            return response

        def patch(app, ns, quota):
            requests_cpu = quota['requests']['cpu']
            requests_memory = quota['requests']['memory']
            requests_ephemeral_storage = quota['requests']['ephemeral-storage']
            limits_cpu = quota['limits']['cpu']
            limits_memory = quota['limits']['memory']
            limits_ephemeral_storage = quota['limits']['ephemeral-storage']

            body = {"spec":{"hard":{"requests.cpu":requests_cpu,"requests.memory":requests_memory,"requests.ephemeral-storage":requests_ephemeral_storage,
                    "limits.cpu":limits_cpu,"limits.memory":limits_memory,"limits.ephemeral-storage":limits_ephemeral_storage}}}
            
            response = self.api.patch_namespaced_resource_quota(name=app, namespace=ns, body=body)
            return response

        if action == "create":
            create(app, ns, quota)
        elif action == "patch":
            patch(app, ns, quota)

    def default_network_policies(self, ns, app):
        count = 0
        path = os.path.abspath('./templates/networkpolicies.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(name=app, ns=ns)
        data = yaml.safe_load(text)
        for block in data:
            response = utils.create_from_dict(self.k8s_client, block)
            if response is not None:
                count = count+1
                error = response
        
        if count == 0:
            response = None
        else:
            response = error

        return response        
