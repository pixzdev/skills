# Routing → Adaptive Capability Activation (2.0)

> v1.1.0 "routing" = task → skill set. v2.0 **activation** = assessment → mode → *which* capabilities, *how deeply*, *under what verification*, *for how long*. `scripts/resolve.py` still resolves **install-time** dependencies only — do not conflate.

## Model

```
TASK
  → ORIENT (state? environment?)
  → ASSESS (complexity · risk · uncertainty · reversibility · horizon — bands)
  → MODE (fast | balanced | deep | autonomous)
  → ACTIVATE (registry metadata → match → progressive load → record activation)
  → ACT / OBSERVE / VERIFY (continuous)
  → REINVOKE (reactivation conditions) or COMPLETE
  → DECIDE (done | continue | replan | delegate | research | challenge | escalate | stop)
```

Every activation and every rejection is recorded (reason required) — activation precision/recall are measurable in the successor benchmark.

## Activation Policy by Band

| Band (any dimension high/critical) | Typical activations |
|-----------------------------------|--------------------|
| all low (trivial) | none — direct ACT→VERIFY. Orchestrator not invoked. |
| medium | 1–3 relevant capabilities + verification floor if orchestrated; environment-awareness when env-dependent; context-engineering when requirements are unclear |
| high | domain skill(s) + verification + epistemic-reasoning; challenger on consequential claims; change-safety classification mandatory |
| critical / irreversible | all of high + independent verification passes + source-of-record checks + pre-action checkpoints; confirmation before irreversible actions (static policy) |

## Failure Modes & Mitigations

| Mode | Example | Mitigation |
|------|---------|------------|
| **Under-activation** | security task without verification | evidence floor: orchestrator aggregate = verification (machine-checked invariant); change-safety static |
| **Over-activation** | rename triggers 5 skills | budget rule; trivial-task mode fast; rejected-with-reason ledger |
| **Dropped activation** | security review forgotten after moving to implementation | `capabilities[]` state + `reactivation_conditions`; resume protocol re-establishes |
| **Recursive activation** | orchestrator → skill → orchestrator | depth caps + cycle DFS + no sub-subagents |
| **Irrelevant activation** | UI task activates k8s | trigger/task-fit match + runtime compat + sufficiency |
| **Missed safety** | prod change skips safety tiers | static policy, not routed |
| **Skill spam** | deep mode loads all 12 optional skills | every activation needs a reason; deep = "more relevant skills *when justified*", not "all" |
| **Blind trust** | subagent return accepted unread | mandatory return fields + inspection verdict (accepted/returned/escalated) |

## Router Invariants (machine-checked, `evals/behavioral/runner.py`)

1. Evidence floor: orchestrator mandatory closure contains `pixz.core.verification`.
2. Trivial-task budget: orchestrator mandatory closure ≤ 4 nodes (v1.1.0: 10).
3. No cycles (separate `check-cycles.py`).
4. Mode consistency: risk=low never selects deep/autonomous; risk=high/critical never selects fast.
5. No false-positive activations per scenario (`should_not_select`).

The heuristic keyword router in the smoke runner is **documented as smoke** — the production router is the model itself, guided by `AGENTS.md`. Model-graded activation precision/recall belongs to the successor benchmark.

## How to run

```bash
python evals/behavioral/runner.py            # invariants + 23 scenario smokes
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude     # 4 nodes
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional  # +12
python scripts/validate.py
```
