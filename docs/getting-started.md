# Getting Started — PixzFlow

## 1. What it is

**PixzFlow** is a persistent, adaptive, model-agnostic **operating layer** for capable AI agents: an entry protocol (`AGENTS.md`), operating modes (fast/balanced/deep/autonomous), a persistent task-state + evidence protocol, a skill ecosystem (35 skills with stable IDs and explicit dependencies), a vetted free/no-signup MCP + skill universe (`mcp/catalog.json`, `scripts/mcp.py`), and runtime overlays (e.g. `ZAI.md` for Super Z / GLM / Z.AI Web). PIXZ.DEV is the brand.

## 2. Why

Agents fail when they guess *what* capability to use, *when* to activate it, *how* to verify it, and *how* to continue after interruption. The GLM benchmark showed native models already handle basic engineering — what they need is **consistency, persistence, inspectability, and recoverability**, not a bigger checklist. This repo separates model / runtime / operating layer / overlay / capability / execution / state (see `docs/architecture.md`).

## 3. Choose a skill

Scan `registry.json` (machine) or `llms.txt` (LLM map) — the AGENTS.md contract tells the model how to match triggers.

**Main skill:** `pixz.core.orchestrator` is the practical operating skill. Specialist skills answer HOW. If you want more practical multi-step methodology, activate the orchestrator; load `core/orchestrator/references/operating-methodology.md` when the work is complex.

- `coordinate, complex task` → `pixz.core.orchestrator` (MAIN)
- `plan, roadmap` → `pixz.core.planning`
- `security review, audit` → `pixz.security.review`
- `gsap, scrolltrigger` → `pixz.motion.gsap`
- `framer motion, useScroll, AnimatePresence` → `pixz.motion.framer-motion`
- `ui design, color palette, typography` → `pixz.frontend.ui-ux-pro` · `design dna, design drift` → `pixz.design.project-adapt`
- `repro, flaky test, bisect` → `pixz.core.repro` · `pre-commit, secret scan` → `pixz.security.commit-hygiene`
- `mcp, mcp server, mcp config, mcpmarket` → `pixz.core.mcp`

## 4. Install (don't just clone)

**Source ≠ install.** Clone is development; install registers where the runtime discovers it.

Fastest (any agent with `npx skills`):

```bash
npx skills add pixzdev/skills --list
npx skills add pixzdev/skills --skill orchestrator
npx skills list
```

Pick your runtime in `docs/install/README.md` for exact path (Claude, OpenClaw, OpenCode, Hermes, Generic).

## 5. Verify

```bash
# structural + doc + behavioral smoke (layers 1-3)
python scripts/validate.py
python scripts/check-cycles.py
python evals/runner.py
python evals/behavioral/runner.py   # 36 scenarios + registry invariants

# resolver
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude           # 4 nodes
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional  # 17 nodes
```

See `docs/evaluation.md` for the 4 layers and what each proves.

## 6. Use

Enter the protocol: `ORIENT → MODEL → ASSESS → MODE → PLAN → ACT → OBSERVE → VERIFY → DECIDE` (`AGENTS.md#entry-protocol`). Follow the activated skill's `SKILL.md` contract (Purpose, When to use/NOT, Inputs, Methodology, Verification). Keep state in `.pixz/task-state.json` when the task outlives one step; emit typed findings + evidence, not adjectives.

Example single-skill task (minimal):
```bash
# context: pnpm vs npm mismatch
ls pnpm-lock.yaml  # environment-awareness prevents hallucination
pnpm test
```

Example orchestrated task: see `examples/orchestrated-task.md` (full ORIENT→DECIDE loop at mode deep, with challenger + quality-gate).

## 7. Limitations (honest)

- `pinned` channel: **documented future** (no `pixz.lock` yet)
- Behavioral eval is heuristic + smoke; not model-graded
- Generic runtime: partially verified (spec exists, no CI smoke)
- Installation requires `npx` (Node 18+) or manual `cp -r` — not zero-step for offline

See `docs/troubleshooting.md`.

## 8. Next

- Develop: `docs/development/creating-a-skill.md`
- Architecture: `docs/architecture.md`, `docs/architecture/routing.md`
- Research + benchmark: `docs/research/frontier-agent-findings.md`, `docs/benchmark/`
