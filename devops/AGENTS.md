# AGENTS.md — DevOps (`devops/`)

> Hierarchical registry for `devops/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.
>
> **Main skill:** specialist skills here answer HOW. For practical multi-step operating methodology, activate `pixz.core.orchestrator` (and load `core/orchestrator/references/operating-methodology.md` when the work is complex).

## Skills in `devops/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.devops.docker` | Docker & Containers | `devops/docker/` | docker, container |
| `pixz.devops.kubernetes` | Kubernetes | `devops/kubernetes/` | k8s, helm |

## Discovery
```bash
cat devops/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.devops.docker --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `devops/*/SKILL.md` for methodology contracts and `devops/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
