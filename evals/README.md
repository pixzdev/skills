# Evals — PIXZ Skills

> A skill repository should not merely contain prompts. It should contain a way to evaluate skill behavior.

## Harness

- **Runner:** `evals/runner.py` — iterates `evals/cases/*.yaml` validated by `schemas/eval.schema.json`
- **Cases:** one YAML per expectation; categories: `trigger | method | output | failure | verification | scope | hallucination | consistency`
- **Scoring:** `should_trigger`, `must_contain`, `must_not_contain`, `verifies`, `artifacts` with `weight`/`threshold`

## Run

```bash
python evals/runner.py                  # all cases
python evals/runner.py --skill pixz.core.orchestrator
python evals/runner.py --category trigger
```

## Case Anatomy

```yaml
id: eval.orchestrator.trigger-01
skill_id: pixz.core.orchestrator
description: Orchestrator triggers on multi-step production request
category: trigger
input:
  prompt: "Orchestrate a rate-limited public API for our Next.js monorepo"
  runtime: claude
expect:
  should_trigger: true
  must_contain: ["DISCOVER","PLAN","verification"]
  verifies: ["routing does not place HOW in orchestrator"]
scoring: {weight: 1.0, threshold: 0.7}
```

## Coverage Goal

- Every core skill has >= 1 trigger + 1 method + 1 verification case
- Niche skills have trigger + method cases
- Hallucination/scope cases for `environment-awareness`, `anti-ai-slop`, `change-safety`

Runner does lightweight heuristic checks (keyword/convention presence); it is evidence, not proof — real verification needs human review and integration evals.
