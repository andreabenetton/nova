#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"


def validate_data(path: Path, data: object, schema: dict) -> list[str]:
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")
    return errors


def load_yaml(path: Path) -> tuple[object | None, list[str]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"{path.relative_to(ROOT)}: YAML error: {exc}"]


def load_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"{path.relative_to(ROOT)}: JSON error: {exc}"]


def main() -> int:
    scenario_schema = json.loads((SIM / "schemas" / "scenario.schema.json").read_text(encoding="utf-8"))
    profile_schema = json.loads((SIM / "schemas" / "profile.schema.json").read_text(encoding="utf-8"))
    trace_schema = json.loads((SIM / "schemas" / "trace.schema.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    scenarios = sorted((SIM / "scenarios").glob("*.yaml"))
    scenario_documents: list[tuple[Path, dict]] = []
    for scenario in scenarios:
        data, load_errors = load_yaml(scenario)
        errors.extend(load_errors)
        if load_errors:
            continue
        errors.extend(validate_data(scenario, data, scenario_schema))
        if isinstance(data, dict):
            scenario_documents.append((scenario, data))

    profiles = sorted((SIM / "profiles").glob("*.yaml"))
    profile_names: set[str] = set()
    for profile in profiles:
        data, load_errors = load_yaml(profile)
        errors.extend(load_errors)
        if load_errors:
            continue
        errors.extend(validate_data(profile, data, profile_schema))
        if not isinstance(data, dict) or not isinstance(data.get("name"), str):
            continue
        if data["name"] in profile_names:
            errors.append(f"{profile.relative_to(ROOT)}: duplicate profile name {data['name']!r}")
        profile_names.add(data["name"])

    for scenario, data in scenario_documents:
        for path in data.get("paths", []):
            profile = path.get("profile")
            if profile not in profile_names:
                errors.append(f"{scenario.relative_to(ROOT)}: unknown profile {profile!r}")

    traces = sorted((SIM / "traces").glob("*.json"))
    for trace in traces:
        data, load_errors = load_json(trace)
        errors.extend(load_errors)
        if load_errors:
            continue
        errors.extend(validate_data(trace, data, trace_schema))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"validated {len(scenarios)} simulation scenarios, "
        f"{len(profiles)} profiles, and {len(traces)} trace file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
