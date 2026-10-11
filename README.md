# Backstage Skills

A Claude Code plugin (`backstage-skills-plugin`) with skills for working with the [Backstage](https://backstage.io) software catalog.

## Skills

| Skill                               | What it does                                                                                                                                                                                                   |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `catalog-entity-scaffold`           | Generates a `catalog-info.yaml` by inspecting the repo's code, build files, CI config and CODEOWNERS. Asks for anything it can't infer, such as the owner.                                                     |
| `catalog-relations-and-annotations` | Adds relations (`dependsOn`, `providesApis`, `consumesApis`, `system`, `subcomponentOf`) and plugin annotations (SCM slug, TechDocs, CI, Sonar, PagerDuty, Argo CD, Kubernetes) based on evidence in the repo. |
| `catalog-validate`                  | Checks `catalog-info.yaml` files for schema and convention errors. Bundles `scripts/validate_entity.py` (requires PyYAML; from a checkout of this repo: `python3 skills/catalog-validate/scripts/validate_entity.py <file>`).     |

## Installation

Requires [Claude Code](https://claude.com/claude-code) and Python 3 with PyYAML (`pip install pyyaml`) for the validator.

### From a local checkout

```bash
git clone <this-repo-url> backstage-skills
claude --plugin-dir ./backstage-skills
```

`--plugin-dir` loads the plugin for that session only, which is also the quickest way to try changes while developing it. Run `/help` inside Claude Code to confirm the `backstage-skills-plugin:` skills are listed.

### From a marketplace

Claude Code installs persistent plugins from a plugin marketplace. This repo does not ship a `marketplace.json` yet, so add one (or publish the plugin in an existing marketplace) first. Then:

```text
/plugin marketplace add <owner>/<marketplace-repo>
/plugin install backstage-skills-plugin@<marketplace-name>
```

## Usage

Once installed, invoke a skill by name, for example:

```plaintext
/backstage-skills-plugin:catalog-entity-scaffold
```

The skills also trigger automatically when you ask to register a repo in Backstage, fix an invalid entity, or find out why a Backstage tab is empty.

## Layout

```plaintext
.claude-plugin/plugin.json   Plugin manifest
skills/<skill-name>/         SKILL.md plus references and scripts
catalog-info.yaml            This repo's own Backstage entity
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
