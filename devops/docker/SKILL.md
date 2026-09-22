---
name: Docker & Containers
description: Reproducible container construction — digest-pinned bases, multi-stage builds, non-root runtime, supply-chain and runtime verification. Use for images and Dockerfiles. Never unpinned latest tags. For rollout work, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.devops.docker
category: devops
triggers: [docker, container, dockerfile, image]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Docker & Containers — `pixz.devops.docker`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for image → registry → deploy work.

## Purpose

Deterministic, minimal, verifiable images.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Writing/reviewing Dockerfiles, compose files, image hardening | "Run this script on my laptop" with no container need |
| CI image build | Kubernetes rollout details (that's `pixz.devops.kubernetes`) |

## Methodology

### 1. Base

Pin digest (`node:20-alpine@sha256:...`), minimal variant. Never unpinned floating tags. Re-pin deliberately when you intend to move.

### 2. Layers (cache + leak control)

- Order for cache: package manifests → install → source → build.
- `.dockerignore` must exclude `.git`, secrets, `node_modules`, `.env*`.
- **multi-stage**: builder has compilers/devDeps; runtime copies only the artifact.
- Secrets: BuildKit `--secret` / mount; never `ENV AWS_SECRET=` or `COPY .env`.

### 3. Supply chain

- Verify base provenance when the org requires it.
- Scan (`trivy`, `docker scout`) and treat CRITICAL/HIGH as findings, not wallpaper.
- Pin lockfiles into the image (`pnpm-lock.yaml` etc.) so installs are reproducible.

### 4. Runtime

- **non-root** user (`USER` after `adduser`).
- Read-only root FS where the app allows (`--read-only` + tmpfs).
- `HEALTHCHECK` that hits a real readiness path, not `true`.
- Resource limits at run/orchestrator layer.
- Drop capabilities; no `--privileged` without a recorded exception.

### 5. Pattern (Node example — adapt to the real stack)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine@sha256:<digest> AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile --prod=false

FROM deps AS build
COPY . .
RUN pnpm build

FROM node:20-alpine@sha256:<digest> AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S app && adduser -S app -G app
COPY --from=build --chown=app:app /app/dist ./dist
COPY --from=deps  --chown=app:app /app/node_modules ./node_modules
USER app
EXPOSE 3000
HEALTHCHECK CMD wget -qO- http://127.0.0.1:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

Inspect lockfiles before choosing `pnpm` vs others (`pixz.core.environment-awareness`).

### 6. Verify

- Rebuild reproducibility (`docker build --no-cache` twice → same meaningful layers / digest intent).
- Size budget vs previous image.
- Runtime probe as the **non-root** user.
- `docker history` / `docker scout` / `trivy`: no secrets in layers.
- `docker run --read-only` smoke if claimed.

## Outputs

`container_report` {dockerfile ref, layers, scan results, runtime verification, residual_risks}

## Failure Conditions

- Unpinned floating tags → blocked.
- Root runtime without exception → blocked.
- Secrets in layers → blocked; rebuild with secret mounts.

## Example

> Node API image. Multi-stage, digest-pinned alpine, `USER app`, healthcheck on `/health`, trivy HIGH=0. Verify: `docker run --user 1001` still serves; `docker history` shows no `.env`.

## Main Skill

Image + scan + registry + k8s rollout is orchestrator work. Activate `pixz.core.orchestrator`.
