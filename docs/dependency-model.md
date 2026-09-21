# Dependency Model — PIXZ Skills

## Types

- **requires**: hard dependency — resolver fails if missing, version-incompatible or runtime-incompatible. Transitive.
- **aggregates**: orchestrator composition — installing parent installs aggregates and their `requires` recursively.
- **optional**: soft — capability enhances parent; install if available/compatible.
- **conflicts**: mutual exclusion — resolver rejects graph containing both.

No other types without justification.

## Resolver Flow (`scripts/resolve.py`)

```
install <skill-id>
  → expand aggregates (recursive)
  → expand requires (recursive)
  → add optional if present & compatible & non-conflicting
  → check conflicts (any pair in graph → fail)
  → check runtime compatibility (skill.compatible_runtimes ∩ requested_runtime → fail if empty)
  → validate versions (SemVer satisfies pin; latest/stable resolved via VERSION)
  → detect cycles (DFS; including orchestrator→skill→orchestrator)
  → enforce limits (max_skill_chain_depth, max_orchestration_depth, max_iterations)
  → install complete graph (topologically sorted)
```

Fail conditions are explicit — no silent omission of hard deps.

## Example

```
install pixz.core.orchestrator
  aggregates: planning, context-engineering, environment-awareness, capability-discovery,
              workflow-continuity, epistemic-reasoning, verification, quality-gate
  → planning requires context-engineering (already in graph)
  → workflow-continuity requires context-engineering
  → verification requires epistemic-reasoning
  → quality-gate requires verification, change-safety
  → final graph: 12 nodes, 0 conflicts, 0 cycles
```

## Cycles

Forbidden examples detected:

- `A requires B, B requires C, C requires A`
- `orchestrator aggregates A, A requires orchestrator` (bounded recursion)

Detected via DFS with path stack; resolver exits with `CYCLE_DETECTED` and cycle path.

## Versioning

- IDs stable: `pixz.<domain>.<name>` — filename is not identity.
- Version in `metadata.yaml`; registry pins via `VERSION` + `channel`.
- `latest` → HEAD of main; `stable` → latest tag matching `v*.*.*`; `pinned` → exact SemVer in consumer lockfile.
- Silent breaking change is a release violation — major bump required.

## Runtime Compatibility

Each skill declares `compatible_runtimes`. Resolver filters by target runtime:

- `claude` — progressive disclosure SKILL.md
- `openclaw` — `~/.openclaw/skills/` + allowlist
- `opencode` / `hermes` / `codex` / `generic` — via adapter translation

Incompatible skill in required set → hard failure with suggestion.
