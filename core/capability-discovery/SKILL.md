---
name: Capability Discovery
description: Persistent capability discovery and invocation — progressive loading of skills, agents, tools, MCP servers and libraries, with tracked activation state that survives phase transitions.
version: 2.0.0
id: pixz.core.capability-discovery
category: core
triggers: [discover, what can I use, available tools, find skill, activate skill]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Capability Discovery — `pixz.core.capability-discovery`

> "Discover first, select second, use third — and keep using." Skills are persistent capabilities, not one-time prompt attachments.

## Purpose
Prevents both failure modes observed in the GLM benchmark: (a) models not discovering installed capabilities (availability ≠ invocation), and (b) models loading everything because something exists (skill spam). Provides the **persistent activation protocol** used by the orchestrator and by any agent working under PixzFlow.

## Methodology

### 1. DISCOVER (lightweight)
Scan capability **metadata only**: `registry.json` (machine) / `llms.txt` (LLM map) — names + descriptions + triggers. Do not load skill bodies. Inventory tools/MCP (`list_tools` or runtime equivalent), CLIs, libraries in repo.

### 2. MATCH
Rank by trigger/task fit + runtime compatibility. Record: `discovered` (seen) → `considered` (evaluated) with reason. Record rejected capabilities **with reason** — this is the anti-skill-spam audit trail.

### 3. LOAD (progressive)
Metadata → `SKILL.md` body → bundled references, in that order, only as deep as the task needs. Never preload bodies for speculative use.

### 4. ACTIVATE (persistent state)
Write into task-state `capabilities[]`:
```yaml
- id: pixz.security.review
  status: active
  reason: "auth change in scope; risk=high"
  state_digest: "Checked token handling; 2 unresolved items"
  findings: [...]
  unresolved: [...]
  required_verification: ["replay window check before deploy"]
  last_verified: "2026-09-22T10:00Z"
  reactivation_conditions: ["authentication changes", "deployment changes"]
```
`state_digest` is compact — never full skill text in state.

### 5. USE + VERIFY
Follow the skill's methodology; feed findings into task-state; run the skill's `required_verification` entries when their conditions fire.

### 6. PERSIST ACROSS TRANSITIONS
A task may pass through security → architecture → implementation → testing → deployment. An activated capability's state **does not disappear** because the model moved on. Status lifecycle:
`available → discovered → considered → activated → active → suspended | reactivation_required → completed`.
- Phase change that invalidates prior results → status `reactivation_required` (re-load body only if needed).
- Capability finished and verified → `completed` (state retained, not re-activated).
- On resume/compaction: read task-state and re-establish all non-completed capabilities.

### 7. SELECT MINIMAL SET
Do not invoke every capable tool — pick the smallest set that satisfies verification. Every activation needs a reason (budget accountability).

## Outputs
`capability_map` {available[], discovered[], considered[{id, reason}], rejected[{id, why}], activated[{id, status, reason}], tools_available[]}

## Failure Conditions
- Activating a skill without a stated reason → over-activation, flag it.
- Dropping an active capability's unresolved items at a phase transition → continuity failure; restore from state.
- Preloading all skill bodies "just in case" → context waste; stop.

## Verification
- On resume, all `active`/`reactivation_required` capabilities re-established from state.
- Every activation has a reason; every rejection has a reason.
- No duplicate activation of a capability already `active`.

---
