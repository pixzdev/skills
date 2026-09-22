---
name: Kubernetes
description: Declarative Kubernetes delivery with rollout, probes, PDBs, resource limits and rollback. Use for k8s/helm manifests. Do not force-apply. For multi-step delivery, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.devops.kubernetes
category: devops
triggers: [kubernetes, k8s, helm, deployment, pod]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Kubernetes — `pixz.devops.kubernetes`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for production rollouts (change-safety, verification, second pass).

## Purpose

Declarative delivery that can roll forward *and* back, with health signals that actually mean healthy.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Deployments, services, ingress, helm, jobs, HPA, PDB | Local Docker-only bring-up (that's `pixz.devops.docker`) |
| Changing probes, resources, rollout strategy | Editing application business logic with no manifest change |

Irreversible cluster actions need confirmation in every mode (`pixz.core.change-safety`).

## Methodology

### 1. Declare the minimum viable set

- Workload: Deployment (stateless) or StatefulSet (identity/storage).
- Service (stable DNS) + Ingress/Gateway as required.
- ConfigMap for non-secret config; Secrets via an external controller (ESO, Sealed Secrets) — not plaintext in git.
- `resources.requests` **and** `limits` (CPU/memory). No unbounded pods in shared clusters.
- Security context: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop ALL caps add back only what is needed.

### 2. Rollout

- **readiness** probe = "can take traffic". **liveness** = "restart me". Do not point both at the same expensive check. Startup probe if boot is slow.
- PDB: `minAvailable` or `maxUnavailable` so voluntary evictions don't zero the service.
- Strategy: RollingUpdate with explicit `maxUnavailable`/`maxSurge`.
- Helm: **pin chart version** and app version; `helm diff` before `upgrade`.

### 3. Safety

- `kubectl apply --dry-run=server` and `kubectl diff` before apply.
- Runbook for rollback (`rollout undo` / previous helm revision) written *before* the apply.
- No `kubectl delete` / `--force` / `--grace-period=0` without a change-safety gate and confirmation.
- Images come from `pixz.devops.docker` (digest-pinned).

### 4. Verify

- `kubectl --dry-run=server` accepted.
- `kubectl rollout status` succeeds.
- Probe actually flips: break the readiness path in staging and watch the Service endpoints drop.
- HPA: confirm metrics-server/adapter exists before adding HPA (otherwise it's fiction).
- `kubectl auth can-i` for the deploy identity.

## Failure Conditions

- Liveness on a check that fails when the app is busy → restart loop; split probes.
- No requests/limits in a noisy cluster → noisy-neighbor; add them.
- Apply without diff/dry-run on prod → process failure.

## Example

> Roll out api:2.1.0. Image digest pinned. Diff shows probe path change. Dry-run server OK. PDB maxUnavailable=1. Rollout status waits. Rollback revision N-1 documented. Verify: `/ready` 200 from a cluster-local curl Job.

## Structured Output

```yaml
k8s:
  workload: Deployment|StatefulSet
  probes: {readiness, liveness, startup}
  pdb: {...}
  resources: {requests, limits}
  image: {ref, digest}
  verify: [dry-run=server, rollout status, endpoint]
  rollback: "helm rollback … / rollout undo"
  residual_risks: [...]
```

## Main Skill

Prod delivery (image + manifest + verify + rollback) is orchestrator work. Activate `pixz.core.orchestrator`.
