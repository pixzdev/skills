# Getting Started — PIXZ Skills

## 1. What it is

A **portable, dependency-aware, versioned** collection of 28 skills for Code/Agent runtimes (Claude, OpenClaw, OpenCode, Hermes, generic). Each skill is a **reusable methodology** (how) — not a persona. See `AGENTS.md` for registry.

## 2. Why

Agents need a capability layer that answers: *what skill for this task, what does it require, which runtime can run it, how is it verified, should it be challenged?* This repo separates agent / skill / tool / orchestrator / protocol / policy / eval / registry.

## 3. Choose a skill

Scan `AGENTS.md` trigger table or `registry.json`:

- `coordinate, complex task` → `pixz.core.orchestrator`
- `plan, roadmap` → `pixz.core.planning`
- `security review, audit` → `pixz.security.review`
- `gsap, scrolltrigger` → `pixz.motion.gsap`

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
# structural + doc + quick behavioral (layers 1-2)
python scripts/validate.py
python scripts/check-cycles.py
python evals/runner.py

# resolver
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional  # 12 nodes
```

See `docs/evaluation.md` for 4 layers.

## 6. Use

Follow that skill's `SKILL.md` contract (Purpose, When to use/NOT, Inputs, Methodology, Verification). Emit structured output (`findings`, `assumptions`, `unknowns`, `evidence`, `verification`).

Example single-skill task (minimal):
```bash
# context: pnpm vs npm mismatch
ls pnpm-lock.yaml  # environment-awareness prevents hallucination
pnpm test
```

Example orchestrated task: see `examples/orchestrated-task.md` (full DISCOVER→SHIP with challenger + quality-gate).

## 7. Limitations (honest)

- `pinned` channel: **documented future** (no `pixz.lock` yet)
- Behavioral eval is heuristic + smoke; not model-graded
- Generic runtime: partially verified (spec exists, no CI smoke)
- Installation requires `npx` (Node 18+) or manual `cp -r` — not zero-step for offline

See `docs/troubleshooting.md`.

## 8. Next

- Develop: `docs/development/creating-a-skill.md`
- Architecture: `docs/architecture.md`, `docs/architecture/routing.md`
- Concepts: `docs/concepts/` (coming)
