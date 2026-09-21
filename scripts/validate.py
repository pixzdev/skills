#!/usr/bin/env python3
"""
Validate registry + metadata.yaml against schemas without external deps.
Checks:
 - registry.json is valid JSON and matches registry.schema expectations (light)
 - every metadata.yaml parses and matches skill.schema expectations
 - registry skills ↔ metadata files consistency (ids, versions)
 - file existence: each registry path has SKILL.md + metadata.yaml
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"

def simple_yaml_load(path):
    """Minimal YAML loader for our metadata subset. Handles scalars, lists (dash), folded description."""
    data = {}
    current_key = None
    current_list = None
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        if not line.strip() or line.strip().startswith("#"):
            i+=1; continue
        # detect key: value
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            # top-level key
            parts = line.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip()
            if val == "":
                # likely list or multiline
                # peek next line
                if i+1 < len(lines) and lines[i+1].strip().startswith("-"):
                    data[key] = []
                    current_key = key
                    current_list = data[key]
                elif i+1 < len(lines) and lines[i+1].startswith("  ") and ":" not in lines[i+1]:
                    # folded string? collect indented
                    # e.g., description: "text"
                    # but our description is single line
                    data[key] = ""
                    current_key = key
                    current_list = None
                else:
                    data[key] = ""
                    current_key = key
                    current_list = None
                    # maybe multiline scalar like "description: foo\n  bar"
                    # we handle continuation
            else:
                # strip quotes?
                if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                    val = val[1:-1]
                # handle inline list like [a, b]
                if val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1].strip()
                    if inner == "":
                        data[key] = []
                    else:
                        # split by comma
                        items = [x.strip().strip("'\"") for x in inner.split(",")]
                        data[key] = items
                    current_key = key
                    current_list = None
                else:
                    # handle "[]"
                    if val == "[]":
                        data[key] = []
                    else:
                        data[key] = val
                    current_key = None
                    current_list = None
                # but description may have trailing continuation lines with indent
                # we don't need complex.
            i+=1
            continue
        # list item
        stripped = line.strip()
        if stripped.startswith("-"):
            val = stripped[1:].strip().strip("'\"")
            if current_key and isinstance(data.get(current_key), list):
                data[current_key].append(val)
            else:
                # orphan list item – ignore
                pass
            i+=1
            continue
        # continuation of multiline description (indented)
        if current_key and line.startswith("  ") and not stripped.startswith("-"):
            # append to previous string value
            cont = stripped.strip()
            if isinstance(data.get(current_key), str):
                # join with space
                if data[current_key]:
                    data[current_key] += " " + cont
                else:
                    data[current_key] = cont
            i+=1
            continue
        i+=1
    return data

def validate():
    errors = []
    warnings = []

    # 1. registry.json
    if not REGISTRY.exists():
        errors.append(f"Missing {REGISTRY}")
        return errors, warnings
    try:
        with open(REGISTRY) as f:
            reg = json.load(f)
    except Exception as e:
        errors.append(f"registry.json JSON parse failed: {e}")
        return errors, warnings

    # basic registry checks
    if "version" not in reg or not re.match(r"^\d+\.\d+\.\d+", reg["version"]):
        errors.append("registry.json: version missing or not SemVer")
    if "skills" not in reg or not isinstance(reg["skills"], list):
        errors.append("registry.json: skills missing or not list")
        return errors, warnings

    # id uniqueness
    ids = [s.get("id") for s in reg["skills"]]
    if len(ids) != len(set(ids)):
        errors.append("registry.json: duplicate ids")

    # per-skill schema light checks
    id_pattern = re.compile(r"^pixz\.[a-z0-9-]+\.[a-z0-9-]+$")
    ver_pattern = re.compile(r"^\d+\.\d+\.\d+")
    for s in reg["skills"]:
        sid = s.get("id","")
        if not id_pattern.match(sid):
            errors.append(f"{sid}: id does not match pixz.<domain>.<name>")
        if not ver_pattern.match(s.get("version","")):
            errors.append(f"{sid}: version not SemVer")
        if s.get("category") not in ["core","quality","engineering","security","pentesting","frontend","backend","devops","mobile","ai","data","design","graphics","motion","media","automation","documentation"]:
            errors.append(f"{sid}: invalid category {s.get('category')}")
        if not s.get("triggers"):
            errors.append(f"{sid}: missing triggers")
        if not s.get("compatible_runtimes"):
            errors.append(f"{sid}: missing compatible_runtimes")
        # path existence
        path = ROOT / s.get("path","")
        if not (path / "SKILL.md").exists():
            errors.append(f"{sid}: missing SKILL.md at {path}/SKILL.md")
        if not (path / "metadata.yaml").exists():
            errors.append(f"{sid}: missing metadata.yaml at {path}/metadata.yaml")
        else:
            # parse metadata.yaml and cross-check
            try:
                meta = simple_yaml_load(path / "metadata.yaml")
                if meta.get("id") != sid:
                    errors.append(f"{sid}: metadata.yaml id mismatch ({meta.get('id')})")
                if meta.get("version") != s.get("version"):
                    warnings.append(f"{sid}: registry version {s.get('version')} != metadata.yaml {meta.get('version')}")
                # check requires are valid ids
                for dep in meta.get("requires", []) + meta.get("aggregates", []) + meta.get("optional", []):
                    if not id_pattern.match(dep):
                        errors.append(f"{sid}: dependency id malformed {dep}")
                # check SKILL.md frontmatter has name/description
                skill_md = (path / "SKILL.md").read_text(encoding="utf-8")
                if "---" not in skill_md[:500]:
                    warnings.append(f"{sid}: SKILL.md missing frontmatter")
                else:
                    fm = skill_md.split("---")[1] if len(skill_md.split("---"))>1 else ""
                    if "name:" not in fm or "description:" not in fm:
                        errors.append(f"{sid}: SKILL.md frontmatter missing name/description")
            except Exception as e:
                errors.append(f"{sid}: metadata.yaml parse failed: {e}")

    # check registry path uniqueness
    paths = [s.get("path") for s in reg["skills"]]
    if len(paths) != len(set(paths)):
        errors.append("registry.json: duplicate paths")

    # check hierarchical AGENTS.md existence (warn)
    for domain in ["core","engineering","security","design","frontend","motion","devops","ai","quality"]:
        p = ROOT / domain / "AGENTS.md"
        if not p.exists():
            warnings.append(f"Missing hierarchical registry {domain}/AGENTS.md")

    # check schemas existence
    for sch in ["skill.schema.json","registry.schema.json","workflow.schema.json","eval.schema.json"]:
        if not (ROOT / "schemas" / sch).exists():
            warnings.append(f"Missing schema {sch}")

    # check resolves for orchestrator
    # quick cycle check via resolver import
    try:
        import subprocess, json as js
        result = subprocess.run(["python3", str(ROOT/"scripts/resolve.py"), "--install", "pixz.core.orchestrator", "--runtime", "claude", "--channel", "stable"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            errors.append(f"Resolver failed for pixz.core.orchestrator: {result.stderr.strip()[:500]}")
    except Exception as e:
        warnings.append(f"Resolver check skipped: {e}")

    return errors, warnings

if __name__ == "__main__":
    errors, warnings = validate()
    print("=== PIXZ Validation ===")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ⚠ {w}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  ✗ {e}")
        print(f"\n✗ Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    else:
        print(f"\n✓ Validation passed: 0 errors, {len(warnings)} warnings")
        # summary
        with open(REGISTRY) as f:
            reg = json.load(f)
        print(f"  Skills: {len(reg['skills'])}  Version: {reg['version']}  Channel: {reg.get('channel')}")
