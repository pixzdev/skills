#!/usr/bin/env python3
"""
PixzFlow Adoption Assessment — how completely has this runtime adopted the
PixzFlow workflow? (2.2.0)

Doctrine (read before judging the number):
  - This is an ADOPTION score, not a quality score. It sums named, objectively
    checkable adoption facts (each worth fixed points, each printed PASS/FAIL
    with evidence). It never grades model quality, output quality, or workflow
    effectiveness — that belongs to the successor benchmark (UNRUN), and this
    repo does not invent numeric quality scores (docs/evaluation.md).
  - UNVERIFIED items score 0 — gaps are listed, never credited.
  - Auto-runs after `activation.py mark-adapted` (first-run completion), so the
    install prompt does not need to remember it.

Groups (100 points total):
  A. Installation & discovery ........ 30
  B. Activation & adaptation ......... 35
  C. Operability ..................... 25
  D. Learning & continuity ........... 10

Usage:
  python3 scripts/assess.py [--state PATH] [--root PATH] [--runtime NAME] [--full]
  --full  additionally RUNS layer-1 structural checks + lifecycle suite and
          reports them as evidence (points unchanged; depth of proof improves).

Exit: 0 = assessed (any score) · 1 = assessment itself failed (bad inputs).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import activation as act  # noqa: E402

VERDICTS = [(90, "FULLY ADOPTED"), (70, "SUBSTANTIALLY ADOPTED"), (40, "PARTIALLY ADOPTED"), (0, "NOT ADOPTED")]


class Tally:
    def __init__(self):
        self.rows = []
        self.total = 0

    def add(self, group, points, ok, what, evidence="", hint=""):
        self.rows.append({"group": group, "points": points, "ok": bool(ok), "what": what,
                          "evidence": evidence, "hint": hint})
        if ok:
            self.total += points

    def subtotal(self, group):
        got = sum(r["points"] for r in self.rows if r["group"] == group and r["ok"])
        cap = sum(r["points"] for r in self.rows if r["group"] == group)
        return got, cap


def assess(root, state_path, runtime=None, full=False):
    t = Tally()

    # ---------- A. Installation & discovery (30) ----------
    reg = None
    try:
        reg = json.loads((root / "registry.json").read_text(encoding="utf-8"))
        t.add("A", 10, re.match(r"^\d+\.\d+\.\d+", reg.get("version", "")),
              "A1 registry.json parses, version SemVer", f"version={reg.get('version')}")
    except Exception as e:
        t.add("A", 10, False, "A1 registry.json parses, version SemVer", str(e), "is --root a PixzFlow source root?")

    if reg:
        bad = []
        for s in reg.get("skills", []):
            p = root / s.get("path", "")
            if not re.match(r"^pixz\.[a-z0-9-]+\.[a-z0-9-]+$", s.get("id", "")) \
               or not re.match(r"^\d+\.\d+\.\d+", s.get("version", "")) \
               or not (p / "SKILL.md").exists() or not (p / "metadata.yaml").exists():
                bad.append(s.get("id"))
        t.add("A", 10, not bad, "A2 skills well-formed (ids, SemVer, files present)",
              f"{len(reg.get('skills', []))} skills" + (f"; bad: {bad}" if bad else ""))
    else:
        t.add("A", 10, False, "A2 skills well-formed", "no registry")

    st = None
    if state_path and state_path.exists():
        try:
            st = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            st = None
    installed_flags = st and any(e.get("installed") and e.get("verified") for e in st.get("inventory", []))
    t.add("A", 10, bool(installed_flags), "A3 installation recorded as discovery-verified in adaptation state",
          "inventory carries installed+verified flags" if installed_flags else "no verified-install record",
          hint="run the install protocol, then activation.py mark-installed")

    # ---------- B. Activation & adaptation (35) ----------
    t.add("B", 5, st is not None, "B1 adaptation state exists and parses",
          str(state_path) if st else "missing", hint="scripts/activation.py init")
    if st and reg:
        try:
            drift = act.compute_drift(st.get("inventory", []), [
                {"id": s["id"], "version": s["version"], "path": s.get("path", ""),
                 "digest": act.skill_digest(root, s)} for s in reg.get("skills", [])])
            t.add("B", 10, not drift, "B2 inventory in sync with source (no drift)",
                  "no drift" if not drift else f"{len(drift)} change(s)", hint="inspect delta, then activation.py sync")
        except Exception as e:
            t.add("B", 10, False, "B2 inventory in sync with source (no drift)", str(e))
        adapt = st.get("adaptation", {})
        ready = adapt.get("status") == "ready"
        t.add("B", 10, ready, "B3 adaptation.status == ready",
              f"status={adapt.get('status')}", hint="adapt behavior, verify at RUNTIME-ACTIVE depth, mark-adapted")
        t.add("B", 5, bool(str(adapt.get("evidence", "")).strip()), "B4 adaptation evidence recorded",
              (adapt.get("evidence") or "")[:80] or "(empty)", hint="mark-adapted refuses without evidence — that's the point")
        dims = st.get("dimensions", {})
        known = sum(1 for k in ("state_persistence", "verification", "delegation", "research") if dims.get(k) != "unknown")
        rt_known = (st.get("runtime", {}).get("name") or "unknown") != "unknown"
        t.add("B", 5, rt_known and known >= 3, "B5 baseline recorded (runtime + >=3 known dimensions)",
              f"runtime={st.get('runtime', {}).get('name')}, known dims={known}/4",
              hint="scripts/doctor.py --write measures what is measurable")
    else:
        for pts, rid, what in ((10, "B2", "B2 inventory in sync"), (10, "B3", "B3 adaptation ready"),
                               (5, "B4", "B4 adaptation evidence"), (5, "B5", "B5 baseline recorded")):
            t.add("B", pts, False, what, "no adaptation state")

    # ---------- C. Operability (25) ----------
    probe = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "activation.py"),
                            "--state", str(state_path or root / ".pixz" / "adaptation-state.json"),
                            "--root", str(root), "status"], capture_output=True, text=True, timeout=60)
    t.add("C", 10, probe.returncode in (0, 10), "C1 activation probe functional (exit 0|10)",
          f"exit={probe.returncode}")
    schemas_ok = all(json.loads((root / "schemas" / s).read_text()) is not None
                     for s in ("task-state.schema.json", "adaptation-state.schema.json", "handoff.schema.json",
                               "skill.schema.json", "registry.schema.json", "eval.schema.json")
                     if (root / "schemas" / s).exists()) \
        and (root / "schemas" / "adaptation-state.schema.json").exists()
    t.add("C", 5, schemas_ok, "C2 schemas present and parse (incl. adaptation-state)")
    n_scen = len(list((root / "evals" / "behavioral").glob("eval.behavioral.*.json"))) if (root / "evals" / "behavioral").exists() else 0
    t.add("C", 5, n_scen >= 30 and (root / "evals" / "lifecycle" / "run_tests.py").exists(),
          "C3 evals present (>=30 behavioral scenarios + lifecycle suite)", f"behavioral={n_scen}")
    agents = (root / "AGENTS.md")
    agents_ok = agents.exists() and "Self-Learning" in agents.read_text(encoding="utf-8")
    t.add("C", 5, agents_ok, "C4 AGENTS.md reachable and carries the self-learning contract")

    # ---------- D. Learning & continuity (10) ----------
    valid_ledger = True
    ledger_info = "no ledger yet (fine before first lesson)"
    if st and st.get("learning"):
        lessons = st["learning"].get("lessons", [])
        imps = st["learning"].get("improvements", [])
        l_ok = all(l.get("id") and l.get("lesson") and l.get("status") in ("candidate", "stable", "superseded") for l in lessons)
        i_ok = all(i.get("id") and i.get("what") and i.get("kind") in ("mechanism", "test", "procedure", "policy-tweak")
                   and i.get("status") in ("proposed", "challenged", "implemented", "verified", "regressed", "rejected") for i in imps)
        valid_ledger = l_ok and i_ok
        ledger_info = f"lessons={len(lessons)}, improvements={len(imps)}"
    t.add("D", 5, valid_ledger, "D1 learning ledger structurally valid (statuses/kinds per schema)", ledger_info)
    hist = (st or {}).get("history", [])
    t.add("D", 5, st is not None and len(hist) <= 50, "D2 history present and bounded (<=50)",
          f"{len(hist)} entries" if st else "no state")

    # ---------- optional full-depth evidence (points unchanged) ----------
    full_results = []
    if full:
        for name, cmd in (("validate.py", ["validate.py"]), ("check-cycles.py", ["check-cycles.py"]),
                          ("lifecycle", [str(root / "evals" / "lifecycle" / "run_tests.py")])):
            exe = sys.executable if not name.startswith("lifecycle") else sys.executable
            target = [str(root / "scripts" / cmd[0])] if name != "lifecycle" else [cmd[0]]
            r = subprocess.run([exe] + target, capture_output=True, text=True, timeout=300)
            full_results.append({"check": name, "pass": r.returncode == 0})

    return t, full_results


def render(t, full_results, runtime):
    lines = []
    score = t.total
    verdict = next(v for cut, v in VERDICTS if score >= cut)
    lines.append("=== PIXZFLOW ADOPTION ASSESSMENT ===")
    lines.append(f"score: {score}/100 — {verdict}" + (f" (runtime: {runtime})" if runtime else ""))
    for group, title in (("A", "Installation & discovery"), ("B", "Activation & adaptation"),
                         ("C", "Operability"), ("D", "Learning & continuity")):
        got, cap = t.subtotal(group)
        lines.append(f"\n{group}. {title} — {got}/{cap}")
        for r in t.rows:
            if r["group"] != group:
                continue
            mark = "PASS" if r["ok"] else "FAIL"
            pts = f"+{r['points']}" if r["ok"] else " 0"
            lines.append(f"  [{mark}] {r['what']}  {pts}  ({r['evidence']})")
            if not r["ok"] and r.get("hint"):
                lines.append(f"         -> {r['hint']}")
    if full_results:
        lines.append("\nFull-depth evidence (layer-1 + lifecycle executed):")
        for fr in full_results:
            lines.append(f"  [{'PASS' if fr['pass'] else 'FAIL'}] {fr['check']}")
    lines.append("\nDoctrine: adoption score = sum of named evidence-backed checks. It is NOT a model-quality or")
    lines.append("workflow-effectiveness metric (successor benchmark, UNRUN). Unverified items score 0 by design.")
    return "\n".join(lines), score, verdict


def main():
    p = argparse.ArgumentParser(description="PixzFlow adoption assessment 0-100 (2.2.0)")
    p.add_argument("--state", help="adaptation-state path (default <root>/.pixz/adaptation-state.json)")
    p.add_argument("--root", help="PixzFlow source root (default: this repo)")
    p.add_argument("--runtime", help="runtime name (default: from adaptation state)")
    p.add_argument("--full", action="store_true", help="also run layer-1 structural + lifecycle checks as evidence")
    args = p.parse_args()
    root = Path(args.root) if args.root else ROOT
    state_path = Path(args.state) if args.state else root / ".pixz" / "adaptation-state.json"
    runtime = args.runtime
    if not runtime and state_path.exists():
        try:
            runtime = json.loads(state_path.read_text()).get("runtime", {}).get("name")
        except Exception:
            pass
    try:
        t, full_results = assess(root, state_path, runtime=runtime, full=args.full)
    except Exception as e:
        print(f"ASSESSMENT FAILED — {e}")
        return 1
    out, score, verdict = render(t, full_results, runtime)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
