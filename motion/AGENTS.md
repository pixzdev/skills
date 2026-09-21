# AGENTS.md — Motion (`motion/`)

> Hierarchical registry for `motion/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.

## Skills in `motion/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.motion.gsap` | GSAP Motion | `motion/gsap/` | gsap, scrolltrigger |
| `pixz.motion.remotion` | Remotion | `motion/remotion/` | remotion, video |

## Discovery
```bash
cat motion/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.motion.gsap --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `motion/*/SKILL.md` for methodology contracts and `motion/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
