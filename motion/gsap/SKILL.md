---
name: GSAP Motion
description: GSAP timeline and ScrollTrigger methodology with performance and accessibility constraints. Use when motion must aid comprehension. Do not animate layout properties. For multi-step UI work, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.motion.gsap
category: motion
triggers: [gsap, scrolltrigger, tween, timeline animation]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# GSAP Motion — `pixz.motion.gsap`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when motion is part of a larger UX change.

## Purpose

Procedural motion that earns its existence — not decorative filler.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Choreographed sequences, scroll-linked storytelling, shared-element transitions | Random hover wiggle on every card |
| Existing GSAP codebase | CSS transition of `opacity` for a simple fade — CSS is enough |

## Methodology

### 1. Justify

Does motion aid comprehension or transition? If purely decorative, flag via `pixz.quality.anti-ai-slop` and skip or reduce.

### 2. Compose

- Use `gsap.context()` (or `useGSAP`) so tweens kill on unmount/HMR.
- Timelines with labeled sequencing (`tl.addLabel`, `tl.to(..., '<0.2')`).
- ScrollTrigger: set `scroller` if not the viewport; `scrub` only when the scroll *is* the playhead; `pin` only after overflow/layout checks; always `ScrollTrigger.refresh()` after fonts/images/layout.
- Honor `prefers-reduced-motion`: replace motion with an instant end-state (no `scrub` pin-jacking).

```js
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (reduce) { /* set final styles, no tweens */ return; }
```

### 3. Perform

- Composited properties only: **`transform`**, **`opacity`**. Never tween `top/left/width/height/margin` for continuous motion.
- Batch reads/writes; don't read layout inside `onUpdate`.
- `will-change` scoped to the animating element for the duration, then removed.
- FPS budget: 60 on mid-tier mobile. If you can't hit it, cut pins and blurs first.

### 4. Safety

- Kill tweens on unmount (`ctx.revert()`).
- No layout thrash; test rotation and resize (ScrollTrigger must refresh).
- Avoid animating huge `filter: blur()` on text during scroll.

### 5. Verify

- Timeline scrub test (and reverse).
- `prefers-reduced-motion` disables motion.
- No CLS regression (no layout properties animated).
- Keyboard users are not trapped in a pin.

## Outputs

`motion_spec` {timeline ref, triggers[], performance notes, a11y handling, verification}

## Failure Conditions

- Animating `top`/`height` for a scroll story → rewrite to transform.
- Tweens leaking across route changes → must `revert`.
- Ignoring reduced-motion → blocked on user-facing pages.

## Example

> Hero pin + fade-up. Justify: explains product in three beats. `gsap.context` in a client leaf. Tweens `y` + `opacity` only. Reduced-motion shows beat 3 immediately. Verify: resize, route away/back, axe still passes.

## Main Skill

Motion inside a product flow is orchestrator work when it touches UX, a11y, and performance together. Activate `pixz.core.orchestrator`.
