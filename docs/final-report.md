# Final Report — PIXZ.DEV Universal Agent Skills Ecosystem

> Version: 1.0.0 · Date: 2026-09-21 · Branch: main · Maintainer: pixzdev <rfalixhost@gmail.com>
> Lifecycle: DEFINE → DISCOVER → RESEARCH → NORMALIZE → ARCHITECT → PLAN → IMPLEMENT → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP

---

## 1. Architecture Summary

Portable, composable, dependency-aware, versioned skill ecosystem separating **AGENT** (who) / **SKILL** (how) / **TOOL** (what) / **ORCHESTRATOR** (WHEN/WHO/WHAT/WHY) / **PROTOCOL** (how agents behave) / **POLICY** (constraints) / **EVAL** (how to measure) / **REGISTRY** (discovery).

- **Universal Core → Adapter**: vendor-neutral methodology (`SKILL.md` + `metadata.yaml` + schemas) → thin translation (`.claude/skills/`, `~/.openclaw/skills/`, `.opencode/skills/`, `hermes/skills/`). Adapters document compatibility differences but never fork methodology.
- **Governing loop**: `UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP` with complexity-aware routing (trivial → minimal, high risk×uncertainty×impact → full with challenger + quality-gate).
- **Observability**: logical workflow model (`schemas/workflow.schema.json`) — persistence runtime-specific, fields universal (objective, phase, decisions, assumptions, arguments with falsification, evidence, unknowns, verification, residual risks, iteration history).
- **Safety**: `requires`/`aggregates`/`optional`/`conflicts`, cycle detection, runtime/version gates, depth/iteration caps, change-safety tiers (reversible/partially/irreversible).

## 2. Final Taxonomy

### Mandatory (via orchestrator aggregates — 13 core)
`orchestrator`, `planning`, `context-engineering`, `environment-awareness`, `capability-discovery`, `workflow-continuity`, `delegation-handoff`, `epistemic-reasoning`, `epistemic-challenger`, `verification`, `change-safety`, `replanning`, `quality-gate` → installing orchestrator resolves 10 transitively (others optional/leaf).

### Nice-to-Have (optional aggregates: 3)
`epistemic-challenger`, `change-safety`, `anti-ai-slop` — intensive verification paths.

### Niche (curated, not persona stubs: 14)
`api-design`, `system-design`, `security review`, `threat-modeling`, `uiux`, `design-system`, `react`, `accessibility`, `gsap`, `remotion`, `docker`, `kubernetes`, `rag`, `agent-design` — each with real methodology, failure modes, verification (vs “you are a Vue expert” persona).

### Protocol (4)
Context Protocol, Workflow Propagation, Argumentation (ledger + position attribution), Escalation Ladder — see `docs/architecture.md`, `schemas/workflow.schema.json`.

### Policy (4)
Scope Control, Simplicity, Change Safety, Anti-AI Slop (diagnostic criteria, not dogmatic bans).

### Dependency (4 types)
`requires` (hard), `aggregates` (composition), `optional` (best-effort), `conflicts` (mutual exclusion) — see `docs/dependency-model.md`.

### Agent (2 defined)
`orchestrator` (meta-coordinator) + `specialist` (bounded executor). Challenger/verifier/researcher are roles using skills, not separate agent types. See `agents/`.

### Tool (tool selection as policy, not registry)
Selection by task-fit/cost/freshness/reversibility/risk; local inspection before expensive calls. Tools are MCP/bash-provided, not forked per skill.

### Eval (15 cases)
Runner `evals/runner.py` + 15 `evals/cases/*.json` validated by `schemas/eval.schema.json` — categories trigger/method/verification/scope/hallucination/output. Weighted score 1.00 (heuristic).

### Registry / Metadata (2 truths)
`AGENTS.md` (human+agent entry) + `registry.json` (machine) + hierarchical `*/AGENTS.md` (navigation). Schemas: `skill`, `registry`, `workflow`, `eval`. `VERSION` SemVer.

## 3. Skills Created (28)

**Core (13)**
- `pixz.core.orchestrator` — meta-coordination, WHEN/WHO/WHAT/WHY, mandatory aggregates
- `pixz.core.planning` — decomposing into verifiable sequenced steps
- `pixz.core.context-engineering` — acquisition order → sufficiency → preservation
- `pixz.core.environment-awareness` — inspect OS/runtime/framework/lockfile/git before assuming
- `pixz.core.capability-discovery` — discover→select→use, minimal set
- `pixz.core.workflow-continuity` — logical state + handoff + persistence abstraction
- `pixz.core.delegation-handoff` — structured dispatch & inspected return
- `pixz.core.epistemic-reasoning` — FACT/SOURCE/INFERENCE/ASSUMPTION/UNKNOWN labeling, confidence with basis, argument ledger
- `pixz.core.epistemic-challenger` — risk×uncertainty×impact-scaled intensity, seven questions, exit verdict
- `pixz.core.verification` — five checks (inspection/failure-mode/regression/consistency/impact), evidence not proof
- `pixz.core.change-safety` — reversible tiers, authority/scope gate
- `pixz.core.replanning` — escalation ladder + alternate enumeration
- `pixz.core.quality-gate` — ship/revise/replan with diminishing returns & residual unknowns

**Quality (1)**
- `pixz.quality.anti-ai-slop` — diagnostic taxonomy for design/code/research/docs; purposeful justification gate

**Engineering / Security / Design / Frontend / Motion / DevOps / AI (14)**
As listed in §2 niche.

## 4. Skills Intentionally Merged and Why

| Merged Concepts | Into | Why |
|-----------------|------|-----|
| workflow persistence + continuation + handoff + iteration state | `workflow-continuity` (+ `delegation-handoff` for dispatch) | Single lifecycle; dispatch is distinct contract |
| OS+runtime+framework+PM+repo+fs+deps+git+deploy+resource+permissions+MCP/tool | `environment-awareness` | One “inspect before assuming” prevention check |
| evidence discipline+uncertainty+assumption+confidence+argumentation+integrity+anti-confirmation | `epistemic-reasoning` | One disciplined reasoning skill; fragmentation would dilute |
| inspection+regression+consistency+impact | `verification` (evidence) + `quality-gate` (decision) | Separate gathering from ship verdict — inspect vs decide |
| tool selection+safe use+authority+scope+reversibility+simplicity | `change-safety` | Single pre-mutation gate |
| reconnaissance/web/API/auth testing (pentesting initial) | merged into `security.review` + `threat-modeling` | Responsible pentesting overlaps security review; separate skills would duplicate without distinct methodology for authorized-env scope; TODO if pentesting proves standalone |
| initiative+research+source evaluation | folded into `capability-discovery` + `context-engineering` | Research is tool use, not standalone methodology |

Avoids 30–40 micro-skills; 28 is smallest coherent that covers critical paths.

## 5. Dependencies

- Orchestrator aggregates 8 mandatory → resolver expands transitive requires to 10-node graph (stable).
- Hard edges all justified: e.g., `verification` requires `epistemic-reasoning` (needs labeling), `quality-gate` requires `verification` + `change-safety`, `kubernetes` requires `docker`.
- `optional` used sparingly (orchestrator→challenger/change-safety/anti-slop).
- `conflicts` none needed in v1 — reserved.
- Resolver flow: expand aggregates→requires→optional (compatible) → conflict check → runtime check → version check → cycle DFS → limits → topo-sort.
- Limits: `max_skill_chain_depth=15` (actual max 11), `max_orchestration_depth=6`, `max_iterations=8`.

## 6. Runtime Compatibility

All 28 skills: `compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]`

- **Claude:** progressive disclosure (`name`/`description` always visible, body on relevance, `references/`/`scripts/` on demand); frontmatter required; installed `.claude/skills/<name>/`; import via `CLAUDE.md: @AGENTS.md` (4-hop limit, <200 lines).
- **OpenClaw:** loading order workspace→project→personal→managed→workshop→bundled; `agents.entries.*.skills` allowlist is FINAL (non-merging); `openclaw skills install github:pixzdev/skills` or local copy; workshop skills per-agent.
- **OpenCode/Hermes/Codex/generic:** generic `SKILL.md` import; see `adapters/README.md` table for differences.
- Research via official docs: Anthropic Skills spec, AGENTS.md Foundation spec (Aug 2026), OpenClaw `/tools/skills` + `/tools/skills-config`.

## 7. Registry Architecture

- **Root:** `AGENTS.md` (human+agent, full trigger table, discovery workflow) + `registry.json` (machine, validated by `schemas/registry.schema.json`). `AGENTS.md` projection is generated from `registry.json` — never divergent.
- **Hierarchical:** `core/AGENTS.md`, `engineering/AGENTS.md`, etc. (9 files) — navigation only, delegate truth to root + `registry.json`. Eliminates duplicate truth.
- **Install concept:** `pixzdev/skills/AGENTS.md` canonical; `scripts/resolve.py` implements conceptual `install orchestrator → resolve aggregates → requires → conflicts → runtime → versions → cycle → install topo`.
- **Discovery:** agent scans triggers table → resolves deps → follows that skill's `SKILL.md` contract → emits structured output → verifies via `quality-gate`.

## 8. Evaluation Strategy

- **Per-skill contract:** `SKILL.md` (purpose/triggers/methodology/verification/example/structured output) + `metadata.yaml` (machine contract) per folder.
- **Central evals:** `evals/runner.py` + `schemas/eval.schema.json` + 15 cases in `evals/cases/` (trigger, method, verification, scope, hallucination, output). Checks `must_contain`/`must_not_contain`/`should_trigger` heuristically.
- **Current score:** 15/15 passing, weighted 1.00. Heuristic, not proof — real trigger accuracy needs integration harness with actual runtimes (TODO).
- **Quality rubric:** trigger accuracy, method adherence, output quality, failure handling, verification behavior, scope control, hallucination resistance, consistency.
- **CI gate:** `scripts/validate.py` (schema+registry+metadata+frontmatter) + `scripts/check-cycles.py` + `evals/runner.py` must pass.

## 9. Major Design Decisions

1. **Portable methodology over vendor prompt hack** — universal core + thin adapters; core never forks.
2. **Taxonomy normalization** — 7-criteria test for standalone skill; otherwise merge into skill or protocol. Prevents skill explosion.
3. **Orchestrator mandatory aggregates** — installing orchestrator resolves its 8 + transitive requires; correct recursion bounded by depth caps and DFS cycle detection.
4. **Protocols as docs/schemas, not skills** — context/workflow/argumentation/escalation are cross-cutting behaviors, not classes of work with HOW.
5. **Epistemic discipline separate from challenger** — reasoning builds, challenger breaks with scaled intensity and exit conditions.
6. **Anti-AI-slop diagnostic, not dogmatic** — “No effect without communicative purpose” vs “Never use gradients”.
7. **Resolver as explicit Python without external deps** — stdlib json, minimal yaml loader; portable, auditable.
8. **Evaluation as artifact, not afterthought** — harness + cases shipped with repo; skill without eval is experimental.

## 10. Risks / Limitations

- **Hallucinated runtime assumption** still possible if tool access denied — mitigated by UNKNOWN labeling + low confidence, but not eliminated.
- **Heuristic eval** may miss semantic correctness — needs LLM-judged integration runner.
- **Pentesting as security sub-skill** may under-serve users expecting dedicated recon/exploitation guidance — deliberately scoped to authorized-env, but may need split.
- **Version lockfile** concept not yet persisted — `pinned` channel accepted but not written.
- **Workflow persistence** logical-only — no concrete `.pixz/workflow.json` adapter example.
- **Token budget** grows with skill count — 28 is near comfortable limit for Claude/Claw frontmatter budget; 50+ would need pruning or lazy manifest.
- **No integration smoke tests** on actual Claude Code / OpenClaw CLIs in sandbox — relied on docs.

## 11. Self-Critique (summary of `docs/self-audit.md`)

- Assumed agents read AGENTS.md hierarchically — confirmed via spec but not integration-tested.
- Resolver optional expansion may over-install — needs `--no-optional`.
- Metadata loader fragile for complex multiline — constrained by generator to avoid.
- 54% skill-eval coverage (15/28) — need per-skill minimum.
- Dependencies minimal and audited; no redundancy found after merge pass.
- No overengineering detected after second pass (removed yaml dep, adapter forks).
- Architecture does not recurse unboundedly (caps + cycle DFS).

## 12. Self-Audit Findings

- 9 `AGENTS.md` warnings → fixed (created hierarchical registries)
- 14 generic SKILL.md placeholders → replaced with operational methodology
- 2 eval false positives (`must_not` on quoted counterexamples) → fixed
- Frontmatter progressive disclosure respected (name+description short, body loaded on relevance)
- Hierarchical registries verified to delegate truth (no duplicate `requires`)
- `validate.py` now 0 errors 0 warnings; `check-cycles` 0 cycles; `evals` 1.00

## 13. Changes Made After Self-Audit (see §12)

1. Enhanced 28 SKILL.md with real methodology.
2. Created 9 hierarchical registries.
3. Stdlib-only scripts.
4. Eval fixes.
5. Anti-slop diagnostic clarification.
6. Documented pentesting merge.

## 14. Remaining TODOs

- [ ] Machine-grade eval runner (model-judged) + ≥1 case per skill (currently 15/28)
- [ ] Lockfile writer for `pinned` channel (`pixz.lock` with SHA)
- [ ] Filesystem workflow persistence example (`examples/workflow-state.json`)
- [ ] Smoke tests for adapters (Claude/OpenClaw real install)
- [ ] `references/` deep docs for top-5 core skills (progressive disclosure tier 3)
- [ ] Optional pentesting split if usage data demands distinct methodology

---

## Quality Gate Checklist (Section 41)

**Architecture**
- [x] Agent/skill/tool/orchestrator separation clear
- [x] Protocols not unnecessarily represented as skills
- [x] Policies separated from methodologies
- [x] Dependency model coherent (`requires`/`aggregates`/`optional`/`conflicts`)
- [x] No circular dependencies (DFS + resolver)
- [x] No unnecessary fragmentation (taxonomy normalization, 28 skills)

**Registry**
- [x] Root AGENTS.md exists
- [x] Skills discoverable (trigger table + registry.json)
- [x] IDs stable (`pixz.<domain>.<name>`)
- [x] Metadata consistent (validate.py)
- [x] Dependencies machine-readable (registry.json + metadata.yaml)
- [x] Runtime compatibility explicit

**Skills**
- [x] Operational methodology (not persona)
- [x] Triggers defined
- [x] Inputs/outputs defined
- [x] Failure conditions defined
- [x] Verification defined
- [x] Niche skills meaningful (real constraints)

**Reasoning**
- [x] Evidence distinguished from inference (epistemic labels)
- [x] Assumptions tracked (fragility + ledger)
- [x] Uncertainty explicit (unknowns)
- [x] Arguments can be challenged (challenger skill)
- [x] Position changes explainable (attribution)
- [x] Confirmation bias mitigated (risk-scaled challenger)

**Workflow**
- [x] Parent workflows propagate (workflow-continuity)
- [x] Handoffs preserve relevant state (handoff contract)
- [x] Replanning supported (escalation ladder)
- [x] Stop conditions exist (quality-gate)
- [x] Escalation exists

**Safety**
- [x] Tool use deliberate (task-fit + change-safety)
- [x] Authority boundaries exist
- [x] Irreversible actions stronger scrutiny (change-safety tiers)
- [x] Secrets not exposed (no hardcoded secrets; review checklist)
- [x] Scope controlled (requested/necessary/optional/out-of-scope)

**Quality**
- [x] Anti-AI-slop exists (quality/anti-ai-slop)
- [x] Simplicity enforced (policy + gate)
- [x] Consistency checked (validate + verification)
- [x] Skill evaluations exist (evals/)
- [x] Self-audit performed (docs/self-audit.md)

**Verdict:** **SHIP** — all gates pass, residual risks & TODOs documented, diminishing returns reached. Tag `v1.0.0` ready.

---

*Build the ecosystem, not merely the prompts. — Smallest coherent system that makes agents more reliable, transparent, safe and portable.*

