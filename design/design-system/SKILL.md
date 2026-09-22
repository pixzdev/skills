---
name: Design System
description: Define and enforce tokens, components, patterns and governance for consistent UIs. Use when creating or extending a system. Do not invent a second button. For product-wide rollouts, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.design.design-system
category: design
triggers: [design system, tokens, components, consistency]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Design System — `pixz.design.design-system`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when introducing or migrating a system.

## Purpose

One source of visual and interaction truth so product UI does not fork into snowflakes.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Introducing tokens, adding a canonical component, deprecating a duplicate | One-off marketing page with no reuse |
| Governance (versioning, contribution) | Restyling a single instance against the system |

## Methodology

### 1. Tokens (layered)

```
primitive (pink.500) → semantic (color.danger) → component (button.bg.danger)
```

Cover: color, type, space, radius, motion, z-index, elevation. Semantic names, not "blue2". Motion tokens must include a `reduced` counterpart.

### 2. Components

- **One canonical per pattern.** If a second Button appears, it is a bug — extend the first or justify a variant.
- Props API minimal: `variant`, `size`, `tone`, `isDisabled`, `isLoading`. No kitchen-sink `style=` escape without an documented exception.
- States covered: default, hover, focus-visible, active, disabled, loading, error. Focus rings are not optional.
- Compose; do not fork. Slot/children over prop explosion.

### 3. Patterns

Document the few flows that must be consistent: forms, dialogs, navigation, toasts, empty states. Point to `pixz.design.uiux` for the interaction rationale.

### 4. Governance

- Contribution: new component needs a use-count ≥ 2 or a written exception.
- Deprecation: alias old name → new, warn, remove next major.
- Versioning: tokens and public component props are the API. Breaking = major.
- Anti-slop: template duplication and decorative-only variants fail `pixz.quality.anti-ai-slop`.

### 5. Verify

- a11y on every canonical (`pixz.frontend.accessibility`)
- visual regression on tokens + components
- consistency scan: grep for raw hex / duplicate Button files

## Failure Conditions

- Primitive tokens used directly in product views → leak; consume semantic.
- New component duplicating an existing one → reject.
- No focus-visible on a canonical → blocked.

## Example

> Team added `PrimaryButton` and `AppButton`. Canonicalize to `Button` with `tone=brand|neutral|danger`. Deprecate aliases. Replace raw `#6366f1` with `color.action`. Visual snapshot + axe on Button stories.

## Structured Output

```yaml
system:
  tokens: {primitive, semantic, component}
  components: [{name, props, states, a11y}]
  deprecations: [{from, to, major}]
  verification: {a11y, visual_regression, duplicates}
```

## Main Skill

A design-system adoption across an app is orchestrator work. Activate `pixz.core.orchestrator`.
