# AGENTS.md — AI & Agents (`ai/`)

> Hierarchical registry for `ai/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.
>
> **Main skill:** specialist skills here answer HOW. For practical multi-step operating methodology, activate `pixz.core.orchestrator` (and load `core/orchestrator/references/operating-methodology.md` when the work is complex).

## Skills in `ai/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.ai.rag` | RAG Systems | `ai/rag/` | rag, retrieval |
| `pixz.ai.agent-design` | Agent Design | `ai/agent-design/` | agent design, tool calling |

## Discovery
```bash
cat ai/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.ai.rag --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `ai/*/SKILL.md` for methodology contracts and `ai/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
