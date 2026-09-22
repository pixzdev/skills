# Frontier-Agent Research Findings (Phase Zero, 2026-09-22)

> Research performed **before** the PixzFlow 2.0 reconstruction. Every observation is classified:
> **DOCUMENTED** (official spec/docs) · **OBSERVED** (directly reproducible) · **REPORTED** (credible third-party, not primary) · **INFERRED** (derived) · **HYPOTHESIS** (untested) · **UNKNOWN**.
> We study observable architecture and behavior — never private chain-of-thought.

## 1. Persistent instruction files (AGENTS.md ecosystem)

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 1.1 | AGENTS.md is an open plain-markdown standard read by 30+ agent runtimes; maintained under the Agentic AI Foundation (Linux Foundation). | DOCUMENTED | agents.md standard; gemini-cli discussion #1471 |
| 1.2 | OpenAI Codex CLI reads AGENTS.md root→leaf, joins them, and **truncates at 32 KiB** default (`project_doc_max_bytes`); `AGENTS.override.md` can override. | DOCUMENTED | OpenAI Codex system prompt spec (gist 0xdevalias) |
| 1.3 | Recommended practice: root file ≈ under 150 lines, sections < 50 lines, command-first, closure-defined ("done" criteria), front-load critical rules. | REPORTED | blakecrosley.com; atlan.com; morphllm.com |
| 1.4 | Longer instruction files deliver diminishing returns; content duplicated from README measurably hurts; shorter files let agents spend attention on the task. | REPORTED | multi-source synthesis (Princeton study cited in morphllm guide) |
| 1.5 | Factory Droid documents context budgets for instruction files (initial guideline load 80k chars, dynamic read-path discovery 40k chars) and recommends moving reusable procedures into skills. | DOCUMENTED | docs.factory.ai/cli/configuration/agents-md |
| 1.6 | Claude Code loads CLAUDE.md (+ AGENTS.md), auto-memory, MCP tool names, and **skill descriptions** into context before the first message. | DOCUMENTED | code.claude.com/docs/en/context-window |

**Design consequence:** AGENTS.md must be high-authority, high-signal, low-redundancy, ≤ ~170 lines, with the machine registry (registry.json) and LLM map (llms.txt) carrying bulk data — never duplicated in three places.

## 2. Agent Skills (progressive disclosure)

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 2.1 | Anthropic Agent Skills: SKILL.md = YAML frontmatter (`name`, `description` required) + markdown. At startup the agent pre-loads **only name+description of every installed skill**; the full body loads only when the agent decides the skill is relevant; bundled reference files load only on demand. | DOCUMENTED | anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| 2.2 | The spec was released as an open standard (agentskills.io) 2025-12-18. | REPORTED | articsledge.com guide |
| 2.3 | Skill selection happens via **LLM reasoning over the description field**, not algorithmic keyword matching. | OBSERVED (reverse-engineered internals) | leehanchung.github.io deep dive |
| 2.4 | Rule of thumb: SKILL.md body < ~5,000 tokens; reference detail in bundled files. | REPORTED | multiple skill-authoring guides |
| 2.5 | Snyk "ToxicSkills" audit of 3,984 public skills: 36.8% contain ≥1 security flaw, 13.4% critical — skills are an attack surface; installation must be verified. | REPORTED | Snyk study via termdock.com |
| 2.6 | Claude Code re-injects **invoked skill bodies after compaction** (capped 5,000 tokens/skill, 25,000 total, oldest dropped first) — skill state must therefore be re-derivable from disk, not only from conversation. | DOCUMENTED | code.claude.com/docs/en/context-window |

**Design consequence:** PixzFlow's activation protocol must be progressive (metadata → body → references), must track **activation state** (not just "installed"), and must persist compact per-capability state because conversation context is lossy and compaction drops it.

## 3. Claude Code (context, compaction, subagents)

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 3.1 | Auto-compaction triggers near the context limit; the system prompt, CLAUDE.md, **plans written in plan mode**, path-scoped rules, up to 5 recently-read files, and invoked skill bodies are **re-injected from disk** after compaction; conversation middle is summarized and original messages discarded. | DOCUMENTED | code.claude.com/docs/en/context-window |
| 3.2 | Subagents run in **separate context windows**; only the summary + small metadata trailer returns to the parent. Large reads are delegated to subagents precisely to keep the parent context lean. | DOCUMENTED | code.claude.com/docs/en/context-window |
| 3.3 | Documented context techniques: compaction (with focus instructions), `/clear` between tasks, structured note-taking, sub-agent architectures; "treat context as a precious resource"; just-in-time retrieval over pre-loading. | DOCUMENTED | Anthropic "Effective context engineering for AI agents" (2025-09-29) |
| 3.4 | Reverse-engineered: 3-tier compaction (tool-result cleanup → server-side strategy → full LLM summarization producing a structured ~9-section summary, then reconstruction with boundary marker + recent files + skills + CLAUDE.md). | REPORTED (source analysis) | barazany.dev |
| 3.5 | Community observation: compaction silently destroys rejected approaches and discovered edge cases; externalizing constraints/decisions into persistent artifacts preserves continuity. | REPORTED | dev.to (jsmanifest) |

**Design consequence:** durable task state must live in a **file** (re-injectable), decisions/failures must be written down (not kept in conversation), and delegation is a **context-isolation** mechanism, not a capability upgrade by itself.

## 4. OpenAI (Codex CLI / Agents SDK)

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 4.1 | Agents SDK primitives: agents, tools, **handoffs** (transfer of loop control — the receiving agent owns the conversation), **guardrails** (single-purpose tripwires running concurrently), **tracing** (every run emits an inspectable record of model calls, tool calls, handoffs, guardrail outcomes). | DOCUMENTED | developers.openai.com agents docs |
| 4.2 | Recommended practice: explicit handoff criteria (not "use your judgment"), bounded agents ("answer and stop"), short structured instructions, triage agent routing to specialists, structured output types. | REPORTED (SDK prompting guides) | sureprompts.com; getstream.io |
| 4.3 | Codex AGENTS.md spec: nested files take precedence; programmatic checks listed in AGENTS.md **must be run after changes** even for docs-only changes. | DOCUMENTED | OpenAI Codex system prompt spec |

**Design consequence:** delegation needs an explicit **contract** (objective, bounds, expected return, inspection), and observability should record decisions/evidence — never private reasoning.

## 5. Gemini CLI

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 5.1 | Subagents: isolated context window, own system prompt/tools/history; **return a consolidated summary**; configured via Markdown + frontmatter (`name`, `description`, `tools`, `model`, `max_turns`, `timeout_mins`). Built-ins: `generalist`, `codebase_investigator`, `cli_help`. | DOCUMENTED | geminicli.com/docs/core/subagents |
| 5.2 | **Recursion protection: subagents cannot call other subagents** (even with `*` tool wildcard). | DOCUMENTED | geminicli.com/docs/core/subagents |
| 5.3 | Google frames the main agent as a "strategic orchestrator" that treats its context window as its most precious resource and delegates heavy lifting to specialists. | DOCUMENTED (vendor framing) | morphllm comparison citing Google docs |
| 5.4 | Context assembly: GEMINI.md (project instructions, AGENTS.md alias configurable via settings), MCP, conversation; `ContextCompressionService` landed v0.38.1 alongside subagents; `@agent_name` forces delegation. | DOCUMENTED | gemini-cli release notes v0.38.1 |

**Design consequence:** depth caps and "no subagent-spawns-subagent" are industry practice; parallelism is used for **independent** research/analysis only.

## 6. OpenCode

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 6.1 | OpenCode (Go, open source, 75+ providers) reads AGENTS.md natively; `.opencode/skill/` (singular) for skills; plan mode; non-interactive `-p` for CI. | DOCUMENTED/REPORTED | opencode docs; ssntpl.com guide |
| 6.2 | Community "crash course" model of agent context: fixed layers (system prompt + rules file) vs. managed layers (conversation, files, active skill body); `/clear` for new tasks, `/compact` at phase boundaries; "conversations get worse as they get longer". | REPORTED | panaversity.org crash course |

## 7. Long-horizon / verification research

| # | Finding | Class | Source |
|---|---------|-------|--------|
| 7.1 | **HORIZON** diagnostic benchmark: horizon-dependent degradation in SOTA agents (GPT-5/Claude families) across 3,100+ trajectories; failures concentrate in early task stages. | DOCUMENTED (peer-venue paper) | arXiv via HF Daily Papers |
| 7.2 | **LongCLI-Bench**: SOTA coding agents <20% pass on long-horizon CLI tasks; **plan injection + interactive guidance beats self-correction alone**; self-correction gains are marginal without new information. | DOCUMENTED (paper) | arXiv:2602.14337 |
| 7.3 | **LH-Bench**: given structured verification feedback during execution, agents self-correct ~70% of runtime errors; recovery is dependent on error-message quality. | DOCUMENTED (paper) | arXiv:2603.22744 |
| 7.4 | **PRO-LONG**: a complete structured interaction log + efficient search over it ("programmatic memory") supports long-horizon reasoning — state-as-log, not state-in-conversation. | DOCUMENTED (paper) | arXiv via HF Daily Papers |
| 7.5 | **YC-Bench**: goal drift and context distraction are the characteristic multi-session failure modes — invisible to short-horizon benchmarks. | DOCUMENTED (paper) | arXiv:2604.01212 (cited in zylos.ai synthesis) |
| 7.6 | 2026 synthesis: "reliability decay" over long horizons, SWE-bench contamination concerns, SlopCodeBench showing iterative degradation. | REPORTED | zylos.ai research synthesis |
| 7.7 | CorrectBench: **external** correction (tool/test feedback) works; purely intrinsic self-correction is weak. | DOCUMENTED (paper) | arXiv:2510.16062 |
| 7.8 | openJiuwen (2026): letting evolving evidence dynamically affect context/feedback/task control at runtime beats static harness policies on SWE-bench Verified / Terminal-Bench. | REPORTED (vendor + leaderboard) | HF Daily Papers |

**Design consequence:** (a) the workflow must be **stateful and resumable** (state file + checkpoint); (b) verification feedback is what enables recovery, so verification must be a **continuous loop**, not a final ceremony; (c) retries must bring new information; (d) long-horizon tasks need explicit drift counters (objective restatement, requirement tracking).

## 8. Failure modes observed in our own GLM benchmark (see `docs/benchmark/GLM-benchmark-findings.md`)

- 52/52 objective acceptance in **both** conditions → correctness ceiling; PixzFlow must not claim correctness gains.
- Native ≈ 4.77 vs Pixz ≈ 4.94 blind grading → small, honest delta.
- Native ≈ 33.8k vs Pixz ≈ 50.0k tokens → **1.48× overhead**, worst on trivial tasks → orchestration must have an explicit budget.
- Native GLM already spontaneously inspects, verifies, recovers, continues → don't teach basics; make behavior **consistent, persistent, inspectable, transferable, recoverable**.
- B ≈ B1 and C ≈ A → **skills alone ≈ no measurable advantage**; the value must come from activation + state + evidence discipline.
- T11 (source-of-record) = strongest narrow differentiator, n=2 → hypothesis-generating, now promoted to a formal protocol.
- Native GLM did not spontaneously discover installed skills; when made explicit it used them → **availability ≠ invocation**.

## 9. Patterns adopted (mechanisms, not vendor terminology)

1. Progressive disclosure for capabilities (metadata → body → references). [2.1]
2. Compact re-injectable state files as the continuity substrate. [3.1, 7.4]
3. Subagents as context isolation + summary return; no sub-subagents; parallelism only for independent work. [3.2, 5.2, 5.3]
4. Explicit delegation contracts + inspection of returns (no blind trust). [4.1, 4.2]
5. Structured tracing of decisions/evidence (never private reasoning). [4.1]
6. Instruction files: short, command-first, closure-defined, no README duplication. [1.2, 1.3, 1.5]
7. Verification as continuous feedback loop; recovery quality depends on error-message quality. [7.3, 7.7]
8. Plan quality + external feedback beat self-talk; failures cluster early → orient/assess hard, drift counters later. [7.1, 7.2, 7.5]
9. Adaptive depth over fixed phase lists (harness policies that adapt to evolving evidence outperform static ceremony). [7.8]
10. Orchestration budget: every added capability must earn its context cost. [3.3, 1.5, benchmark §6]

## 10. What we explicitly did NOT adopt

- Fixed N-phase "pipeline theater" (our 11-phase enum) — replaced by a state/transition model; phases kept only as optional narrative labels.
- "Always challenge / always delegate / always verify 5×" rules — intensity is risk×uncertainty×impact×irreversibility-scaled with explicit stopping rules.
- A graph database for evidence — a compact typed ledger with references is sufficient (anti-overengineering gate).
- Numeric scoring of tasks — qualitative bands (LOW/MEDIUM/HIGH/CRITICAL) are more robust across models (HYPOTHESIS; to be tested in the successor benchmark).
