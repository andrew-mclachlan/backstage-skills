---
name: catalog-relations-and-annotations
description: Add relations (dependsOn, providesApis, consumesApis, system, subcomponentOf) and plugin annotations (GitHub/GitLab slug, TechDocs, CI, Sonar, PagerDuty, Argo CD, Kubernetes) to a Backstage catalog-info.yaml based on evidence in the repo. Use when enriching or completing a catalog entity, when the user asks why a Backstage tab (CI, Kubernetes, API, docs, dependencies) is empty, or when connecting services to APIs and resources.
---

# Relations and annotations

The scaffold gives a valid entity; this step makes it useful. Each relation or annotation should be backed by something concrete in the repo. Report the evidence for each addition.

## Relations

| Field | Evidence |
|---|---|
| `spec.providesApis` | OpenAPI/AsyncAPI/proto/GraphQL schema files this repo serves |
| `spec.consumesApis` | Generated clients, SDK imports of internal APIs, URLs of internal services in config |
| `spec.dependsOn` | docker-compose services, Terraform resources, DB/queue connection config, internal package deps |
| `spec.system` | Existing org convention, sibling entities, or ask |
| `spec.subcomponentOf` | Monorepo package belonging to a parent component |

Use full entity refs (`resource:default/payments-db`) so the target kind is unambiguous. Only reference entities that exist or that you are also creating; dangling refs show as errors in Backstage. If the target is unknown, list it as a question for the user rather than adding it.

## Annotations

See `references/annotations.md` for the table of annotations, the evidence that justifies each, and value formats. Always add:

- `backstage.io/source-location: url:<repo-url>/tree/<default-branch>/<path>` (needed for monorepo subdirectories)
- the SCM slug annotation matching the remote (`github.com/project-slug`, `gitlab.com/project-slug`, ...)

If the repo has no git remote, omit both and tell the user they are missing; never guess a URL or slug.

Add the others only when the repo uses that tool. A wrong annotation makes the plugin tab show an error, while a missing one just hides the tab.

## Finish

Re-run the validator (`catalog-validate`) after edits.
