# AGENTS.md — Security (`security/`)

> Hierarchical registry for `security/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.
>
> **Main skill:** specialist skills here answer HOW. For practical multi-step operating methodology, activate `pixz.core.orchestrator` (and load `core/orchestrator/references/operating-methodology.md` when the work is complex).

## Skills in `security/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.security.review` | Security Review | `security/review/` | security review, audit |
| `pixz.security.threat-modeling` | Threat Modeling | `security/threat-modeling/` | threat model, STRIDE |

## Discovery
```bash
cat security/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.security.review --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `security/*/SKILL.md` for methodology contracts and `security/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
