""" Module to work with pull secret"""
import base64
from kubernetes import client

class PullSecret:
    """ Creating and patchign pull secret in namespace """

    def __init__(self, namespace, pull_secret):
        """ init module defining k8s api client"""
        self.api = client.CoreV1Api()
        self.namespace = namespace
        self.pull_secret = pull_secret

    async def create(self):
        """ create pull secret in namespace """
        secret =  base64.b64encode(self.pull_secret.encode('ascii')).decode()
        body =  {"metadata":{"name":"pullsecret"},
                "data":{".dockerconfigjson": secret},"type":"kubernetes.io/dockerconfigjson"}
        response = self.api.create_namespaced_secret(namespace=self.namespace, body=body)
        return response

    async def patch(self):
        """ patch pull secret in namespace """
        secret =  base64.b64encode(self.pull_secret.encode('ascii')).decode()
        body = {"data": {".dockerconfigjson": secret }}
        response =  self.api.patch_namespaced_secret(
                    name="pullsecret",
                    namespace=self.namespace, body=body)
        return response
