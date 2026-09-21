# AGENTS.md — Engineering (`engineering/`)

> Hierarchical registry for `engineering/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.

## Skills in `engineering/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.engineering.api-design` | API Design | `engineering/api-design/` | api design, openapi |
| `pixz.engineering.system-design` | System Design | `engineering/system-design/` | system design, architecture |

## Discovery
```bash
cat engineering/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.engineering.api-design --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `engineering/*/SKILL.md` for methodology contracts and `engineering/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
