# Creating a Skill — Contract

Each skill MUST have (see schemas/skill.schema.json):

```yaml
id: pixz.<domain>.<name>   # stable, kebab-case, never filename
name: "<Title Case>"       # human title; frontmatter `name` SHOULD be kebab-case slug matching folder for CLI compat
description: "<what it does + when; <500 chars"
version: "1.0.0"
triggers: ["keyword", "phrase"]
requires: ["pixz.core.context-engineering"]
aggregates: []  # only orchestrator-grade
optional: []    # opt-in via --with-optional
conflicts: []
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
inputs: [objective, constraints, context]
outputs: [artifact, verification]
```

Folder:
```
<domain>/<name>/
  SKILL.md          # required: frontmatter name/description + body Contract (Purpose, When to use/NOT, Inputs, Outputs, Methodology, Dependencies, Tools, Constraints/Failure, Verification, Examples, Structured output)
  metadata.yaml     # required: validated vs schema
  references/       # optional tier-3 (progressive disclosure)
  scripts/          # optional helpers
```

SKILL.md is **instructions at invocation time**, not docs. Long rationale → `docs/`.

Classification before creating (7 criteria): distinct objective, reusable methodology, independent trigger, meaningful I/O, failure conditions, independent value, not a fragment. If not, use PROTOCOL/POLICY/SCHEMA not SKILL. See `docs/taxonomy.md`.

Register: add to `registry.json` (via manual + `scripts/validate.py` cross-check) and `*/AGENTS.md` navigation.

Validate: `python scripts/validate.py && python scripts/check-cycles.py && python evals/runner.py --layer doc`
