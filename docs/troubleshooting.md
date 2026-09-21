# Troubleshooting

## Install issues

**`npx skills add` says skill not found**
- `--skill` value must be **folder** name (`orchestrator`, not `pixz.core.orchestrator`). Run `npx skills add pixzdev/skills --list` to see available.
- Repo has nested folders (`core/orchestrator`); CLI resolves by folder name, not namespaced ID. Resolver uses ID.

**OpenClaw `openclaw skills install` fails**
- Check priority: workspace `skills/` vs `~/.openclaw/skills/` — `openclaw skills list` shows where it tried.
- `skills-sh:` requires `npx skills` listing to be reachable — verify `npx skills add pixzdev/skills --list` works first.
- `git:` needs `SKILL.md` at repo root or `--as` slug — this repo's SKILL.md are nested, so prefer `./core/orchestrator --as pixz-orchestrator`.

**Claude doesn't pick up skill**
- File must be exactly `SKILL.md` (caps), with frontmatter `---` containing `name:` and `description:`. `ls ~/.claude/skills/<name>/SKILL.md && head -20` .
- Restart session after install — scan runs at startup. Check `/skills` slash.

**OpenCode not discovering**
- Primary is singular `skill`: `.opencode/skill/<name>/SKILL.md` (checked first). Plural `skills` also scanned. Copy to both if unsure.
- Writes via `npx skills` may land in `.claude/skills/` — copy to `.opencode/skill/` if needed (cross-compatible verified).

**`python scripts/resolve.py` fails `LIMIT_EXCEEDED`**
- With `--with-optional`, `pixz.ai.agent-design` → 13 > `max_skill_chain_depth=15`? Should now pass with 15 limit (v1.0.1). Check `registry.json#limits`.

## Workflow / routing

**Orchestrator over-routes trivial task**
- Minimal workflow should be `UNDERSTAND→EXECUTE→VERIFY` for rename/typo — not full loop. See `docs/architecture/routing.md` under-routing/over-routing table. File an issue with scenario.

**Verification skipped**
- `quality-gate` is mandatory via resolver for orchestrated tasks; if gate missing, `scripts/validate.py` should fail. Run `python scripts/validate.py`.

## Validation

**`scripts/validate.py` reports `registry vs metadata mismatch`**
- `registry.json` is generated from `metadata.yaml`; do not edit registry without editing metadata, then `python scripts/validate.py` again.

**Cycle detected**
- Run `python scripts/check-cycles.py` — it prints full cycle path. Fix `requires`/`aggregates` loop.

## Still stuck?

- See `docs/install/<runtime>.md` for runtime-specific verification commands.
- Paste `SKILL INSTALLATION REPORT` (from `docs/install-as-skill.md`) with evidence — do not fabricate PASS.
