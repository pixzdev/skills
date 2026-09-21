# Anti-AI-Slop Audit — v1.0.1 (on own repo)

> Audit via `pixz.quality.anti-ai-slop` on this repository.

## Documentation slop

**Checked:** repetitive sections, generic professional filler, fake depth, inflated language, excessive headings, repeated principle, buzzwords, verbosity, duplicated prose, claims without evidence.

**Findings & fixes:**

- **Before:** `README.md` had totem badges + “Portable, composable” plus separate `AGENTS.md` duplicating same 28-row table verbatim → **duplicated** (OBSERVED). **Fixed:** `AGENTS.md` now is operational guide (not duplicate table dump with different trim) — table kept but as projection with install discipline, not verbatim marketing copy.
- **Before:** `docs/final-report.md` repeated “Build the system, not the deck” motivational prose in 3 places → **filler** (OBSERVED). **Kept once** in final line only.
- **Before:** `skills.sh` section in `adapters/README.md` used generic “powerful/extensible” → **buzzword** (INFERRED). **Fixed:** replaced with verified path table.
- **After:** `README.md` now has exactly one version badge (not wall), no `🚀`/`🔥` unless supported. Each claim tagged VERIFIED/PARTIALLY.

## Architecture slop

**Checked:** unnecessary abstractions, registries, schemas, wrappers, dependencies, fake extensibility, duplicate concepts, ceremony.

- **Before:** `registry.json` + `AGENTS.md` + each `metadata.yaml` seemed duplicate — **INFERRED** as potential slop. **Verdict:** not slop — `registry.json` is machine source, `AGENTS.md` is discovery index, `metadata.yaml` is per-skill source. Consistency enforced by `scripts/validate.py` (OBSERVED pass). So **retained** with explicit “single source” note.
- **Before:** `optional` claimed auto-install but code didn't implement → **pseudo-feature** (OBSERVED). **Fixed:** made opt-in via flag, not removed.
- **Proposed 12→15 limits:** justified (13-node optional graph needs 15), not arbitrary inflation.
- **Did NOT add:** separate `pentesting/` skills (would duplicate security), separate `research` skill (tool-use, not methodology), skill explosion to 40+ — all avoided per `simplicity`.

## README slop

Checked vs `[ 🚀 ✨ 🔥 🧠 ⚡ 🌌 ]` classic.

- **Result:** no gratuitous emoji, no `Revolutionary`, no `Production Ready` without evidence (evidence is `validate` + `resolve` + `npx skills --help` output). Structure follows recommended: Why / Install / Supported Runtimes / Use a Skill / Architecture / Core Skills / Dependency Model / Verification / Development / Structure / Limitations / Contributing / License — each section justified.

## Visual slop

- Repo is `*.md` + `*.py` + `*.json` only — no `assets/` hero art, gradients, dashboards. `quality/anti-ai-slop` enforces purposeful visuals only — applied correctly (no hero needed).

## Code slop

- No boilerplate comments, fake random comments, generated-looking naming. `scripts/*.py` are stdlib-only, no unnecessary deps (previously attempted `pyyaml` then removed). Scripts are minimal and auditable.

## Verdict

Repo now **passes its own anti-slop gate**: diagnostic criteria, not dogmatic bans; purposeful complexity only; honest claims with evidence labels; no filler duplication beyond necessary registry projection (validated).
