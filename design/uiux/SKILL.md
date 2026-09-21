---
name: UI/UX Design
description: Human-centered interface methodology — flows, hierarchy, affordance and usability verification.
version: 1.0.1
id: pixz.design.uiux
category: design
triggers: [ui design, ux review, interaction design, usability, interface]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# UI/UX Design — `pixz.design.uiux`

## Purpose
Delivers interfaces that are perceivable, operable, understandable and purposeful — not templated. Connects to anti-ai-slop, simplicity, accessibility and consistency.

## Methodology

### 1. Discover User & Context
- Who, goal, constraints, device, environment, accessibility needs.
- Via `context-engineering`: gather flows, content, brand tokens, accessibility baseline.

### 2. Flows & Hierarchy
- Map primary task flows (happy + unhappy paths). One primary CTA per view.
- Hierarchy: size, contrast, proximity, whitespace conveys order — decorative effects must justify themselves.

### 3. Affordance & Interaction
- Controls signal action (button vs link, affordance without guessing).
- States: default / hover / active / disabled / loading / error / empty.
- Responsive: mobile-first, but not breakpoint cargo-cult.

### 4. Anti-Slop Gate
- No generic SaaS grid unless it maps to real data hierarchy. Flag glassmorphism, template cards, fake complexity per `pixz.quality.anti-ai-slop`.

### 5. Verify
- Accessibility pass per `pixz.frontend.accessibility` (keyboard, screen reader, contrast).
- Usability: can a user complete primary task without instruction? Evidence via inspection or prototype test.
- Visual: does every decorative element have communicative purpose?

## Outputs
`uiux_artifact` {flows[], wireframes/prototype ref, hierarchy rationale, interaction specs, verification{ a11y, usability, slop_check }, residual_risks}

---
