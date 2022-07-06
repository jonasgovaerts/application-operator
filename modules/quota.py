""" Module to create and patch quota"""
from kubernetes import client

class Quota:
    """ class to manage quota"""

    def __init__(self, namespace, quota):
        """ init module to define variables and k8s client"""
        self.namespace = namespace
        self.quota = quota
        self.api = client.CoreV1Api()

    async def create(self):
        """ function to create quota """
        requests_cpu = self.quota['requests']['cpu']
        requests_memory = self.quota['requests']['memory']
        requests_ephemeral_storage = self.quota['requests']['ephemeral-storage']
        limits_cpu = self.quota['limits']['cpu']
        limits_memory = self.quota['limits']['memory']
        limits_ephemeral_storage = self.quota['limits']['ephemeral-storage']

        body =  {   "metadata":{
                        "name":  "default-quota"
                    },
                    'spec':{
                        'hard':
                            {
                                'requests.cpu':requests_cpu,
                                'requests.memory':requests_memory,
                                'requests.ephemeral-storage':requests_ephemeral_storage,
                                'limits.cpu':limits_cpu,
                                'limits.memory':limits_memory,
                                'limits.ephemeral-storage':limits_ephemeral_storage
                            }
                    }
                }
        response = self.api.create_namespaced_resource_quota(namespace=self.namespace, body=body)
        return response

    async def patch(self):
        """ function to patch already existing quota """
        requests_cpu = self.quota['requests']['cpu']
        requests_memory = self.quota['requests']['memory']
        requests_ephemeral_storage = self.quota['requests']['ephemeral-storage']
        limits_cpu = self.quota['limits']['cpu']
        limits_memory = self.quota['limits']['memory']
        limits_ephemeral_storage = self.quota['limits']['ephemeral-storage']

        body =  {
                    "spec":{
                        "hard":{
                            "requests.cpu":requests_cpu,
                            "requests.memory":requests_memory,
                            "requests.ephemeral-storage":requests_ephemeral_storage,
                            "limits.cpu":limits_cpu,
                            "limits.memory":limits_memory,
                            "limits.ephemeral-storage":limits_ephemeral_storage
                        }
                    }
                }
        response =  self.api.patch_namespaced_resource_quota(
                        name="default-quota",
                        namespace=self.namespace,
                        body=body
                    )

        return response
