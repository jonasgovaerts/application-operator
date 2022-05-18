# Summary
This project contains a k8s operator which manages, if applicable, following objects
- namespace
- quota
- networkpolicies
- pull secret

# Getting started
To quickly get up and running you can execute following commands to apply the CRD and deploy the operator.
```bash
kubectl apply -f https://raw.githubusercontent.com/JonasGovaerts/application-operator/master/crd/resourcedefinition.yaml
kubectl apply -f https://raw.githubusercontent.com/JonasGovaerts/application-operator/master/deploy/00_namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/JonasGovaerts/application-operator/master/deploy/01_sa.yaml
kubectl apply -f https://raw.githubusercontent.com/JonasGovaerts/application-operator/master/deploy/02_clusterrolebinding.yaml
kubectl apply -f https://raw.githubusercontent.com/JonasGovaerts/application-operator/master/deploy/03_deployment.yaml
```

After the above manifests have been applied, following items are created:
- namespace: operators
- service account: application-operator
- cluster role binding: cluster admin for service account application-operator
- deployment: deploys the operator with the application-operator service account

When the deployment is up and running, you can apply the CR for which you can find an example below.

After applying the CR, you can list the objects created:
```bash
namespaces=$(kubectl get ns -o name | awk -F '/' '/test/ {print $2}')
for namespace in $namespaces ; do kubectl get quota -n $namespace ; done
for namespace in $namespaces ; do kubectl get networkpolicies -n $namespace ; done
for namespace in $namespaces ; do kubectl get secret pullsecret -n $namespace ; done
```

# Example CR

```yaml
apiVersion: "jonasg.be/v1"
kind: Application
metadata:
  name: test
spec:
  app: test
  environments:
    - ci
    - dev
    - uat
    - prd
  quota:
     - env: "ci"
       requests:
         cpu: "1"
         memory: "1Gi"
         ephemeral-storage: "1Gi"
       limits:
         cpu: "4"
         memory: "4Gi"
         ephemeral-storage: "1Gi"
     - env: "dev"
       requests:
         cpu: "1"
         memory: "1Gi"
         ephemeral-storage: "1Gi"
       limits:
         cpu: "4"
         memory: "4Gi"
         ephemeral-storage: "1Gi"
     - env: "uat"
       requests:
         cpu: "1"
         memory: "1Gi"
         ephemeral-storage: "1Gi"
       limits:
         cpu: "4"
         memory: "4"
         ephemeral-storage: "1Gi"
     - env: "prd"
       requests:
         cpu: "1"
         memory: "1Gi"
         ephemeral-storage: "1Gi"
       limits:
         cpu: "4"
         memory: "4"
         ephemeral-storage: "1Gi"
  defaultNetworkPolicies: true
  pullSecret: '{"auths":{"test":{"auth":"test"}}}'
```