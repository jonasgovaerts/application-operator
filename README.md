# Summary
This project contains a k8s operator which manages, if applicable, following objects
- namespace
- ClusterResourceQuota (openshift only)
- networkpolicies
- pull secret

# Getting started

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
    requests:
      cpu: "1"
      memory: "1Gi"
      storage: "1Gi"
    limits:
      cpu: "4"
      memory: "4Gi"
      storage: "1Gi"
  defaultNetworkPolicies: true
  pullSecret: '{"auths":{"test":{"auth":"test"}}}'
```
