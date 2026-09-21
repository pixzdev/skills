---
name: Agent Design
description: Designs tool-enabled agents with bounded autonomy, verification and escalation.
version: 1.0.0
id: pixz.ai.agent-design
category: ai
triggers: [agent design, tool calling, orchestration, autonomous agent, tool use]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Agent Design — `pixz.ai.agent-design`

## Methodology
1. **Bound autonomy:** loop cap, tool allowlist, scope ticket, human gate for irreversible.
2. **Tool contract:** each tool has purpose, inputs/outputs, failure modes, idempotency.
3. **Orchestrate:** orchestrator determines WHEN/WHO/WHAT/WHY; agent executes HOW via skill; recursive orchestration capped.
4. **Verify & Escalate:** plan includes verification + challenger + escalation ladder retry→...→user.

---
