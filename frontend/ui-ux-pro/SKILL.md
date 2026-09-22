---
name: UI/UX Pro
description: UI/UX design intelligence for frontend builds — product-type-driven style direction, contrast-verified color systems, modular type scales, spacing/radius/shadow tokens, iconography rules, chart-type selection, and an a11y-first UX priority checklist. Project-adaptive: reuses the project's existing design language (Design DNA) before recommending anything new. Use when designing or building web UI.
version: 1.0.0
id: pixz.frontend.ui-ux-pro
category: frontend
triggers: [ui design, color palette, typography, landing page design, dashboard design, design tokens]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# UI/UX Pro — `pixz.frontend.ui-ux-pro`

> **Specialist HOW skill (frontend).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`.
>
> This skill is *project-adaptive and evidence-checked*: it designs inside the existing design language when one exists, and verifies contrast math instead of guessing hex codes.

## Purpose

Produce sound, implementation-ready design decisions for web UI: style direction, color system, typography, spacing, iconography, data-viz choice, and UX priorities — each as a decision with a reason, not decoration.

## When to Use / When NOT

| Use | Use instead |
|-----|-------------|
| Designing/building web UI, choosing palette/type/chart for a project | Interaction-quality critique, IA, usability review → `pixz.design.uiux` |
| Greenfield OR extending an existing design system | Token extraction from existing artifacts → `pixz.design.project-adapt` (run first if the project has UI) |
| Design decisions that need implementation (hand to builder) | Full design-system spec (tokens + components + docs) → `pixz.design.design-system` |

## Methodology

1. **PROJECT-ADAPT FIRST (do not skip when the project has UI).** Check for an existing design language: CSS variables/tokens, Tailwind theme, design tokens file, screenshots of shipped screens. If found → run `pixz.design.project-adapt` (Design DNA) and **recommend within that DNA** (extend, don't replace). New recommendations must cite which DNA slot they use. Only for greenfield projects do you invent from scratch.
2. **STYLE DIRECTION FROM PRODUCT TYPE** (greenfield). Match style to audience and job-to-be-done, never to taste:
   - B2B dashboard/SaaS → dense, neutral base, one accent, high data legibility
   - E-commerce → product-forward, minimal chrome, trust signals, fast CTAs
   - Fintech → conservative palette, strong hierarchy, precision typography
   - Developer tools → dark-leaning, monospace accents, information density
   - Marketing/landing → large type, generous whitespace, one primary action
   - Consumer entertainment → expressive motion, bold color, playful but legible
   - Health/education → calm palette, high readability, low anxiety
3. **COLOR SYSTEM WITH MATH (not vibes).**
   - Build roles: `bg` / `surface` / `text` / `text-secondary` / `primary` / `accent` / `success` / `warning` / `error` / `border`. A palette without roles is not a palette.
   - Contrast is a hard gate, not a preference: body text **≥ 4.5:1** against its background; large text (≥24px or 19px bold) and UI component boundaries **≥ 3:1**. Compute the ratio (relative luminance formula) for every text/background pair — if it fails, adjust the color and recompute. Never "it should be fine".
   - One dominant hue + neutrals; accent used ≤10% of surface. Dark themes: never pure `#000` bg / `#fff` text (halation) — use near-black/near-white pairs.
4. **TYPOGRAPHY.** Max **2 typefaces** (1 for display/heading + 1 for body, or one family with weights). Modular scale: pick ratio 1.2 (tight) – 1.333 (roomy); base 16px; cap ~6 sizes in normal use. Line height: 1.1–1.25 headings, 1.5–1.6 body. Measure body in px at 16–20 for UI; never below 14px for reading text.
5. **SPACING / RADIUS / SHADOW TOKENS.** 4pt base scale (4/8/12/16/24/32/48/64); consistent radius per component class (input ≠ card ≠ overlay is fine; random radii are not); shadows tied to elevation levels, not aesthetics (2–3 levels max).
6. **ICONOGRAPHY.** SVG only, one collection per project, consistent stroke width, `viewBox="0 0 24 24"`, size in `em`/rem for text alignment. Never emoji as UI icons. For an existing project, use the `better-icons` MCP `scan_project_icons` to find the installed collection before recommending anything.
7. **DATA-VIZ SELECTION** (when charts are needed): trend → line · comparison → bar (few categories) · composition → stacked bar or donut (≤5 slices, else table) · distribution → histogram · correlation → scatter · flow/funnel → funnel · relationships → tree/sankey · geography → map. One chart per question; if the answer is a number, show the number.
8. **UX PRIORITY CHECKLIST (in this order).** 1) Accessibility (contrast, focus order, labels, keyboard) 2) Feedback (every action gets a state: loading/success/error) 3) Responsive (breakpoints are design decisions, not accidents) 4) Performance (image formats, lazy loading, bundle) 5) Consistency with existing DNA.
9. **VERIFY.** Render and look: `chrome-devtools` MCP (screenshot + computed styles) or `playwright`. Check contrast in the real render, check focus visibility, check the page at mobile width. Anti-slop pass with `pixz.quality.anti-ai-slop`: generic hero trinity, indigo/violet defaults, lorem, gradient-everything — all failures.

## Outputs

- Design decisions sheet: style direction + rationale, color roles with **computed contrast ratios**, type scale, spacing/radius tokens, icon collection, chart choices (per screen)
- A11y checklist status (pass/fail per item)
- Render evidence (screenshots) where the skill was run in a browser

## Failure Conditions

- Body text under 4.5:1 (or 3:1 for large text) — the palette fails
- Invented a new style while ignoring the project's existing design language
- More than 2 typefaces or more than 6 type sizes in normal use
- Emoji or mixed icon sets in UI
- No loading/success/error states on actions
- Anti-slop failures (generic hero, violet-gradient default, lorem content)
- "Pretty" screenshots that were never rendered (claimed, not verified)

## Verification

Contrast values `COMPUTED` (numbers, per pair) · design `RENDERED` (real screenshots) · a11y checklist `EXECUTED` item-by-item. A palette reported as "looks good" without computed ratios is `UNVERIFIED` and not acceptable as final.

## Main Skill

For orchestration of larger work, use `pixz.core.orchestrator`. For critique of interaction quality, `pixz.design.uiux`; for full token/component specs, `pixz.design.design-system`.
