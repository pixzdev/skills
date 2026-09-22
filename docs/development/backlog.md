# Improvement Backlog — PixzFlow (post-2.1.0)

> Ideas recorded 2026-09-22 during the self-learning upgrade session. Each passed an initial
> anti-overengineering reading (failure prevented / behavior enabled / cost), but none is committed
> work. Re-assess through the full gate before implementing. Evidence classes per repo convention.

## P1 — cheap, prevents real failures

| # | Idea | Evidence it's a real gap | Failure prevented |
|---|------|--------------------------|-------------------|
| B1 | GitHub Actions CI running the 4+1 gate (`validate.py`, `check-cycles.py`, `evals/runner.py`, `evals/behavioral/runner.py`, `evals/lifecycle/run_tests.py`, `integration-smoke.sh`) | OBSERVED: no `.github/workflows` exists while CONTRIBUTING.md says "CI must run these" | silent registry/eval drift; contract rot between PRs |
| B2 | Fix no-op `should_not_select` entries — bare names (`"orchestrator"`, `"security.review"`, `"epistemic-challenger"`) never match full skill IDs in `evals/behavioral/runner.py` (exact list membership) | OBSERVED in runner code + scenario files; the guard silently does nothing for those entries | false sense of over-activation protection (verification-depth violation in our own evals) |
| B3 | `validate.py`: cross-check `requires`/`aggregates`/`optional`/`conflicts` between registry.json and each metadata.yaml (currently only ID *format* is checked) | OBSERVED; same drift class as v1 audit finding #8 (optional documented but not implemented) | dependency truth diverging between registry and skill metadata |

## P2 — moderate, activates claimed behavior

| # | Idea | Evidence it's a real gap | Behavior enabled |
|---|------|--------------------------|------------------|
| B4 | Minimal stdlib JSON-Schema subset validator (~type/required/enum/const/pattern/minItems) wired into `validate.py` for adaptation-state instances, eval cases, and any task-state fixtures | OBSERVED: our own schemas are never actually validated against instances; activation.py checks 4 keys only | SCHEMA-COMPLIANT rung becomes real for PixzFlow's own artifacts, zero new dependencies |
| B5 | `scripts/activation.py lesson|improvement add/list` subcommands with status-ladder enforcement (proposed→challenged→implemented→verified; regressed/rejected terminal-with-reason) + lifecycle tests | OBSERVED: learning ledger currently writable only by hand-editing JSON | machine-writable, testable learning ledger; less schema-violating hand edits |
| B6 | `schemas/handoff.schema.json`: optional `adaptation` field in the dispatch contract | OBSERVED: AGENTS.md claims "subagents receive adaptation status in the handoff packet" but the schema has no such field | the claim becomes schema-grounded; subagents can honor READY without probing |

## P3 — deferred (testing phase or larger scope)

| # | Idea | Note |
|---|------|------|
| B7 | `pixz.lock` pinned channel (resolver reads/writes a lockfile) | standing TODO in docs/self-audit.md #25 |
| B8 | Layer-2 documentary coverage to ≥1 case per skill (18/29 today) | standing TODO in docs/self-audit.md |
| B9 | Successor-benchmark runner scaffolding for cells I/J/K (self-learning ablation A=native, B=2.1 w/o self-learning, C=with, D=no persistence) | belongs to the testing phase; design already in docs/benchmark/successor-benchmark.md |
| B10 | Real-runtime session-boundary trial (install → kill session → resume with zero user prompts) on Claude Code + OpenClaw | first candidate when testing starts; upgrades lifecycle claims from state-machine-VERIFIED to behaviorally OBSERVED |

## Explicitly NOT queued (gate rejected for now)

- Windows PowerShell versions of the bash gates (cost > current audience evidence).
- Skills.sh marketplace metadata beyond the existing CLI flow (no measured demand).
- Any new skill/agent/schema beyond B6 — proliferation budget is spent until P1–P2 evidence says otherwise.
