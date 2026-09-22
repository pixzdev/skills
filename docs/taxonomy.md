# Taxonomy Normalization — PixzFlow Skills

## Method
Each proposed concept was classified as exactly one of:
`SKILL | PROTOCOL | POLICY | DEPENDENCY | AGENT | TOOL | EVAL | REGISTRY`

A standalone SKILL requires: distinct objective + reusable methodology + independent invocation + triggers + I/O + failure conditions + standalone value. Otherwise merged into a higher-level skill or protocol.

## Decisions

### Merged → SKILL
- `workflow persistence + continuation + handoff + iteration state` → **workflow-continuity** (single lifecycle skill; delegation-handoff handles dispatch)
- `evidence discipline + uncertainty + assumption tracking + confidence scaling + argumentation + integrity + anti-confirmation` → **epistemic-reasoning** (one disciplined reasoning skill). **epistemic-challenger** kept separate because challenger has adaptive intensity, exit conditions and counter-methodology — merging would dilute both.
- `OS + runtime + framework + package-manager + repo + filesystem + dependency + git + deployment + resource + permissions + MCP/tool` → **environment-awareness** (one prevention skill). Keeps “inspect before assuming” as a single check.
- `inspection + verification + failure-mode + regression + consistency + change-impact + quality gate` splitted: **verification** (evidence gathering) + **quality-gate** (ship decision) — separation preserves inspect-vs-decide clarity.
- `tool selection + safe tool use + authority + scope + reversibility + simplicity` → **change-safety** (single pre-mutation gate)
- `initiative + capability discovery + research + source evaluation + synthesis` → **capability-discovery** + **research** folded into context-engineering/discovery loop (not a separate skill)

### PROTOCOL (not a skill)
- Context Protocol (what/where/authority/staleness/preservation, acquisition order)
- Workflow Propagation Protocol (parent → child inheritance, handoff schema)
- Argumentation Protocol (claim lifecycle, position change attribution)
- Escalation Ladder (retry → inspect → alternate → research → specialist → challenge → parent → user)

### POLICY (global constraints)
- Scope Control (requested vs necessary vs optional vs out-of-scope)
- Simplicity (minimum necessary, not minimum possible)
- Safe Execution / Authority Awareness
- Change Safety (reversible/partially/irreversible tiers)
- Anti-AI-Slop (diagnostic criteria, not dogmatic bans)

### Kept Distinct — Justification
- **planning** vs **replanning**: replanning has distinct triggers (failed verification, new constraints) and methodology (root-cause → alternate → re-verify). Merging would hide escalation path.
- **delegation-handoff** vs **workflow-continuity**: continuity owns state persistence; delegation owns dispatch contract. Different failure modes.
- **epistemic-challenger** vs **epistemic-reasoning**: reasoning builds arguments; challenger tries to break them with `risk×uncertainty×impact`-scaled intensity. Separate exit conditions.

## Final Categories

### Mandatory Core (installed with orchestrator aggregates)
- pixz.core.orchestrator
- pixz.core.planning
- pixz.core.context-engineering
- pixz.core.environment-awareness
- pixz.core.capability-discovery
- pixz.core.workflow-continuity
- pixz.core.epistemic-reasoning
- pixz.core.verification
- pixz.core.quality-gate

### Core (hard-requires, but accessed via orchestrator or directly)
- pixz.core.delegation-handoff
- pixz.core.epistemic-challenger
- pixz.core.change-safety
- pixz.core.replanning

### Quality
- pixz.quality.anti-ai-slop

### Domain / Niche (intentionally curated, not persona stubs)
- pixz.engineering.api-design, pixz.engineering.system-design
- pixz.security.review, pixz.security.threat-modeling
- pixz.design.uiux, pixz.design.design-system
- pixz.frontend.react, pixz.frontend.accessibility
- pixz.motion.gsap, pixz.motion.remotion
- pixz.devops.docker, pixz.devops.kubernetes
- pixz.ai.rag, pixz.ai.agent-design

### Intentionally NOT Created (merged or policy)
- Separate skills for: planning vs delegation vs coordination vs escalation (covered by orchestrator+planning+delegation+replanning)
- Micro-skills for: argumentation, confidence-scaling, uncertainty-management (inside epistemic-reasoning)
- Micro-skills for: OS/runtime/framework awareness (inside environment-awareness)
- “Research” standalone (method inside capability-discovery + context-engineering; research is tool-use, not methodology)
- Dozens of niche personas (e.g., “Vue expert”, “Svelte expert”) — each must prove methodology; curated set proves pattern.

## Skill Count Rationale
35 skills (28 in 2.0.0; +self-learning in 2.1.0; +mcp in 2.4.0; +framer-motion, ui-ux-pro, project-adapt, repro, commit-hygiene in 2.5.0): small enough to be coherent, large enough to cover critical paths. Adding a skill must pass the seven criteria above; removing one must not break dependency or leave a methodology gap.

## 2.0.0 Decisions

### New concepts classified as PROTOCOL / POLICY (not skills)
- **Source-of-Record** → `pixz.protocol.source-of-record` (a verification protocol, not a skill — it has no independent invocation triggers beyond verification; merging into `pixz.core.verification` methodology keeps the graph lean).
- **Capability Activation** → `pixz.protocol.capability-activation` (the persistent invocation lifecycle — it is *how* capabilities are used, owned by `capability-discovery`, not a separate capability).
- **Task State & Continuity** → `pixz.protocol.task-state` (the state model is a schema + `workflow-continuity` methodology, not a skill).
- **Orchestration Budget** → `pixz.policy.orchestration-budget` (a global constraint on activation/delegation, not a skill).
- **Handoff Contract** → `pixz.protocol.handoff-contract` (a schema + `delegation-handoff` methodology).

### Kept Distinct (2.0)
- **verification** (evidence gathering + source-of-record) vs **quality-gate** (the done-decision) — separation preserves inspect-vs-decide clarity.
- **capability-discovery** (activation lifecycle) vs **orchestrator** (decides which/how-deeply/for-how-long) — discovery is the mechanism, orchestration is the decision.

## 2.1.0 Decisions (self-learning upgrade)

### New SKILL — `pixz.core.self-learning`
Passed the seven standalone criteria: distinct objective (post-install adaptation + evidence-driven self-improvement) · reusable methodology (activation lifecycle + improvement loop with six challenges) · independent invocation (runs alone on any fresh runtime) · clear triggers (post-install, first activation, skill version changed, learn from failure, …) · meaningful I/O (baseline, delta report, learning ledger) · meaningful failure conditions (fake learning, duplicate setup, proliferation, drift denial) · verification method (lifecycle suite + probe exit codes + behavioral E-series). Kept distinct from capability-discovery (which owns invocation of *task* capabilities) because self-learning owns the *runtime ↔ workflow* relationship across sessions — different lifetime, different failure modes.

### New SCHEMA — `schemas/adaptation-state.schema.json`
Runtime-level state (baseline, digested inventory, adaptation status, learning ledger). NOT a parallel memory architecture: same `.pixz/` substrate, same evidence discipline, same compactness rules as task-state; different lifetime (runtime-wide vs per-task). Task-state gains only an optional `adaptation` pointer.

### New PROTOCOLS (not skills)
- **Self-Learning Lifecycle** → `core/self-learning/SKILL.md` owns the methodology (same pattern as Capability Activation → capability-discovery).
- **Verification Depth** → `core/verification/SKILL.md` owns the ladder (same pattern as Source-of-Record → verification). No new skill: the ladder has no independent invocation beyond verification.

### Extended POLICY (not new)
- Simplicity policy absorbs the **improvement-economy (anti-proliferation) gate**: failures must not spawn new skills/agents/protocols/schemas/instruction files/dependencies unless existing mechanisms cannot express the fix, the failure class recurs, and benefit justifies permanent cost.

### New TOOL — `scripts/activation.py`
Deterministic state machine (probe/init/mark-adapted/sync/mark-installed) — the machine-verifiable half of self-learning; the behavioral half stays with the agent. Exit codes make adaptation observable without a model.

### Intentionally NOT created in 2.1
No "memory" skill (adaptation-state + task-state already cover it) · no self-improvement *agent* type (the loop is methodology, not a role) · no separate validation-depth skill (protocol + verification skill suffice) · no re-training scheduler (probe-at-ORIENT + drift detection suffice) · no lesson database (compact JSON ledger suffices).

## 2.5.0 Decisions (motion & frontend design intelligence + held-ideas batch)

### New SKILL — `pixz.motion.framer-motion`
React/Next.js declarative motion is a **different methodology** from the existing `pixz.motion.gsap` (vanilla JS / Vue / Webflow, pinning, horizontal-scroll hijack): different library, different mental model (variants/props vs timeline API), different failure modes (`AnimatePresence` exits, hydration, `useTransform` binding). One skill per library avoids cross-wiring the wrong patterns; the **routing table (when Framer vs when GSAP)** lives inside the new skill and cross-references the GSAP skill. `optional` on `pixz.core.verification` only.

### New SKILL — `pixz.frontend.ui-ux-pro`
Design intelligence for frontend *builds*: product-type style direction, contrast-**computed** color roles, type-scale discipline, tokens, iconography, chart selection, a11y-first UX priority. **Kept distinct from `pixz.design.uiux`** (interaction/UX *quality critique* — review-oriented): uiux owns "is this usable/well-structured", ui-ux-pro owns "what should the visual system be + how do I implement it". Overlapping trigger (`ui design`) is deliberate — both should fire on UI work and they answer different questions; the boundary is documented in each skill's When NOT table. Differentiated from the community `ui-ux-pro-max` by being project-adaptive (Design DNA first), evidence-checked (contrast computed, not vibes), and integrated with the MCP set (better-icons, chrome-devtools, animation-inspector); its dataset is an optional quarantine import, never a copy.

### New SKILL — `pixz.design.project-adapt` (Design DNA)
The token-extraction + enforcement protocol as a standalone capability: INVENTORY → EXTRACT (typed, evidence-backed) → PROFILE (`.pixz/design-dna.json`) → constrained GENERATE → DRIFT CHECK → REPORT. Reused by ui-ux-pro (project-adaptive first step) and any future design work — a methodology with its own invocation, not a section of another skill.

### New SKILL — `pixz.core.repro`
Repro-before-fix is a **core** discipline (applies to every failure class, not just one domain): REPRO → CLASSIFY → MINIMIZE → FREEZE → FIX → VERIFY; a fix without a repro is a failure unless `NOT_REPRODUCIBLE` with an attempt log. `optional` on the orchestrator (mandatory closure stays 4 nodes).

### New SKILL — `pixz.security.commit-hygiene`
Security gate at the **commit boundary** (pre-publication): secrets in the staged diff (BLOCK, values never echoed), manifest/lockfile drift, stray artifacts, message↔diff consistency. Kept in `security` (not `core`) — it is a domain gate; `pixz.core.change-safety` stays the pre-change gate. No overlap with `pixz.security.review` (deep review) — commit-hygiene is a fast tripwire.

### New TOOLS — `scripts/vet-skill.py` · `mcp.py usage` · `resolve.py --lock`
- **vet-skill.py** — quarantine scanner for external skill bundles (injection/exfiltration/secret blockers → exit 1; consistency + budget warnings → exit 10; frontmatter structure; script inventory; `--json`). Deterministic half of the skill-import quarantine protocol (which stays agent-driven for the judgment calls). TOOL, not skill: no triggers, no invocation of its own.
- **mcp.py usage** — per-server usage report (task-state `mcp.<id>` activations × check evidence × catalog → keep/verify/vet/suspend/check/idle). Extends the existing maintenance step with evidence instead of memory.
- **resolve.py --lock / `pixz.lock`** — the `pinned` channel becomes real (self-audit TODO #25 closed): lockfile = version snapshot; pinned resolves verify against it, drift = hard fail. Repo ships `pixz.lock`.

### CATALOG — motion & devtools additions
`chrome-devtools` (T1 official — the strongest RUNTIME-ACTIVE evidence tool: performance traces, network, console, screenshots) and `animation-inspector` (T2 — animation-system detection + frame capture; core keyless). **Excluded on evidence:** `gsap-mcp` (bl00dclot) — capable, but clone+build install with no npx one-liner fails the zero-friction auto-config criterion (watchlist); Framer Motion/Motion MCP — none published at check date (docs via context7).

### Intentionally NOT created in 2.5
No Three.js/Lottie skills (no verified free no-key MCP + methodology demand; animation-inspector covers verification) · no per-MCP skills for the two new servers (catalog + existing skills cover them) · no copying of the `ui-ux-pro-max` dataset (quarantine-import protocol instead) · no new schemas (design DNA lives in `.pixz/design-dna.json` as a project artifact, not a repo schema).

## 2.4.0 Decisions (MCP + external capability integration)

### New SKILL — `pixz.core.mcp`
Passed the seven standalone criteria: distinct objective (vetted integration of MCP servers + external skills) · reusable methodology (trust tiers → vetting gate → live-check-first → idempotent auto-config → budgeted activation → untrusted-output rule → maintenance) · independent invocation (runs alone: "add an MCP server") · clear triggers (`mcp`, `mcp server`, `mcpmarket`, `external tools`, …) · meaningful I/O (catalog entries, check evidence, config artifacts, report) · meaningful failure conditions (wiring blind, just-in-case tooling, untrusted output treated as fact, credential leakage, clobbering user config, auto-enabling imports) · verification method (live `initialize`+`tools/list` evidence in `.pixz/mcp-check.json` + documentary/behavioral evals). Kept distinct from capability-discovery because MCP has a **trust boundary + supply-chain surface** (vetting, untrusted output, idempotent config writes) that capability-discovery's invocation lifecycle does not cover — different failure modes. `optional` on the orchestrator (never an aggregate — the 4-node mandatory closure stays intact; trivial tasks stay cheap).

### New TOOL — `scripts/mcp.py`
Deterministic half of the protocol: catalog listing, tier mapping, live probes (stdio + streamable-HTTP + legacy SSE JSON-RPC), idempotent per-runtime config writers, status/detect. Stdlib-only like the rest of `scripts/`. Evidence file `.pixz/mcp-check.json` makes liveness observable without a model.

### New PROTOCOL — `pixz.protocol.mcp-integration`
Points at `core/mcp/SKILL.md` (same pattern as Capability Activation → capability-discovery). No new state schema: MCP activations live in task-state `capabilities[]` (`mcp.<server-id>` entries) and the check evidence file — no parallel substrate.

### New POLICY — `pixz.policy.pixzflow-mandate`
The complex-task obligation (complex work MUST run under the full protocol; skipping it = contractual failure GAGAL; trivial exempt). A policy, not a skill: it constrains *all* work and has no independent invocation.

### NEW CATALOG — `mcp/catalog.json` (+ `mcp/README.md`)
Machine source of truth for the integration universe: free + no signup + no API key by policy, trust tiers, per-entry verification sources, `excluded_with_reason` for auth-required entries. It is a **projection of curation decisions, not a second registry** — servers are not `registry.json` skills; the skill is `pixz.core.mcp`.

### Intentionally NOT created in 2.4
No per-server skills (23 servers as 23 skills would be micro-skill proliferation — the catalog + one skill covers them) · no MCP client skill (the runtime *is* the client) · no secrets-manager skill (policy: user-managed credentials, outside this repo's artifacts) · no automatic skill-merger from mcpmarket.com (imports are quarantined + reviewed + explicitly enabled — never auto) · no behavioral eval that fakes a network handshake (the live check runs at setup time on a networked runtime; evals assert routing + documentary gates only).

## 2.2.0 Decisions (adoption tooling)

### New TOOLS (scripts — not skills, not schemas)
- **doctor.py** — measured baseline: converts self-reported dimensions into observed ones; the unmeasurable stays `unknown`. Classification: TOOL (no methodology to invoke, no triggers — it serves the self-learning lifecycle).
- **assess.py** — adoption score 0–100. Classification: TOOL with an explicit doctrine guard: it sums *named evidence-backed adoption checks* (each PASS/FAIL, UNVERIFIED scores 0). This is **not** the "numeric task-scoring engine" rejected in 2.0 (that one would grade model/task quality); adoption completeness is a checklist of verifiable facts, and the report prints the doctrine with every run.
- **sitrep.py** — one-block ORIENT/handoff report over existing state files. TOOL (read-only composition).
- **hooks.py** — runtime contract wiring (append-only, idempotent; claude-only write path, native runtimes verify-only). TOOL.
- **verify-installed** (activation.py subcommand) — installed-copy integrity vs source digests. Extends the existing drift family; no new concept.

### Intentionally NOT created in 2.2
No new skills/schemas/agents; no daemon/watcher; no global cross-project state; no task templates (no evidence of need yet).

### Anti-Overengineering Gate applied (things NOT built in 2.0)
- No separate "evidence graph database" — the graph is references inside `task-state.schema.json` (simpler, same benefit).
- No numeric task-scoring engine — qualitative bands (hypothesis, to be validated by successor benchmark).
- No per-phase sub-skills — the 11-phase model was retired for state+transitions.
- No new "challenger agent" type beyond the existing role — intensity + stop rule added to the existing skill instead.
- No duplicate "workflow" skill alongside `workflow-continuity` — one lifecycle skill owns state.
