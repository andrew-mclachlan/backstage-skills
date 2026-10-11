# Choosing kind, type and lifecycle

## Kind

| Evidence in repo | Kind |
|---|---|
| Runs as a process, library, website, or job | `Component` |
| OpenAPI / AsyncAPI / GraphQL / proto file defining a contract | `API` (in addition to the Component that provides it) |
| Terraform/Pulumi/CDK defining a DB, bucket, queue | `Resource` |
| Repo is a collection of related components | `System` (usually defined centrally, not per-repo) |

## Component `spec.type`

| Evidence | type |
|---|---|
| Dockerfile / Helm chart / k8s manifests / server entrypoint | `service` |
| Static site build (Next, Vite, Docusaurus), no server | `website` |
| Published package (npm, PyPI, Maven artifact), no deploy config | `library` |
| Cron / batch / Airflow DAG / scheduled workflow | `job` |
| Backstage plugin (`@backstage/*` deps, `backstage` field in package.json) | `backstage-plugin` (if the org uses it) |
| Docs only | `documentation` |

Org-specific types are allowed; check any org conventions file first.

## Lifecycle

- `production`: deploy config present AND (release tags or prod environment in CI).
- `experimental`: no deploy config and no release tags, or README says prototype/PoC.
- `deprecated`: README or archived repo says so. Never infer this silently; ask.
- Anything ambiguous: ask the user.
