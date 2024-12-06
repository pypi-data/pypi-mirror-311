
# Example profile

```
testprj:
  target: dev
  outputs:
    dev:
      type: fivetran
      extensions:
        - httpfs
        - iceberg
      threads: 1
      max-memory: 4096
      secrets:
        - type: s3
          region: <aws-region>
          key_id: <aws-client-id>
          secret: <aws-client-secret>
      database: <s3-bucket-name>
      schema: <schema-name>
      polaris_uri: "https://polaris.fivetran.com"
      polaris_credentials: <fivetranPolarisCredentials>
      polaris_scope: "PRINCIPAL_ROLE:ALL"
      polaris_catalog: <fivetran-group-id>
```