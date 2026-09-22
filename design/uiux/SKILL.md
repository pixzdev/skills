---
name: UI/UX Design
description: Human-centered interface methodology — flows, hierarchy, affordance, states, and usability verification. Use when designing or reviewing UI. Do not use for backend-only work. For multi-step product work, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.design.uiux
category: design
triggers: [ui design, ux review, interaction design, usability]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# UI/UX Design — `pixz.design.uiux`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` and use the Visitor / User Simulator role on user-facing work.

## Purpose

Delivers interfaces that are perceivable, operable, understandable and purposeful — not templated. Connects to anti-ai-slop, simplicity, accessibility and consistency.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| New flow, dashboard, onboarding, empty/error/permission states | API-only change, schema migration |
| UX review of an existing screen | "Change the hex of this token" (that's design-system) |

## Methodology

### 1. Discover user & context

Who, goal, constraints, device, environment, accessibility needs. Via `context-engineering`: gather flows, content, brand tokens, accessibility baseline.

### 2. Flows & hierarchy

- Map primary task flows (happy + unhappy paths). One primary CTA per view.
- Hierarchy: size, contrast, proximity, whitespace conveys order — decorative effects must justify themselves.

### 3. Affordance & interaction

- Controls signal action (button vs link, affordance without guessing).
- States: default / hover / active / disabled / loading / error / empty / permission-denied.
- Responsive: mobile-first, but not breakpoint cargo-cult. Thumb reach for primary actions on small screens.

### 4. Copy as UI

Labels, empty states, errors, and confirmations are part of the interface. Errors say what happened and what to do. No lorem, no "Oops something went wrong" without a next step.

### 5. Anti-slop gate

No generic SaaS grid unless it maps to real data hierarchy. Flag glassmorphism, template cards, fake complexity per `pixz.quality.anti-ai-slop`.

### 6. Visitor test (required on primary flows)

Walk the primary task as a new user with no interior knowledge. Note: where do they get stuck, what is unlabeled, what requires hover-only discovery, what breaks at 320px, what fails keyboard-only.

### 7. Verify

- Accessibility pass per `pixz.frontend.accessibility` (keyboard, screen reader, contrast).
- Usability: can a user complete the primary task without instruction? Evidence via inspection or prototype test.
- Visual: does every decorative element have communicative purpose?

## Outputs

`uiux_artifact` {flows[], wireframes/prototype ref, hierarchy rationale, interaction specs, verification{ a11y, usability, slop_check }, residual_risks}

## Failure Conditions

- Happy path only — missing empty/error/denied → incomplete.
- Multiple competing CTAs of equal weight → hierarchy failure.
- Decorative motion or glassmorphism without purpose → slop; revise.

## Example

> Analytics dashboard. Primary task: "see today's conversion and drill into a dip." Flow: landing → date range → metric → drill. Hierarchy: one number + sparkline, not six equal cards. Empty: "No events in this range — ingest is on /settings/sources". Visitor test fails if filters are icon-only.

## Main Skill

End-to-end product work (research → UX → UI → a11y → impl → verify) is orchestrator work. Activate `pixz.core.orchestrator`.
