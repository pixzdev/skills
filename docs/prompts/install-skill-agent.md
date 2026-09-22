# Prompt — Install a PIXZ Skill Natively (Runtime-Adaptive)

> For pasting into **Claude Code, OpenClaw, OpenCode, Hermes, Cursor, Codex, or any Agent Skills runtime**. This is the user-facing prompt the repo guarantees.

## Copy Everything Below — Paste Into the Target Agent

```markdown
You are not being asked to clone or study a skills repository. You are being asked to **install one or more skills into the current AI agent runtime**.

Repo: https://github.com/pixzdev/skills
Default skill: pixz.core.orchestrator @ core/orchestrator/SKILL.md (if user did not name one, install this; otherwise install the skill whose ID/trigger matches the user's request).

## Phases

### 1 — Detect Runtime (do not assume)

Probe environment before acting. Use `environment-awareness` signals:

- Files: `ls -la ~/.claude/skills` , `ls -la .claude/skills` , `ls -la .opencode/skill` , `ls -la ~/.config/opencode/skill` , `ls -la ~/.hermes/skills` , `ls -la .agents/skills` , `ls -la ./skills`
- Commands: `npx skills --help 2>&1 | head -n 20` , `openclaw --help 2>&1 | head` , `opencode --help 2>&1 | head` , `hermes --help 2>&1 | head` , `claude --version 2>&1`
- Report: runtime name + evidence (which path/command succeeded).

If multiple runtimes detected, prefer the **active** one (the CLI you are running inside). State your choice and why.

### 2 — Discover Capability (do not infer)

Read `docs/install/README.md` matrix row for detected runtime. Verify install syntax from that file — do not invent. If runtime not in matrix (UNKNOWN), state that and treat as generic `.agents/skills` with manual copy (documented as fallback).

### 3 — Identify Skill

- Read `registry.json` at repo root; find entry where `id == <requested>` or `triggers` overlap user request.
- Confirm `path` and that `<path>/SKILL.md` exists with frontmatter `name`/`description`.
- Record: id, name, version (from `metadata.yaml:version`), path, commit SHA (`git rev-parse HEAD` or VERSION file).

### 4 — Install Natively (never just `git clone`)

Choose **one** native mechanism for detected runtime (in order of preference for that runtime):

| Runtime | Preferred | Fallback |
|---------|-----------|----------|
| skills.sh | `npx skills add pixzdev/skills --skill <folder> [-g]` | `npx skills add pixzdev/skills --skill <folder> --agent <runtime>` |
| Claude Code | `npx skills add pixzdev/skills --skill <folder> --agent claude-code` | `git clone` + `mkdir -p ~/.claude/skills/<folder> && cp -r core/<folder>/* ~/.claude/skills/<folder>/` or `.claude/skills/` project |
| OpenClaw | `openclaw skills install ./core/<folder> --as pixz-<folder>` or `skills-sh:pixzdev/skills/<folder>` or `git:pixzdev/skills@main` | same with `--global` for `~/.openclaw/skills/` |
| OpenCode | `mkdir -p .opencode/skill/<folder> && cp -r core/<folder>/* .opencode/skill/<folder>/` (singular `skill` verified) | `npx skills add` then copy from `.claude/skills` if CLI landed there |
| Hermes | `mkdir -p ~/.hermes/skills/<folder> && cp -r core/<folder>/* ~/.hermes/skills/<folder>/` or `skills/<folder>/` project | — |
| Generic | `mkdir -p .agents/skills/<folder> && cp -r core/<folder>/* .agents/skills/<folder>/` | `~/.agents/skills/` global |

Execute **exactly one** install command; capture stdout/stderr and exit code. Do not run multiple installs without reporting the first's result.

### 5 — Installation Verification (mandatory)

Run the runtime's discovery verification and capture output:

- skills.sh: `npx skills list 2>&1`
- OpenClaw: `openclaw skills list 2>&1` ; `openclaw skills check 2>&1` ; `openclaw skills verify <slug> --card 2>&1` if applicable
- Claude/OpenCode/Hermes/Generic: `ls -R <installed path>/SKILL.md 2>&1` ; `head -20 <installed path>/SKILL.md 2>&1` ; `npx skills list 2>&1` if CLI available

If verification fails, you have **failed installation** — do not proceed to claim success.

### 6 — Discovery & Invocation Verification

- Confirm the installed SKILL.md is at the **installed location**, not just source. `ls` the installed path.
- Read the installed SKILL.md (installed copy) and run its lightest verification smoke (e.g., for `pixz.core.orchestrator`: `python scripts/resolve.py --install pixz.core.orchestrator --runtime <detected> 2>&1` from source, but confirm invocation would load the installed copy).
- If runtime supports `/skills` or `/<name>` slash, note it.

### 7 — Smoke Test (where feasible)

Run a controlled task relevant to the skill (examples):

- orchestrator: `python scripts/resolve.py --install pixz.core.orchestrator --runtime <detected> --with-optional`
- verification: `python scripts/validate.py`
- environment-awareness: `ls pnpm-lock.yaml 2>&1` simulation vs assumed `npm`.

Record actual behavior — do not fake PASS.

### 8 — Report (required format, no fabrication)

```
SKILL INSTALLATION REPORT
Runtime: <name, evidence>
Skill: <id, name, version, path>
Source: pixzdev/skills@<SHA or VERSION>
Installation: SUCCESS | FAILED — <command, exit, output excerpt>
Installed location: <actual verified path>
Discovery: PASS | FAIL — <list/check/ls output excerpt>
Invocation: PASS | FAIL — <how, result>
Smoke test: PASS | FAIL | SKIPPED — <command, result, reason if skipped>
Version/ref: <metadata.yaml:version, VERSION, git SHA>
Notes: <limitations, fallback used?, next steps>
```

Rules:
- Never fabricate paths, versions, SHA, or PASS when you saw FAIL.
- Never claim `git clone` alone is installation.
- If installation impossible (no CLI, no write permission, runtime unsupported), explain **why** with evidence, give nearest manual `cp -r` command, and mark Installation: FAILED — <reason>.
- Do not hide that you fell back to manual copy — report it as `Installation: SUCCESS (manual fallback)` with method noted.

### 9 — Limitations & Trust

- SKILL.md is instructions; `scripts/` may contain executable code — review before installing third-party skills.
- Scope: this install is local to the detected runtime/environment only; it does not affect other machines.
- If skill declares `requires.env` or `requires.config` (OpenClaw gating), verify those before claiming readiness.

You have succeeded only when steps 5–7 produce **evidence-backed PASS**.
```

## Example Reports

Good (OpenClaw):
```
SKILL INSTALLATION REPORT
Runtime: OpenClaw (openclaw --help succeeded, ~/.openclaw/skills exists)
Skill: pixz.core.orchestrator v1.1.0 core/orchestrator
Source: pixzdev/skills@068ad5d
Installation: SUCCESS — `openclaw skills install ./core/orchestrator --as pixz-orchestrator` (exit 0)
Installed location: ./skills/pixz-orchestrator/SKILL.md (verified ls)
Discovery: PASS — `openclaw skills list` shows pixz-orchestrator [eligible]
Invocation: PASS — read installed SKILL.md, description matches orchestrate
Smoke test: PASS — `python scripts/resolve.py --install pixz.core.orchestrator --runtime openclaw` → 4 nodes (14 with --with-optional)
Version/ref: 1.1.0 / 068ad5d
Notes: No --global used (workspace scope)
```

Bad (fabricated, do not do):
```
Installation: SUCCESS (no command shown)
Installed location: ~/.claude/skills/orchestrator (no ls evidence)
Discovery: PASS (no output)
```

See also `docs/install-as-skill.md` (short copy-paste) and `docs/install/README.md` (matrix).
