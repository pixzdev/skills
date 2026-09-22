---
name: Anti-AI Slop
description: Diagnostic (not dogmatic) detection of generic, decorative, boilerplate or hallucinated artifacts — judges purpose and value, never surface traits alone.
version: 2.0.0
id: pixz.quality.anti-ai-slop
category: quality
triggers: [anti slop, generic design, boilerplate, AI slop]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
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
- filler, repetition, excessive verbosity without information, generic statements, repetitive documentation across files

### Never "slop" merely because
An artifact is **not** slop by surface trait alone. Do not flag something because it is: verbose · abstract · animated · componentized · AI-generated · unconventional · long · sophisticated. Judge **purpose and value**: what does it communicate or enable, and does it earn its cost? A long doc that carries unique information is not filler; an abstraction that removes real duplication is not fake complexity; an animation that conveys state is not decoration. When in doubt, the element passes and the doubt is recorded — false positives waste trust faster than missed slop.

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
