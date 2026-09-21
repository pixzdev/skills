---
name: Docker & Containers
description: Reproducible container construction — layering, supply-chain and runtime verification.
version: 1.0.1
id: pixz.devops.docker
category: devops
triggers: [docker, container, dockerfile, image, layer]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Docker & Containers — `pixz.devops.docker`

## Purpose
Deterministic, minimal, verifiable images.

## Methodology
1. **Base:** pin digest (`node:20-alpine@sha256:...`), minimal variant, no latest.
2. **Layers:** order for cache (deps before code), `.dockerignore`, multi-stage for dev vs runtime.
3. **Supply:** verify base provenance, scan (`docker scout`, `trivy`), pin transitive.
4. **Runtime:** non-root user, read-only FS where possible, healthcheck, resource limits.
5. **Verify:** build reproducibility (`--no-cache` re-build equals), size budget, runtime probe, no secrets in layers (`docker history` + buildkit secret).

## Outputs
`container_report` {dockerfile ref, layers, scan results, runtime verification, residual_risks}

---
