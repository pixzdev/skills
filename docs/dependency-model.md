# Dependency Model — PIXZ Skills

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

## Example — Verified Output (v1.0.1)

```bash
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
# → 10 nodes (mandatory only)
# python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional
# → 12 nodes (+ pixz.core.epistemic-challenger + pixz.quality.anti-ai-slop)
```

**Breakdown mandatory (10):**
```
pixz.core.orchestrator
 ├── pixz.core.planning → requires pixz.core.context-engineering
 ├── pixz.core.context-engineering
 ├── pixz.core.environment-awareness
 ├── pixz.core.capability-discovery
 ├── pixz.core.workflow-continuity → requires pixz.core.context-engineering
 ├── pixz.core.epistemic-reasoning → requires pixz.core.context-engineering
 ├── pixz.core.verification → requires pixz.core.epistemic-reasoning
 └── pixz.core.quality-gate → requires pixz.core.verification, pixz.core.change-safety → requires pixz.core.environment-awareness
# count: orchestrator + planning + context + environment + capability-discovery + workflow-continuity + epistemic-reasoning + verification + quality-gate + change-safety = 10
```

**With `--with-optional` (+2):** adds `pixz.core.epistemic-challenger` (requires epistemic-reasoning) and `pixz.quality.anti-ai-slop` (requires verification) → **12**.

**Agent-design (11 mandatory):** `pixz.ai.agent-design` → requires `pixz.core.orchestrator` + `pixz.core.change-safety` → expands to same 10 + agent-design itself = **11** (12 with optional). This corrects audit finding #7 where docs incorrectly said 12 mandatory.

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
