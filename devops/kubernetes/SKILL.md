---
name: Kubernetes
description: Declarative Kubernetes delivery with rollout, health-check and failure-mode discipline.
version: 1.0.1
id: pixz.devops.kubernetes
category: devops
triggers: [kubernetes, k8s, helm, deployment, pod, rollout]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Kubernetes — `pixz.devops.kubernetes`

## Methodology
1. **Declare:** Deployment/StatefulSet + Service + Ingress/GR, ConfigMap/Secret (external secrets), resource requests/limits.
2. **Rollout:** readiness+liveness, PDB, rolling strategy, helm chart pinned version.
3. **Safety:** apply --dry-run, diff, runbook for rollback; no kubectl --force without gate.
4. **Verify:** `kubectl --dry-run=server`, rollout status, probe success, HPA budget.

---
