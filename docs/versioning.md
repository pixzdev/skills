# Versioning — PIXZ Skills

## Strategy

- **SemVer** for ecosystem (`VERSION` file) and per-skill (`metadata.yaml:version`).
- **IDs stable** — `pixz.security.review` etc never change; renames use `replaces` field.
- **Channels:**
  - `latest` — HEAD of `main` (moving, for development)
  - `stable` — latest git tag `v*.*.*` that passed `quality-gate` (production default)
  - `pinned` — exact version in consumer lockfile (`pixz.lock` or git SHA pin) — no surprise upgrades

## Consumer Usage

```bash
# latest
git clone https://github.com/pixzdev/skills.git

# stable (recommended for production)
git clone --branch v1.0.0 https://github.com/pixzdev/skills.git

# pinned via resolver
python scripts/resolve.py --install pixz.core.orchestrator --channel stable --runtime claude
```

## Breaking Changes

- Major bump required for: ID rename, schema breaking change, removed trigger, new hard `requires`, or changed `inputs/outputs` contract.
- Deprecation path: mark `status: deprecated` + `deprecated_reason` + `replaces`, keep for one major, then remove.

## Registry Channel Resolution

`registry.json#channel` defaults to `stable`. `scripts/resolve.py --channel` overrides.

## Release Checklist

1. `schemas/*` validates
2. `scripts/validate.py` passes (metadata + registry + no cycles)
3. `evals/runner.py` sufficient score
4. `quality-gate` + `anti-ai-slop` inspection passes
5. Tag `vX.Y.Z`, update `VERSION`, push
