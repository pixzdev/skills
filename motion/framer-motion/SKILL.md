---
name: Framer Motion
description: Framer Motion (Motion v12) for React/Next.js — declarative animations, variants, layout animations, gestures, scroll-driven motion (useScroll/useTransform/useSpring), AnimatePresence exits, springs vs tweens, performance (transform/opacity only, LazyMotion), prefers-reduced-motion, and the GSAP-vs-Framer library decision. Use when animating React components.
version: 1.0.0
id: pixz.motion.framer-motion
category: motion
triggers: [framer motion, motion animation, useScroll, AnimatePresence, spring animation, layout animation]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Framer Motion — `pixz.motion.framer-motion`

> **Specialist HOW skill (motion, React).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`.
>
> Library decision first, animation second. Wrong library is a 10× rework; nice easing on the wrong library is still rework.

## Purpose

Implement motion in React/Next.js with Framer Motion (package `motion` since v12; `framer-motion` still works, same API) — declarative, interruptible, performance-safe, accessible, and verified in a real browser.

## When to Use / When NOT

| Use Framer Motion | Use instead |
|-------------------|-------------|
| React/Next.js, declarative style, component state ↔ animation | Vanilla JS / Webflow / Vue → **GSAP** (`pixz.motion.gsap`) |
| Entrance/hover/exit tied to React state (`AnimatePresence`) | Pinning, horizontal scroll hijack, complex multi-step timelines → **GSAP ScrollTrigger** |
| `whileInView` entrances, layout animations (`layoutId`) | Non-React DOM → GSAP or CSS |
| Spring physics for interactive elements (drag, tap) | Video/render pipelines → `pixz.motion.remotion` |

If both in one app: Framer for component-level motion, GSAP for page-level scroll choreography — do not mix both on the same element.

## Methodology

1. **DESIGN THE MOTION BEFORE CODE.** For each animation state: *intent* (what the user should feel/notice), *trigger* (state change / hover / in-view / scroll), *properties* (**transform + opacity only** — never animate width/height/box-shadow/top/left), *easing* (spring for interactive, tween `ease: [0.22, 1, 0.36, 1]`-class curves for entrances), *duration* (100–300ms interactive · 300–600ms entrance). Restraint rule: one page should not have more than 2–3 distinct motion idioms.
2. **STRUCTURE WITH VARIANTS.** Parent orchestrates via `variants` + `animate`/`initial`/`exit`; children inherit via the variant propagation (`show`/`hide`/`exit` naming). This keeps sequencing in one place — no scattered timeouts.
3. **CHOOSE SPRING vs TWEEN.** Springs: interactive, interruptible, physical (buttons, drags, layout) — tune with `stiffness`/`damping`/`mass`, or presets (`type: "spring", stiffness: 300, damping: 30`). Tweens: timed entrances, scroll-linked.
4. **EXITS NEED `AnimatePresence`.** Conditional removal only animates inside `<AnimatePresence>` with a stable `key`. Without it, "exit" is an instant unmount — a silent failure.
5. **SCROLL MOTION (when scroll is the driver).** `useScroll({ target, offset })` → `useTransform(progress, [0, 1], [from, to])` → bind via `style={{ y, opacity }}` on a `motion.*` element (the transformed value must land on a motion element, not a plain div). `useSpring` to smooth jumpy progress. Never put `useTransform` output on a plain DOM style object.
6. **NEXT.JS RULES.** `'use client'` on any file using motion hooks/components. SSR-safe defaults: prefer `initial={false}` or `whileInView` for above-the-fold entrances to avoid hydration mismatch flashes.
7. **PERFORMANCE.** Animate `transform`/`opacity` only. For large lists/pages: `LazyMotion` + `m.*` (or `useAnimate`) to cut bundle — verify the bundle delta when you add the lib. Avoid re-render loops: no `useTransform` computed from state that the animation itself updates.
8. **ACCESSIBILITY (non-negotiable).** Honor `MotionConfig reducedMotion="user"` (or `useReducedMotion()`) — under reduced motion, skip movement and keep opacity/none. Focusable elements must remain reachable mid-animation.
9. **VERIFY IN A REAL BROWSER (RUNTIME-ACTIVE).** The code compiling is not proof of the motion. Use the `animation-inspector` MCP (discovers Framer Motion systems, captures frames at scroll positions) or `playwright` MCP: screenshot the entrance at start/mid/end, check the exit actually plays (unmount timing), check no console errors, check it still works under reduced motion. Evidence = frames + what you observed.

## Outputs

- Working animation code + the motion decision table (intent/trigger/properties/easing/duration per animation)
- Bundle delta when the library was added
- Browser frames/console evidence of the actual motion

## Failure Conditions

- "Exit" doesn't play (missing `AnimatePresence` / unstable key)
- Animation stutters or causes re-render loops (non-transform properties, state feedback)
- Hydration mismatch flash in Next.js (missing `'use client'` / unsafe `initial`)
- Motion ignored under `prefers-reduced-motion`
- `useTransform` output bound to a plain div (nothing moves)
- Library chosen for the wrong stack (GSAP territory forced into React declarative style)

## Verification

Code `CORRECT` (runs, no errors) → motion `RUNTIME-ACTIVE` (frames/screenshots show it moving as designed, exit plays, reduced-motion respected). Report which rung the evidence supports.

## Main Skill

For orchestration of larger work, use `pixz.core.orchestrator`. For non-React motion, `pixz.motion.gsap`; for video rendering, `pixz.motion.remotion`.
