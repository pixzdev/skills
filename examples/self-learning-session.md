# Example — A Self-Learning Session (first activation, then a later session)

Two sessions, same runtime. No prompt is pasted in session 2 — that is the point.

## Session 1 — right after install

```bash
$ python3 scripts/activation.py status
STATE=NEW — no adaptation state; run: activation.py init (first activation)
pixzflow=2.1.0 skills=29
# exit code 10

$ python3 scripts/activation.py init --runtime claude \
    --source pixzdev/skills@a1b2c3d --channel stable \
    --signal ".claude/skills exists" --signal "claude --version ok" \
    --instruction-source "CLAUDE.md @AGENTS.md import" \
    --dim state_persistence=yes --dim verification=yes \
    --dim delegation=unknown --dim research=yes
STATE=BASELINED — wrote .pixz/adaptation-state.json
```

The agent then adapts (reads AGENTS.md, adopts the entry protocol, modes, evidence
rules, verification triggers) and **verifies the adaptation** — here by running the
repo's own layers and observing output:

```bash
$ python3 scripts/validate.py        # ✓ 0 errors
$ python3 evals/behavioral/runner.py # ✓ 33/33
$ python3 scripts/activation.py mark-adapted \
    --evidence "validate.py 0 errors; behavioral 33/33; probe exit 10->0 transition"
STATE=READY — adaptation recorded with evidence.
```

Note what was NOT stored: no transcript, no chain-of-thought — an inventory with
digests, observed dimensions (delegation stayed `unknown` — not invented), and the
adaptation evidence string.

## Session 2 — days later, fresh context

The runtime reads `AGENTS.md` at session start. The ORIENT step probes once:

```bash
$ python3 scripts/activation.py status
STATE=READY
pixzflow=2.1.0 (adapted=2.1.0) skills=29 adaptation=ready
evidence: validate.py 0 errors; behavioral 33/33; probe exit 10->0 transition
Adaptation verified; continue working — do NOT re-run setup.
# exit code 0
```

No duplicate setup. The task starts immediately.

## Session 3 — after a skill upgrade

```bash
$ python3 scripts/activation.py status
STATE=STALE
DRIFT:
      version  pixz.core.planning  — 2.0.0 -> 2.1.0 (content changed)
```

The agent inspects the **actual diff** (never assumes version change = behavior
change), finds a new verification requirement in planning's methodology, re-adapts
only that capability, re-verifies, then:

```bash
$ python3 scripts/activation.py sync
$ python3 scripts/activation.py mark-adapted --evidence "planning 2.1.0 delta inspected; new step-verification re-verified"
STATE=READY
```

## A captured improvement (learning ledger excerpt)

```json
"learning": {
  "lessons": [{
    "id": "L-003",
    "lesson": "Run discovery commands before claiming a skill is installed; source presence is not installation.",
    "origin": "install reported SUCCESS while runtime listing was empty",
    "status": "stable"
  }],
  "improvements": [{
    "id": "I-002",
    "what": "install report must quote discovery-command output",
    "kind": "procedure",
    "origin_lesson": "L-003",
    "status": "verified",
    "challenge_outcome": "survived failure/regression/overfitting/complexity/confirmation/adversarial",
    "verification": "3 subsequent installs all quoted listing output; zero false SUCCESS",
    "regression_check": "install flow unchanged for runtimes already verified"
  }]
}
```

Status discipline: `I-002` is a VERIFIED IMPROVEMENT because it carries verification
+ regression evidence. A successful task alone would not have earned that status.
