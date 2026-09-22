---
name: Accessibility
description: WCAG-grounded auditing and remediation — perceivable, operable, understandable, robust. Use for UI that people must use. Do not skip keyboard or screen-reader checks. For full product work, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.frontend.accessibility
category: frontend
triggers: [a11y, accessibility, wcag, aria, screen reader]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Accessibility — `pixz.frontend.accessibility`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when a11y is part of a larger ship.

## Purpose

Guarantees POUR principles with verifiable remediation — not a lighthouse screenshot waved as proof.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Any user-facing UI, design system canonical, forms, dialogs, media | Backend-only, CLI-only (unless the CLI is the product UI) |
| Pre-ship a11y gate | "We'll do a11y later" on a primary flow — that *is* when to use this |

## Methodology

### 1. Audit (POUR, WCAG 2.2 AA)

- **Perceivable:** text alternatives, captions, contrast **4.5:1** normal text / **3:1** large and UI components, don't use color alone, `prefers-reduced-motion`.
- **Operable:** keyboard-only traversal, visible focus, no keyboard trap, skip link, target size ≥ 24px (2.2), motion from interaction can be disabled.
- **Understandable:** labels, errors identified in text, language on `<html>`, consistent nav.
- **Robust:** valid HTML, ARIA only when native is insufficient, name/role/value available to assistive tech.

### 2. Codify (implementation order)

1. Semantic HTML (`button`, `a`, `label`, headings in order, lists, `main`/`nav`).
2. Native control before ARIA. If you use `div onClick`, you already failed.
3. Visible `:focus-visible` ring using the design-system token.
4. `aria-*` only to fill a native gap; never `aria-label` that disagrees with visible text.
5. Dialogs: focus trap, restore focus, `Escape` closes, `aria-modal`.
6. Live regions for async status (`aria-live="polite"`), not for every keystroke.

### 3. Verify (automation is evidence, not proof)

- Automated: axe, lighthouse, eslint-plugin-jsx-a11y — collect as evidence.
- Manual **keyboard**: Tab/Shift+Tab/Enter/Space/Escape through the primary flow.
- Manual **screen-reader** (VoiceOver / NVDA as available): name, role, value of interactive controls.
- Contrast check on actual computed colors (tokens can drift).
- Zoom 200% and 320px width: no clipped essential content.

### 4. Report

`{barrier, WCAG criterion, impact, evidence, fix, re-test procedure}`

## Inputs / Outputs

- Inputs: markup/component, environment report, design tokens
- Outputs: `a11y_report` {violations[], fixes[], verification, residual_risks}

## Failure Conditions

- "axe passed" as the only check → insufficient for CORRECT on a primary flow.
- `aria-label` hiding a visible label that says something else → lie to AT; fix.
- Custom checkbox without role/keyboard → blocked.

## Example

> Modal checkout. Violations: no focus trap (2.1.2), submit is a `<div>` (4.1.2), error only in red (1.4.1). Fixes: `role="dialog"` + trap, real `<button>`, error text + `aria-describedby`. Re-test: keyboard-only complete purchase; screen-reader announces error.

## Main Skill

A11y across a product release is orchestrator work (design + frontend + verification). Activate `pixz.core.orchestrator`.
