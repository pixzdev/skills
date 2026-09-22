# Runtime Profiles — Isolation Contract

> A **profile** is a runtime-specific **operating overlay** (class: PROFILE — a POLICY restricted to one runtime). It is **not a SKILL**.

## Why a profile is not a skill

A standalone skill requires (see `docs/taxonomy.md`): distinct objective, reusable **universal** methodology, meaningful invocation triggers, inputs/outputs, failure conditions, and independent value **across runtimes**.

A profile has none of that portability: it exists because **one specific runtime** (e.g., Super Z / GLM / Z.AI Web) may offer unusually generous context, subagent, tool, and compute availability, and needs operating parameters (mode selection, compute policy) that must **not** leak into universal skill design.

Therefore: profiles live outside the skill graph. They are not in `registry.json`, have no `pixz.*` skill ID, are not resolved by `scripts/resolve.py`, and are not installed with skills. They ship in the repository and are referenced by the README prompts.

## Isolation contract (applies to every profile)

1. A profile **does not change** universal skill semantics: `SKILL.md` methodology, `registry.json`, the dependency model, resolver behavior, and the 4 verification layers are untouched by any profile.
2. A profile **only** parameterizes the orchestrator's operating depth (MINIMAL → DEEP VERIFICATION) and the runtime's compute/interaction policy.
3. On conflict, the skill's `SKILL.md` and the repository policies (change-safety tiers, verification layers, honest reporting) **win** over the profile.
4. A profile must disclose its epistemic status: what is **SPECIFIED** by its specification and what is **UNVERIFIED** behaviorally. It must not claim behavioral effectiveness it has not demonstrated.
5. A profile must degrade gracefully: if its required runtime capability (e.g., `AskUserQuestion`) is unavailable, it states that and falls back to a defined default — it never blocks the task.

## Profiles

| Profile | Applies to | File | Status |
|---------|-----------|------|--------|
| Super Z / GLM / Z.AI Web | agents self-identifying as Super Z, GLM, or Z.AI Web (web) | `profiles/super-z/PROFILE.md` | SPECIFIED (2026-09-22); behavioral effect UNVERIFIED |

## Machine check

`scripts/validate.py` verifies (layer 1, structural):

- `profiles/README.md` and `profiles/super-z/PROFILE.md` exist;
- the Super Z profile contains the four modes (`FAST`, `BALANCED`, `DEEP`, `AUTONOMOUS`), the `AskUserQuestion` requirement, the isolation statement, and the UNVERIFIED disclosure;
- `README.md` contains the copy-paste **AI Agent Installation Prompt** and the **Super Z / GLM / Z.AI Web Prompt** sections.

## Adding a profile

1. Create `profiles/<runtime>/PROFILE.md` following the isolation contract above (identify → required interaction → mode/parameter semantics → compute policy → never-list → degradation → epistemic status).
2. Add the required-content check in `scripts/validate.py` (keep it mechanical — section presence, not semantics).
3. Reference it from `README.md`, `AGENTS.md`, and `llms.txt`.
4. Do **not** add the runtime to any skill's `compatible_runtimes` unless installation/discovery for that runtime is actually verified — a profile is not an installation claim.
