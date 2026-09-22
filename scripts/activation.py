#!/usr/bin/env python3
"""
PixzFlow Activation — post-install self-learning state machine (2.1.0).

The machine-verifiable half of `pixz.core.self-learning`: it detects whether the
current environment has adapted to the installed PixzFlow workflow, baselines the
capability inventory with content digests, detects drift (skill added / removed /
version changed / content changed), and records the adaptation transition. The
behavioral half (actually changing working behavior + verifying it) belongs to the
agent; this script refuses to record "ready" without evidence.

State file: .pixz/adaptation-state.json (schemas/adaptation-state.schema.json).

Commands:
  status        probe: STATE=NEW|BASELINED|READY|STALE, drift report
  init          create the baseline (refuses if state exists, unless --force)
  mark-adapted  baselined|stale -> ready; REQUIRES --evidence (anti-fake gate)
  sync          accept current inventory after inspecting a delta (records drift)
  mark-installed  record that capabilities were verified at their install location

Exit codes: 0 = READY (no drift) · 10 = attention (new/baselined/stale/drift)
            · 1 = error (bad state, bad registry) · 2 = usage error.

No external dependencies (stdlib only), so it runs wherever Python 3 runs.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "1.0"
EXIT_READY = 0
EXIT_ATTENTION = 10
EXIT_ERROR = 1

DIMENSION_KEYS = {"state_persistence", "verification", "delegation", "research"}


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_registry(root):
    reg_path = root / "registry.json"
    if not reg_path.exists():
        raise FileNotFoundError(f"registry.json not found at {reg_path}")
    return json.loads(reg_path.read_text(encoding="utf-8"))


def skill_digest(root, skill):
    path = root / skill.get("path", "")
    parts = []
    for fname in ("SKILL.md", "metadata.yaml"):
        f = path / fname
        if not f.exists():
            raise FileNotFoundError(f"missing {f} for skill {skill.get('id')}")
        parts.append(f.read_bytes())
    return hashlib.sha256(b"\x00".join(parts)).hexdigest()


def current_inventory(root):
    reg = load_registry(root)
    inv = []
    for s in reg.get("skills", []):
        inv.append({
            "id": s["id"],
            "version": s["version"],
            "path": s.get("path", ""),
            "digest": skill_digest(root, s),
            "installed": False,
            "verified": False,
        })
    return reg, inv


def state_path_for(args):
    if args.state:
        return Path(args.state)
    root = Path(args.root) if args.root else ROOT
    return root / ".pixz" / "adaptation-state.json"


def load_state(path):
    if not path.exists():
        return None
    try:
        st = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"adaptation state is not valid JSON ({e}); re-init with --force")
    for req in ("schema_version", "pixzflow", "inventory", "adaptation"):
        if req not in st:
            raise ValueError(f"adaptation state missing required key '{req}'; re-init with --force")
    if st.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"adaptation state schema_version {st.get('schema_version')!r} != {SCHEMA_VERSION}; re-init with --force")
    return st


def save_state(path, st):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(st, indent=2) + "\n", encoding="utf-8")


def add_history(st, event, summary):
    st.setdefault("history", []).append({"at": now_iso(), "event": event, "summary": summary})
    # compact event log: keep the newest 50
    st["history"] = st["history"][-50:]


def compute_drift(stored_inv, current_inv):
    stored = {e["id"]: e for e in stored_inv}
    current = {e["id"]: e for e in current_inv}
    drift = []
    for sid, cur in current.items():
        if sid not in stored:
            drift.append({"id": sid, "change": "added", "detail": f"new skill v{cur['version']}"})
        else:
            old = stored[sid]
            if old["version"] != cur["version"] and old["digest"] != cur["digest"]:
                drift.append({"id": sid, "change": "version", "detail": f"{old['version']} -> {cur['version']} (content changed)"})
            elif old["version"] != cur["version"]:
                drift.append({"id": sid, "change": "version-only", "detail": f"{old['version']} -> {cur['version']} (no content delta — inspect before assuming behavior change)"})
            elif old["digest"] != cur["digest"]:
                drift.append({"id": sid, "change": "content", "detail": "same version, different content (digest drift)"})
    for sid in stored:
        if sid not in current:
            drift.append({"id": sid, "change": "removed", "detail": f"was v{stored[sid]['version']}"})
    return drift


def effective_status(st, drift):
    if st is None:
        return "NEW"
    if drift:
        return "STALE"
    return st["adaptation"].get("status", "baselined").upper()


def cmd_status(args):
    root = Path(args.root) if args.root else ROOT
    path = state_path_for(args)
    try:
        reg, cur_inv = current_inventory(root)
        st = load_state(path)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"STATE=ERROR — {e}")
        return EXIT_ERROR
    if st is None:
        print("STATE=NEW — no adaptation state; run: activation.py init (first activation)")
        print(f"pixzflow={reg.get('version')} skills={len(cur_inv)}")
        return EXIT_ATTENTION
    drift = compute_drift(st.get("inventory", []), cur_inv)
    status = effective_status(st, drift)
    print(f"STATE={status}")
    print(f"pixzflow={reg.get('version')} (adapted={st['pixzflow'].get('version')}) "
          f"skills={len(cur_inv)} adaptation={st['adaptation'].get('status')}")
    if drift:
        print("DRIFT:")
        for d in drift:
            print(f"  {d['change']:>13}  {d['id']}  — {d['detail']}")
        print("Inspect the actual delta before assuming behavior change; then re-adapt and run: "
              "activation.py sync && activation.py mark-adapted --evidence ...")
    elif status == "READY":
        ev = st["adaptation"].get("evidence", "")
        print(f"evidence: {ev[:200]}")
        print("Adaptation verified; continue working — do NOT re-run setup.")
    return EXIT_READY if status == "READY" else EXIT_ATTENTION


def cmd_init(args):
    root = Path(args.root) if args.root else ROOT
    path = state_path_for(args)
    if path.exists() and not args.force:
        print(f"STATE EXISTS at {path} — refusing duplicate setup (second activation is a check, not a re-run).")
        print("Use 'status' to probe; use --force only to rebuild the baseline deliberately.")
        return EXIT_ATTENTION
    try:
        reg, inv = current_inventory(root)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"INIT FAILED — {e}")
        return EXIT_ERROR
    dims = {"state_persistence": "unknown", "verification": "unknown",
            "delegation": "unknown", "research": "unknown"}
    if args.dim:
        for kv in args.dim:
            if "=" not in kv:
                print(f"bad --dim {kv!r} (want key=value)")
                return 2
            k, v = kv.split("=", 1)
            if k in DIMENSION_KEYS and v not in ("yes", "no", "unknown"):
                print(f"bad --dim value for {k}: {v!r} (want yes|no|unknown)")
                return 2
            if k in DIMENSION_KEYS:
                dims[k] = v
            elif k in ("tools", "session"):
                dims[k] = v
            else:
                print(f"unknown dimension key {k!r}")
                return 2
    st = {
        "schema_version": SCHEMA_VERSION,
        "runtime": {
            "name": args.runtime or "unknown",
            "model": args.model or "unknown",
            "signals": [s for s in (args.signal or [])],
            "instruction_sources": [s for s in (args.instruction_source or [])],
        },
        "pixzflow": {
            "version": reg.get("version", "unknown"),
            "source": args.source or "unknown",
            "channel": args.channel or "stable",
        },
        "dimensions": dims,
        "inventory": inv,
        "adaptation": {"status": "baselined", "baselined_at": now_iso()},
        "learning": {"lessons": [], "improvements": []},
        "history": [],
    }
    add_history(st, "init", f"baseline: {len(inv)} skills, pixzflow {reg.get('version')}")
    save_state(path, st)
    print(f"STATE=BASELINED — wrote {path}")
    print(f"pixzflow={reg.get('version')} skills={len(inv)} runtime={st['runtime']['name']}")
    print("Next: ADAPT behavior + VERIFY it, then: activation.py mark-adapted --evidence '<what was observed>'")
    return EXIT_ATTENTION


def cmd_mark_adapted(args):
    root = Path(args.root) if args.root else ROOT
    path = state_path_for(args)
    try:
        _, cur_inv = current_inventory(root)
        st = load_state(path)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"MARK-ADAPTED FAILED — {e}")
        return EXIT_ERROR
    if st is None:
        print("no adaptation state — run 'init' first")
        return EXIT_ATTENTION
    if not args.evidence or not args.evidence.strip():
        print("REFUSED — --evidence is required. 'ready' is a verified claim, not an assertion "
              "(verification-depth ladder: RUNTIME-ACTIVE needs runtime evidence).")
        return EXIT_ERROR
    drift = compute_drift(st.get("inventory", []), cur_inv)
    if drift:
        print(f"REFUSED — {len(drift)} unexamined drift item(s); inspect the delta, re-adapt, then 'sync' before 'mark-adapted'.")
        for d in drift:
            print(f"  {d['change']:>13}  {d['id']}  — {d['detail']}")
        return EXIT_ATTENTION
    if st["adaptation"].get("status") == "ready":
        print("already READY with no drift — nothing to adapt (duplicate-setup guard).")
        return EXIT_READY
    st["adaptation"]["status"] = "ready"
    st["adaptation"]["evidence"] = args.evidence.strip()
    st["adaptation"]["adapted_at"] = now_iso()
    add_history(st, "adapted", f"adaptation verified: {args.evidence.strip()[:140]}")
    save_state(path, st)
    print("STATE=READY — adaptation recorded with evidence.")
    return EXIT_READY


def cmd_sync(args):
    root = Path(args.root) if args.root else ROOT
    path = state_path_for(args)
    try:
        reg, cur_inv = current_inventory(root)
        st = load_state(path)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"SYNC FAILED — {e}")
        return EXIT_ERROR
    if st is None:
        print("no adaptation state — run 'init' first")
        return EXIT_ATTENTION
    old = {e["id"]: e for e in st.get("inventory", [])}
    drift = compute_drift(st.get("inventory", []), cur_inv)
    # carry over installed/verified flags for unchanged skills
    for entry in cur_inv:
        prev = old.get(entry["id"])
        if prev and prev["digest"] == entry["digest"]:
            entry["installed"] = prev.get("installed", False)
            entry["verified"] = prev.get("verified", False)
    st["inventory"] = cur_inv
    st["pixzflow"]["version"] = reg.get("version", st["pixzflow"].get("version"))
    if drift:
        add_history(st, "drift-detected", f"{len(drift)} change(s): " +
                    "; ".join(f"{d['id']}:{d['change']}" for d in drift)[:200])
        if st["adaptation"].get("status") == "ready":
            st["adaptation"]["status"] = "stale"
            st["adaptation"]["notes"] = "drift accepted by sync; re-adapt the delta and mark-adapted"
        add_history(st, "synced", f"inventory updated to pixzflow {reg.get('version')} ({len(cur_inv)} skills)")
        save_state(path, st)
        print(f"SYNCED with drift ({len(drift)} change(s)); adaptation.status={st['adaptation']['status']}")
        for d in drift:
            print(f"  {d['change']:>13}  {d['id']}  — {d['detail']}")
        print("Version/content change != behavior change: inspect the delta, re-adapt only what changed,")
        print("then: activation.py mark-adapted --evidence '<what was re-verified>'")
        return EXIT_ATTENTION
    add_history(st, "synced", f"inventory refreshed, no drift ({len(cur_inv)} skills)")
    save_state(path, st)
    print(f"SYNCED — no drift ({len(cur_inv)} skills); adaptation.status={st['adaptation']['status']}")
    return EXIT_READY if st["adaptation"]["status"] == "ready" else EXIT_ATTENTION


def cmd_mark_installed(args):
    path = state_path_for(args)
    try:
        st = load_state(path)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"MARK-INSTALLED FAILED — {e}")
        return EXIT_ERROR
    if st is None:
        print("no adaptation state — run 'init' first")
        return EXIT_ATTENTION
    changed = 0
    for entry in st.get("inventory", []):
        if args.all or entry["id"] in (args.id or []):
            entry["installed"] = True
            entry["verified"] = True
            changed += 1
    if changed == 0:
        print("no matching skill ids in inventory")
        return EXIT_ERROR
    add_history(st, "note", f"install verified for {changed} skill(s)")
    save_state(path, st)
    print(f"recorded installed+verified for {changed} skill(s)")
    return EXIT_READY


def main():
    p = argparse.ArgumentParser(description="PixzFlow post-install activation state machine (2.1.0)")
    p.add_argument("--state", help="adaptation-state path (default <root>/.pixz/adaptation-state.json)")
    p.add_argument("--root", help="PixzFlow source root containing registry.json (default: this repo)")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("status", help="probe adaptation state + drift")

    pi = sub.add_parser("init", help="create the adaptation baseline (first activation)")
    pi.add_argument("--force", action="store_true", help="rebuild even if state exists")
    pi.add_argument("--runtime", help="claude|openclaw|opencode|hermes|codex|cursor|generic|<other>")
    pi.add_argument("--model", help="model self-report if available")
    pi.add_argument("--source", help="where PixzFlow came from (repo@sha, skills.sh, copy)")
    pi.add_argument("--channel", choices=["latest", "stable", "pinned"])
    pi.add_argument("--signal", action="append", help="observable runtime identity signal (repeatable)")
    pi.add_argument("--instruction-source", action="append", help="how the runtime reaches PixzFlow (repeatable)")
    pi.add_argument("--dim", action="append",
                    help="dimension key=value: state_persistence|verification|delegation|research=yes|no|unknown, tools=..., session=... (repeatable)")

    pm = sub.add_parser("mark-adapted", help="record verified adaptation (requires --evidence)")
    pm.add_argument("--evidence", required=True, help="what was actually observed (command output refs, eval ids)")

    sub.add_parser("sync", help="accept current inventory after inspecting drift")

    pmi = sub.add_parser("mark-installed", help="record discovery-verified installation")
    pmi.add_argument("--id", action="append", help="skill id (repeatable)")
    pmi.add_argument("--all", action="store_true")

    args = p.parse_args()
    handlers = {"status": cmd_status, "init": cmd_init, "mark-adapted": cmd_mark_adapted,
                "sync": cmd_sync, "mark-installed": cmd_mark_installed}
    if args.cmd not in handlers:
        p.print_help()
        return 2
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
