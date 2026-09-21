# claude Adapter — PIXZ Universal Skills

> Thin translation of universal core into claude conventions. No methodology fork.

## Install
See `../README.md` compatibility table. Core skill body is identical across runtimes; only paths/imports differ.

## Wiring

- **claude path:** see README compatibility table.
- **Registry:** always `AGENTS.md` + `registry.json` (validated by schemas/registry.schema.json)
- **Verification:** run `python scripts/resolve.py --runtime claude --install pixz.core.orchestrator`

## Notes for claude
- Keep SKILL.md frontmatter `name` + `description` under progressive disclosure budget (~500 chars total body guidance in OpenClaw; <200 lines CLAUDE.md).
- Do not duplicate methodology per runtime — file a bug if adapter diverges.

