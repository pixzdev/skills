---
name: Remotion
description: Declarative video composition with timeline verification and render-pipeline discipline.
version: 1.0.1
id: pixz.motion.remotion
category: motion
triggers: [remotion, programmatic video, react video, timeline render]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Remotion — `pixz.motion.remotion`

## Methodology
1. **Justify:** does programmatic video solve edit-scale? If one-off, static render may beat pipeline.
2. **Compose:** declarative timeline, sequence with `from`/`durationInFrames`, handle frame-rate, `interpolate` for eases; respect reduced-motion where interactive preview.
3. **Pipeline:** deterministic render (no network during render), artifact hash, duration budget.
4. **Verify:** local render parity, frame scrub, no off-by-one, asset missing fails fast.

---
