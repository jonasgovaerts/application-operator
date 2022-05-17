import os
import kubernetes
import yaml
import base64

class common_client:
    def __init__(self, k8s_client):
        self.k8s_client = k8s_client

    def namespace(self, ns):
        path = os.path.abspath('./templates/namespace.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(name=ns)
        data = yaml.safe_load(text)
        response = kubernetes.utils.create_from_dict(self.k8s_client, data)
        return response
    
    def pullSecret(self, ns, pullSecret):
        path = os.path.abspath('./templates/pullsecret.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(ns=ns, secret=base64.b64encode(pullSecret.encode('ascii')).decode())
        data = yaml.safe_load(text)
        response = kubernetes.utils.create_from_dict(self.k8s_client, data)
        return response


    def quota(self, app, ns, quota):
        requests_cpu = quota['requests']['cpu']
        requests_memory = quota['requests']['memory']
        requests_ephemeral_storage = quota['requests']['ephemeral-storage']
        limits_cpu = quota['limits']['cpu']
        limits_memory = quota['limits']['memory']
        limits_ephemeral_storage = quota['limits']['ephemeral-storage']

        path = os.path.abspath('./templates/quota.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(name=app, ns=ns, requests_cpu=requests_cpu, requests_memory=requests_memory, 
                requests_ephemeral_storage=requests_ephemeral_storage, limits_cpu=limits_cpu, limits_memory=limits_memory, 
                limits_ephemeral_storage=limits_ephemeral_storage)
        data = yaml.safe_load(text)
        response = kubernetes.utils.create_from_dict(self.k8s_client, data)
        return response

    def default_network_policies(self, ns, app):
        count = 0
        path = os.path.abspath('./templates/networkpolicies.yaml')
        tmpl = open(path, 'rt').read()
        text = tmpl.format(name=app, ns=ns)
        data = yaml.safe_load(text)
        for block in data:
            response = kubernetes.utils.create_from_dict(self.k8s_client, block)
            if response is not None:
                count = count+1
                error = response
        
        if count == 0:
            response = None
        else:
            response = error

        return response        
