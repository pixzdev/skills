# Evaluation — 4 Layers

> A passing structural check must never be presented as behavioral proof.

## Layers — Separation Required (audit fix #11/#12)

### Layer 1 — Structural validation (VERIFIED, automated)

What: machine-contract checks.

- frontmatter valid (`name`/`description` present, SKILL.md == SKILL.md)
- required files exist (`SKILL.md` + `metadata.yaml` per skill)
- IDs valid (`pixz.<domain>.<name>`, SemVer)
- registry consistency (`registry.json` ↔ `metadata.yaml`, no duplicate IDs/paths)
- dependency graph valid, topo-sorted
- no cycles (DFS)
- schemas valid (JSON Schema draft-07)
- limits enforced

How: `python scripts/validate.py` + `python scripts/check-cycles.py` + JSON Schema (manual). Exit non-zero on fail. Result: **PASS/FAIL + evidence list**, not a numeric score.

### Layer 2 — Documentary validation (VERIFIED, heuristic)

What: does the skill document what it should?

- required sections in SKILL.md (Purpose, Triggers, When to use/NOT, Inputs, Methodology, Verification, Example, Structured output)
- installation commands present where relevant
- examples present
- metadata complete (`triggers`, `compatible_runtimes`)

How: `python evals/runner.py` (layer=doc) does keyword/section presence checks on 15 cases (see `evals/cases/*.json`). Heuristic, not semantic. Score is `passed/total` + `weighted 1.00` but **no fake precision** — report is `15/15 heuristic`.

Limitations: keyword presence ≠ correctness. Layer 2 never implies behavioral success.

### Layer 3 — Behavioral evaluation (PARTIALLY VERIFIED, smoke)

What: actually execute skill methodology against controlled tasks; measure:

- task success / correctness
- verification behavior (did it produce evidence, not just claim?)
- adherence to constraints (scope control)
- appropriate tool usage (env-awareness prevented npm vs pnpm halluc)
- appropriate skill selection vs false positives/negatives
- stopping behavior (quality-gate diminishing returns)
- uncertainty handling (UNKNOWN labeling)
- challenge behavior (did challenger run at high risk?)
- regression detection

How: `evals/behavioral/` smoke runner (see below). Each result contains:

```yaml
test_id: eval.behavioral.orchestrator-trivial-rename
skill: pixz.core.orchestrator
category: behavioral
scenario: trivial file rename (should use minimal, not full orchestration)
expected: selects zero or one skill, no challenger, no full loop
actual: {selected: [], challenger: not_run, verification: minimal}
pass: true
evidence: resolver output, SKILL.md read, overhead measured
limitations: single scenario, heuristic router simulation
```

### Layer 4 — Integration evaluation (VERIFIED where possible, PARTIALLY elsewhere)

What: **repository → installer → runtime → discovery → invocation → execution**

- clean env `npx skills list` before/after
- `npx skills add pixzdev/skills --skill orchestrator` → `npx skills list` shows it
- `openclaw skills install ...` → `openclaw skills list`/`check`/`verify --card`
- manual `cp -r` → `ls <installed>/SKILL.md` + `head -20` frontmatter + `/skills` slash
- execute controlled task (e.g., `python scripts/resolve.py --install pixz.core.orchestrator`)

How: `scripts/integration-smoke.sh` (see `docs/install/README.md#integration`). Where CI cannot test runtime (no OpenClaw/Hermes binary), doc is **manual smoke** with required `ls`/`list`/`verify` evidence. Claim level per runtime: VERIFIED vs PARTIALLY VERIFIED (see `docs/install/README.md` matrix).

## Scoring

- No invented numeric quality score. Report per layer: structural PASS/FAIL, documentary heuristic score, behavioral PASS/FAIL per scenario with evidence, integration PASS/FAIL per runtime with evidence.
- Runner aggregates: `X/Y passed` per layer, not a single ecosystem score.

## Artifacts

- `evals/cases/*.json` — layer 2 docs validation (15)
- `evals/behavioral/` — layer 3 smoke definitions (routing, orchestrator decisions)
- `scripts/integration-smoke.sh` — layer 4 (where feasible)
- `docs/architecture/routing.md` — router test results (false pos/neg, under/over-routing)

## Limitations

- Behavioral is smoke, not model-graded; integrations for Hermes/Codex are manual-only (no CI binary). Document in each result's `limitations`.
