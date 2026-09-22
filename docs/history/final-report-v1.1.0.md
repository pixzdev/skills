# Final Report — PIXZ.DEV Universal Agent Skills Ecosystem (v1.1.0)

> Version: 1.1.0 · Date: 2026-09-22 · Branch: `arena/01a0c6a2-skills` (branched from `main` @ `20fd94d`)
> Mission: Frontier Reconstruction & Refinement — repository archaeology, capability-model reconstruction, Super Z / GLM / Z.AI Web profile, README agent bootstrap, adversarial self-audit.
> Prior report: `docs/history/final-report-v1.0.0.md` · Repair history: `docs/repair-report.md`
> Classification labels used below: **OBSERVED** (traced in source/execution this session) · **SPECIFIED** (stated in spec/config, not independently re-verified) · **INFERRED** (reasonable conclusion from evidence) · **UNKNOWN** (no evidence)

---

## 1. Repository state discovered

**OBSERVED** (all verified by execution in this session, 2026-09-22):

- 28 skills in 9 domains (`core` 13, `quality` 1, `engineering` 2, `security` 2, `design` 2, `frontend` 2, `motion` 2, `devops` 2, `ai` 2), each `SKILL.md` + `metadata.yaml`.
- `registry.json` = machine source of truth (28 entries, limits `chain=15 / orchestration=6 / iterations=8`, channel `stable`); `AGENTS.md` = human/agent projection; `*/AGENTS.md` = navigation.
- Pre-change state passed: `validate.py` 0 errors / 0 warnings; `check-cycles.py` 0 cycles; `evals/runner.py` 15/15 (heuristic); `evals/behavioral/runner.py` 15/15 (heuristic smoke); resolver resolved 10 nodes mandatory / 12 with `--with-optional` for `pixz.core.orchestrator`.
- Adapters: `claude`, `openclaw`, `opencode`, `hermes` (each `AGENT.md` + `install.sh`); `install.sh` only ran the resolver and printed a pointer — it does **not** copy files (SPECIFIED in README as "adapter = thin translation"; copy steps are documented manually in `docs/install/README.md`).
- 4 verification layers implemented as documented (structural / documentary / behavioral / integration).
- No Super Z / GLM / Z.AI Web concept existed anywhere (`grep` over full tree: zero word-boundary matches). **OBSERVED absence.**
- README pointed to prompt docs (`docs/install-as-skill.md`, `docs/prompts/install-skill-agent.md`) but contained **no inline copy-paste prompt**. **OBSERVED absence.**

## 2. Architecture reconstructed

- **Orchestrator** (`pixz.core.orchestrator`): meta-skill; aggregates 8 mandatory skills (→ 10 nodes with transitive `requires`), 2 optional (`epistemic-challenger`, `anti-ai-slop`, opt-in). Determines WHEN/WHO/WHAT/WHY.
- **Skills** (28): HOW — universal methodology, runtime-agnostic, frontmatter `name`/`description` for progressive disclosure.
- **Agents** (`agents/orchestrator.yaml`, `agents/specialist.yaml`): role definitions (meta-coordinator, bounded executor) with handoff contracts.
- **Protocols** (4): context acquisition order, workflow propagation, argumentation (claim lifecycle), escalation ladder.
- **Policies** (5): scope control, simplicity, change-safety tiers (reversible/partially/irreversible), anti-AI-slop (diagnostic), REINITIATE (restart-from-DEFINE control-flow policy, not a state).
- **Infra**: `scripts/resolve.py` (deterministic, cycle-DFS, runtime gates, depth caps), `scripts/validate.py` (layer 1), `scripts/check-cycles.py`, `scripts/integration-smoke.sh` (layer 4), `schemas/` (skill/registry/workflow/eval, JSON Schema draft-07), `evals/` (layer 2 + 3).
- **Workflow state**: `schemas/workflow.schema.json` — 11 machine states; methodological `NORMALIZE`/`ARCHITECT`→`PLAN`, `IMPLEMENT`→`EXECUTE`; `REINITIATE` = policy.
- **New (this mission)**: `profiles/` — isolated runtime overlays (class PROFILE). Not skills: no ID, not in registry, not resolver-managed; only parameterize orchestrator depth + runtime compute/interaction policy; skills win on conflict.

## 3. Important inconsistencies found

| ID | Class | Finding | Evidence |
|----|-------|---------|----------|
| G-1 | gap | Super Z / GLM / Z.AI Web profile (mission §19) absent | full-tree grep, zero matches |
| G-2 | gap | README lacked inline copy-paste agent install prompt + Super Z prompt (mission §20) | README inspection |
| D-1 | doc/code drift | **28/28** SKILL.md frontmatter `compatible_runtimes` = `[claude, openclaw, opencode, hermes]` vs registry 6 (missing `codex`, `generic`) | scripted cross-check |
| D-2 | doc/code drift | **20/28** frontmatter `triggers` were supersets of registry triggers (e.g. orchestrator had `route work` only in frontmatter) | scripted cross-check |
| D-3 | doc drift | README + AGENTS.md claimed "layer 3 (4 scenarios)"; actual = 15 | runner output `15/15` |
| D-4 | doc drift | `adapters/README.md` listed `claude/SKILL_TEMPLATE.md` — file absent | `find` |
| D-5 | defect | `adapters/*/install.sh` used relative `scripts/resolve.py` → broke when run from `adapters/<rt>/` | traced + reproduced |
| D-6 | doc drift | orchestrator SKILL.md loop string = 13 stages (ROUTE/DELEGATE/COORDINATE/RE-EXECUTE) vs canonical 11-phase loop + 11-state enum; mapping undocumented | diff vs `docs/architecture.md` |
| D-7 | doc drift | adapters/README install paths diverged from verified matrix (OpenCode `.opencode/skills/`, Hermes `hermes/skills/`) | diff vs `docs/install/README.md` |
| D-8 | config drift | `agents/orchestrator.yaml` `max_skill_chain_depth: 12` vs registry `15`; agent yamls 4 runtimes vs 6 | file diff |
| V-1 | weakness | `validate.py` never cross-checked SKILL.md frontmatter vs registry → D-1/D-2 invisible | source read |
| V-2 | weakness | no machine check for README prompt sections / profile presence | source read |

**Not found** (checked): registry↔metadata drift (none), cycles (none), version mismatches pre-bump (none), fake resolver features (none — `pinned` honestly documented as future), duplicate skill concepts (none beyond documented merges in `docs/taxonomy.md`).

## 4. Changes implemented

1. `profiles/README.md` (new) — profile isolation contract; taxonomy justification (PROFILE, not SKILL); extension rules.
2. `profiles/super-z/PROFILE.md` (new) — Super Z / GLM / Z.AI Web operating contract (§5 below).
3. `README.md` — inline **AI Agent Installation Prompt** (runtime-agnostic: IDENTIFY RUNTIME → INSPECT ENVIRONMENT → LOCATE SKILLS → DISCOVER INSTALLATION METHOD → RESOLVE DEPENDENCIES → INSTALL → VERIFY → REPORT; official mechanisms only; config preserved; no success without evidence) + separate **Super Z / GLM / Z.AI Web Prompt**; full-ecosystem install line (`npx skills add pixzdev/skills`); **Runtime Profiles** section; scenario count 4→15; version 1.0.1→1.1.0.
4. `scripts/validate.py` — new: SKILL.md frontmatter cross-check (`id`/`version`/`triggers`/`compatible_runtimes` vs registry, hard error); profile presence + required-section checks; README prompt-section checks.
5. All 28 SKILL.md frontmatters synced to registry (D-1/D-2); orchestrator SKILL.md loop aligned to canonical 11 phases with explicit substep mapping (D-6) + one-line profile pointer in Runtime Notes.
6. `AGENTS.md` — Runtime Profiles section; frontmatter contract documented; scenario count 4→15; prompt pointers; version 1.1.0.
7. `llms.txt` — version 1.1.0; profiles line; README prompt mention.
8. `adapters/README.md` — stale `SKILL_TEMPLATE.md` removed (D-4); OpenCode/Hermes install paths aligned to verified matrix (D-7).
9. `adapters/*/install.sh` ×4 — repo-root resolution from script location (D-5); regression-tested from `adapters/claude/`.
10. `agents/orchestrator.yaml` / `agents/specialist.yaml` — runtimes → 6; `max_skill_chain_depth` 12→15 (D-8).
11. `docs/evaluation.md` — layer 1 list updated (frontmatter + profile/README contracts).
12. `docs/self-audit.md` — v1.1.0 audit section (findings table + anti-confirmation check).
13. Version bump 1.0.1 → 1.1.0 across `VERSION`, `registry.json` (1+28), 28 `metadata.yaml`, 28 SKILL.md, `scripts/resolve.py`, current-state doc references. Historical reports (repair-report, anti-slop-audit, v1.0.0 final report) **not** rewritten.
14. `docs/final-report.md` → archived as `docs/history/final-report-v1.0.0.md` (git mv).

## 5. Skills added / removed / consolidated

- **Added: 0. Removed: 0. Consolidated: 0.** Total stays **28**.
- The Super Z profile was **deliberately not made a skill**: it fails the 7 standalone-skill criteria as a universal capability (no universal methodology, no runtime-neutral invocation), and the taxonomy + mission §19/§18 require runtime-specific behavior to stay isolated from universal design. It is a PROFILE (restricted POLICY), machine-checked but registry-free. **INFERRED** correct under `docs/taxonomy.md`; **SPECIFIED** by mission.

## 6. Dependency changes

- **None.** `requires`/`aggregates`/`optional`/`conflicts` graph unchanged; cycle check re-run clean (0 cycles); resolver re-verified: 10 nodes mandatory, 12 with `--with-optional`, all 6 runtimes (`claude`, `openclaw`, `opencode`, `hermes`, `codex`, `generic`). Mission §24: preserve working behavior — the graph was already correct.
- `compatible_runtimes` data unchanged (still 6 per skill). **No `zai`/`glm` runtime added** — that would claim unverified runtime compatibility; the profile covers Super Z via the generic adapter path instead (honesty per §7/§23).

## 7. Runtime adapter changes

- `install.sh` ×4: path robustness only (D-5). Semantics unchanged (resolve + pointer).
- `adapters/README.md`: removed reference to non-existent file (D-4); OpenCode canonical singular `.opencode/skill/` + Hermes `~/.hermes/skills/` global / `skills/` project aligned with the verified matrix (D-7).
- No new adapter for Z.AI / GLM: **UNKNOWN** — no verified install/discovery mechanism exists for it; the profile is a runtime-level overlay, not an install claim. Adding an unverified adapter would violate §23 (documentation as executable contract).

## 8. AGENTS.md changes

- New "Runtime Profiles (isolated — not skills)" section: class, current profile, epistemic status, machine check, README entry points.
- Validation section now states what `validate.py` checks (frontmatter consistency + contracts).
- Frontmatter convention: `id`/`version`/`triggers`/`compatible_runtimes` must equal registry (hard error).
- "4 scenarios" → "15 scenarios"; version line → 1.1.0; install section now lists the inline README prompts first.

## 9. README.md changes

- **AI Agent Installation Prompt** (inline, copy-paste, runtime-agnostic; uses repo's official installer/resolver; preserves user config; evidence-based verification + structured report; no invented formats).
- **Super Z / GLM / Z.AI Web Prompt** (inline, copy-paste: recognize → AskUserQuestion mode selection (default BALANCED) → discover/install/verify → mode behavior → compute policy → never-override list).
- Full-ecosystem install line; Runtime Profiles section; scenario count fix; version 1.1.0; repo-structure tree updated (`profiles/`, adapter note).

## 10. Super Z / GLM profile changes

- **New** `profiles/super-z/PROFILE.md`:
  - Identification: applies only when the agent self-identifies as Super Z / GLM / Z.AI Web from observable identity signals; otherwise inapplicable.
  - **Mandatory** `AskUserQuestion` mode selection before substantive work: FAST / BALANCED / DEEP / AUTONOMOUS; **default BALANCED**; graceful degradation (states + proceeds at BALANCED) when the capability is absent.
  - Mode semantics mapped onto the existing depth axis (MINIMAL→DEEP VERIFICATION): target depth is an upper tendency, never minimum ceremony — trivial tasks still route minimal.
  - Compute policy (DEEP/AUTONOMOUS): exploit generous compute **only when it materially improves the task** (discover skills before implementation, complementary multi-skill use with stated reasons, rich structured handoffs, parallel independent investigations, independent verification, risk-scaled challenge, evidence preservation, iterate while EV positive).
  - Never-list: auto-invoke all skills; subagents without independent responsibility; researching trivial facts; ceremony for trivial changes; continuing past justified stop.
  - Principle: *maximum useful intelligence, not maximum activity*.
  - Never-overrides: skill semantics, dependency resolution, change-safety confirmations, verification layers, honest reporting.
- **New** `profiles/README.md`: isolation contract (5 rules), profile table, machine check, extension rules.
- Wiring: README prompts, AGENTS.md section, llms.txt line, one-line pointer in orchestrator Runtime Notes.

## 11. Installation prompt

- Location: `README.md` (inline blocks) — the copy-paste surface for agents.
- Flow enforced: `IDENTIFY RUNTIME → INSPECT ENVIRONMENT → LOCATE SKILLS → DISCOVER INSTALLATION METHOD (docs/install/README.md matrix + adapters/) → RESOLVE DEPENDENCIES (scripts/resolve.py) → INSTALL (exactly one official mechanism; clone ≠ install) → VERIFY (discovery output, installed path) → REPORT (structured, no fabrication)`.
- Guarantees: no single runtime hard-coded; official installer/resolver preferred; existing user configuration never overwritten (same-name skill → stop + report); no success claim without step 7 evidence; honest FAILED acceptable.
- Full runtime-adaptive version remains at `docs/prompts/install-skill-agent.md` (unchanged); short version at `docs/install-as-skill.md` (unchanged).

## 12. Verification performed (all executed this session)

| Check | Result |
|-------|--------|
| `python3 scripts/validate.py` (incl. new frontmatter + profile/README contract checks) | **PASS — 0 errors, 0 warnings, 28 skills, v1.1.0** |
| `python3 scripts/check-cycles.py` | **PASS — 0 cycles, limits 15/6/8** |
| `python3 evals/runner.py` (layer 2, 15 cases) | **PASS 15/15** (heuristic, disclosed) |
| `python3 evals/behavioral/runner.py` (layer 3, 15 scenarios) | **PASS 15/15** (heuristic smoke, disclosed) |
| Resolver: orchestrator @ claude / generic / openclaw / opencode / hermes / codex | **PASS — 10 nodes each** |
| Resolver: `--with-optional` | **PASS — 12 nodes** |
| Resolver: `pixz.ai.agent-design` (transitive orchestrator dep) | **PASS — 11 nodes** |
| `adapters/claude/install.sh` from `adapters/claude/` (D-5 regression) | **PASS** |
| **Negative tests (validator is real, not documentary):** injected frontmatter trigger drift → hard error + exit 1; deleted profile → error; removed README prompt sections → errors; all restored → exit 0 | **PASS** |

## 13. Evaluation performed

- Layer 2 (documentary) and layer 3 (behavioral smoke) re-run after changes: **15/15 + 15/15** — confirms no regression from frontmatter sync, loop rewrite, or doc changes.
- The new Super Z profile is **not** covered by behavioral evaluation (none exists that can judge profile-driven depth selection without a model grader). It is covered by **structural** checks only (presence + required sections).
- No new eval cases were added to `evals/cases/`: that harness is keyed by registry `skill_id`; a profile is not a skill, so forcing it there would misrepresent the eval layer (see `docs/evaluation.md`).

## 14. Tests that remain documentary-only

- **All 15 layer-2 cases** — keyword/section presence heuristics; they prove documentation shape, not behavior.
- **All 15 layer-3 scenarios** — heuristic keyword-overlap router simulation; disclosed as smoke, not model-graded.
- **`scripts/integration-smoke.sh`** (layer 4) — where runtime CLIs are absent (this sandbox: no `openclaw`/`hermes`/`claude` binaries; `npx skills` not exercised), it captures skip evidence and marks PARTIALLY VERIFIED. **OBSERVED** in prior sessions per its own docs; not re-run end-to-end against live runtimes this session.
- **New profile checks** — documentary (section presence), by design; behavioral effect is UNVERIFIED.

## 15. Known limitations

- `pinned` channel: **DOCUMENTED ONLY** (no `pixz.lock`) — unchanged from v1.0.1.
- Behavioral eval: heuristic smoke; no LLM-judged trigger accuracy (standing TODO).
- Generic runtime (Codex/Cursor): PARTIALLY VERIFIED (spec + manual only).
- Super Z / GLM / Z.AI Web profile: **SPECIFIED, behaviorally UNVERIFIED** — no evaluation demonstrates an agent operating differently/better under it.
- Z.AI / GLM has no verified install/discovery mechanism in `docs/install/README.md` — not claimed.
- Eval coverage: 15 of 28 skills have a dedicated layer-2 case (~54%); standing TODO.
- `adapters/*/install.sh` resolve-only by design; actual copy is documented manual steps (SPECIFIED behavior, unchanged).

## 16. Remaining unknowns

- **UNKNOWN**: actual discovery/invocation behavior of the Super Z / GLM / Z.AI Web runtime (this session ran in a different runtime; the profile's identification signals are SPECIFIED, not tested).
- **UNKNOWN**: whether `AskUserQuestion` is present in the real Super Z / GLM / Z.AI Web runtime (profile degrades to BALANCED default if absent — SPECIFIED behavior).
- **UNKNOWN**: live skills.sh `npx skills` end-to-end on this repo state (not executed this session).
- **UNKNOWN**: whether the runtime frontmatter `triggers` list (now registry-equal) affects any runtime's description matching (INFERRED: runtimes index `name`/`description`; the `triggers` key is a repo-local aid).

## 17. Risks

- **Low**: frontmatter sync changed what some runtimes see in frontmatter `triggers` (20/28 were supersets). Risk: a runtime that indexes `triggers` (none known to) would match fewer keywords. Mitigation: registry values are the declared truth; description fields unchanged; layer 1+2 pass.
- **Low**: README inline prompts duplicate (condensed) content in `docs/prompts/install-skill-agent.md` — divergence risk over time. Mitigation: README block is explicitly the condensed surface; full doc remains canonical for details; validate.py pins the section presence.
- **Medium**: profile is unverified behaviorally — an agent could follow it performatively without the intended depth/compute discipline. Mitigation: isolation contract + explicit UNVERIFIED label + next-iteration behavioral eval (below).
- **Low**: version bump requires consumers on `stable` to re-resolve; no breaking ID/schema/graph changes, so SemVer-minor is safe.

## 18. Recommended next iteration

1. **Behavioral evaluation for the Super Z profile** (highest value): LLM-judged scenarios comparing an agent with vs. without the profile under DEEP/AUTONOMOUS — does it actually use more complementary skills, richer handoffs, independent verification, and stop at justified conditions? Until then the profile stays labeled UNVERIFIED.
2. **Lockfile writer/reader for `pinned`** (long-standing TODO; unblocks reproducible installs).
3. **LLM-judged layer 3** (machine-grade trigger accuracy) to replace the keyword heuristic.
4. **Per-skill layer-2 coverage to 28/28** (remotion, kubernetes, etc. lack dedicated cases).
5. **Live integration in CI** for at least one runtime (skills.sh `npx skills` end-to-end) to move layer 4 from "where CLI available" to scheduled.
6. **Z.AI / GLM install verification**: obtain the runtime, run the actual discovery/invocation, then (and only then) add a real adapter row to `docs/install/README.md` — do not pre-claim.
7. Filesystem workflow persistence example (`.pixz/workflow.json`) — standing TODO.

---

### Ship verdict (per §26 quality gate)

| Gate | Status |
|------|--------|
| Requirements satisfied (mission §19 profile, §20/§21 README prompts, §22 integrity, §23 doc-as-contract) | ✅ |
| Architecture coherent (orchestrator/skill/agent/tool/policy/protocol/infra/profile separation intact) | ✅ |
| Implementation verified (layers 1–3 executed; negative tests prove new checks) | ✅ |
| Documentation synchronized (drift D-1…D-8 fixed; validator prevents recurrence) | ✅ |
| Runtime compatibility verified | ✅ where previously VERIFIED; Z.AI explicitly NOT claimed |
| Dependency graph valid (0 cycles, caps, runtime gates re-run) | ✅ |
| Evaluation passes (15/15 + 15/15) | ✅ (heuristic, disclosed) |
| Known limitations disclosed (§15) | ✅ |
| Residual risk acceptable (§17) | ✅ |

**SHIP v1.1.0** — with the disclosed limitations and the next-iteration list above.

*The system moves an agent from "I have a task" to "I know what I need, what I can use, what I selected and why, what I verified, and what remains uncertain — and I know when to stop." That is now also true for Super Z / GLM / Z.AI Web, with a mode the user controls.*
