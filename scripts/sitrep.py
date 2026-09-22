#!/usr/bin/env python3
"""
PixzFlow Sitrep — one-command orientation report (2.2.0).

F3: a single compact block for ORIENT, post-compaction restore, and handoff.
Read-only: adaptation probe + active task-state + learning ledger highlights.
Designed to be cheap enough to run at every session start and small enough to
paste into a handoff context packet.

Usage:
  python3 scripts/sitrep.py [--root PATH] [--state PATH] [--task-state PATH]
Exit: 0 always (informational), 2 usage error.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser(description="PixzFlow situation report (2.2.0)")
    p.add_argument("--root", help="PixzFlow source root (default: this repo)")
    p.add_argument("--state", help="adaptation-state path (default <root>/.pixz/adaptation-state.json)")
    p.add_argument("--task-state", help="task-state path (default <root>/.pixz/task-state.json)")
    args = p.parse_args()
    root = Path(args.root) if args.root else ROOT
    state_path = Path(args.state) if args.state else root / ".pixz" / "adaptation-state.json"
    task_path = Path(args.task_state) if args.task_state else root / ".pixz" / "task-state.json"

    print("=== PIXZFLOW SITREP ===")

    # 1. adaptation probe (fresh process — proof it works, not a cached claim)
    probe = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "activation.py"),
                            "--state", str(state_path), "--root", str(root), "status"],
                           capture_output=True, text=True, timeout=60)
    first = probe.stdout.splitlines() or [""]
    print(f"ADAPTATION  {first[0]} (probe exit {probe.returncode})")

    st = read_json(state_path)
    if st:
        rt = st.get("runtime", {})
        dims = st.get("dimensions", {})
        known = [f"{k}={v}" for k, v in dims.items() if v not in (None, "unknown", "")]
        print(f"RUNTIME     {rt.get('name', 'unknown')} · model={rt.get('model', 'unknown')} · "
              f"dims: {', '.join(known) if known else 'unrecorded'}")
        learn = st.get("learning", {})
        lessons = learn.get("lessons", [])
        stable = [l for l in lessons if l.get("status") == "stable"]
        imps = learn.get("improvements", [])
        verified = [i for i in imps if i.get("status") == "verified"]
        print(f"LEARNING    lessons={len(lessons)} (stable={len(stable)}) · "
              f"improvements={len(imps)} (verified={len(verified)})")
        for l in stable[-3:]:
            print(f"  · {l.get('lesson', '')[:110]}")
    else:
        print("RUNTIME     no adaptation state — first activation pending (scripts/activation.py init)")

    # 2. active task state (continuity substrate)
    ts = read_json(task_path)
    if ts:
        caps = ts.get("capabilities", [])
        active = [c.get("id") for c in caps if c.get("status") in ("active", "reactivation_required")]
        adapt = ts.get("adaptation", {})
        print(f"TASK        [{ts.get('status', '?')}] {str(ts.get('objective', '(no objective)'))[:110]}")
        print(f"            mode={ts.get('mode', '?')} · adaptation={adapt.get('status', '?')} · "
              f"active caps: {', '.join(active) if active else '(none)'}")
        na = ts.get("next_action")
        print(f"NEXT ACTION {na if na else '(none recorded — resume protocol requires one at checkpoints)'}")
        unresolved = [u for c in caps for u in c.get("unresolved", [])]
        if unresolved:
            print(f"UNRESOLVED  {len(unresolved)} item(s); first: {unresolved[0][:100]}")
    else:
        print("TASK        no task state at .pixz/task-state.json (new task or stored elsewhere)")

    print("SITREP END — safe to paste into a handoff context packet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
