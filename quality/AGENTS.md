# AGENTS.md — Quality (`quality/`)

> Hierarchical registry for `quality/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.
>
> **Main skill:** specialist skills here answer HOW. For practical multi-step operating methodology, activate `pixz.core.orchestrator` (and load `core/orchestrator/references/operating-methodology.md` when the work is complex).

## Skills in `quality/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.quality.anti-ai-slop` | Anti-AI Slop | `quality/anti-ai-slop/` | anti slop, boilerplate |

## Discovery
```bash
cat quality/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.quality.anti-ai-slop --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `quality/*/SKILL.md` for methodology contracts and `quality/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
