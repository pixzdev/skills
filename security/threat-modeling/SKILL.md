---
name: Threat Modeling
description: Systematic threat enumeration, impact scoring and mitigation mapping — STRIDE-based.
version: 1.1.0
id: pixz.security.threat-modeling
category: security
triggers: [threat model, STRIDE, attack surface, abuse case]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Threat Modeling — `pixz.security.threat-modeling`

## Methodology
1. **DFD:** data flows + trust boundaries + entrypoints.
2. **Enumerate:** STRIDE per element (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation).
3. **Score:** impact × likelihood; prioritize.
4. **Mitigate:** control per threat, residual risk.
5. **Verify:** misuse case test.

## Outputs
`threat_model` {dfd, threats[], mitigations[], residual_risks}
---
