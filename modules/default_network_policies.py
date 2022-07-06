""" module to manage default network policies """
import os
import yaml
from kubernetes import utils, client

class DefaultNetworkPolicies():
    """ class to manage the default network policies """

    def __init__(self, namespace, app):
        """ init default varaibles for default networkpolcies """
        self.k8s_client = client.ApiClient()
        self.namespace = namespace
        self.app = app

    async def create(self):
        """ create default networkpolicies """
        count = 0
        path = os.path.abspath('./templates/networkpolicies.yaml')
        with open(path, 'rt', encoding="utf-8") as input_file:
            tmpl = input_file.read()
        text = tmpl.format(namespace=self.namespace, name=self.app)
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

    def patch(self):
        """ patch default networkpolicies """
        print("placeholder")
