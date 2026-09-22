---
name: Project Adapt — Design DNA
description: Extract a typed, evidence-backed design DNA from an existing project (palette, typography, spacing, radii, shadows, motion, density) and enforce it for all new UI so additions match instead of clashing; drift detection against the DNA and a per-surface report. Use when designing inside an existing product or when new UI looks off against the rest.
version: 1.0.0
id: pixz.design.project-adapt
category: design
triggers: [design dna, match project style, design drift, project design system, consistent design]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Project Adapt (Design DNA) — `pixz.design.project-adapt`

> **Specialist HOW skill (design).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`.
>
> The project's own design language is the ground truth. New UI that doesn't match is a defect, not a preference.

## Purpose

Turn "make it look like the rest of the app" into an executable protocol: inventory → extract typed tokens with evidence → persist as `design-dna.json` → constrain generation to the DNA → detect and report drift.

## When to Use / When NOT

| Use | Use instead |
|-----|-------------|
| Designing/building new UI inside an existing product | Greenfield (no existing UI) → `pixz.frontend.ui-ux-pro` step 2+ |
| Auditing whether recent UI matches the established language | Full token/component spec authoring → `pixz.design.design-system` |
| Onboarding: "what are the design rules here?" | Interaction/usability critique → `pixz.design.uiux` |

## Methodology

1. **INVENTORY.** Collect the evidence set: CSS/SCSS files, Tailwind config + `globals.css`, theme/token files (CSS custom properties, design-tokens JSON, shadcn/ui CSS variables), component libraries in use, 3–5 rendered screenshots (`chrome-devtools`/`playwright` MCP). Record what exists before judging anything.
2. **EXTRACT — typed, with evidence.** For each dimension, record the value *and* where it came from:
   - `palette`: roles → hex + `evidence` (file:selector or screenshot region)
   - `typography`: families, size scale, line heights, weights + evidence
   - `spacing`: base unit + scale + evidence
   - `radii`, `shadows`: per component class + evidence
   - `motion`: duration/easing conventions found in CSS/JS + evidence
   - `density`: observed component gaps, table row heights
   - `iconography`: collection + stroke width + source package
   If a dimension is ambiguous (two scales coexist), record **both** and flag `conflict` — do not silently average.
3. **PERSIST — `design-dna.json`.** Write the DNA to the project (`.pixz/design-dna.json`):
   ```json
   { "schema": "pixz/design-dna/1", "project": "<name>", "extracted_at": "<date>",
     "palette": { "primary": {"value": "#...", "evidence": "src/index.css:var(--primary)"} },
     "typography": { ... }, "spacing": { ... }, "radii": { ... }, "shadows": { ... },
     "motion": { ... }, "density": { ... }, "iconography": { ... },
     "conflicts": [], "missing": [] }
   ```
   This file is the contract for everything generated afterwards. If the project's own token file already exists and is authoritative, point the DNA at it (`source: "tokens"`) instead of duplicating values.
4. **GENERATE (constrained).** Any new UI must use DNA values. The rule set: reuse a DNA slot when one covers the need → extend by deriving *within* the existing scale (new size = next scale step, new color = new shade of an existing hue) → **off-DNA values require explicit user approval and are recorded in the report as deviations with reasons.**
5. **DRIFT CHECK.** Compare new/changed UI against the DNA: off-palette colors, off-scale sizes, wrong radius, new font family, ad-hoc spacing values (e.g. `17px`, `13px` outside the scale). Each drift gets severity: `block` (breaks visual contract) / `warn` (minor inconsistency) / `info`.
6. **REPORT.** Per surface: what matches, what deviates, recommended fix (use DNA slot X). End with overall consistency status and the DNA file location.

## Outputs

- `.pixz/design-dna.json` (the typed contract, evidence-backed)
- Constraint decisions for the generated UI (DNA slot used per token)
- Drift report: per-surface findings with severity + fix
- Consistency verdict: `CONSISTENT` / `CONSISTENT WITH WARNINGS` / `DRIFT`

## Failure Conditions

- Generating new UI without first running inventory/extract on an existing product
- DNA values without evidence (no file/selector/screenshot source)
- Silently picking one of two conflicting scales instead of flagging the conflict
- Off-DNA values used without approval + recorded deviation
- Drift reported as "it's fine, close enough" (block-level drift is a failure)
- Duplicating the project's authoritative token file instead of pointing at it

## Verification

DNA `EXTRACTED` (every dimension has evidence) · generation `CONSTRAINED` (every token traceable to a DNA slot or an approved deviation) · drift `MEASURED` (specific files/values cited, not impressions).

## Main Skill

For orchestration of larger work, use `pixz.core.orchestrator`. For greenfield design intelligence, `pixz.frontend.ui-ux-pro`; for full design-system authoring, `pixz.design.design-system`.
