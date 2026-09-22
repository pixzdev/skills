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
28 skills: small enough to be coherent, large enough to cover critical paths. Adding a skill must pass the seven criteria above; removing one must not break dependency or leave a methodology gap.

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

### Anti-Overengineering Gate applied (things NOT built in 2.0)
- No separate "evidence graph database" — the graph is references inside `task-state.schema.json` (simpler, same benefit).
- No numeric task-scoring engine — qualitative bands (hypothesis, to be validated by successor benchmark).
- No per-phase sub-skills — the 11-phase model was retired for state+transitions.
- No new "challenger agent" type beyond the existing role — intensity + stop rule added to the existing skill instead.
- No duplicate "workflow" skill alongside `workflow-continuity` — one lifecycle skill owns state.
