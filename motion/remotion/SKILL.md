---
name: Remotion
description: Declarative video composition with timeline verification and render-pipeline discipline. Use for programmatic video at edit-scale. Do not stand up Remotion for a one-off clip. For pipeline work, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.motion.remotion
category: motion
triggers: [remotion, programmatic video, react video]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Remotion — `pixz.motion.remotion`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for render-pipeline / CI work.

## Purpose

Frame-accurate, deterministic video from React — when many variants or data-driven edits justify a pipeline.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Hundreds of variants, data-driven titles, CI-rendered social clips | A single 15s explainer better made in an editor |
| Existing Remotion project | Animating a website (that's GSAP/CSS) |

## Methodology

### 1. Justify

Does programmatic video solve edit-scale? If one-off, a static render or editor export may beat a pipeline.

### 2. Compose

- `<Composition id fps width height durationInFrames component />` registered in `src/Root.tsx` (or the project's root).
- Sequences with explicit `from` / `durationInFrames`. Never infer duration from CSS.
- `interpolate` / `spring` for eases; clamp `extrapolateLeft/Right`.
- `useCurrentFrame` + `useVideoConfig` — don't read wall-clock time.
- Interactive preview should honor reduced-motion where the preview is the product; rendered video is a recording, not an a11y surface, but captions still matter.

### 3. Assets & I/O

- Local assets only during render. **No network during render** (`delayRender`/`continueRender` must resolve from local or prefetched data).
- `calculateMetadata` for duration that depends on data (audio length, item count).
- Fonts: wait for `loadFont` before drawing text.

### 4. Pipeline

- Deterministic render: pin Remotion version, pin Chromium, hash inputs → artifact name.
- Duration budget: fail the composition if `durationInFrames` exceeds the agreed cap.
- Encode explicitly (`--codec h264`, bitrate). Don't rely on "whatever Studio exported last time".

### 5. Verify

- Local render parity with Studio (same frame, same hash of a still).
- Frame scrub at 0, mid, last frame — no off-by-one blank tail.
- Missing asset fails fast (throw), never a black frame.
- Captions/subtitles present if the video has speech.

## Failure Conditions

- Fetching in `useEffect` during render → non-deterministic; prefetch.
- Duration hardcoded while data length varies → clipped or padded; use `calculateMetadata`.
- Off-by-one last frame black → duration vs sequence mismatch.

## Example

> Weekly stats video. `calculateMetadata` sets duration from row count. Sequences per section. Prefetch JSON in the render script, pass as `inputProps`. CI: `npx remotion render Stats out/stats.mp4` with pinned version. Verify still of frame 0 against fixture.

## Structured Output

```yaml
remotion:
  compositions: [{id, fps, size, durationInFrames}]
  input_props: [...]
  determinism: {no_network: true, pinned: true}
  verification: {still_hash, last_frame, captions}
```

## Main Skill

A video pipeline (data → composition → CI render → QA) is orchestrator work. Activate `pixz.core.orchestrator`.
