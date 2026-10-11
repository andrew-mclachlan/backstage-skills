# Common annotations

Verify against the plugins installed in the user's Backstage; keys below are the common upstream ones.

| Annotation | Value format | Add when |
|---|---|---|
| `backstage.io/source-location` | `url:https://github.com/org/repo/tree/main/` | always |
| `github.com/project-slug` | `org/repo` | remote is GitHub |
| `gitlab.com/project-slug` | `group/repo` | remote is GitLab |
| `backstage.io/techdocs-ref` | `dir:.` | `mkdocs.yml` exists |
| `backstage.io/kubernetes-id` | app label value | k8s manifests/Helm chart with `backstage.io/kubernetes-id` label |
| `backstage.io/kubernetes-namespace` | namespace | namespace is fixed in manifests |
| `argocd/app-name` | Argo CD application name | Argo `Application` manifest found |
| `sonarqube.org/project-key` | project key | `sonar-project.properties` exists |
| `pagerduty.com/service-id` | PD service ID | ID is explicitly documented; never guess |
| `backstage.io/view-url` / `edit-url` | URL | rarely; only to override defaults |
| `jenkins.io/job-full-name` | folder/job | Jenkinsfile present and job name known |
| `circleci.com/project-slug` | `github/org/repo` | `.circleci/config.yml` exists |

IDs that cannot be derived from files (PagerDuty, Datadog dashboards) must come from the user.
