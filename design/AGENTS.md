# AGENTS.md — Design (`design/`)

> Hierarchical registry for `design/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.

## Skills in `design/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.design.uiux` | UI/UX Design | `design/uiux/` | ui design, ux review |
| `pixz.design.design-system` | Design System | `design/design-system/` | design system, tokens |

## Discovery
```bash
cat design/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.design.uiux --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `design/*/SKILL.md` for methodology contracts and `design/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
