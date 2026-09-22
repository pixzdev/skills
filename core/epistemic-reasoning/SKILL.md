---
name: Epistemic Reasoning
description: Disciplined reasoning that separates fact from inference, tracks assumptions, and calibrates confidence.
version: 1.1.0
id: pixz.core.epistemic-reasoning
category: core
triggers: [reason, evidence, assumption, confidence, uncertainty]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Epistemic Reasoning — `pixz.core.epistemic-reasoning`

> How to think reliably under uncertainty. Every claim labeled; every position revisable.

## Purpose
Provides the argumentation system and epistemic discipline the ecosystem requires. Prevents silent position flips, unjustified certainty, and confirmation bias. Aggregates: evidence discipline, uncertainty management, assumption tracking, confidence scaling, argument integrity, anti-confirmation bias.

## Triggers
- Any decision requiring tradeoff, claim, or recommendation
- Verification, threat modeling, system design, or pre-ship review

## Core Taxonomy (label every claim)

| Label | Meaning | Requires |
|-------|---------|----------|
| `FACT` | Reproduced or primary-source confirmed | evidence + citation |
| `SOURCE CLAIM` | Quoted claim from source | citation + fidelity |
| `AGENT INFERENCE` | Derived via reasoning | premises + gap disclosure |
| `ASSUMPTION` | Taken as given without proof | basis + fragility (low/med/high) + validation plan |
| `SPECULATION` | Low-evidence stretch | explicit flag + not used for decisions |
| `UNKNOWN` | Acknowledged gap | documented in `unknowns` |
| `UNVERIFIED` | Not yet checked | verification step required |
| `CONTRADICTED` | Evidence against | preserved, not suppressed |

Do NOT present inference as fact. Confidence numbers are forbidden unless they have a basis.

## Methodology

### 1. Build Arguments, Not Assertions
For each key decision, produce:
```
claim + position + rationale + evidence[+source, strength] + assumptions[+fragility]
        + constraints + alternatives + counterarguments + rebuttal
        + falsification_conditions + confidence(low/med/high + basis) + status + revision_history
```
Store in `schemas/workflow.schema.json#arguments`.

### 2. Track & Scale Confidence
Confidence is three-valued with basis:
```
high:   primary docs confirm + reproduced locally + no contradiction
medium: primary docs confirm + not reproduced (or partial evidence)
low:    secondary source or inference without reproduction
```
Example basis:
```yaml
confidence: medium
basis:
  - primary documentation confirms behavior
  - reproduced locally (unit)
  - production environment not tested
unknowns: [behavior under production load]
```

### 3. Seek Disconfirming Evidence (risk-scaled)
Intensity proportional to `risk × uncertainty × impact`. Routine rename → minimal; prod security architecture → substantial.
Actively ask: What evidence would contradict this? Search for it.

### 4. Preserve Position Integrity
Do NOT silently flip, nor cling to a prior position. Position changes attributable ONLY to:
- new evidence
- better reasoning
- changed constraints
- discovered assumption failure
- failed verification
- new requirement
Record attribution in `revision_history`.

### 5. Argument Ledger
Maintain an append-only ledger: every position change logs predecessor, cause, new evidence, and confidence delta. Ledger is inspectable by verifier/challenger.

## Inputs / Outputs
- **Inputs:** claims to evaluate, evidence pool, constraints
- **Outputs:** `reasoning_artifact` {arguments[], assumptions[], unknowns[], confidence_map, ledger}

## Failure Conditions
- Fabricated evidence or citation dumping (quantity over quality).
- Decorative confidence numbers without basis.
- Suppressing counterevidence.

## Verification
- Challenger can independently reproduce or falsify per `falsification_conditions`.
- Inspection checks: each `FACT` has primary source; each `INFERENCE` discloses gap; each `confidence` has basis; `unknowns` non-empty for non-trivial tasks.
- Anti-AI-slop cross-check: no filler reasoning verbosity without information.

## Structured Output
```yaml
arguments:
  - claim: "p95 latency < 200ms with current PG indexes"
    position: "holds for 10k rps"
    rationale: "..."
    evidence: [{claim: "...", source: "EXPLAIN ANALYZE on staging", strength: medium}]
    assumptions: [{claim: "staging mirrors prod", fragility: high}]
    counterarguments: ["write amplification under hotspot"]
    falsification: ["p95 > 300ms at 10k rps on staging"]
    confidence: medium
    confidence_basis: ["primary docs confirm index type", "not load-tested at prod scale"]
    status: active
unknowns: ["hotspot write pattern not observed"]
```

## Runtime Notes
Identical across runtimes. Adapters do not affect epistemic labeling.

---
*Companion: `pixz.core.epistemic-challenger` provides adaptive stress-testing for these arguments.*
