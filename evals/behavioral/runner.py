#!/usr/bin/env python3
"""Behavioral smoke — routing/activation/mode simulation (heuristic). Not a model grader.

2.0.0: scenarios now carry `expected_mode` (operating mode the assessment should select)
and the runner checks mode-consistency invariants plus registry safety invariants:
  - evidence floor: orchestrator aggregate closure always contains pixz.core.verification
  - trivial-task budget: orchestrator mandatory closure (aggregates + transitive requires)
    is small (<= 4 nodes = the evidence-floor chain) so trivial tasks stay cheap
    (GLM benchmark obligation). v1.1.0 was 10; v2.0.0 is 4.

Each result contains PASS/FAIL with evidence and limitations. Layer-3 status: PARTIALLY
VERIFIED (heuristic smoke; no model grader) — see docs/evaluation.md.
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
REG = json.loads((ROOT / "registry.json").read_text())
SKILLS = {s["id"]: s for s in REG["skills"]}
VALID_MODES = {"fast", "balanced", "deep", "autonomous"}


def route(task_desc: str, context: str = ""):
    """Heuristic keyword router (trigger substring overlap) over the task as the agent
    would see it (scenario + working context). Not the production router — the production
    router is the model itself, guided by AGENTS.md."""
    desc = (task_desc + " " + context).lower()
    return [sid for sid, meta in SKILLS.items() if any(t.lower() in desc for t in meta.get("triggers", []))]


def closure(sid):
    """Mandatory install-time closure (aggregates + transitive requires)."""
    seen, stack = set(), [sid]
    while stack:
        cur = stack.pop()
        if cur in seen or cur not in SKILLS:
            continue
        seen.add(cur)
        stack.extend(SKILLS[cur].get("aggregates", []) + SKILLS[cur].get("requires", []))
    return seen


def main():
    scenarios = sorted((ROOT / "evals" / "behavioral").glob("eval.behavioral.*.json"))
    passed = 0
    failures = []

    # Global registry invariants (checked once, reported per run)
    orch = SKILLS["pixz.core.orchestrator"]
    orch_closure = closure("pixz.core.orchestrator")
    inv_floor = "pixz.core.verification" in orch_closure
    inv_budget = len(orch_closure) <= 4
    print("Registry invariants:")
    print(f"  [{'PASS' if inv_floor else 'FAIL'}] evidence floor: orchestrator mandatory closure contains pixz.core.verification (closure={sorted(orch_closure)})")
    print(f"  [{'PASS' if inv_budget else 'FAIL'}] trivial-task budget: orchestrator mandatory closure = {len(orch_closure)} nodes (<= 4, was 10 in v1.1.0) — everything else activates on demand")
    print()
    if not (inv_floor and inv_budget):
        sys.exit(1)

    for p in scenarios:
        sc = json.loads(p.read_text())
        risk = sc.get("risk", "")
        mode = sc.get("expected_mode", "")
        actual = route(sc["scenario"], sc.get("context", ""))
        should_not = [s for s in sc.get("should_not_select", [])]
        should_select = [s for s in sc.get("should_select", []) if not s.startswith("none")]
        reasons = []
        ok = True

        # 1. mode is valid
        if mode not in VALID_MODES:
            ok = False
            reasons.append(f"invalid expected_mode: {mode!r}")
        # 2. mode-consistency invariants (no ceremony on trivial, no fast on high risk)
        if risk == "low" and mode not in {"fast", "balanced"}:
            ok = False
            reasons.append(f"ceremony check: risk=low but expected_mode={mode} (must be fast|balanced)")
        if risk in {"high", "critical"} and mode == "fast":
            ok = False
            reasons.append(f"safety check: risk={risk} but expected_mode=fast")
        # 3. false-positive activations
        for bad in should_not:
            if bad in actual:
                ok = False
                reasons.append(f"false positive / over-activation: {bad}")
        # 4. expected activations present (heuristic)
        for good in should_select:
            if good not in actual:
                ok = False
                reasons.append(f"missed activation: {good} not selected by trigger match")
        # 5. trivial guard (belt & braces)
        if "trivial" in sc["scenario"] and "pixz.core.orchestrator" in actual:
            ok = False
            reasons.append("over-routing: orchestrator selected for trivial")

        if not reasons:
            reasons.append("PASS — invariants hold")
        status = "✓" if ok else "✗"
        print(f"{status} {sc['id']} — {sc['scenario'][:80]}")
        print(f"    risk={risk} expected_mode={mode} expected_challenge={sc.get('expected_challenge')}")
        print(f"    heuristic selection: {actual or '(none)'}")
        print(f"    -> {'; '.join(reasons)}")
        print(f"    verifies: {sc.get('verifies', sc.get('expected_routing', ''))}")
        print()
        if ok:
            passed += 1
        else:
            failures.append(sc["id"])

    print(f"{passed}/{len(scenarios)} behavioral smokes passed (heuristic).")
    if failures:
        print(f"FAILED: {failures}")
    print("limitations: heuristic keyword overlap + registry invariants; not model-graded; see docs/evaluation.md")
    sys.exit(0 if passed == len(scenarios) else 1)


if __name__ == "__main__":
    main()
