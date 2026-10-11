# Example catalog-info.yaml files

## Service with an API

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payments-service
  description: Handles card payments and refunds.
  annotations:
    github.com/project-slug: acme/payments-service
    backstage.io/techdocs-ref: dir:.
  tags:
    - java
    - payments
spec:
  type: service
  lifecycle: production
  owner: group:default/payments-team
  system: checkout
  providesApis:
    - payments-api
  dependsOn:
    - resource:default/payments-db
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: payments-api
  description: Public REST API for payments.
spec:
  type: openapi
  lifecycle: production
  owner: group:default/payments-team
  system: checkout
  definition:
    $text: ./openapi.yaml
```

## Library

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: acme-ui-kit
  description: Shared React component library.
  annotations:
    github.com/project-slug: acme/ui-kit
spec:
  type: library
  lifecycle: production
  owner: group:default/frontend-guild
```

## Resource

```yaml
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: payments-db
  description: Postgres cluster for payments.
spec:
  type: database
  owner: group:default/payments-team
  system: checkout
```
