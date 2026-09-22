---
name: Context Engineering
description: Explicit context lifecycle — discover, filter, prioritize, load, compress, pin, update, evict, restore — maximizing useful information per context token.
version: 2.1.0
id: pixz.core.context-engineering
category: core
triggers: [context, requirements, what do we know, gather context, compaction]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Context Engineering — `pixz.core.context-engineering`

> **Specialist HOW skill (context).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when the task is long-horizon (research, pin, restore).
>
> Context is a precious, lossy, expensive resource. The goal: **maximize useful information per context token** — and make everything that must survive, survive in a file.

## Purpose
Prevents hallucinated assumptions by acquiring sufficient, authoritative, fresh context before execution — and manages the context lifecycle over long tasks (compaction, drift, staleness). Distinguishes requested scope from necessary scope.

## Triggers
- Task requires project conventions, requirements, existing code, docs, or domain knowledge
- Planning, delegation handoff, handoff inspection, resume-after-compaction

Do NOT use for purely mechanical edits where context is self-contained and risk is negligible.

## Methodology

### Context Lifecycle (explicit)
```
DISCOVER → FILTER → PRIORITIZE → LOAD → COMPRESS → PIN → UPDATE → EVICT → RESTORE
```

1. **DISCOVER / FILTER / PRIORITIZE** — map available context (task state, repo, tools/MCP, docs, research); filter by relevance to objective; rank by authority + freshness.
2. **LOAD (progressive)** — acquire in priority order; stop when sufficiency is met:
   ```
   existing task state (FIRST — it is the authoritative record of this task)
     → repository / local (AGENTS.md, configs, code, tests, git state)
     → available tools / MCP (list before using)
     → documentation (repo docs first, official docs next)
     → external research (official sources first; cite primary)
     → user clarification (LAST — never ask for discoverable info)
   ```
3. **COMPRESS** — before compaction events and at phase boundaries, move what matters into task-state (decisions, findings, evidence refs, capability state, next_action). A summary keeps the shape and drops specifics — so specifics (names, flags, paths, versions) get written to state **before** compressing.
4. **PIN** — facts that must not be lost (objective, acceptance criteria, irreversible-constraint list, active assumptions) live in task-state and are re-stated on resume.
5. **UPDATE** — after mutations: stale entries get re-checked or marked. Stale-context detection: any `findings` entry older than a relevant change is suspect.
6. **EVICT** — drop working context that is neither pinned nor referenced (dead-end explorations, superseded drafts). Record one line of why if it was costly.
7. **RESTORE** — after compaction/session restart: re-inject from task-state + re-establish active capabilities; re-read only the files the current step needs (not the whole history).

### Sufficiency Check
Is context sufficient to plan and execute safely? Sufficiency = enough to produce the correct artifact with verifiable criteria, without guessing. List gaps explicitly. **Stop acquiring when sufficiency is met** — extra research beyond diminishing returns is waste.

### Authority & Freshness
`task state > repo/local primary artifacts > tools/MCP > docs > external research > user memory` — for **this task's** decisions, task state wins; for **system-state claims**, the source-of-record rule (`pixz.core.verification`) wins (actual artifacts over descriptive records). Label each fact: FACT / OBSERVED / SOURCE CLAIM / INFERENCE / ASSUMPTION / UNKNOWN / UNVERIFIED / CONTRADICTED per epistemic discipline.

## Inputs / Outputs
- **Inputs:** objective, constraints, current task state, trigger context
- **Outputs:** `context_packet` {facts[{claim, source, freshness, authority_rank}], ranked_sources[], gaps[], staleness[], sufficiency_verdict, preserved_handoff}

## Dependencies
- Requires: none (leaf)
- Optional: `pixz.core.environment-awareness` (to avoid stack hallucination during repo inspection)

## Tools
Prefer `read_file`/`bash` local reads over web search. Research only when local context is insufficient; evaluate source quality (official > maintainer > high-quality secondary).

## Failure Conditions
- Sufficiency cannot be reached (contradictory or missing authoritative source) → escalate to user with a precise question.
- All sources stale or contradicted → mark UNVERIFIED, reduce confidence; do not fabricate.
- Compaction happened and pinned specifics are missing from state → they are lost; re-acquire, don't guess.

## Verification
- Every claim in `context_packet` cites source and freshness.
- Sufficiency is checkable: would another agent with the same packet reach the same plan?
- After a compaction/resume, restore is reproducible from the state file alone.
- Handoff contains no inference presented as fact.

## Structured Output
```yaml
facts: [{claim, source, freshness, authority_rank}]
gaps: [...]
unknowns: [...]
staleness: [{claim, last_verified, risk}]
sufficiency: {verdict: sufficient|insufficient, basis}
preserved_handoff: {for_next_agent: "..."}
```

## Example
> Task: "Add OAuth to Next.js app" (resume after compaction)
> RESTORE: task-state says objective + next_action="configure provider", active capability `pixz.engineering.api-design`. RE-READ: `package.json` (next-auth present?), `auth/` folder only. SUFFICIENCY: provider credentials missing → research official docs → ask user only for credentials.

## Runtime Notes
Cross-runtime identical; adapters affect discovery paths (`CLAUDE.md` import chain vs OpenClaw workspace priority vs generic). Where the runtime offers compaction events or `/compact`-style commands, write state **before** triggering them.
