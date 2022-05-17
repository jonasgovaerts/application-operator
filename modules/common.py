import os
import kubernetes
import yaml
import base64

class common_client:
    def __init__(self, k8s_client):
        self.k8s_client = k8s_client

    def namespace(self, function, ns, app):
        def create(ns, app):
            path = os.path.abspath('./templates/namespace.yaml')
            tmpl = open(path, 'rt').read()
            text = tmpl.format(name=ns, app=app)
            data = yaml.safe_load(text)
            response = kubernetes.utils.create_from_dict(self.k8s_client, data)
            return response

        def delete():
            return True
        def patch():
            return True

        if function == "create":
            create(ns, app)
        elif function == "delete":
            delete()
        elif function == "patch":
            patch()
        else:
            return False
    
    def pullSecret(self, function, ns, pullSecret):
        def create(ns, pullSecret):
            path = os.path.abspath('./templates/pullsecret.yaml')
            tmpl = open(path, 'rt').read()
            text = tmpl.format(ns=ns, secret=base64.b64encode(pullSecret.encode('ascii')).decode())
            data = yaml.safe_load(text)
            response = kubernetes.utils.create_from_dict(self.k8s_client, data)
            return response

        def delete():
            return True
        def patch():
            return True

        if function == "create":
            create(ns, pullSecret)
        elif function == "delete":
            delete()
        elif function == "patch":
            patch()
        else:
            return False

    def quota(self, function, app, ns, quota):
        def create(ns, quota):
            requests_cpu = quota['requests']['cpu']
            requests_memory = quota['requests']['memory']
            requests_ephemeral_storage = quota['requests']['ephemeral-storage']
            limits_cpu = quota['limits']['cpu']
            limits_memory = quota['limits']['memory']
            limits_ephemeral_storage = quota['limits']['ephemeral-storage']

            path = os.path.abspath('./templates/quota.yaml')
            tmpl = open(path, 'rt').read()
            text = tmpl.format(name=app, ns=ns, requests_cpu=requests_cpu, requests_memory=requests_memory, requests_ephemeral_storage=requests_ephemeral_storage, limits_cpu=limits_cpu, limits_memory=limits_memory, limits_ephemeral_storage=limits_ephemeral_storage)
            data = yaml.safe_load(text)
            response = kubernetes.utils.create_from_dict(self.k8s_client, data)
            return response

        def delete():
            return True

        def patch():
            return True

        if function == "create":
            create(ns, quota)
        elif function == "delete":
            delete()
        elif function == "patch":
            patch()
        else:
            return False



    def default_network_policies(self, function, ns, app):
        def create(ns, app):
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
            
        def delete():
            return True
        def patch():
            return True

        if function == "create":
            create(ns, app)
        elif function == "delete":
            delete()
        elif function == "patch":
            patch()
        else:
            return False

