# Versioning — PixzFlow

## 2.0.0 Migration Notes (breaking)

| 1.1.0 | 2.0.0 | Migration |
|-------|-------|-----------|
| `schemas/workflow.schema.json` (11-phase enum) | `schemas/task-state.schema.json` (+ `schemas/handoff.schema.json`) | Field mapping: `phase` → retired (use `status` + `plan.steps`); `completed_work`/`pending_work` → `plan.steps[].status`; `arguments[]` → `findings[]` (typed, with transitions); `evidence: [string]` → `evidence[]` (typed entries + `verified_against`); `assumptions[]` → `findings[]` with `type: assumption`; new: `capabilities[]`, `failures[]`, `delegations[]`, `next_action`, `checkpoint`, `assessment`, `mode`. |
| `profiles/super-z/PROFILE.md` | top-level `ZAI.md` | Read `ZAI.md`; content consolidated, isolation contract in `profiles/README.md`. |
| orchestrator aggregates 8 (10-node install) | aggregates 1 = `pixz.core.verification` (4-node closure) | Re-run `scripts/resolve.py`; activate other capabilities at runtime per the capability-activation protocol. |
| "PIXZ Skills" identity | "PixzFlow" operating layer | Docs/identity rename only — skill IDs unchanged. |

Skill IDs are **stable** across this migration (no renames). Skill versions bumped to 2.0.0 only where contract/methodology changed (13 core + anti-ai-slop); unchanged domain skills remain 1.1.0.

## Model

- **Repository version:** `VERSION` (SemVer, VERIFIED)
- **Skill version:** `metadata.yaml:version` (SemVer, per-skill, VERIFIED)
- **Channel:**
  - `latest` → HEAD of `main` (VERIFIED)
  - `stable` → latest tag `v*.*.*` that passed `quality-gate` (VERIFIED — resolver `--channel stable` works)
  - `pinned` → exact version / SHA in consumer lockfile — **DOCUMENTED ONLY / FUTURE**: resolver accepts `--channel pinned` but does not yet read/write `pixz.lock`. Do not claim pinned is fully implemented. Creating/reading a lockfile is in `docs/self-audit.md#remaining-todos`. See audit finding #25.

## IDs

Stable: `pixz.<domain>.<name>` — never use filename as identity. `replaces` field handles renames.

## Consumer

```bash
# stable (recommended)
git clone --branch v1.0.0 https://github.com/pixzdev/skills.git
# with resolver
python scripts/resolve.py --install pixz.core.orchestrator --channel stable --runtime claude
# future pinned (not yet)
# python scripts/resolve.py --install pixz.core.orchestrator --channel pinned --lock pixz.lock
```

## Breaking Changes

Major bump for: ID rename, schema break, removed trigger, new hard `requires`, changed I/O contract. Deprecation path: `status: deprecated` + `deprecated_reason` + `replaces` for one major.

## Release Checklist

1. `schemas/*` validates
2. `scripts/validate.py` + `scripts/check-cycles.py` pass
3. `evals/runner.py` structural/documentary pass + behavioral subset pass
4. `quality-gate` + `anti-ai-slop` pass
5. Tag `vX.Y.Z`, update `VERSION`, push to origin/main
