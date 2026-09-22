# PixzFlow 2.0.0 — Final Engineering Report (2026-09-22)

> Mission: reconstruct PixzFlow as a persistent, adaptive, model-agnostic operating layer — research first, model second, design third, implement fourth, measure fifth. Optimize for **observable agent performance**, not the appearance of intelligence.

## Executive Summary

PixzFlow was reconstructed from "a skills repository with an 11-phase workflow" into a **benchmark-driven adaptive operating layer**: an entry protocol with qualitative assessment, four behavioral operating modes, a persistent capability-activation protocol, a compact task-state + typed-evidence substrate, a formal source-of-record protocol, an intensity-scaled challenger with a binding stop rule, an economics-gated delegation contract, and a formal failure-recovery ladder. The orchestrator's mandatory install closure dropped from 10 nodes to 4 (the evidence floor). Everything is validated, documented, and honestly classified; nothing is claimed that is not backed by evidence.

## Research Findings (Phase Zero — `docs/research/frontier-agent-findings.md`)

Frontier-agent patterns identified (classified DOCUMENTED/OBSERVED/REPORTED/INFERRED/HYPOTHESIS):

1. **Instruction files are context-budgeted**: Codex truncates AGENTS.md at 32 KiB; recommended practice is <150 lines, command-first, closure-defined, no README duplication. → AGENTS.md rewritten as a high-signal contract; the 28-row table moved to `llms.txt`.
2. **Progressive disclosure is the skill mechanism** (Anthropic, documented): metadata at startup (~50–100 tokens/skill), body on relevance, references on demand; Claude Code re-injects invoked skill bodies after compaction (capped). → Activation protocol is progressive and tracks activation *state*.
3. **Subagents are context isolation + summary return** (Claude Code, Gemini CLI documented); Gemini CLI enforces no-sub-subagents. → Delegation contract + recursion prohibition.
4. **Handoffs transfer control and require explicit criteria + structured returns + guardrails** (OpenAI Agents SDK documented). → `schemas/handoff.schema.json` with mandatory return fields + parent inspection.
5. **Compaction silently destroys conversation** (Claude Code documented; community observed): system prompt, plans, CLAUDE.md, skills re-inject from disk; rejected approaches vanish. → Task state is a **file**; pinned specifics written before compaction.
6. **Context engineering** (Anthropic documented): compaction, structured note-taking, sub-agents; treat context as precious; just-in-time retrieval. → Context lifecycle DISCOVER→…→RESTORE with PIN/RESTORE.
7. **Long-horizon research**: horizon-dependent degradation (HORIZON); failures cluster early; plan injection + interactive guidance beat self-correction alone (LongCLI-Bench); structured verification feedback enables ~70% test-time recovery (LH-Bench); state-as-log (PRO-LONG); goal drift across sessions (YC-Bench); external > intrinsic correction (CorrectBench). → Stateful/resumable design, verification as continuous loop, formal recovery ladder, drift counters (objective restatement, decision marking).

We studied observable architecture and behavior — no claims about private model internals.

## Benchmark Findings (record: `docs/benchmark/GLM-benchmark-findings.md`)

- 52/52 objective acceptance in **both** conditions → correctness ceiling; **no correctness-claim made**.
- Blind grading: native ≈ 4.77 vs Pixz ≈ 4.94 (≈ +0.17) — small; reported as such.
- Tokens: native ≈ 33.8k vs Pixz ≈ 50.0k (≈ 1.48×), worst on trivial tasks; T12 continuation showed Pixz cheaper in phase 2 → amortization **hypothesis**, not proof.
- Native GLM spontaneously inspects/verifies/recovers/continues → don't teach basics; make behavior consistent/persistent/inspectable/transferable/recoverable.
- **B ≈ B1, C ≈ A** → skills alone ≈ no measurable advantage.
- T11 source-of-record: strongest narrow differentiator, **n=2** → promoted to a formal protocol; replication at n≥5 is successor-benchmark priority #1.
- Native didn't discover installed skills; used them when explicit → availability ≠ invocation → persistent activation protocol.

## Architecture Delta (OLD → NEW)

| OLD (1.1.0) | NEW (2.0.0) |
|---|---|
| "PIXZ.DEV Skills" | **PixzFlow** operating layer (PIXZ.DEV = brand) |
| 11-phase runtime enum (workflow.schema.json) | State + transitions: task-state.schema.json (status + plan + typed findings + evidence + capabilities + failures + next_action + checkpoint) |
| Orchestrator aggregates 8 (10-node install) | Orchestrator aggregates 1 — `verification` evidence floor (4-node closure) |
| Skills: installed = invoked; no state | Persistent activation protocol: 8-state lifecycle, compact state digests, reactivation conditions |
| Evidence: `[string]` | Typed claims (11 types) + typed evidence (10 kinds) + `verified_against` (compact graph via references) |
| Challenger: risk×uncertainty×impact, "must exit" | + irreversibility factor + **binding stop rule** (spent intensity / zero marginal gain / verdict produced) |
| Delegation: handoff fields in workflow schema | Economics test + handoff.schema.json + mandatory structured return + inspection + anti-delegation eval |
| Context: acquisition order only | Full lifecycle DISCOVER→FILTER→PRIORITIZE→LOAD→COMPRESS→PIN→UPDATE→EVICT→RESTORE |
| Failure: escalation ladder | Formal 9-step ladder; each retry adds information; failures[] with lesson |
| Modes only in super-z profile | Universal fast/balanced/deep/autonomous (behavioral table in AGENTS.md) |
| profiles/super-z/PROFILE.md | Top-level **ZAI.md** (Level 2.5; discoverability) |
| 15 doc + 15 routing smokes | 15 doc + 23 behavioral (8 new mechanism scenarios) + registry invariants + successor benchmark design (ablation A–H) |

## New PixzFlow Model

- **AGENTS.md** — canonical operating contract: entry protocol, modes, assessment bands, activation protocol, state/continuity, evidence + source-of-record, verification triggers, delegation economics, challenge, recovery, stopping, repo ops, pointers.
- **ZAI.md** — isolated runtime overlay (Super Z / GLM / Z.AI Web): mandatory mode question (default Balanced), mode semantics, compute policy ("generous compute is not permission to waste compute"), never-list, graceful degradation. SPECIFIED; behaviorally UNVERIFIED.
- **Skills** — 28 stable IDs, unchanged for the 14 domain skills; 13 core + anti-ai-slop rewritten to the 2.0 mechanisms (version 2.0.0 where contract changed).
- **State** — `.pixz/task-state.json` per task (schema-validated); checkpoint discipline; deterministic resume protocol; decisions marked, never deleted.
- **Evidence** — typed findings with explicit transitions; typed evidence with source-of-record weighting; the "graph" is references, not a database.
- **Agents** — orchestrator + specialist role contracts updated (loop, handoff, no recursion); challenger/verifier/researcher roles conditional on the economics test.
- **Tools/MCP** — selected by fit/cost/risk; listed before use; local inspection before research.
- **Verification** — loop with explicit triggers and six kinds; proven/trusted/unknown distinction; residual risks always reported.

## Major Changes

1. Identity: PixzFlow (README, AGENTS.md, llms.txt, docs, agents).
2. `AGENTS.md` rewritten as operating contract (~160 lines; no duplicated capability table).
3. `ZAI.md` created (top-level overlay); `profiles/super-z/PROFILE.md` consolidated and deleted.
4. `schemas/task-state.schema.json` + `schemas/handoff.schema.json` created; `schemas/workflow.schema.json` deleted (migration mapping in `docs/versioning.md`).
5. Orchestrator redesigned as adaptive operating system (assessment → mode → activation → budget → decision loop); aggregates 8→1.
6. Core skills rewritten: capability-discovery (activation lifecycle), workflow-continuity (state/checkpoint/resume), verification (source-of-record + triggers + kinds), epistemic-reasoning (taxonomy + transitions), epistemic-challenger (intensity + stop rule), planning (mode-sized), replanning (recovery ladder), context-engineering (lifecycle), delegation-handoff (economics + contract), quality-gate (stop decision), change-safety (static policy restated), environment-awareness (ORIENT hook), anti-ai-slop ("never slop merely because…").
7. `registry.json` 2.0.0: graph change + 7 protocols + 5 policies (incl. new Orchestration Budget).
8. `scripts/validate.py`: ZAI.md + AGENTS.md + new-schema checks; 2.0 migration guards (old files must be absent).
9. Evals: runner upgraded (mode invariants + registry invariants + scenario context); 8 new behavioral scenarios (skill-discovery, skill-persistence, continuation-resume, source-of-record, requirement-change, anti-delegation, tool-failure, compaction).
10. Docs: architecture (layers + delta), routing (activation), evaluation (layers + successor benchmark), GLM benchmark record, research findings, successor benchmark (ablation A–H), versioning migration, dependency-model update, taxonomy 2.0 decisions, getting-started, troubleshooting, examples, agents, profiles contract.
11. README rewritten around PixzFlow with the two required copy-paste prompts (AI Agent Installation Prompt — 9-step evidence-based; Super Z / GLM Install & Activation Prompt — 8-step).

## Deleted / Reduced Complexity

- **`schemas/workflow.schema.json`** — deleted (superseded by task-state schema; 11-phase enum retired).
- **`profiles/super-z/PROFILE.md`** — deleted (consolidated into ZAI.md).
- **Orchestrator mandatory aggregates: 8 → 1** (10-node install → 4-node closure) — benchmark-grounded (B≈B1, C≈A, 1.48× overhead).
- **AGENTS.md 28-row discovery table** — removed (single projection in llms.txt; no triple duplication).
- **No new skills created** (anti-overengineering gate applied): source-of-record = protocol inside verification; capability activation = protocol inside capability-discovery; task state = schema + workflow-continuity; evidence graph = references inside task-state (no graph DB); challenger redesign = existing skill upgraded (no new agent type).

## Validation (exact results, run 2026-09-22 on this checkout)

```
validator (scripts/validate.py):        PASS — 0 errors, 0 warnings; 28 skills, version 2.0.0
registry consistency:                   PASS — id/version/triggers/runtime frontmatter ↔ registry cross-check
dependency resolution:                  PASS — no cycles (check-cycles.py); orchestrator → 4 nodes (14 with --with-optional); agent-design → 7 nodes
skill tests (layer 2 doc eval):         15/15 (heuristic)
behavioral evals (layer 3 smoke):       23/23 (heuristic) + 2/2 registry invariants (evidence floor PASS; trivial-task budget 4 nodes PASS)
persistence evals:                      DESIGN ONLY — task-state/handoff schemas JSON-valid; resume protocol specified; no in-repo model runs (UNRUN — see limitations)
runtime adapter tests (layer 4):        integration-smoke.sh PASS (structural+doc+behavioral re-run; installer paths VERIFIED-via-docs where CLI absent — clean env, as documented)
benchmark regression:                   GLM v1 record preserved in docs/benchmark/GLM-benchmark-findings.md; successor benchmark cells A–H UNRUN by design (no model access in-repo); trivial-task overhead guard now machine-checked (budget invariant)
```

No "everything works" claims: layers 1–3 prove structure, documentation, and heuristic routing consistency only; behavioral effectiveness on real models is the successor benchmark's job.

## Known Limitations

1. **Behavioral evals are heuristics** — keyword routing + static invariants; not model-graded. Successor benchmark cells are UNRUN.
2. **ZAI.md behavioral effect is UNVERIFIED** (SPECIFIED only) — the mode ritual's actual effect on GLM/Super Z is a hypothesis.
3. **Bands-over-numbers is a HYPOTHESIS** — qualitative assessment assumed more robust across models; untested cross-model.
4. **Amortization (T12) is a HYPOTHESIS** — state structure reducing phase-2 tokens untested at scale.
5. `pinned` channel still future-only (no `pixz.lock`).
6. Generic runtime still PARTIALLY VERIFIED.
7. The 4-node evidence floor still pulls a 3-skill chain (verification→epistemic-reasoning→context-engineering); a future ablation could test a thinner floor.
8. No hosted marketplace; install via skills.sh or manual copy.

## Hypotheses Still Unverified (explicit)

| # | Hypothesis | Evidence for | Test |
|---|-----------|--------------|------|
| H1 | Source-of-record discipline measurably improves evidence integrity (T11, n=2) | v1 benchmark T11 | Successor cell: false-authority × n≥5, cells B/G |
| H2 | Persistent task-state amortizes over long-horizon continuation (T12) | v1 benchmark T12 (phase-2 tokens) | Successor cell: long-horizon + compaction + restart, cells B/E |
| H3 | Adaptive activation (vs v1's 8-aggregate bundle) matches quality at lower token cost | v1 overhead 1.48×; B≈B1, C≈A | Successor cells A/B/B′/D across model classes |
| H4 | ZAI.md overlay (mode ritual + compute policy) is behaviorally effective on Super Z/GLM | none (SPECIFIED) | Successor cell H vs C |
| H5 | Qualitative bands beat numeric scoring across model classes | inference from model-agnostic instruction guidance | cross-model successor runs |
| H6 | Anti-delegation evals catch over-orchestration regressions | v1 overhead on trivial tasks | successor trivial cells, cell B vs A |

## Next Experiments (by expected information gain)

1. **H1 replication at n≥5** (false-authority tasks; cell B vs G vs A) — validates the evidence-architecture investment; highest gain.
2. **H2** (long-horizon + forced compaction + session restart; cell B vs E) — decides the task-state protocol's worth.
3. **H3** (full ablation A/B/B′/C/D on ≥2 model classes, n≥5) — the central "which mechanisms contribute" question.
4. **H4** (ZAI overlay on GLM/Super Z; cell H vs C) — first behavioral evidence for the overlay.
5. **H6 + overhead guard** (trivial cells: token overhead ratio B/A must stay ≈1.0) — regression guard for the performance target.
6. Thin-floor ablation (4-node vs 2-node evidence floor) — possible further context reduction.

---

*Optimize for observable agent performance. A model that ignores an unnecessary skill is better than one that invokes ten ceremonially.*
