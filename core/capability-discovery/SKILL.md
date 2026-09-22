---
name: Capability Discovery
description: Discovers relevant skills, agents, tools, MCP servers and libraries before selecting.
version: 1.1.0
id: pixz.core.capability-discovery
category: core
triggers: [discover, what can I use, available tools, find skill]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Capability Discovery — `pixz.core.capability-discovery`

## Purpose
“Discover first, select second, use third.” Prevents tool/skill misuse and hallucinated libraries.

## Methodology
1. **Inventory:** list eligible skills (registry), agents, tools/MCP (`list_tools`), commands (`pnpm -v`, `ls`), libraries in repo.
2. **Match:** by trigger overlap and task fit; rank by reliability, freshness, reversibility, cost.
3. **Select minimal set:** do not invoke every capable tool — pick smallest that satisfies verification.
4. **Record:** chosen vs rejected with reason; preserve for inspection.

## Outputs
`capability_map` {eligible[], selected[], rejected[{why}], tools_available[]}

---
