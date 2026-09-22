# Versioning — PixzFlow

## 2.5.0 Notes (non-breaking, additive)

| Change | Detail |
|---|------|
| New skills (5) | `pixz.motion.framer-motion` v1.0.0 — Framer Motion (Motion v12) for React/Next.js: variants, layout animations, `useScroll`/`useTransform`/`useSpring`, `AnimatePresence` exits, springs vs tweens, transform/opacity-only performance, `LazyMotion` bundles, `prefers-reduced-motion`, GSAP-vs-Framer routing, browser-verified `RUNTIME-ACTIVE` evidence · `pixz.frontend.ui-ux-pro` v1.0.0 — design intelligence: product-type style direction, contrast-**computed** color roles (4.5:1/3:1 hard gates), modular type scales (max 2 typefaces), spacing/radius/shadow tokens, iconography rules, chart-type selection, a11y-first UX priority checklist, anti-slop pass; **project-adaptive** (reuses the project Design DNA before inventing anything) · `pixz.design.project-adapt` v1.0.0 — Design DNA: INVENTORY → EXTRACT (typed, evidence-backed) → PROFILE (`.pixz/design-dna.json`) → constrained GENERATE (off-DNA = approval) → DRIFT CHECK → REPORT · `pixz.core.repro` v1.0.0 — REPRO→CLASSIFY→MINIMIZE→FREEZE→FIX→VERIFY; a fix without a repro is a failure unless `NOT_REPRODUCIBLE` with attempt log · `pixz.security.commit-hygiene` v1.0.0 — pre-commit/pre-push gate: secrets BLOCK (values never echoed), manifest/lockfile diff review, stray artifacts, message↔diff consistency; PASS/WARN/BLOCK |
| Catalog 1.1.0 → 1.2.0 | +`chrome-devtools` (T1 official, Chrome DevTools team — browser + performance traces + network + console + emulation) · +`animation-inspector` (T2 — animation-system detection: CSS/GSAP/Framer/Lottie/WebGL/scroll/cursors; frame capture; core keyless) · 21 → 23 servers · `excluded_with_reason` += gsap-mcp (no npx one-liner — friction; watchlist) + Framer Motion/Motion MCP (none published) |
| New script | `scripts/vet-skill.py` (stdlib-only) — quarantine scanner for external skill bundles: injection/exfiltration/secret blockers (exit 1), consistency + budget warnings (exit 10), frontmatter structure, script inventory, `--json`. Wired into the quarantine protocol (`pixz.core.mcp`), README, mcp/README, integration smoke |
| New command | `scripts/mcp.py usage` — per-server usage report: task-state `mcp.<id>` activations vs live-check evidence vs catalog → recommendation `keep/verify/vet/suspend/check/idle` |
| Lockfile | **`pinned` channel is now real** (closes self-audit TODO #25): `resolve.py --lock pixz.lock` — non-pinned resolves WRITE/update the lock; `--channel pinned` VERIFIES every resolved version against it (`LOCK_MISMATCH` / `LOCK_MISSING_ENTRY` = hard fail, exit 1). Repo ships `pixz.lock` = version snapshot of all 35 skills |
| Orchestrator | `optional` += `pixz.core.repro` (mandatory closure stays 4 nodes; `--with-optional` 16 → 17) |
| Evals | documentary 21 → **26** (one per new skill) · behavioral 34 → **36** (`eval.behavioral.motion-react-framer` — Framer for React, GSAP excluded; `eval.behavioral.debug-flaky-repro` — repro-before-fix routing) · integration smoke += Layer 4b (vet-skill blocks injection fixture; pinned channel verifies against `pixz.lock`) |
| Counts | 30 → **35 skills** (core 15 → 16) · 21 → **23 MCP servers** (10 remote no-auth + 13 local stdio) · all living-doc counts synced |

No IDs renamed, no triggers removed, no hard `requires` added — minor bump.

## 2.4.0 Notes (non-breaking, additive)

| Change | Detail |
|---|------|
| New skill | `pixz.core.mcp` v1.0.0 — **MCP & External Capability Integration**: trust tiers (T1/T2/T3) + security vetting gate, free + no-signup-first universe, live-check-first (`initialize` + `tools/list`) before wiring, idempotent runtime-agnostic auto-config, budgeted activation, untrusted-tool-output rule, skill-import quarantine protocol |
| New catalog | `mcp/catalog.json` (21 vetted servers: 10 remote no-auth + 11 local stdio — 6 official reference + 5 design (shadcn-ui, magic-ui, better-icons, excalidraw, shadcnspace); 4 skill sources incl. mcpmarket.com free/official + skills.sh; `excluded_with_reason` for auth-required entries incl. all Figma routes) + `mcp/README.md` (human guide) |
| New script | `scripts/mcp.py` (stdlib-only): `list` · `tier` · `check` (live probe → evidence `.pixz/mcp-check.json`) · `add`/`remove` (idempotent, non-destructive; per-runtime config shapes; codex snippet) · `status` · `detect` |
| New protocol | `pixz.protocol.mcp-integration` (points at `core/mcp/SKILL.md`) |
| New policy | `pixz.policy.pixzflow-mandate` — **complex tasks MUST run under the full PixzFlow protocol; a complex task completed without it is a contractual failure (GAGAL)**, not accepted as complete until retrofitted with evidence; trivial work exempt. Canonical text: `AGENTS.md#pixzflow-mandate-complex-task-obligation` |
| Setup tiers | **Minimal / Medium / Full** — the agent MUST ask before setup (README install prompt step 1; `ZAI.md` pre-work questions; default Minimal, stated). Tiers set installation footprint (skills + MCP set), never the mandate |
| Orchestrator | `optional` += `pixz.core.mcp` (mandatory closure stays 4 nodes; `--with-optional` 15 → 16); contractual failure condition for mandate violations (2.1.0 → 2.2.0) |
| Limits | `max_skill_chain_depth` 15 → 20 (headroom: the full `--with-optional` orchestrator closure is now 16 nodes; the cap still bounds runaway chains) |
| ZAI.md | re-specified for 2.4.0: mandatory pre-work questions now cover **setup tier** (probe first, never re-ask READY) + operating mode; mandate carry-over (universal semantics — never overridden by tier/mode); stale "PixzFlow 2.0" reference fixed |
| MCP auto-config prompt | `docs/prompts/mcp-autocfg-agent.md` (standalone) + embedded as step 10 of the README install prompt |
| Evals | documentary 19 → **21** (`eval.mcp.vetting-gate`, `eval.mcp.autocfg`) · behavioral 33 → **34** (`eval.behavioral.mcp-add-free-server`) · `trivial-rename` `should_not_select` += `pixz.core.mcp` |
| Version fix | stale "PixzFlow 2.0" references in living docs fixed → 2.4 (ZAI.md header, `docs/architecture.md`, `docs/evaluation.md` incl. "now (2.1.0)" → "now (2.4.0)"); historical records (benchmark docs, final report) intentionally unchanged |

No IDs renamed, no triggers removed, no hard `requires` added — minor bump.

## 2.3.0 Notes (non-breaking, additive)

| Change | Detail |
|---|------|
| Main skill | `pixz.core.orchestrator` 2.0.0 → **2.1.0** is documented as the **MAIN practical operating skill**. Specialist skills answer HOW; the orchestrator answers WHEN/WHY/WHICH/HOW DEEPLY. |
| Progressive disclosure | Full practical operating loop lives in `core/orchestrator/references/operating-methodology.md` (loaded only for complex/high-risk work). SKILL.md body stays invocation-sized. |
| Domain skills | All 15 domain skills 1.1.0 → **1.2.0** — stubs expanded to executable methodology (when/not, steps, examples, verification, failure conditions, structured output). |
| Core skills | Remaining core skills + `anti-ai-slop` bumped (2.0.0 → 2.1.0; verification 2.1.0 → 2.2.0; self-learning 2.1.0 → 2.2.0) with a main-skill pointer and practical additions. |
| Routing copy | Every SKILL.md tells the agent: if you want more practical multi-step methodology, use `pixz.core.orchestrator`. |
| Evals | Documentary cases 18 → 19 (`eval.orchestrator.main-skill-01`). Mandatory orchestrator closure unchanged (4 nodes; budget invariant holds). |

No IDs renamed, no triggers removed, no hard `requires` added — minor bump.

## 2.2.0 Notes (non-breaking, additive)

| Change | Detail |
|---|------|
| New script | `scripts/doctor.py` — measured runtime baseline (state persistence, command execution, tools, contract reachability); `--write` fills only `unknown` dimensions; the unmeasurable (delegation, research) stays unknown |
| New script | `scripts/assess.py` — adoption score 0–100 as a sum of named evidence-backed checks (A installation 30 · B activation 35 · C operability 25 · D learning 10); UNVERIFIED items score 0; `--full` executes layer-1 + lifecycle as deeper evidence. Doctrine printed with every report: adoption score ≠ quality metric |
| Auto-run | `activation.py mark-adapted` now runs the assessment automatically at first-run completion and records it in history (never blocks the READY transition) |
| New command | `activation.py verify-installed --runtime <rt>` — installed copies vs source digests; MODIFIED → exit 10 (tamper/corruption detection) |
| New script | `scripts/sitrep.py` — one-block orientation report (adaptation probe + task state + learning highlights) for ORIENT/compaction/handoff |
| New script | `scripts/hooks.py` — runtime contract wiring: `check`/`install`, append-only and idempotent; Claude `CLAUDE.md → @AGENTS.md`, native AGENTS.md runtimes are documented no-ops; repo self-wires its own `CLAUDE.md` |
| Contracts | AGENTS.md self-learning section carries doctor/assess/sitrep/integrity/wiring; ZAI.md explicit that the overlay never overrides the lifecycle or the assessment; install prompts (README + docs/prompts) require the auto-assessment score + integrity result in the final report |
| Evals | lifecycle suite 9 → 14 deterministic tests (doctor, integrity, sitrep, assessment incl. fresh-env-low-score + auto-run, hooks idempotency) |

No skill contracts changed; no schema changes; no triggers changed — minor bump.

## 2.1.0 Notes (non-breaking, additive)

| Change | Detail |
|---|---|
| New skill | `pixz.core.self-learning` v2.1.0 (post-install activation, adaptation baseline, drift handling, improvement loop) |
| New schema | `schemas/adaptation-state.schema.json` (runtime-level self-learning state); `task-state.schema.json` gains optional `adaptation` pointer |
| New script | `scripts/activation.py` (probe/init/mark-adapted/sync/mark-installed; exit codes 0/10/1) |
| New evals | 3 documentary cases (18 total) · 10 behavioral E-series scenarios (33 total) · 9 deterministic lifecycle tests (`evals/lifecycle/`) |
| Changed skill | `pixz.core.verification` 2.0.0 → 2.1.0 (verification-depth ladder added) |
| New protocols | `pixz.protocol.self-learning` · `pixz.protocol.verification-depth` (both point at owning SKILL.md — no new truth files) |
| Policy extension | `pixz.policy.simplicity` absorbs the improvement-economy (anti-proliferation) gate |
| Orchestrator | `optional` gains `pixz.core.self-learning` — mandatory closure unchanged (4 nodes; budget invariant holds) |

No IDs renamed, no triggers removed, no hard `requires` added to existing skills — minor bump per the breaking-change rules below.

## 2.0.0 Migration Notes (breaking)

| 1.1.0 | 2.0.0 | Migration |
|-------|-------|-----------|
| `schemas/workflow.schema.json` (11-phase enum) | `schemas/task-state.schema.json` (+ `schemas/handoff.schema.json`) | Field mapping: `phase` → retired (use `status` + `plan.steps`); `completed_work`/`pending_work` → `plan.steps[].status`; `arguments[]` → `findings[]` (typed, with transitions); `evidence: [string]` → `evidence[]` (typed entries + `verified_against`); `assumptions[]` → `findings[]` with `type: assumption`; new: `capabilities[]`, `failures[]`, `delegations[]`, `next_action`, `checkpoint`, `assessment`, `mode`. |
| `profiles/super-z/PROFILE.md` | top-level `ZAI.md` | Read `ZAI.md`; content consolidated, isolation contract in `profiles/README.md`. |
| orchestrator aggregates 8 (10-node install) | aggregates 1 = `pixz.core.verification` (4-node closure) | Re-run `scripts/resolve.py`; activate other capabilities at runtime per the capability-activation protocol. |
| "PIXZ Skills" identity | "PixzFlow" operating layer | Docs/identity rename only — skill IDs unchanged. |

Skill IDs are **stable** across this migration (no renames). Skill versions bumped to 2.0.0 only where contract/methodology changed (13 core + anti-ai-slop); unchanged domain skills remain 1.1.0.

## Model

- **Repository version:** `VERSION` (SemVer, VERIFIED)
- **Skill version:** `metadata.yaml:version` (SemVer, per-skill, VERIFIED)
- **Channel:**
  - `latest` → HEAD of `main` (VERIFIED)
  - `stable` → latest tag `v*.*.*` that passed `quality-gate` (VERIFIED — resolver `--channel stable` works)
  - `pinned` → exact skill versions in a lockfile — **IMPLEMENTED (2.5.0)**: `resolve.py --channel pinned --lock pixz.lock` verifies the resolved graph against the lock (`LOCK_MISMATCH`/`LOCK_MISSING_ENTRY` = hard fail); non-pinned resolves with `--lock` write/update it. The repo ships `pixz.lock` (version snapshot of the full registry). Closes self-audit TODO #25.

## IDs

Stable: `pixz.<domain>.<name>` — never use filename as identity. `replaces` field handles renames.

## Consumer

```bash
# stable (recommended)
git clone --branch v1.0.0 https://github.com/pixzdev/skills.git
# with resolver
python scripts/resolve.py --install pixz.core.orchestrator --channel stable --runtime claude
# pinned (2.5.0) — verify against the lockfile; drift is a hard fail
python scripts/resolve.py --install pixz.core.orchestrator --channel pinned --lock pixz.lock
# (re)pin: run a stable resolve with --lock to write/update the lock
python scripts/resolve.py --install pixz.core.orchestrator --channel stable --lock pixz.lock --runtime claude
```

## Breaking Changes

Major bump for: ID rename, schema break, removed trigger, new hard `requires`, changed I/O contract. Deprecation path: `status: deprecated` + `deprecated_reason` + `replaces` for one major.

## Release Checklist

1. `schemas/*` validates
2. `scripts/validate.py` + `scripts/check-cycles.py` pass
3. `evals/runner.py` structural/documentary pass + behavioral subset pass
4. `quality-gate` + `anti-ai-slop` pass
5. Tag `vX.Y.Z`, update `VERSION`, push to origin/main
