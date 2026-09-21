# Evals — 4 Layers

> Structural PASS must never be presented as behavioral proof (audit #11).

## Layers

| Layer | What it tests | Harness | Result |
|-------|---------------|---------|--------|
| **1 Structural** | frontmatter, files, IDs, registry consistency, dependency graph, no cycles, schemas | `scripts/validate.py` + `scripts/check-cycles.py` | PASS/FAIL per check, no score |
| **2 Documentary** | required sections, install commands, examples, metadata completeness (keyword/section presence) | `evals/runner.py` on `evals/cases/*.json` (15 cases) | heuristic `X/Y passed` |
| **3 Behavioral** | task success, correctness, verification, constraints, tool choice, skill selection, stopping, uncertainty, challenge, regression | `evals/behavioral/runner.py` on `evals/behavioral/*.json` (4 scenarios) | PASS/FAIL per scenario + evidence + limitations |
| **4 Integration** | repo → installer → runtime → discovery → invocation → execution | `scripts/integration-smoke.sh` (skills.sh + openclaw + manual `ls`) | PASS/FAIL per runtime + evidence |

Never present layer 1–2 as layer 3–4. See `docs/evaluation.md`.

## Run

```bash
python scripts/validate.py                  # layer 1
python scripts/check-cycles.py              # layer 1
python evals/runner.py                      # layer 2 (all doc cases)
python evals/runner.py --skill pixz.core.orchestrator  # filtered
python evals/behavioral/runner.py           # layer 3 (routing smoke)
bash scripts/integration-smoke.sh           # layer 4 (where runtime available, else manual)
```

## Case Anatomy (layer 2)

```json
{
  "id": "eval.orchestrator.trigger-01",
  "skill_id": "pixz.core.orchestrator",
  "description": "Orchestrator triggers on multi-step production request",
  "category": "trigger",
  "input": {"prompt": "Orchestrate a rate-limited public API for our Next.js monorepo", "runtime": "claude"},
  "expect": {"should_trigger": true, "must_contain": ["DISCOVER","PLAN","verification"], "verifies": ["routing does not place HOW in orchestrator"]},
  "scoring": {"weight": 1.0, "threshold": 0.7}
}
```

Layer 3 cases add `expected_routing`, `should_select`, `should_not_select`, `risk` — see `evals/behavioral/*.json`.

## Coverage

- Layer 2: 15 doc cases (core + niche)
- Layer 3: 4 behavioral smokes (orchestrator trivial/ UI / security / prod migration) — smoke, not model-graded
- Layer 4: smoke covers resolver + discovery `ls`/`list` per runtime

Add cases as `evals/cases/eval.<skill>.<id>.json` (layer 2) or `evals/behavioral/eval.behavioral.*.json` (layer 3).

Runner is heuristic for layers 2–3 — report includes `limitations: heuristic keyword overlap only`.
