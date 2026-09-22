# Contributing — PixzFlow

## Principle

> Smallest coherent capability system. No skill explosion, no vendor lock-in, no filler.

## Adding or Changing a Skill

Every concept must be classified as one of: `SKILL | PROTOCOL | POLICY | DEPENDENCY | AGENT | TOOL | EVAL | REGISTRY`

A standalone skill MUST have all seven:

1. Distinct objective
2. Reusable methodology (not “you are an expert in X”)
3. Independent invocation (value alone)
4. Clear triggers
5. Meaningful inputs/outputs
6. Meaningful failure conditions
7. Verification method

Otherwise merge it into a higher-level skill or protocol. See `docs/taxonomy.md`.

## Folder Contract

```
<domain>/<name>/
  SKILL.md        # required — YAML frontmatter (name, description) + full methodology contract
  metadata.yaml   # required — validated against schemas/skill.schema.json
  references/     # optional — deep docs loaded on demand (progressive disclosure)
  scripts/        # optional — helpers the skill may invoke
  assets/         # optional — templates, examples
```

- `id` is stable `pixz.<domain>.<name>` — never use filename as identity.
- `version` SemVer; breaking contract changes require major bump.
- `compatible_runtimes` explicit — test your adapter path.

## What a SKILL.md Must Contain

Purpose · Triggers · When to use / when NOT · Inputs · Required context · Methodology (operational steps) · Dependencies · Tools · Constraints/Failure conditions · Verification · Examples · Structured output schema

Methodology must be executable — steps an agent can follow, not a persona.

## Dependencies

Declare `requires` / `aggregates` / `optional` / `conflicts` in `metadata.yaml`.

- `requires` hard — resolver fails if missing.
- `aggregates` only on orchestrator-grade skills.
- Resolver (`scripts/resolve.py`) checks cycles, runtime incompatibility, version conflicts — test with it before PR.

## Validation Checklist (CI must run these)

```bash
python scripts/validate.py        # schema + registry + metadata consistency
python scripts/check-cycles.py    # no circular deps
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
python evals/runner.py            # eval harness (if touching evals)
```

All four must pass. Tag releases `v*.*.*` only after quality-gate.

## Style / Quality

- No generic SaaS glassmorphism, template cards, fake complexity (enforced by `pixz.quality.anti-ai-slop`).
- No boilerplate comments, fake evidence, citation dumping.
- Document compatibility differences in `adapters/README.md` when touching runtime behavior.
- Respect complexity-aware orchestration — don't add orchestration that exceeds task value.

## PR Process

1. Open issue describing capability gap + taxonomy class
2. Implement skill + metadata + eval case
3. Run `scripts/validate.py` + `scripts/check-cycles.py`
4. Add entry to hierarchical `*/AGENTS.md` only if it aids navigation (no duplicate truth)
5. Update `registry.json` (machine truth) and keep the `llms.txt` projection in sync — never create a third copy of the capability list
6. Request review — taxonomy + anti-slop + verification bar

## Versioning

- Update `VERSION` + per-skill `version` in same commit.
- Channels `latest/stable/pinned` — see `docs/versioning.md`.
- Deprecation: `status: deprecated` + `deprecated_reason` + `replaces`, keep one major.

## Questions

Read `docs/architecture.md`, `docs/taxonomy.md`, `docs/dependency-model.md` first.
