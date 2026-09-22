# AGENTS.md — Frontend (`frontend/`)

> Hierarchical registry for `frontend/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.
>
> **Main skill:** specialist skills here answer HOW. For practical multi-step operating methodology, activate `pixz.core.orchestrator` (and load `core/orchestrator/references/operating-methodology.md` when the work is complex).

## Skills in `frontend/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.frontend.react` | React Engineering | `frontend/react/` | react, next.js |
| `pixz.frontend.accessibility` | Accessibility | `frontend/accessibility/` | a11y, wcag |

## Discovery
```bash
cat frontend/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.frontend.react --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `frontend/*/SKILL.md` for methodology contracts and `frontend/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
