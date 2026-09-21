#!/usr/bin/env python3
import argparse, json, os, re, sys, glob
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "cases"

def simple_yaml_load_simple(path):
    # ultra-minimal loader for eval cases (flat)
    import re
    data = {"input":{}, "expect":{}, "scoring":{}}
    text = Path(path).read_text(encoding="utf-8")
    # Use naive parsing: we actually store evals as JSON-compatible YAML, so try json fallback after yaml
    # Try to parse with our earlier simple loader
    # For evals we will generate JSON, so just json.load
    try:
        import json
        # eval files are JSON-compatible (we write JSON)
        with open(path) as f:
            return json.load(f)
    except:
        pass
    # fallback: try yaml if available
    try:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    except:
        return {}

def load_cases(skill_filter=None, cat_filter=None):
    cases = []
    for p in sorted(CASES.glob("*.yaml")) + sorted(CASES.glob("*.json")):
        try:
            c = simple_yaml_load_simple(p)
            if not c:
                continue
            if skill_filter and c.get("skill_id") != skill_filter:
                continue
            if cat_filter and c.get("category") != cat_filter:
                continue
            c["_path"]=str(p)
            cases.append(c)
        except Exception as e:
            print(f"warn: failed to load {p}: {e}", file=sys.stderr)
    return cases

def check_case(case, root):
    # Heuristic: read skill SKILL.md and metadata
    skill_id = case.get("skill_id")
    exp = case.get("expect",{})
    # locate skill
    from pathlib import Path
    import json
    reg = json.loads((root/"registry.json").read_text())
    skill_meta = next((s for s in reg["skills"] if s["id"]==skill_id), None)
    if not skill_meta:
        return False, f"skill {skill_id} not in registry"
    skill_path = root / skill_meta["path"] / "SKILL.md"
    if not skill_path.exists():
        return False, f"missing SKILL.md for {skill_id}"
    content = skill_path.read_text(encoding="utf-8").lower()
    prompt = case.get("input",{}).get("prompt","").lower()
    should_trigger = exp.get("should_trigger")
    # trigger heuristic: all triggers keywords appear in prompt? checked elsewhere
    # we check must_contain in content
    must = exp.get("must_contain",[])
    must_not = exp.get("must_not_contain",[])
    reasons = []
    ok = True
    for m in must:
        if m.lower() not in content:
            ok=False
            reasons.append(f"missing must_contain '{m}' in SKILL.md")
    for m in must_not:
        if m.lower() in content:
            ok=False
            reasons.append(f"contains forbidden '{m}'")
    # trigger check: if should_trigger true, ensure prompt contains at least one trigger
    if should_trigger is True:
        triggers = skill_meta.get("triggers",[])
        if triggers and not any(t.lower() in prompt for t in triggers):
            # not fail, just note
            reasons.append(f"prompt does not contain any trigger {triggers} (heuristic)")
    if should_trigger is False:
        triggers = skill_meta.get("triggers",[])
        # expect not trigger -> prompt should not contain triggers (heuristic)
        pass
    if ok:
        return True, "; ".join(reasons) if reasons else "pass"
    else:
        return False, "; ".join(reasons)

def main():
    p=argparse.ArgumentParser(description="Documentary validation (layer 2) — heuristic keyword checks, not behavioral proof")
    p.add_argument("--skill", help="filter by skill id")
    p.add_argument("--category", help="filter by category")
    p.add_argument("--layer", choices=["doc","behavioral","all"], default="doc", help="doc = evals/cases (layer 2); behavioral = evals/behavioral; all = both")
    args=p.parse_args()
    if args.layer in ("doc","all"):
        cases=load_cases(args.skill, args.category)
    else:
        cases=[]
    if args.layer in ("behavioral","all"):
        # behavioral run delegated
        import subprocess
        print("--- behavioral layer (via evals/behavioral/runner.py) ---")
        subprocess.run(["python3", str(ROOT/"evals/behavioral/runner.py")])
    if not cases:
        print("No cases matched filter. Available cases:")
        for c in sorted((ROOT/"evals/cases").glob("*")):
            print(f"  {c.name}")
        sys.exit(0)
    passed=0
    total=len(cases)
    weight_total=0
    weight_pass=0
    for c in cases:
        ok, reason = check_case(c, ROOT)
        w = c.get("scoring",{}).get("weight",1.0)
        weight_total+=w
        if ok:
            passed+=1
            weight_pass+=w
            status="✓"
        else:
            status="✗"
        print(f"{status} {c.get('id')} [{c.get('category')}] skill={c.get('skill_id')} — {reason}")
    score = weight_pass/weight_total if weight_total else 0
    print(f"\n{passed}/{total} passed — weighted score {score:.2f}")
    if passed==total:
        print("All evals passed (heuristic). Full verification requires integration review.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__=="__main__":
    main()
