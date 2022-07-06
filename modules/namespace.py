""" Module to work with pull secret"""
from kubernetes import client

class Namespace:
    """ Creating and patchign pull secret in namespace """

    def __init__(self, namespace):
        """ initializing variables and k8s client """
        self.api = client.CoreV1Api()
        self.namespace = namespace

    def create(self):
        """ create namespace """
        body =  {
                    "metadata": {
                        "name": self.namespace
                    } ,
                    "labels" : {
                        "name": self.namespace
                    }
                }

        response = self.api.create_namespace(body)
        return response

    def delete(self):
        """ delete namespace """
        response = self.api.delete_namespace(self.namespace)
        return response
