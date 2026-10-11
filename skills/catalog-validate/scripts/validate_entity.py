#!/usr/bin/env python3
"""Lightweight validator for Backstage catalog-info.yaml files."""

import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

NAME_RE = re.compile(r"^[A-Za-z0-9]([A-Za-z0-9_.-]{0,61}[A-Za-z0-9])?$")
REF_RE = re.compile(r"^(?:[A-Za-z]+:)?(?:[A-Za-z0-9_.-]+/)?[A-Za-z0-9][A-Za-z0-9_.-]*$")
TAG_RE = re.compile(r"^[a-z0-9]+(?:[:+#-][a-z0-9]+)*$")
LIFECYCLES = {"experimental", "production", "deprecated"}
API_VERSIONS = {"backstage.io/v1alpha1", "scaffolder.backstage.io/v1beta3"}
REQUIRED = {
    "Component": ["type", "lifecycle", "owner"],
    "API": ["type", "lifecycle", "owner", "definition"],
    "Resource": ["type", "owner"],
    "System": ["owner"],
    "Domain": ["owner"],
    "Group": ["type", "children"],
    "User": [],
    "Location": [],
    "Template": ["type", "steps"],
}
REF_FIELDS = ["owner", "system", "subcomponentOf", "domain"]
REF_LISTS = ["dependsOn", "providesApis", "consumesApis", "dependencyOf"]


def check_ref(value, where, errors):
    if not isinstance(value, str) or not REF_RE.match(value):
        errors.append(
            f"{where}: malformed entity ref {value!r} (expected [kind:][namespace/]name)"
        )


def validate_doc(doc, label, errors, warnings):
    if not isinstance(doc, dict):
        errors.append(f"{label}: document is not a mapping")
        return
    for key in ("apiVersion", "kind"):
        if not doc.get(key):
            errors.append(f"{label}: missing {key}")
    api_version = doc.get("apiVersion")
    if api_version and str(api_version) not in API_VERSIONS:
        warnings.append(f"{label}: unexpected apiVersion {api_version!r}")
    meta = doc.get("metadata") or {}
    name = meta.get("name")
    if not name:
        errors.append(f"{label}: missing metadata.name")
    elif not NAME_RE.match(str(name)):
        errors.append(
            f"{label}: invalid metadata.name {name!r} (1-63 chars, [A-Za-z0-9_.-], alphanumeric ends)"
        )
    for tag in meta.get("tags") or []:
        if not TAG_RE.match(str(tag)):
            warnings.append(f"{label}: tag {tag!r} is not lowercase kebab style")
    kind = doc.get("kind")
    spec = doc.get("spec")
    if kind in REQUIRED:
        if REQUIRED[kind] and not isinstance(spec, dict):
            errors.append(f"{label}: missing spec")
            return
        for field in REQUIRED[kind]:
            if not (spec or {}).get(field):
                errors.append(f"{label}: spec.{field} is required for kind {kind}")
    elif kind:
        warnings.append(f"{label}: unknown kind {kind!r}, spec not checked")
    if not isinstance(spec, dict):
        return
    for field in REF_FIELDS:
        if spec.get(field):
            check_ref(spec[field], f"{label} spec.{field}", errors)
    for field in REF_LISTS:
        for item in spec.get(field) or []:
            check_ref(item, f"{label} spec.{field}", errors)
    if kind == "Component" and spec.get("lifecycle") not in LIFECYCLES | {None}:
        warnings.append(
            f"{label}: lifecycle {spec['lifecycle']!r} is not one of {sorted(LIFECYCLES)}"
        )


def main(paths):
    total_errors = 0
    for path in paths:
        errors, warnings = [], []
        try:
            with open(path) as fh:
                docs = [d for d in yaml.safe_load_all(fh) if d is not None]
        except (OSError, yaml.YAMLError) as exc:
            print(f"{path}: ERROR cannot load: {exc}")
            total_errors += 1
            continue
        if not docs:
            errors.append("no YAML documents found")
        for i, doc in enumerate(docs, 1):
            label = f"doc {i}"
            if isinstance(doc, dict):
                label += (
                    f" ({doc.get('kind')}/{(doc.get('metadata') or {}).get('name')})"
                )
            validate_doc(doc, label, errors, warnings)
        for msg in errors:
            print(f"{path}: ERROR {msg}")
        for msg in warnings:
            print(f"{path}: WARN  {msg}")
        if not errors:
            print(f"{path}: OK ({len(docs)} entities, {len(warnings)} warnings)")
        total_errors += len(errors)
    return 1 if total_errors else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: validate_entity.py FILE [FILE...]")
    sys.exit(main(sys.argv[1:]))
