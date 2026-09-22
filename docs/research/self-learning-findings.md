# Self-Learning & Runtime Adaptation — Research Findings (2026-09-22, PixzFlow 2.1)

> Research performed **before** designing the post-install self-learning lifecycle (mission §2).
> Classification: **DOCUMENTED** (official spec/docs/paper) · **OBSERVED** (directly reproducible) ·
> **REPORTED** (credible third-party, not primary) · **INFERRED** (derived) · **HYPOTHESIS** (untested) · **UNKNOWN**.
> Companion document: `frontier-agent-findings.md` (skills, context, delegation, long-horizon research).
> We study observable architecture and behavior — never private chain-of-thought, never proprietary internals.

## 1. Why post-install adaptation is the gap

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 1.1 | Agent runtimes read instruction files (AGENTS.md / CLAUDE.md / GEMINI.md) **at session start**, every session, without user action. A durable instruction file is the only context guaranteed to survive restarts, compaction and model changes. | DOCUMENTED (AGENTS.md spec ecosystem; Claude Code context docs) | agents.md; code.claude.com docs; see frontier findings 1.1–1.6, 5.4 |
| 1.2 | Coding agents start each session knowing nothing about the project; anything important must be re-encountered via persistent files. Community practice: read a memory file at session start, write it at session end. | REPORTED | humanlayer.dev "Writing a good CLAUDE.md"; r/ClaudeAI memory-skill writeups |
| 1.3 | Claude Code pre-loads only skill **name+description** at startup; bodies load on relevance. Installation therefore makes capabilities *available*, not *behaviorally active*. | DOCUMENTED | Anthropic Agent Skills engineering post (frontier findings 2.1) |
| 1.4 | PixzFlow's own GLM benchmark: skills were not discovered natively but were used when made explicit (availability ≠ invocation). | OBSERVED (this repo's benchmark) | docs/benchmark/GLM-benchmark-findings.md |

**Design consequence:** the activation trigger must live in a file the runtime reads automatically (AGENTS.md), and adaptation state must live in a persistent, machine-readable file — not in conversation, and not in a prompt the user must paste each session.

## 2. Self-improvement without weight updates

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 2.1 | **Reflexion**: agents convert task feedback into *verbal self-reflections*, store them in an episodic memory buffer, and condition the next trial on them — improvement without fine-tuning. Memory is truncated to the last few reflections to prevent bloat. Ablation: self-reflection adds ~8 pts beyond raw episodic memory. | DOCUMENTED (paper) | arXiv:2303.11366 |
| 2.2 | **Voyager**: lifelong learning via a persistent **skill library** — only *self-verified* programs enter the library; skills transfer to new worlds. Ablations: removing self-verification drops performance ~73%; removing the curriculum ~93%. | DOCUMENTED (paper) | arXiv:2305.16291 |
| 2.3 | Self-modifying agent systems exist (Darwin Gödel Machine: reported 20%→50% SWE-bench; SEAL, GEPA prompt evolution) but are capped by **reward hacking and forgetting**; no shipped system recursively improves its own ability to improve. | REPORTED | morphllm.com self-improving-ai survey; Sakana DGM paper (REPORTED numbers, not independently reproduced) |
| 2.4 | Long-horizon benchmarks: self-correction gains are marginal **without new information**; plan injection + guidance beats self-correction alone. | DOCUMENTED (paper) | LongCLI-Bench (frontier findings 7.2) |

**Design consequence:** learning artifacts must be (a) verbal/compact and re-injectable (Reflexion), (b) admitted to persistent state **only after verification** (Voyager's strongest ablation), (c) bounded — an improvement is a lesson, mechanism, test or procedure, never an unbounded proliferation of new skills/agents/schemas (self-improvement explosion), and (d) grounded in new evidence, not in re-trying the same trajectory.

## 3. Persistent memory patterns

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 3.1 | Community memory-skill pattern: 3 tiers (session/ephemeral, project/persistent, global), structured MEMORY.md, tables over prose (token economy), continuation files carrying exact resume points, recovery-from-git when memory goes stale. | REPORTED | r/ClaudeAI memory-bank writeup; claude-mem docs |
| 3.2 | Progressive disclosure applied to memory: index first (what exists + retrieval cost), fetch detail on demand; success metric = high fraction of relevant tokens. | REPORTED | docs.claude-mem.ai |
| 3.3 | Claude Code re-injects invoked skill bodies and CLAUDE.md after compaction from disk — state must be re-derivable from disk. | DOCUMENTED | frontier findings 2.6, 3.1 |
| 3.4 | Auto-generated instruction files are discouraged when they replace human/project-specific judgment; machine-recorded facts + verified lessons are fine, invented preferences are not. | REPORTED | humanlayer.dev |

**Design consequence:** PixzFlow keeps ONE compact runtime-level state file (`.pixz/adaptation-state.json`) beside the existing per-task state (`.pixz/task-state.json`) — same substrate, same evidence discipline. It stores inventory facts, verified lessons and improvement status — never transcripts, never chain-of-thought, never user data beyond what the task state already permits.

## 4. Activation, handoff and runtime-adaptation patterns

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 4.1 | Agent Skills open standard: SKILL.md with `name`+`description` frontmatter works across Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot-class runtimes; runtime-specific fields are ignored safely. | DOCUMENTED/REPORTED | agentskills.io via skill guides (2026) |
| 4.2 | OpenAI Agents SDK: handoffs transfer loop control with explicit criteria; tracing makes every run inspectable. Post-install behavior should likewise be explicit + inspectable, not "agent figures it out". | DOCUMENTED | frontier findings 4.1–4.2 |
| 4.3 | Codex AGENTS.md spec: programmatic checks listed in AGENTS.md must actually be run after changes. | DOCUMENTED | frontier findings 4.3 |
| 4.4 | Skill ecosystems are an attack surface (Snyk ToxicSkills: 36.8% of sampled public skills ≥1 flaw). Post-install activation must verify what was installed before adapting to it. | REPORTED | frontier findings 2.5 |

**Design consequence:** activation is a stated lifecycle (DETECT→INVENTORY→BASELINE→ADAPT→VERIFY→PERSIST→READY) with machine-checkable drift detection, not vibes. Verification depth must match the claim (mission §8) — "installed" is not "active", "active" is not "adapted", "adapted" is not "improved".

## 5. What we do NOT claim

- No claim that any runtime executes this lifecycle identically — behavioral effect is **UNVERIFIED** until model-graded runs exist (successor benchmark cell: self-learning effect).
- No claim about proprietary model internals; all sources are public docs/papers/community reports.
- No claim that self-learning improves measured task quality yet — the mechanisms are VERIFIED structurally + at state-machine level; behavioral improvement is **HYPOTHESIS** pending the successor benchmark ablation (cells A/B/C/D, currently UNRUN).
