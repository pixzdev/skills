---
name: Context Engineering
description: Systematic acquisition, validation, sufficiency-checking and preservation of task context.
version: 1.0.0
id: pixz.core.context-engineering
category: core
triggers: [context, requirements, what do we know, gather context, context sufficiency]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Context Engineering — `pixz.core.context-engineering`

> Answers: What context do I have / need / where to obtain / which is authoritative / stale / must preserve downstream.

## Purpose
Prevents hallucinated assumptions by acquiring sufficient, authoritative, fresh context before execution and preserving it across handoffs. Distinguishes requested scope from necessary scope.

## Triggers
- Task requires understanding project conventions, requirements, existing code, docs, or domain knowledge
- Orchestrator DISCOVER phase; planning; delegation handoff; handoff inspection

Do NOT use for purely mechanical edits where context is self-contained and risk is negligible.

## Methodology

### 1. Inventory What You Have
Map available workflow state: objective, requirements, constraints, phase, decisions, assumptions, evidence, open questions, verification requirements.

### 2. Identify Gaps (Sufficiency Check)
Ask: Is context sufficient to plan and execute safely? Sufficiency = enough to produce correct artifact with verifiable criteria, without guessing. List gaps explicitly.

### 3. Acquire in Priority Order
```
existing workflow state
  → repository / local context (AGENTS.md, README, configs, code, tests, git state)
  → available tools / MCP (list before using)
  → documentation (references/ or docs/)
  → external research (official docs first; cite primary sources)
  → user clarification (LAST — never ask for discoverable info)
```
Track source and freshness per fact.

### 4. Validate & Rank Authority
- `workflow state > repo/local > tools/MCP > docs > external research > user memory`.
- Flag stale (e.g., cached docs vs live repo) and contradictory sources.
- Mark `FACT` (source confirms), `SOURCE CLAIM` (quoted claim), `INFERENCE`, `ASSUMPTION`, `UNKNOWN`, `UNVERIFIED`, `CONTRADICTED` per epistemic discipline.

### 5. Preserve for Downstream
Emit `context_packet` with: canonical facts, ranked sources, gaps/unknowns, staleness notes, and what must be carried to child agents. Store per `schemas/workflow.schema.json`.

### 6. Do Not Over-Acquire
Stop when sufficiency met. Extra research beyond diminishing returns is slop.

## Inputs / Outputs
- **Inputs:** objective, constraints, current workflow state, trigger context
- **Outputs:** `context_packet` {facts[], ranked_sources[], gaps[], staleness[], sufficiency_verdict, preserved_handoff}

## Dependencies
- Requires: none (leaf — used by orchestrator aggregates)
- Optional: environment-awareness (to avoid stack hallucination during repo inspection)

## Tools
Prefer `read_file`/`bash` local reads over web search. Research only when local context insufficient; evaluate source quality (official > maintainer > high-quality secondary).

## Failure Conditions
- Sufficiency cannot be reached (contradictory or missing authoritative source) → escalate to user with precise question.
- All sources stale or contradicted → mark UNVERIFIED and reduce confidence; do not fabricate.

## Verification
- Every claim in context_packet must cite source and freshness.
- Peer skill can verify sufficiency: would another agent with same packet reach same plan?
- Handoff contains no inferred-as-fact.

## Structured Output
```yaml
facts: [{claim, source, freshness, authority_rank}]
gaps: [ ... ]
unknowns: [ ... ]
staleness: [{claim, last_verified, risk}]
sufficiency: {verdict: sufficient|insufficient, basis}
preserved_handoff: {for_next_agent: ...}
```

## Example
> Task: “Add OAuth to Next.js app”
> Acquire: workflow state (no prior), AGENTS.md (conventions), `package.json` (next-auth present?), `.env.example`, `auth/` folder, tool list (MCP auth). Discover gap: provider config missing → research official next-auth docs → ask user only for provider credentials.

## Runtime Notes
Cross-runtime identical; adapters affect discovery paths (`CLAUDE.md` import chain vs OpenClaw workspace priority vs generic).
