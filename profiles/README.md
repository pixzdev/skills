# Runtime Overlays — Isolation Contract

> A **runtime overlay** is a runtime-specific **operating overlay** (class: PROFILE — a POLICY restricted to one runtime). It is **not a SKILL**, and it is **not** the primary workflow (`AGENTS.md` is).

## Why an overlay is not a skill

A standalone skill requires (see `docs/taxonomy.md`): distinct objective, reusable **universal** methodology, meaningful invocation triggers, inputs/outputs, failure conditions, and independent value **across runtimes**. An overlay has none of that portability: it exists because **one specific runtime** may offer unusually generous context, subagent, tool, and compute availability, and needs operating parameters (mode selection, compute policy) that must **not** leak into universal skill design.

Therefore: overlays live outside the skill graph. They are not in `registry.json`, have no `pixz.*` skill ID, are not resolved by `scripts/resolve.py`, and are not installed with skills. They ship in the repository and are referenced by the README prompts.

## 2.0.0 location change

v1.1.0 kept the overlay at `profiles/super-z/PROFILE.md`. 2.0.0 promotes it to **top-level `ZAI.md`** — the benchmark showed discovery is a first-order problem, and a top-level, named overlay is far more discoverable (and matches the mission's Level 2.5 concept). `profiles/super-z/PROFILE.md` was **deleted** (consolidated); `scripts/validate.py` enforces the migration.

## Isolation contract (applies to every overlay)

1. An overlay **does not change** universal semantics: `AGENTS.md` operating rules, `SKILL.md` methodology, `registry.json`, the dependency model, resolver behavior, verification triggers, the evaluation layers, and honest-reporting rules are untouched by any overlay.
2. An overlay **only** parameterizes the operating-mode default/selection ritual and the runtime's compute/interaction policy.
3. On conflict, `AGENTS.md` and the repository policies (change-safety tiers, verification, honest reporting) **win** over the overlay.
4. An overlay must disclose its epistemic status: what is **SPECIFIED** and what is **UNVERIFIED** behaviorally. It must not claim behavioral effectiveness it has not demonstrated.
5. An overlay must degrade gracefully: if its required runtime capability (e.g., `AskUserQuestion`) is unavailable, it states that and falls back to a defined default — it never blocks the task.
6. More compute is **not** automatically better reasoning: overlays may exploit generous compute only where expected value is positive.

## Overlays

| Overlay | Applies to | File | Status |
|---------|-----------|------|--------|
| Super Z / GLM / Z.AI Web | agents self-identifying as Super Z, GLM, or Z.AI Web (web) | `ZAI.md` (repository root) | SPECIFIED (2026-09-22); behavioral effect UNVERIFIED |

## Machine check

`scripts/validate.py` verifies (layer 1, structural):

- `ZAI.md` exists and contains the four modes (`fast`, `balanced`, `deep`, `autonomous`), the `AskUserQuestion` requirement, the isolation statement ("does not change"), and the UNVERIFIED disclosure;
- `profiles/super-z/PROFILE.md` is **gone** (superseded);
- `README.md` contains the copy-paste **AI Agent Installation Prompt** and the **Super Z / GLM / Z.AI Web Install & Activation Prompt** sections.

## Adding an overlay

1. Create a top-level `<RUNTIME>.md` following the isolation contract (identify → required interaction → mode/parameter semantics → compute policy → never-list → degradation → epistemic status).
2. Add the required-content check in `scripts/validate.py` (keep it mechanical — section presence, not semantics).
3. Reference it from `README.md`, `AGENTS.md`, and `llms.txt`.
4. Do **not** add the runtime to any skill's `compatible_runtimes` unless installation/discovery for that runtime is actually verified — an overlay is not an installation claim.
