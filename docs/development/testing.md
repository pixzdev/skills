# Testing — 4 Layers

See `docs/evaluation.md` for layer definitions.

**Layer 1 — structural:** `python scripts/validate.py` + `python scripts/check-cycles.py` (must PASS).

**Layer 2 — documentary:** `python evals/runner.py --layer doc` (heuristic, 15/15).

**Layer 3 — behavioral:** `python evals/behavioral/runner.py` (routing + orchestrator smoke). Each scenario: expected vs actual + evidence + limitations.

**Layer 4 — integration:** `bash scripts/integration-smoke.sh` where feasible (`npx skills list`, `openclaw skills list/check`, `ls <installed>/SKILL.md`). Manual smoke where no CI binary (Hermes/Codex) — still capture `ls`/`list` output.

No numeric ecosystem score. Report per layer.

**Add a case:** create `evals/cases/eval.<skill>.<id>.json` with `expect.must_contain` / `verifies` and `scoring.weight`.

**Before PR:** all layers 1-2 must pass; 3-4 smoke should pass for touched runtime.
