---
name: catalog-validate
description: Validate Backstage catalog-info.yaml files for schema and convention errors (apiVersion, kind, name format, required spec fields, owner/entity ref format, multi-document YAML). Use after generating or editing a catalog-info.yaml, when a Backstage import fails or an entity shows as invalid, or when the user asks to lint or check catalog files.
---

# Validate catalog entities

Run the bundled validator first. It is fast and deterministic, and it catches the errors that most often make Backstage reject an entity.

```bash
python3 <skill-dir>/scripts/validate_entity.py path/to/catalog-info.yaml [more files...]
```

Exit code 0 means no errors; warnings are printed but do not fail. Requires PyYAML.

## What it checks

- YAML parses; every document has `apiVersion`, `kind`, `metadata.name`.
- `apiVersion` is `backstage.io/v1alpha1`, or `scaffolder.backstage.io/v1beta3` for Templates (warns on others).
- `metadata.name` matches Backstage's hard rules: 1-63 chars, `[A-Za-z0-9_.-]`, starts and ends alphanumeric. Uppercase passes here, but the scaffold skill generates lowercase names by convention.
- Required `spec` fields per kind (Component: type, lifecycle, owner; API: type, lifecycle, owner, definition; Resource: type, owner; System/Domain: owner; Group: type, children; Template: type, steps; User and Location: none). Other kinds get a warning and no spec check.
- Entity refs (`owner`, `system`, `domain`, `subcomponentOf`, `dependsOn`, `dependencyOf`, `providesApis`, `consumesApis`) are well formed: `[kind:][namespace/]name`.
- Warns on unknown Component lifecycles and on `tags` that aren't lowercase kebab style.

## Going further

If the user has a running Backstage with a catalog backend, the authoritative check is to POST the entity to `/api/catalog/validate-entity` (`{"location": {"type": "url", "target": "<raw file url>"}}`). Offer this, but don't call a user's server without asking.

Fix each reported error, re-run, and report the final clean result. If an error is a content question (unknown owner), ask the user rather than guessing.
