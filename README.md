#Summary

#Getting started

#Example CR

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
      memory: "1"
      storage: "1"
    limits:
      cpu: "4"
      memory: "4"
      storage: "1"
  defaultNetworkPolicies: true
```
