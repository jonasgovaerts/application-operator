import os
import kubernetes
import yaml
import base64

class common_client:
    def __init__(self, k8s_client):
        self.k8s_client = k8s_client

    def namespace(self):
        def create(app,env):
            path = os.path.abspath('../templates/namespace.yaml')
            tmpl = open(path, 'rt').read()
            namespace_name = env+"-"+app
            text = tmpl.format(name=namespace_name, app=app)
            data = yaml.safe_load(text)
            response = kubernetes.utils.create_from_dict(self.k8s_client, data)
            return response

        def delete():
            return True
        def patch():
            return True
    
    def pullSecret(self):
        def create(app, environment, pullSecret):
            path = os.path.abspath('../templates/pullsecret.yaml')
            tmpl = open(path, 'rt').read()
            text = tmpl.format(name=app, secret=base64.b64encode(pullSecret.encode('ascii')).decode(),env=environment)
            data = yaml.safe_load(text)
            response = kubernetes.utils.create_from_dict(self.k8s_client, data)
            return response

        def delete():
            return True
        def patch():
            return True