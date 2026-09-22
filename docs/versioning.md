# Versioning — PixzFlow

## 2.3.0 Notes (non-breaking, additive)

| Change | Detail |
|---|------|
| Main skill | `pixz.core.orchestrator` 2.0.0 → **2.1.0** is documented as the **MAIN practical operating skill**. Specialist skills answer HOW; the orchestrator answers WHEN/WHY/WHICH/HOW DEEPLY. |
| Progressive disclosure | Full practical operating loop lives in `core/orchestrator/references/operating-methodology.md` (loaded only for complex/high-risk work). SKILL.md body stays invocation-sized. |
| Domain skills | All 15 domain skills 1.1.0 → **1.2.0** — stubs expanded to executable methodology (when/not, steps, examples, verification, failure conditions, structured output). |
| Core skills | Remaining core skills + `anti-ai-slop` bumped (2.0.0 → 2.1.0; verification 2.1.0 → 2.2.0; self-learning 2.1.0 → 2.2.0) with a main-skill pointer and practical additions. |
| Routing copy | Every SKILL.md tells the agent: if you want more practical multi-step methodology, use `pixz.core.orchestrator`. |
| Evals | Documentary cases 18 → 19 (`eval.orchestrator.main-skill-01`). Mandatory orchestrator closure unchanged (4 nodes; budget invariant holds). |

No IDs renamed, no triggers removed, no hard `requires` added — minor bump.

## 2.2.0 Notes (non-breaking, additive)

| Change | Detail |
|---|------|
| New script | `scripts/doctor.py` — measured runtime baseline (state persistence, command execution, tools, contract reachability); `--write` fills only `unknown` dimensions; the unmeasurable (delegation, research) stays unknown |
| New script | `scripts/assess.py` — adoption score 0–100 as a sum of named evidence-backed checks (A installation 30 · B activation 35 · C operability 25 · D learning 10); UNVERIFIED items score 0; `--full` executes layer-1 + lifecycle as deeper evidence. Doctrine printed with every report: adoption score ≠ quality metric |
| Auto-run | `activation.py mark-adapted` now runs the assessment automatically at first-run completion and records it in history (never blocks the READY transition) |
| New command | `activation.py verify-installed --runtime <rt>` — installed copies vs source digests; MODIFIED → exit 10 (tamper/corruption detection) |
| New script | `scripts/sitrep.py` — one-block orientation report (adaptation probe + task state + learning highlights) for ORIENT/compaction/handoff |
| New script | `scripts/hooks.py` — runtime contract wiring: `check`/`install`, append-only and idempotent; Claude `CLAUDE.md → @AGENTS.md`, native AGENTS.md runtimes are documented no-ops; repo self-wires its own `CLAUDE.md` |
| Contracts | AGENTS.md self-learning section carries doctor/assess/sitrep/integrity/wiring; ZAI.md explicit that the overlay never overrides the lifecycle or the assessment; install prompts (README + docs/prompts) require the auto-assessment score + integrity result in the final report |
| Evals | lifecycle suite 9 → 14 deterministic tests (doctor, integrity, sitrep, assessment incl. fresh-env-low-score + auto-run, hooks idempotency) |

No skill contracts changed; no schema changes; no triggers changed — minor bump.

## 2.1.0 Notes (non-breaking, additive)

| Change | Detail |
|---|---|
| New skill | `pixz.core.self-learning` v2.1.0 (post-install activation, adaptation baseline, drift handling, improvement loop) |
| New schema | `schemas/adaptation-state.schema.json` (runtime-level self-learning state); `task-state.schema.json` gains optional `adaptation` pointer |
| New script | `scripts/activation.py` (probe/init/mark-adapted/sync/mark-installed; exit codes 0/10/1) |
| New evals | 3 documentary cases (18 total) · 10 behavioral E-series scenarios (33 total) · 9 deterministic lifecycle tests (`evals/lifecycle/`) |
| Changed skill | `pixz.core.verification` 2.0.0 → 2.1.0 (verification-depth ladder added) |
| New protocols | `pixz.protocol.self-learning` · `pixz.protocol.verification-depth` (both point at owning SKILL.md — no new truth files) |
| Policy extension | `pixz.policy.simplicity` absorbs the improvement-economy (anti-proliferation) gate |
| Orchestrator | `optional` gains `pixz.core.self-learning` — mandatory closure unchanged (4 nodes; budget invariant holds) |

No IDs renamed, no triggers removed, no hard `requires` added to existing skills — minor bump per the breaking-change rules below.

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
