# Dependency Model — PixzFlow Skills

## Types — Explicit Semantics

- **requires**: hard dependency — resolver fails if missing, version-incompatible or runtime-incompatible. Transitive. **Must** be satisfied. *Observation: VERIFIED via resolver and `validate.py`.*
- **aggregates**: orchestrator composition — installing parent installs aggregates and their `requires` recursively. Aggregates are **mandatory** when parent is installed. *VERIFIED.*
- **optional**: soft — capability enhances parent; **NOT auto-installed** by default. Requires explicit `--with-optional` (or individual `--install <optional-id>`). Resolver reports them as `excluded_optional` with reason `optional_not_requested`. If `--with-optional` is used, they are resolved like `requires` (still checked for conflicts/runtime). *IMPLEMENTED as opt-in since v1.0.1; previously documented as auto but not implemented — corrected per audit finding #8.*
- **conflicts**: mutual exclusion — resolver rejects graph containing both. *VERIFIED.*

No other types without justification.

## Resolver Flow (`scripts/resolve.py` v1.0.1+)

```
install <skill-id> [--with-optional]
  → expand aggregates (recursive, mandatory)
  → expand requires (recursive, mandatory)
  → [if --with-optional] expand optional (recursive, treated as requires)
  → [else] collect optional as excluded_optional (reason: optional_not_requested)
  → check conflicts (any pair in graph → fail)
  → check runtime compatibility (skill.compatible_runtimes ∩ requested_runtime → fail if empty)
  → validate versions (SemVer; latest/stable via VERSION; pinned requires lockfile — future)
  → detect cycles (DFS; including orchestrator→skill→orchestrator)
  → enforce limits (max_skill_chain_depth, max_orchestration_depth, max_iterations)
  → return {resolved, excluded_optional, excluded_incompatible, reason, topo_sorted}
```

Fail conditions are explicit — no silent omission of hard deps. Optional omission is explicit and inspectable.

## Example — Verified Output (v2.4.0)

> **2.0.0 change:** the orchestrator's mandatory aggregates dropped from 8 to **1** (`pixz.core.verification`, the evidence floor). The other 12 capabilities are `optional` — activated **at runtime** by the capability-activation protocol, not force-installed. Evidence: GLM benchmark (B≈B1, C≈A, 1.48× trivial-task overhead) — see `docs/benchmark/GLM-benchmark-findings.md`.

```bash
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
# → 4 nodes (mandatory only = the evidence-floor chain)
# python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional
# → 16 nodes (+ all 14 on-demand capabilities)
```

**Breakdown mandatory (4):**
```
pixz.core.orchestrator
 └── pixz.core.verification (aggregate — evidence floor)
      └── pixz.core.epistemic-reasoning (requires)
           └── pixz.core.context-engineering (requires)
```

**With `--with-optional` (+12 new):** planning, environment-awareness, capability-discovery, workflow-continuity, delegation-handoff, epistemic-challenger, replanning, quality-gate, change-safety, anti-ai-slop, self-learning, mcp → **16** (epistemic-reasoning and context-engineering are already in the mandatory floor, so 12 *new* nodes).

**Agent-design:** `pixz.ai.agent-design` → requires `pixz.core.orchestrator` + `pixz.core.change-safety` (which requires `pixz.core.environment-awareness`) → 7 nodes (17 with `--with-optional`).

## Cycles

Forbidden examples detected:

- `A requires B, B requires C, C requires A`
- `orchestrator aggregates A, A requires orchestrator` (bounded recursion)

Detected via DFS with path stack; resolver exits with `CYCLE_DETECTED` and cycle path.

## Versioning / Channel

- IDs stable: `pixz.<domain>.<name>` — filename is not identity.
- Version in `metadata.yaml`; registry pins via `VERSION` + `channel`.
- `latest` → HEAD of main; `stable` → latest tag matching `v*.*.*`; `pinned` → exact SemVer in consumer lockfile — **currently documented as future**: resolver accepts `--channel pinned` but does not yet write/read `pixz.lock`. Do not claim pinned is fully implemented. See `docs/versioning.md`.
- Silent breaking change is a release violation — major bump required.

## Runtime Compatibility

Each skill declares `compatible_runtimes`. Resolver filters by target runtime:

- `claude` — progressive disclosure SKILL.md (VERIFIED)
- `openclaw` — `~/.openclaw/skills/` + allowlist (VERIFIED)
- `opencode` — `.opencode/skill/` / `~/.config/opencode/skill/` + Claude-compatible paths (VERIFIED)
- `hermes` — `~/.hermes/skills/` / `skills/` project (VERIFIED)
- `codex` / `cursor` / generic — `AGENTS.md` + generic `SKILL.md` (PARTIALLY VERIFIED — spec exists, integration smoke not automated)
- `hermes`, `opencode` etc. verified via official docs (see adapters/README.md compatibility table). Claims classified per `docs/architecture.md#runtime-portability`.

Incompatible skill in required set → hard failure with suggestion.
