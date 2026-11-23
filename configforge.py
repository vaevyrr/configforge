#!/usr/bin/env python3
"""Validate and compare JSON/YAML configuration files."""
import argparse
import json
import sys
from pathlib import Path


def load_config(path: Path):
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(text)
    if suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("YAML support requires PyYAML: pip install PyYAML") from exc
        return yaml.safe_load(text)
    raise ValueError("file extension must be .json, .yaml or .yml")


def get_path(data, dotted):
    current = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def differences(left, right, prefix=""):
    changes = []
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(left.keys() - right.keys()):
            changes.append(("removed", f"{prefix}{key}", left[key], None))
        for key in sorted(right.keys() - left.keys()):
            changes.append(("added", f"{prefix}{key}", None, right[key]))
        for key in sorted(left.keys() & right.keys()):
            changes.extend(differences(left[key], right[key], f"{prefix}{key}."))
    elif left != right:
        changes.append(("changed", prefix.rstrip("."), left, right))
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="validate a configuration")
    check.add_argument("file", type=Path)
    check.add_argument("--require", action="append", default=[], metavar="KEY")
    diff = sub.add_parser("diff", help="compare two configurations")
    diff.add_argument("left", type=Path)
    diff.add_argument("right", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            data = load_config(args.file)
            missing = [key for key in args.require if not get_path(data, key)[0]]
            if missing:
                for key in missing:
                    print(f"MISSING {key}")
                return 1
            print(f"OK: {args.file} is valid")
            return 0
        left, right = load_config(args.left), load_config(args.right)
        changes = differences(left, right)
        if not changes:
            print("No differences.")
        for kind, key, before, after in changes:
            print(f"{kind.upper():7} {key}: {before!r} -> {after!r}" if kind == "changed"
                  else f"{kind.upper():7} {key}: {before if kind == 'removed' else after!r}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"configforge: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
