---
name: Accessibility
description: WCAG-grounded auditing and remediation — perceivable, operable, understandable, robust.
version: 1.0.0
id: pixz.frontend.accessibility
category: frontend
triggers: [a11y, accessibility, wcag, aria, screen reader, keyboard nav]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Accessibility — `pixz.frontend.accessibility`

## Purpose
Guarantees POUR principles with verifiable remediation.

## Methodology
1. **Audit:** keyboard-only traversal, screen-reader announcement, color-contrast (WCAG 2.2 AA: 4.5:1 text), focus order, ARIA validity, reduced-motion.
2. **Codify:** semantic HTML first; ARIA only when native insufficient; visible focus; skip links.
3. **Verify:** automated (axe, lighthouse) + manual (keyboard, NVDA/VoiceOver) — automation is evidence, not proof.
4. **Report:** `{barrier, WCAG criterion, impact, evidence, fix, re-test procedure}`

## Inputs / Outputs
- Inputs: markup/component, environment report
- Outputs: `a11y_report` {violations[], fixes[], verification, residual_risks}

---
