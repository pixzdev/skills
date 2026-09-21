# Example — Creating a Custom Skill

> How to add `pixz.domain.myskill` without skill explosion.

## 1. Taxonomy Check

Does the concept pass the seven criteria? (distinct objective, methodology, triggers, I/O, failure conditions, independent value). If not, merge into existing skill or protocol.

Example: “Vue expert” — unless it provides methodology distinct from `pixz.frontend.react` + `pixz.frontend.accessibility` + `pixz.quality.anti-ai-slop`, merge or generalize to `pixz.frontend.vue` with real methodology vs persona stub.

## 2. Scaffold

```bash
mkdir -p mydomain/my-skill
cat > mydomain/my-skill/metadata.yaml <<'YAML'
id: pixz.mydomain.my-skill
name: My Skill
category: engineering
version: 1.0.0
status: experimental
description: What this skill does and when to use it (distinct, verifiable).
triggers: [my trigger, capability]
requires: [pixz.core.context-engineering]
optional: []
conflicts: []
compatible_runtimes: [claude, openclaw, opencode, hermes]
inputs: [objective, constraints, context]
outputs: [artifact, verification]
tools: []
YAML

cat > mydomain/my-skill/SKILL.md <<'MD'
---
name: My Skill
description: What this skill does and when to use it
---
# My Skill — `pixz.mydomain.my-skill`
## Purpose
...
## Methodology
Operational steps, not persona.
MD
```

## 3. Register

Add entry to `registry.json` (machine truth) and `mydomain/AGENTS.md` navigation help. Run validation:

```bash
python scripts/validate.py
python scripts/check-cycles.py
python scripts/resolve.py --install pixz.mydomain.my-skill --runtime claude
python evals/runner.py  # add eval/mydomain.case-01.yaml
```

## 4. Eval Case

```yaml
id: eval.myskill.trigger-01
skill_id: pixz.mydomain.my-skill
description: Triggers on my trigger phrase
category: trigger
input: {prompt: "my trigger for production system", runtime: claude}
expect: {should_trigger: true, must_contain: ["Methodology"], verifies: ["distinct methodology"]}
```

## 5. Adapter Test

```bash
cp -r mydomain/my-skill .claude/skills/my-skill  # or ~/.openclaw/skills/
# Verify frontmatter progressive disclosure: name + description only in system prompt
```

No skill explosion: adding a skill must not increase ecosystem complexity without reducing task uncertainty.
