# GLM Benchmark — Findings Record (do not rewrite)

> Status: **OBSERVED** (controlled experiment, completed). This document preserves the empirical record that motivates the PixzFlow 2.0 design. Numbers are approximate means as reported at the time of the experiment.

## Design

- **A** = native GLM operating behavior
- **B** = GLM + current PIXZ methodology/skills (full system)
- **B1** = B with one key skill removed
- **C** = native GLM allowed to discover/use installed skills **without** the full Pixz methodology
- 52 task-execution runs · 11 blind graders · 22 graded native runs · 22 graded Pixz runs · additional non-blind experimental conditions · repeated tasks · fresh environments · objective verification · blind grading · multiple task classes.

## Results

### Correctness
- **Both A and B achieved 52/52 objective acceptance.**
- Interpretation: the tested GLM environment hit a substantial correctness ceiling.
- **Consequence:** PixzFlow must NOT claim dramatic correctness improvement for frontier-class GLM on this evidence.

### Blind grading (approximate means, 5-point scale)
- Native GLM ≈ **4.77**
- PixzFlow ≈ **4.94**
- Difference ≈ **+0.17** — small. Report it as such.

### Token efficiency (approximate means)
- Native ≈ **33.8k**, Pixz ≈ **50.0k** → ≈ **1.48×** overhead.
- Overhead was largest on **trivial tasks**; complex tasks reduced the relative gap.
- T12 continuation: Pixz used **fewer** tokens in phase 2. Careful reading: this does **not** prove general efficiency; it suggests explicit state/workflow structure can **amortize** over long-horizon continuation (HYPOTHESIS — test in successor benchmark).

### Native GLM spontaneous behavior
Observed without Pixz methodology: understanding, inspection, assumptions, verification, secondary verification, regression awareness, contradiction resolution, failure recovery, security reasoning, long-horizon continuation.
**Consequence:** do not build PixzFlow on the assumption that frontier models must be taught basic engineering. PixzFlow should make strong behavior **more consistent, persistent, inspectable, transferable, and recoverable**.

### Narrow differentiator
- **T11 (source-of-record / evidence integrity):** PixzFlow was more likely to verify apparently authoritative records against actual artifacts instead of trusting the record. **n = 2 → hypothesis-generating signal, not proof.** Promoted to a formal protocol in 2.0 (`pixz.protocol.source-of-record`); validation is the successor benchmark's job.

### Skill marginality
- **B ≈ B1** (removing a key skill changed nothing measurable)
- **C ≈ A** (native + skills available ≈ full Pixz methodology)
- Interpretation: **skills alone did not create a measurable capability advantage.** PixzFlow must move beyond "more skills" into: persistent operating substrate + adaptive capability activation + state continuity + evidence architecture + verification + runtime-aware execution.

### Skill discoverability
- Native GLM did **not** spontaneously discover the installed Pixz skills in the main benchmark.
- When skills were made available explicitly, it often used relevant ones.
- Interpretation: **capability availability and capability invocation are separate problems.** 2.0 introduces a persistent activation protocol; it must not force every skill into every task.

## Design obligations this record imposes on 2.0

1. No correctness claims beyond the evidence.
2. Trivial tasks must stay cheap (explicit orchestration budget).
3. Skills must be activatable on demand, with tracked state — not force-loaded bundles.
4. State structure must be validated for long-horizon amortization (successor benchmark cell: continuation).
5. Source-of-record discipline becomes a reusable, testable protocol.
6. Any claim that a 2.0 component helps must be backed by ablation (see `docs/benchmark/successor-benchmark.md`).
