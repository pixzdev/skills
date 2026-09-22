---
name: Epistemic Reasoning
description: The epistemic state engine — typed claims with explicit transitions (unknown→hypothesis→tested→supported), assumption tracking, calibrated confidence, position integrity.
version: 2.1.0
id: pixz.core.epistemic-reasoning
category: core
triggers: [reason, evidence, assumption, confidence, uncertainty, claim]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Epistemic Reasoning — `pixz.core.epistemic-reasoning`

> **Specialist HOW skill (claims).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for falsification, contradiction handling, and assumption management in the operating loop.
>
> Every consequential claim typed; every position revisable; every transition attributed. Apply where uncertainty matters — do not label every trivial sentence.

## Purpose
The epistemic state engine of PixzFlow: separates fact from inference, tracks assumptions, calibrates confidence, preserves position integrity. Prevents silent position flips, unjustified certainty, confirmation bias, and the T11 failure mode (trusting descriptive records).

## Core Taxonomy (label every consequential claim)

| Type | Meaning | Requires |
|------|---------|----------|
| `fact` | Reproduced or primary-source confirmed | evidence + source |
| `observed` | Seen in this environment (run, read, probe) | source command/path |
| `source_claim` | Quoted claim from a source | citation + fidelity check |
| `inference` | Derived via reasoning | premises + gap disclosure |
| `assumption` | Taken as given without proof | basis + fragility (low/med/high) + validation plan |
| `hypothesis` | Proposed explanation, untested | falsification conditions |
| `unknown` | Acknowledged gap | recorded in unknowns |
| `unverified` | Not yet checked; source may be descriptive | verification step required |
| `contradicted` | Evidence against — **preserved, not suppressed** | the contradicting evidence |
| `verified` | Checked against primary source/artifact | evidence ref + `verified_against` |
| `falsified` | Falsification condition met | the test + result |

## State Transitions (explicit)

```
unknown     → hypothesis  → tested  → supported | verified | falsified
assumption  → challenged  → falsified | supported
claim       → evidence    → verified | contradicted
contradicted→ (re)tested  → verified | superseded
```

A transition without a cause is invalid. Causes: new evidence · better reasoning · changed constraint · discovered assumption failure · failed verification · new requirement. Record the cause in the finding's history (task-state `findings[]`).

## Methodology

### 1. Build Arguments, Not Assertions
For each key decision:
```
claim + position + rationale + evidence[refs into task-state.evidence]
      + assumptions[+fragility] + alternatives + counterarguments
      + falsification_conditions + confidence(low/med/high + basis) + status
```

### 2. Track & Scale Confidence
Three-valued, always with basis:
```
high:   primary source confirms + reproduced locally + no contradiction
medium: primary source confirms + not reproduced (or partial evidence)
low:    secondary source or inference without reproduction
```

### 3. Source-of-Record Check
Any claim about system state inherits the verification skill's source-of-record protocol: prefer actual filesystem / git tree / fresh test output / command output / artifact / deployed state over descriptive records. A `source_claim` that has never been checked against a primary artifact stays at most `unverified`.

### 4. Seek Disconfirming Evidence (risk-scaled)
Intensity proportional to `risk × uncertainty × impact × irreversibility`. Routine rename → minimal; prod security architecture → substantial. Actively ask: what evidence would contradict this? Search for it.

### 5. Preserve Position Integrity
Do NOT silently flip, nor cling to a prior position. Position changes attributable ONLY to the causes above; each change recorded (append-only ledger in task-state).

## Inputs / Outputs
- **Inputs:** claims to evaluate, evidence pool, constraints
- **Outputs:** `reasoning_artifact` {findings[], assumptions[], unknowns[], confidence_map, transitions[]}

## Failure Conditions
- Fabricated evidence or citation dumping (quantity over quality).
- Decorative confidence without basis.
- Suppressing counterevidence (a `contradicted` finding must stay visible).
- Silent position flip without recorded cause.

## Verification
- Challenger can independently reproduce or falsify per `falsification_conditions`.
- Each `fact` has a primary source; each `inference` discloses its gap; each confidence has a basis; `unknowns` non-empty for non-trivial tasks.
- Anti-AI-slop cross-check: no filler reasoning verbosity without information.

## Structured Output
```yaml
findings:
  - claim: "p95 latency < 200ms with current PG indexes"
    type: hypothesis
    status: tested
    evidence_refs: [e3]
    confidence: medium
    confidence_basis: ["EXPLAIN ANALYZE on staging", "not load-tested at prod scale"]
    falsification: ["p95 > 300ms at 10k rps on staging"]
  - claim: "staging mirrors prod"
    type: assumption
    status: active
    confidence: low
    confidence_basis: ["infra owner statement; not inspected"]
    falsification: ["config diff shows differing pool sizes"]
unknowns: ["hotspot write pattern not observed"]
transitions: [{claim: "p95 claim", from: hypothesis, to: tested, cause: "staging benchmark run e3"}]
```

## Runtime Notes
Identical across runtimes. Adapters do not affect epistemic labeling.

---
*Companion: `pixz.core.epistemic-challenger` provides adaptive, intensity-scaled stress-testing with an explicit stop rule.*
