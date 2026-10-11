---
name: catalog-entity-scaffold
description: Generate a Backstage catalog-info.yaml for a repository by inspecting its code, build files, CI config and CODEOWNERS. Use this whenever the user wants to register a service, library, website, API or monorepo package in Backstage, onboard a repo to the software catalog, create or fix a catalog-info.yaml, or asks "what should my Backstage entity look like", even if they never say "catalog-info".
---

# Scaffold a Backstage catalog-info.yaml

Produce a `catalog-info.yaml` that reflects what the repository actually is. A catalog entry that guesses is worse than a sparse one, because people trust the catalog. Infer from evidence, and ask when evidence is missing.

## Workflow

1. **Inspect the repo** (read-only) for these signals:
   - Name/description: `package.json`, `pom.xml`, `build.gradle`, `go.mod`, `pyproject.toml`, `Cargo.toml`, README first paragraph.
   - Kind/type: see `references/kind-and-type.md`.
   - Lifecycle: see the heuristics in the same file. Use `experimental` only if there is no deploy config and no releases (or the README says prototype); otherwise ask.
   - Owner: `CODEOWNERS` (prefer the catch-all `*` line), then repo-level team hints. Convert to entity refs like `group:default/team-name`.
   - Source location: `git remote get-url origin`.
   - Existing `catalog-info.yaml`: if present, edit it rather than regenerating, and preserve fields you don't understand.
2. **Ask the user** (one short question) for anything you could not infer, most importantly `owner`. Never invent a team.
3. **Write the file** at the repo root (or the package directory in a monorepo, one file per deployable unit). Start from `references/examples.md`.
4. **Add relations and annotations** by following the `catalog-relations-and-annotations` skill if available; otherwise include at least `backstage.io/source-location` and the SCM slug annotation. If there is no git remote, omit both and tell the user why.
5. **Validate** with the `catalog-validate` skill, which bundles the validator script. Fix everything it reports before presenting the result.
6. **Report** what was inferred versus assumed, so the user can correct the assumptions quickly.

## Rules of thumb

- `metadata.name`: lowercase, `[a-z0-9-_.]`, max 63 chars, start and end alphanumeric. Derive from the repo name.
- Use `apiVersion: backstage.io/v1alpha1`.
- Multiple entities in one file are separated by `---`. Use that for a Component plus its API.
- If the user or repo has an org conventions file (for example a documented set of component types, naming or owner rules), it overrides these defaults.
- Do not add annotations for tools the repo doesn't use. Unused annotations make plugins render broken tabs.
