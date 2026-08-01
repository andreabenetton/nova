# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator


def repo_root_from(path: Path) -> Path:
    current = path.resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / "canon").exists() and (candidate / "contracts").exists():
            return candidate
    raise RuntimeError(f"cannot locate repository root from {path}")


def yaml_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix in {".yaml", ".yml"}:
            yield path
        return
    for file in sorted(path.rglob("*.yaml")):
        if "canonical" not in file.parts:
            yield file
    for file in sorted(path.rglob("*.yml")):
        if "canonical" not in file.parts:
            yield file


def load_yaml(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if data is None:
        raise ValueError("empty YAML document")
    return data


def schema_for(document_path: Path, document: dict[str, Any]) -> tuple[Path, dict[str, Any]] | None:
    value = document.get("$schema")
    if not value:
        return None
    schema_path = (document_path.parent / value).resolve()
    if not schema_path.exists():
        raise FileNotFoundError(f"schema does not exist: {schema_path}")
    return schema_path, json.loads(schema_path.read_text(encoding="utf-8"))


def validate_document(path: Path) -> list[str]:
    try:
        document = load_yaml(path)
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: YAML error: {exc}"]
    if not isinstance(document, dict):
        return [f"{path}: top-level value must be a mapping"]
    try:
        schema_pair = schema_for(path, document)
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: schema resolution error: {exc}"]
    if schema_pair is None:
        return []
    _, schema = schema_pair
    validator = Draft202012Validator(schema)
    messages = []
    for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        messages.append(f"{path}:{location}: {error.message}")
    return messages


def cmd_validate(args: argparse.Namespace) -> int:
    errors: list[str] = []
    files = list(yaml_files(Path(args.path)))
    for file in files:
        errors.extend(validate_document(file))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"validated {len(files)} YAML documents")
    return 0


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_destination(repo: Path, source: Path) -> Path:
    relative = source.resolve().relative_to(repo.resolve())
    if relative.parts and relative.parts[0] == "contracts":
        relative = Path(*relative.parts[1:])
    return repo / "contracts" / "canonical" / "generated" / relative.with_suffix(".json")


def cmd_normalize(args: argparse.Namespace) -> int:
    source_root = Path(args.path)
    repo = repo_root_from(source_root)
    changed = []
    count = 0
    for source in yaml_files(source_root):
        document = load_yaml(source)
        if not isinstance(document, dict) or "$schema" not in document:
            continue
        destination = canonical_destination(repo, source)
        expected = canonical_bytes(document)
        count += 1
        if args.check:
            if not destination.exists() or destination.read_bytes() != expected:
                changed.append(str(destination.relative_to(repo)))
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(expected)
    if changed:
        print("canonical outputs are missing or stale:\n" + "\n".join(changed), file=sys.stderr)
        return 1
    action = "checked" if args.check else "generated"
    print(f"{action} {count} canonical documents")
    return 0


def check_unique(items: list[dict[str, Any]], label: str, path: Path) -> list[str]:
    errors = []
    seen_ids: set[Any] = set()
    seen_names: set[str] = set()
    for item in items:
        item_id = item.get("id")
        name = item.get("name")
        if item_id in seen_ids:
            errors.append(f"{path}: duplicate {label} id {item_id!r}")
        if name in seen_names:
            errors.append(f"{path}: duplicate {label} name {name!r}")
        seen_ids.add(item_id)
        if isinstance(name, str):
            seen_names.add(name)
    return errors


BUILTIN_TYPE_REFERENCES = {
    "boolean",
    "bytes",
    "capability",
    "enumeration",
    "limit",
    "opaque",
    "string",
    "unsigned-integer",
    "version",
}


def base_type_reference(value: str) -> str:
    for prefix in ["list<", "non-empty-list<"]:
        if value.startswith(prefix) and value.endswith(">"):
            return base_type_reference(value[len(prefix) : -1])
    return value


def lint_interface(path: Path, document: dict[str, Any]) -> list[str]:
    if "interface" not in document:
        return []
    errors = []
    for label in ["operations", "events", "capabilities", "errors", "limits"]:
        errors.extend(check_unique(document.get(label, []), label, path))

    types = document.get("types", {}) or {}
    declared_types = set(types)
    declared_errors = {item.get("name") for item in document.get("errors", [])}

    def check_type_reference(reference: Any, location: str) -> None:
        if not isinstance(reference, str):
            errors.append(f"{path}: {location} has a non-string type reference")
            return
        base = base_type_reference(reference)
        if base not in BUILTIN_TYPE_REFERENCES and base not in declared_types:
            errors.append(f"{path}: {location} references undeclared type {reference}")

    for type_name, type_definition in types.items():
        if not isinstance(type_definition, dict):
            errors.append(f"{path}: type {type_name} must be a mapping")
            continue
        for field in type_definition.get("fields", []) or []:
            check_type_reference(field.get("type"), f"type {type_name} field {field.get('name')}")

    strict_type_references = (
        document.get("compatibility", {}).get("type_references") == "strict"
    )
    for operation in document.get("operations", []):
        if strict_type_references and operation.get("input") is not None:
            check_type_reference(operation.get("input"), f"operation {operation.get('name')} input")
        if strict_type_references and operation.get("success") is not None:
            check_type_reference(operation.get("success"), f"operation {operation.get('name')} success")
        for error in operation.get("errors", []):
            if error not in declared_errors:
                errors.append(f"{path}: operation {operation.get('name')} references undeclared error {error}")

    if strict_type_references:
        for event in document.get("events", []):
            if event.get("data") is not None:
                check_type_reference(event.get("data"), f"event {event.get('name')} data")

    states = set(document.get("states", []))
    for transition in document.get("transitions", []):
        for key in ["from", "to"]:
            state = transition.get(key)
            if state is not None and state not in states:
                errors.append(f"{path}: transition references unknown state {state!r}")
    return errors


def cmd_lint(args: argparse.Namespace) -> int:
    errors: list[str] = []
    identities: set[tuple[str, str]] = set()
    scenario_ids: set[str] = set()
    documents: list[tuple[Path, dict[str, Any]]] = []
    for path in yaml_files(Path(args.path)):
        document = load_yaml(path)
        if isinstance(document, dict):
            documents.append((path, document))

    interface_count = 0
    for path, document in documents:
        if "interface" not in document:
            continue
        interface_count += 1
        interface = document["interface"]
        identity = (str(interface.get("id")), str(interface.get("version")))
        if identity in identities:
            errors.append(f"{path}: duplicate interface identity {identity}")
        identities.add(identity)
        errors.extend(lint_interface(path, document))

    covered: set[tuple[str, str]] = set()
    implementation_count = 0
    scenario_count = 0
    for path, document in documents:
        if "scenario" in document:
            scenario_count += 1
            scenario = document["scenario"]
            scenario_id = str(scenario.get("id"))
            if scenario_id in scenario_ids:
                errors.append(f"{path}: duplicate scenario id {scenario_id}")
            scenario_ids.add(scenario_id)
            identity = (str(scenario.get("interface")), str(scenario.get("version")))
            if identity not in identities:
                errors.append(f"{path}: scenario references unknown Interface version {identity}")
            covered.add(identity)
        if "implementation" in document:
            implementation_count += 1
            for implemented in document.get("implements", []):
                identity = (str(implemented.get("interface")), str(implemented.get("version")))
                if identity not in identities:
                    errors.append(f"{path}: implementation references unknown Interface version {identity}")

    for identity in sorted(identities - covered):
        errors.append(f"Interface version has no machine-readable conformance scenario: {identity}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"linted {interface_count} interfaces, {scenario_count} scenarios, "
        f"and {implementation_count} implementation manifests"
    )
    return 0


def path_exists(repo: Path, value: str) -> bool:
    return (repo / value).exists()


def cmd_context(args: argparse.Namespace) -> int:
    repo = repo_root_from(Path(args.path))
    errors: list[str] = []
    manifests = sorted(repo.rglob("CONTEXT.yaml"))
    schema = repo / "contracts" / "schemas" / "nidl" / "0.1" / "context.schema.json"
    schema_data = json.loads(schema.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema_data)
    for manifest in manifests:
        data = load_yaml(manifest)
        for error in validator.iter_errors(data):
            errors.append(f"{manifest}:{'/'.join(map(str, error.path))}: {error.message}")
        for key in ["required_context", "optional_context", "forbidden_context"]:
            values = data.get(key, []) or []
            if not isinstance(values, list):
                continue
            for value in values:
                if key != "forbidden_context" and not path_exists(repo, value):
                    errors.append(f"{manifest}: {key} path does not exist: {value}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"validated {len(manifests)} context manifests")
    return 0


def crate_dependencies(cargo_path: Path) -> set[str]:
    data = tomllib.loads(cargo_path.read_text(encoding="utf-8"))
    return set((data.get("dependencies") or {}).keys())


def cmd_boundaries(args: argparse.Namespace) -> int:
    policy = load_yaml(Path(args.policy))
    root = Path(args.rust_root)
    errors = []
    checked = 0
    for crate, rules in (policy.get("crates") or {}).items():
        cargo = root / "crates" / crate / "Cargo.toml"
        if not cargo.exists():
            errors.append(f"missing Cargo.toml for policy crate {crate}")
            continue
        checked += 1
        deps = crate_dependencies(cargo)
        forbidden = set(rules.get("forbid") or [])
        allowed = set(rules.get("allow") or [])
        for dep in sorted(deps & forbidden):
            errors.append(f"{crate}: forbidden dependency {dep}")
        local_deps = {dep for dep in deps if dep.startswith("nova-")}
        for dep in sorted(local_deps - allowed):
            errors.append(f"{crate}: local dependency not declared in allow list: {dep}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"checked dependency boundaries for {checked} crates")
    return 0


def map_by_name(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("name")): item for item in items}


def cmd_compatibility(args: argparse.Namespace) -> int:
    old = load_yaml(Path(args.baseline))
    new = load_yaml(Path(args.candidate))
    reasons = []
    classification = "compatible-addition"
    if old.get("interface", {}).get("id") != new.get("interface", {}).get("id"):
        reasons.append("Interface IDs differ")
        classification = "breaking"
    for section in ["operations", "events", "errors", "capabilities"]:
        old_map = map_by_name(old.get(section, []))
        new_map = map_by_name(new.get(section, []))
        removed = sorted(set(old_map) - set(new_map))
        for name in removed:
            reasons.append(f"removed {section[:-1]} {name}")
            classification = "breaking"
        for name in sorted(set(old_map) & set(new_map)):
            if old_map[name].get("id") != new_map[name].get("id"):
                reasons.append(f"changed identifier for {section[:-1]} {name}")
                classification = "breaking"
    if canonical_bytes(old) == canonical_bytes(new):
        classification = "identical"
    print(classification)
    for reason in reasons:
        print(f"- {reason}")
    return 1 if classification == "breaking" and not args.allow_breaking else 0



def cmd_matrix(args: argparse.Namespace) -> int:
    source = Path(args.path)
    repo = repo_root_from(source)
    interfaces: dict[tuple[str, str], dict[str, Any]] = {}
    scenarios: dict[tuple[str, str], list[str]] = {}
    implementations: dict[tuple[str, str], list[str]] = {}
    for path in yaml_files(source):
        document = load_yaml(path)
        if not isinstance(document, dict):
            continue
        if "interface" in document:
            item = document["interface"]
            interfaces[(str(item["id"]), str(item["version"]))] = item
        if "scenario" in document:
            item = document["scenario"]
            key = (str(item["interface"]), str(item["version"]))
            scenarios.setdefault(key, []).append(str(item["id"]))
        if "implementation" in document:
            implementation_id = str(document["implementation"]["id"])
            for implemented in document.get("implements", []):
                key = (str(implemented["interface"]), str(implemented["version"]))
                implementations.setdefault(key, []).append(implementation_id)
    lines = [
        "# Interface compliance matrix",
        "",
        "Generated from NIDL sources and implementation manifests. Do not edit manually.",
        "",
        "| Interface | Version | Kind | Scenarios | Declared providers |",
        "|---|---:|---|---:|---|",
    ]
    for key in sorted(interfaces):
        item = interfaces[key]
        provider_list = ", ".join(sorted(implementations.get(key, []))) or "none"
        lines.append(
            f"| {key[0]} | {key[1]} | {item['kind']} | "
            f"{len(scenarios.get(key, []))} | {provider_list} |"
        )
    content = "\n".join(lines) + "\n"
    output = repo / "generated" / "documentation" / "compliance-matrix.md"
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != content:
            print(f"generated matrix is missing or stale: {output}", file=sys.stderr)
            return 1
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
    print(f"{'checked' if args.check else 'generated'} compliance matrix")
    return 0

def cmd_fingerprint(args: argparse.Namespace) -> int:
    path = Path(args.path)
    document = load_yaml(path)
    digest = hashlib.sha256(canonical_bytes(document)).hexdigest()
    print(digest)
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="nova-contract")
    sub = root.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)

    normalize = sub.add_parser("normalize")
    normalize.add_argument("path")
    normalize.add_argument("--check", action="store_true")
    normalize.set_defaults(func=cmd_normalize)

    lint = sub.add_parser("lint")
    lint.add_argument("path")
    lint.set_defaults(func=cmd_lint)

    context = sub.add_parser("context")
    context.add_argument("path")
    context.set_defaults(func=cmd_context)

    boundaries = sub.add_parser("boundaries")
    boundaries.add_argument("policy")
    boundaries.add_argument("rust_root")
    boundaries.set_defaults(func=cmd_boundaries)

    compatibility = sub.add_parser("compatibility")
    compatibility.add_argument("baseline")
    compatibility.add_argument("candidate")
    compatibility.add_argument("--allow-breaking", action="store_true")
    compatibility.set_defaults(func=cmd_compatibility)

    matrix = sub.add_parser("matrix")
    matrix.add_argument("path")
    matrix.add_argument("--check", action="store_true")
    matrix.set_defaults(func=cmd_matrix)

    fingerprint = sub.add_parser("fingerprint")
    fingerprint.add_argument("path")
    fingerprint.set_defaults(func=cmd_fingerprint)

    return root


def main() -> None:
    args = parser().parse_args()
    try:
        status = args.func(args)
    except Exception as exc:  # noqa: BLE001
        print(f"nova-contract: {exc}", file=sys.stderr)
        status = 2
    raise SystemExit(status)


if __name__ == "__main__":
    main()
