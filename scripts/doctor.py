#!/usr/bin/env python3
"""
PixzFlow Doctor — measure runtime capabilities instead of assuming them (2.2.0).

Self-learning baselines used to rely on agent self-report (`init --dim ...`).
Doctor measures what is locally measurable and leaves the rest explicitly
`unknown` — OBSERVED over ASSUMPTION at the first step of the lifecycle.

Measured dimensions:
  state_persistence  write probe in the state directory (.pixz/)
  verification       command execution works (subprocess probe)
  tools              git / npx / openclaw / opencode / hermes / claude presence
  runtime signals    known skill paths / contract files found
  instruction source AGENTS.md reachable at the repo root

NOT locally measurable (stay unknown unless the agent records them):
  delegation (subagents), research (network) — report them, don't invent them.

Usage:
  python3 scripts/doctor.py [--root PATH] [--state PATH] [--json] [--write]
  --write  merge measured yes/no values into adaptation-state dimensions
           (fills only 'unknown' entries; never overwrites recorded values).

Exit: 0 always (diagnostic), 2 usage error.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME_PATHS = {
    "claude": [".claude/skills", "~/.claude/skills"],
    "opencode": [".opencode/skill", "~/.config/opencode/skill"],
    "hermes": ["skills", "~/.hermes/skills"],
    "openclaw": ["skills", "~/.openclaw/skills"],
    "codex": [".agents/skills"],
    "cursor": [".agents/skills", ".cursor/skills"],
    "generic": [".agents/skills", "skills"],
}

CLIS = ["git", "npx", "openclaw", "opencode", "hermes", "claude", "python3"]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def probe_write(state_dir):
    """Can we persist files where adaptation/task state live?"""
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        probe = state_dir / ".doctor-probe"
        probe.write_text("probe", encoding="utf-8")
        ok = probe.read_text(encoding="utf-8") == "probe"
        probe.unlink()
        return ok
    except Exception:
        return False


def probe_command(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False


def detect_runtime_signals(root):
    found = []
    candidates = []
    for rt, paths in RUNTIME_PATHS.items():
        for p in paths:
            full = Path(p).expanduser()
            if not full.is_absolute():
                full = root / p
            if full.is_dir():
                found.append(str(p))
                candidates.append(rt)
    if (root / "CLAUDE.md").exists():
        found.append("CLAUDE.md")
        candidates.append("claude")
    if (root / "AGENTS.md").exists():
        found.append("AGENTS.md")
    # rank: most specific signals first
    order = ["claude", "openclaw", "opencode", "hermes", "codex", "cursor", "generic"]
    ranked = [rt for rt in order if rt in candidates]
    return found, ranked


def doctor(root, state_path, as_json=False, write=False):
    report = {
        "at": now_iso(),
        "root": str(root),
        "dimensions": {},
        "tools": {},
        "runtime_signals": [],
        "runtime_candidates": [],
        "instruction_sources": [],
        "gaps": [],
    }

    # state persistence (measured)
    state_dir = state_path.parent if state_path else root / ".pixz"
    report["dimensions"]["state_persistence"] = "yes" if probe_write(state_dir) else "no"

    # verification capability (measured): can we execute commands at all?
    report["dimensions"]["verification"] = "yes" if probe_command([sys.executable, "--version"]) else "no"

    # not locally measurable — stay unknown
    report["dimensions"]["delegation"] = "unknown"
    report["dimensions"]["research"] = "unknown"
    report["gaps"].append("delegation: not locally observable — agent must record from runtime self-report")
    report["gaps"].append("research: network availability not probed — record if known")

    # tools inventory
    for cli in CLIS:
        report["tools"][cli] = shutil.which(cli) is not None

    # runtime signals
    signals, candidates = detect_runtime_signals(root)
    report["runtime_signals"] = signals
    report["runtime_candidates"] = candidates

    # instruction sources
    if (root / "AGENTS.md").exists():
        report["instruction_sources"].append("AGENTS.md (repo root)")
    if (root / "CLAUDE.md").exists():
        txt = (root / "CLAUDE.md").read_text(encoding="utf-8")
        if "@AGENTS.md" in txt:
            report["instruction_sources"].append("CLAUDE.md -> @AGENTS.md import")
        else:
            report["gaps"].append("CLAUDE.md exists but does not import @AGENTS.md")

    # registry readable?
    try:
        reg = json.loads((root / "registry.json").read_text(encoding="utf-8"))
        report["registry"] = {"version": reg.get("version"), "skills": len(reg.get("skills", []))}
    except Exception as e:
        report["registry"] = {"error": str(e)}
        report["gaps"].append("registry.json unreadable — is this a PixzFlow source root?")

    if write:
        if state_path and state_path.exists():
            try:
                st = json.loads(state_path.read_text(encoding="utf-8"))
                dims = st.setdefault("dimensions", {})
                filled = []
                for k in ("state_persistence", "verification"):
                    if dims.get(k, "unknown") == "unknown":
                        dims[k] = report["dimensions"][k]
                        filled.append(f"{k}={dims[k]}")
                if not dims.get("tools"):
                    have = [t for t, ok in report["tools"].items() if ok]
                    dims["tools"] = ",".join(have) if have else "none found"
                    filled.append("tools")
                if not st.get("runtime", {}).get("name") or st["runtime"].get("name") == "unknown":
                    if report["runtime_candidates"]:
                        st.setdefault("runtime", {})["name"] = report["runtime_candidates"][0]
                        filled.append(f"runtime={report['runtime_candidates'][0]}")
                st.setdefault("history", []).append(
                    {"at": now_iso(), "event": "note", "summary": "doctor: measured " + ", ".join(filled) if filled else "doctor: nothing new to fill"})
                st["history"] = st["history"][-50:]
                state_path.write_text(json.dumps(st, indent=2) + "\n", encoding="utf-8")
                report["written_to"] = str(state_path)
                report["filled"] = filled
            except Exception as e:
                report["write_error"] = str(e)
        else:
            report["write_error"] = "no adaptation state to update — run activation.py init first"

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("=== PixzFlow Doctor (measured baseline) ===")
        print(f"root: {root}")
        for k, v in report["dimensions"].items():
            print(f"  {k:<18} {v}")
        tools_have = [t for t, ok in report["tools"].items() if ok]
        print(f"  tools found        {', '.join(tools_have) if tools_have else '(none)'}")
        print(f"  runtime signals    {', '.join(report['runtime_signals']) if report['runtime_signals'] else '(none)'}")
        print(f"  runtime candidates {', '.join(report['runtime_candidates']) if report['runtime_candidates'] else '(none)'}")
        print(f"  instruction source {', '.join(report['instruction_sources']) if report['instruction_sources'] else '(none found)'}")
        reg = report.get("registry", {})
        if "error" in reg:
            print(f"  registry           ERROR — {reg['error']}")
        else:
            print(f"  registry           v{reg.get('version')} ({reg.get('skills')} skills)")
        for g in report["gaps"]:
            print(f"  gap: {g}")
        if report.get("written_to"):
            print(f"  wrote measured dimensions -> {report['written_to']} (filled: {', '.join(report.get('filled', [])) or 'none'})")
        if report.get("write_error"):
            print(f"  write skipped: {report['write_error']}")
        print("delegation/research remain UNKNOWN unless the agent records them — unknowns are never invented.")
    return 0


def main():
    p = argparse.ArgumentParser(description="PixzFlow Doctor — measured runtime baseline (2.2.0)")
    p.add_argument("--root", help="PixzFlow source root (default: this repo)")
    p.add_argument("--state", help="adaptation-state path (default <root>/.pixz/adaptation-state.json)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--write", action="store_true", help="merge measured values into adaptation state (unknowns only)")
    args = p.parse_args()
    root = Path(args.root) if args.root else ROOT
    state_path = Path(args.state) if args.state else root / ".pixz" / "adaptation-state.json"
    return doctor(root, state_path, as_json=args.json, write=args.write)


if __name__ == "__main__":
    sys.exit(main())
