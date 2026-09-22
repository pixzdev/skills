---
name: GSAP Motion
description: GSAP timeline and ScrollTrigger methodology with performance and accessibility constraints.
version: 1.1.0
id: pixz.motion.gsap
category: motion
triggers: [gsap, scrolltrigger, tween, timeline animation]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# GSAP Motion — `pixz.motion.gsap`

## Purpose
Procedural motion that earns its existence — not decorative filler.

## Methodology
1. **Justify:** does motion aid comprehension or transition? If purely decorative, flag via anti-ai-slop.
2. **Compose:** timelines with labeled sequencing; ScrollTrigger with `scroller` proxy, `scrub` gated, `pin` with overflow checks; respect `prefers-reduced-motion`.
3. **Perform:** composited properties (`transform`, `opacity`) only; batch reads/writes; `will-change` scoped; FPS budget 60 on mid-tier mobile.
4. **Safety:** guard `ScrollTrigger.refresh()`, kill tweens on unmount, no layout thrash, test rotation/resize.
5. **Verify:** timeline scrub test, reduced-motion disables motion, no CLS regression.

## Outputs
`motion_spec` {timeline ref, triggers[], performance notes, a11y handling, verification}

---
