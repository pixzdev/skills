---
name: Anti-AI Slop
description: Detects and challenges generic, decorative, boilerplate or hallucinated artifacts in design, code and docs.
version: 1.0.0
id: pixz.quality.anti-ai-slop
category: quality
triggers: [anti slop, generic design, boilerplate, AI slop, generic SaaS, template]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Anti-AI Slop — `pixz.quality.anti-ai-slop`

> Diagnostic criteria, not dogmatic bans. Every critique must have a communicative/functional justification.

## Purpose
First-class quality skill that prevents “AI-looking” artifacts: templated layouts, decorative complexity, boilerplate code, hallucinated claims, filler docs. Applies across design / code / research / documentation.

## Triggers
- Pre-ship review of UI, code, or docs
- Optional gate in orchestrator when `quality-gate` or explicit request

## Anti-Pattern Taxonomy

### Design
- generic SaaS layouts, meaningless glassmorphism, excessive gradients
- template-like cards, repetitive spacing, fake visual complexity
- AI-looking illustrations, meaningless animations, generic copy, decorative without purpose
- **Wrong:** “Never use gradients.” **Right:** “Do not introduce visual effects without a communicative, functional, or justified aesthetic purpose.”

### Code
- unnecessary abstraction, boilerplate, fake/random comments
- generated-looking naming, needless dependencies, overengineering, duplicated logic, architecture astronautics

### Research
- citation dumping, weak source quantity over quality, unsupported claims, fabricated evidence, false certainty

### Documentation
- filler, repetition, excessive verbosity without information, generic statements

## Methodology

### 1. Inspect Against Purpose
For each visual/code/docs element ask: *What does this communicate or enable?* If answer is “looks nice” without functional/aesthetic justification, flag it.

### 2. Redundancy Scan
- Design: repeated card/grid patterns without hierarchy differentiation?
- Code: duplicated logic or abstraction that saves no complexity?
- Docs: same generic statement in three places?

### 3. Authenticity Scan
- Copy generic? Illustrations interchangeable with any SaaS?
- Comments explain what code already says? Evidence fabricated?

### 4. Simplicity Test (from policy)
“Do the minimum necessary, but not minimum possible.” Flag over-abstracted microservices, unnecessary micro-skills, excessive orchestration.

### 5. Report, Not Dogmatism
Emit `slop_report` with severity (low/med/high), evidence, and concrete replacement that preserves intent with less artifact. Do not ban aesthetics — demand justification.

## Inputs / Outputs
- **Inputs:** artifact (code + screenshots + docs), context, constraints
- **Outputs:** `slop_report` {findings: [{area, pattern, evidence, severity, why_slop, replacement}], verdict: pass|revise, residual_risks}

## Verification
- Before/after diff shows reduced template footprint without loss of function.
- Second reviewer (human or `verification`) agrees verdict is not dogmatic.
- No filler content remains that lacks information density.

## Structured Output
```yaml
findings:
  - area: "Hero section"
    pattern: "generic glassmorphic card grid"
    evidence: "3 identical cards with Lorem ipsum, no hierarchy"
    severity: high
    why_slop: "Decorative container adds no affordance; copy generic"
    replacement: "Single purposeful hero with concrete value prop + 1 code sample"
verdict: revise
```

## Relationship
Optional in orchestrator, mandatory before ship when design/code/docs quality matters. Works alongside `verification` and `quality-gate`; respects `simplicity` policy.

---
