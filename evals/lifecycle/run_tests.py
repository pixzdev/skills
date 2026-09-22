#!/usr/bin/env python3
"""
Self-learning lifecycle tests — deterministic, model-free, subprocess-isolated.

What this layer VERIFIES (state-machine depth of the verification-depth ladder):
  first activation · duplicate-setup refusal · persisted state reload (fresh process)
  · skill version change · newly discovered skill · failed adaptation (no evidence /
  corrupt state) · regression of a READY adaptation after drift · doctor measured
  baseline · installed-copy integrity · sitrep · adoption assessment (auto-run at
  first-run completion) · runtime hooks wiring.

What this layer does NOT verify (honest limits): that a real model reading AGENTS.md
actually performs the behavioral half of the lifecycle. That belongs to the behavioral
evals (heuristic) and the successor benchmark (model-graded, UNRUN).

Each scenario defines: setup · input (command) · expected behavior · failure condition
· verification (assertion). Run: python3 evals/lifecycle/run_tests.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "activation.py"

RESULTS = []


def run(state, *args, root=None):
    cmd = [sys.executable, str(SCRIPT), "--state", str(state)]
    if root:
        cmd += ["--root", str(root)]
    cmd += list(args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def check(test_id, scenario, ok, evidence, limits=""):
    RESULTS.append((test_id, scenario, ok, evidence, limits))
    print(f"{'✓' if ok else '✗'} {test_id} — {scenario}")
    print(f"    evidence: {evidence}")
    if limits:
        print(f"    limits: {limits}")
    return ok


def fresh_root(tmp):
    """Copy of the repo root without .git — a sandboxed 'installed PixzFlow'."""
    dst = tmp / "pixzroot"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", ".pixz"))
    return dst


def test_first_activation(tmp):
    state = tmp / "a" / "state.json"
    r1 = run(state, "status", root=tmp / "pixzroot")
    r2 = run(state, "init", "--runtime", "claude", "--dim", "state_persistence=yes", root=tmp / "pixzroot")
    st = json.loads(state.read_text()) if state.exists() else {}
    inv = st.get("inventory", [])
    ok = (r1.returncode == 10 and "STATE=NEW" in r1.stdout
          and r2.returncode == 10 and "STATE=BASELINED" in r2.stdout
          and st.get("schema_version") == "1.0"
          and st["adaptation"]["status"] == "baselined"
          and len(inv) >= 29
          and st["dimensions"]["state_persistence"] == "yes"
          and st["dimensions"]["delegation"] == "unknown"  # unobserved stays unknown, not invented
          and all(e["digest"] for e in inv))
    return check("lifecycle.first-activation",
                 "first activation: NEW -> init -> BASELINED with complete digested inventory",
                 ok,
                 f"status exit={r1.returncode} ({r1.stdout.splitlines()[0] if r1.stdout else ''}); "
                 f"init exit={r2.returncode}; inventory={len(inv)} skills; unknown dims stay unknown")


def test_duplicate_setup_refused(tmp):
    state = tmp / "b" / "state.json"
    run(state, "init", root=tmp / "pixzroot")
    before = state.read_bytes()
    r = run(state, "init", root=tmp / "pixzroot")
    after = state.read_bytes()
    ok = r.returncode == 10 and "refusing duplicate setup" in r.stdout and before == after
    return check("lifecycle.second-activation-duplicate-guard",
                 "second activation: init refuses to duplicate setup; state byte-identical",
                 ok, f"exit={r.returncode}; state_changed={before != after}")


def test_reload_and_ready(tmp):
    state = tmp / "c" / "state.json"
    run(state, "init", root=tmp / "pixzroot")
    run(state, "mark-adapted", "--evidence", "validate.py passed; behavioral runner 33/33; probe transitions observed", root=tmp / "pixzroot")
    # fresh process reload — the ONLY persistence proof that survives a session boundary here
    r = run(state, "status", root=tmp / "pixzroot")
    ok = r.returncode == 0 and "STATE=READY" in r.stdout and "do NOT re-run setup" in r.stdout
    return check("lifecycle.persisted-reload",
                 "persisted state reload in a FRESH process reports READY with evidence",
                 ok, f"fresh-process status exit={r.returncode}; line0={r.stdout.splitlines()[0] if r.stdout else ''}")


def bump_skill(root, sid, new_version, touch_content=False):
    reg = json.loads((root / "registry.json").read_text())
    for s in reg["skills"]:
        if s["id"] == sid:
            s["version"] = new_version
            if touch_content:
                p = root / s["path"] / "SKILL.md"
                p.write_text(p.read_text() + "\n<!-- fixture content delta -->\n")
            break
    (root / "registry.json").write_text(json.dumps(reg, indent=2) + "\n")


def test_skill_version_change(tmp):
    root = tmp / "pixzroot"
    state = tmp / "d" / "state.json"
    run(state, "init", root=root)
    run(state, "mark-adapted", "--evidence", "fixture adaptation", root=root)
    bump_skill(root, "pixz.core.planning", "2.0.1", touch_content=True)
    r = run(state, "status", root=root)
    drift_ok = r.returncode == 10 and "STATE=STALE" in r.stdout and "version" in r.stdout and "pixz.core.planning" in r.stdout
    r2 = run(state, "sync", root=root)
    st = json.loads(state.read_text())
    sync_ok = any(h["event"] == "drift-detected" for h in st.get("history", [])) and st["adaptation"]["status"] == "stale"
    r3 = run(state, "mark-adapted", "--evidence", "inspected planning delta; no behavioral change", root=root)
    ok = drift_ok and sync_ok and r3.returncode == 0
    return check("lifecycle.skill-version-change",
                 "skill version changed: drift detected (STALE), sync records delta, re-adapt closes it",
                 ok,
                 f"status exit={r.returncode}; history={[h['event'] for h in st.get('history', [])]}; "
                 f"mark-adapted exit={r3.returncode}")


def test_version_only_no_content(tmp):
    root = tmp / "pixzroot"
    state = tmp / "e" / "state.json"
    run(state, "init", root=root)
    bump_skill(root, "pixz.core.replanning", "2.0.5", touch_content=False)
    r = run(state, "status", root=root)
    ok = "version-only" in r.stdout and "inspect before assuming" in r.stdout
    return check("lifecycle.version-without-content",
                 "version bump without content delta is reported as version-only (never assumed behavior change)",
                 ok, f"drift line: {[l for l in r.stdout.splitlines() if 'replanning' in l]}")


def test_new_skill_discovered(tmp):
    root = tmp / "pixzroot"
    state = tmp / "f" / "state.json"
    run(state, "init", root=root)
    # add a fixture skill to the sandboxed root
    reg = json.loads((root / "registry.json").read_text())
    skdir = root / "core" / "fixture-probe"
    skdir.mkdir(parents=True)
    (skdir / "SKILL.md").write_text("---\nname: Fixture Probe\ndescription: temporary fixture skill for lifecycle testing.\nversion: 0.0.1\nid: pixz.core.fixture-probe\n---\n# fixture\n")
    (skdir / "metadata.yaml").write_text("id: pixz.core.fixture-probe\nname: Fixture Probe\nversion: 0.0.1\n")
    reg["skills"].append({"id": "pixz.core.fixture-probe", "name": "Fixture Probe", "category": "core",
                          "version": "0.0.1", "status": "draft", "description": "temporary fixture skill",
                          "triggers": ["fixture probe"], "compatible_runtimes": ["generic"], "path": "core/fixture-probe"})
    (root / "registry.json").write_text(json.dumps(reg, indent=2) + "\n")
    r = run(state, "status", root=root)
    ok = r.returncode == 10 and "STATE=STALE" in r.stdout and "added" in r.stdout and "fixture-probe" in r.stdout
    r2 = run(state, "sync", root=root)
    st = json.loads(state.read_text())
    ok = ok and any(e["id"] == "pixz.core.fixture-probe" for e in st["inventory"])
    return check("lifecycle.new-skill-discovered",
                 "newly discovered skill: status reports 'added'; sync absorbs it into the inventory",
                 ok, f"status exit={r.returncode}; sync exit={r2.returncode}; inventory has fixture={any(e['id']=='pixz.core.fixture-probe' for e in st['inventory'])}")


def test_failed_adaptation(tmp):
    state = tmp / "g" / "state.json"
    run(state, "init", root=tmp / "pixzroot")
    r1 = run(state, "mark-adapted", "--evidence", "   ", root=tmp / "pixzroot")
    no_fake = r1.returncode == 1 and "REFUSED" in r1.stdout
    # corrupt/adversarial state must fail loudly, not silently continue
    state.write_text("{ this is not json")
    r2 = run(state, "status", root=tmp / "pixzroot")
    corrupt_loud = r2.returncode == 1 and "STATE=ERROR" in r2.stdout
    return check("lifecycle.failed-adaptation",
                 "failed adaptation: no-evidence mark-adapted refused; corrupt state fails loudly (exit 1)",
                 no_fake and corrupt_loud,
                 f"no-evidence exit={r1.returncode}; corrupt-state exit={r2.returncode}")


def test_regression_after_adaptation(tmp):
    root = tmp / "pixzroot"
    state = tmp / "h" / "state.json"
    run(state, "init", root=root)
    run(state, "mark-adapted", "--evidence", "fixture adaptation", root=root)
    pre = run(state, "status", root=root)
    bump_skill(root, "pixz.core.verification", "2.1.1", touch_content=True)
    post = run(state, "status", root=root)
    ok = pre.returncode == 0 and "STATE=READY" in pre.stdout and post.returncode == 10 and "STATE=STALE" in post.stdout
    return check("lifecycle.regression-after-adaptation",
                 "regression: a READY adaptation is downgraded to STALE when its environment changes",
                 ok, f"pre exit={pre.returncode} -> post exit={post.returncode}")


def test_task_state_adaptation_pointer(tmp):
    schema = json.loads((ROOT / "schemas" / "task-state.schema.json").read_text())
    adapt = schema.get("properties", {}).get("adaptation", {})
    statuses = adapt.get("properties", {}).get("status", {}).get("enum", [])
    ok = statuses == ["new", "baselined", "ready", "stale"] and "state_ref" in adapt.get("properties", {})
    return check("lifecycle.task-state-pointer",
                 "task-state schema carries the adaptation pointer (status enum + state_ref)",
                 ok, f"adaptation.status enum={statuses}")


def run_script(tmp, name, *args, root=None):
    script = ROOT / "scripts" / name
    cmd = [sys.executable, str(script)] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def test_doctor_measured_baseline(tmp):
    state = tmp / "doc" / "state.json"
    r = run_script(tmp, "doctor.py", "--root", str(tmp / "pixzroot"), "--state", str(state), "--json")
    rep = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip().startswith("{") else {}
    dims = rep.get("dimensions", {})
    ok = (r.returncode == 0
          and dims.get("state_persistence") in ("yes", "no")      # measured, not assumed
          and dims.get("verification") in ("yes", "no")
          and dims.get("delegation") == "unknown"                  # unmeasurable stays unknown
          and dims.get("research") == "unknown")
    # --write fills only unknowns and never invents the unmeasurable
    run(state, "init", "--runtime", "claude", root=tmp / "pixzroot")
    run_script(tmp, "doctor.py", "--root", str(tmp / "pixzroot"), "--state", str(state), "--write")
    st = json.loads(state.read_text())
    d = st.get("dimensions", {})
    ok = ok and d.get("delegation") == "unknown" and d.get("state_persistence") in ("yes", "no")
    return check("lifecycle.doctor-measured-baseline",
                 "doctor measures baseline dimensions; unmeasurable stay unknown (never invented)",
                 ok, f"dims={dims}; after --write: state_persistence={d.get('state_persistence')}, delegation={d.get('delegation')}")


def test_verify_installed_integrity(tmp):
    root = tmp / "pixzroot"
    state = tmp / "vi" / "state.json"
    run(state, "init", root=root)
    inst = tmp / "vi" / "installed" / "orchestrator"
    inst.mkdir(parents=True)
    import shutil as _sh
    _sh.copy(root / "core" / "orchestrator" / "SKILL.md", inst / "SKILL.md")
    _sh.copy(root / "core" / "orchestrator" / "metadata.yaml", inst / "metadata.yaml")
    r1 = run(state, "verify-installed", "--runtime", "generic",
             "--search-dir", str(tmp / "vi" / "installed"), root=root)
    clean_ok = r1.returncode == 0 and "match" in r1.stdout and "pixz.core.orchestrator" in r1.stdout
    (inst / "SKILL.md").write_text((inst / "SKILL.md").read_text() + "\n<!-- tampered -->\n")
    r2 = run(state, "verify-installed", "--runtime", "generic",
             "--search-dir", str(tmp / "vi" / "installed"), root=root)
    tamper_ok = r2.returncode == 10 and "MODIFIED" in r2.stdout
    return check("lifecycle.verify-installed-integrity",
                 "installed-copy integrity: clean copy matches (exit 0); tampered copy detected (exit 10)",
                 clean_ok and tamper_ok, f"clean exit={r1.returncode}; tampered exit={r2.returncode}")


def test_sitrep_orientation(tmp):
    root = tmp / "pixzroot"
    state = tmp / "sr" / "state.json"
    task = tmp / "sr" / "task-state.json"
    run(state, "init", root=root)
    run(state, "mark-adapted", "--evidence", "fixture", root=root)
    task.write_text(json.dumps({"task_id": "t-1", "objective": "Ship the adapter", "status": "active",
                                "mode": "balanced", "next_action": "run integration smoke",
                                "capabilities": [{"id": "pixz.core.verification", "status": "active"}]}))
    r = run_script(tmp, "sitrep.py", "--root", str(root), "--state", str(state), "--task-state", str(task))
    ok = (r.returncode == 0 and "STATE=READY" in r.stdout and "Ship the adapter" in r.stdout
          and "run integration smoke" in r.stdout and "pixz.core.verification" in r.stdout)
    return check("lifecycle.sitrep-orientation",
                 "sitrep: one block reports adaptation + task objective + next_action + active capabilities",
                 ok, f"exit={r.returncode}; lines={len(r.stdout.splitlines())}")


def test_adoption_assessment(tmp):
    root = tmp / "pixzroot"
    state = tmp / "as" / "state.json"
    # fresh environment: source present but nothing adopted -> must NOT score high
    r0 = run_script(tmp, "assess.py", "--root", str(root), "--state", str(state))
    fresh_score = int(r0.stdout.split("score:")[1].split("/")[0]) if "score:" in r0.stdout else -1
    fresh_ok = 0 <= fresh_score < 70 and "NOT ADOPTED" in r0.stdout or "PARTIALLY ADOPTED" in r0.stdout
    # full first-run: init (+ recorded dim) -> mark-installed -> mark-adapted auto-runs assessment
    run(state, "init", "--runtime", "claude", "--dim", "delegation=yes", root=root)
    run(state, "mark-installed", "--all", root=root)
    r1 = run(state, "mark-adapted", "--evidence", "fixture adoption", root=root)
    auto_ok = "ADOPTION ASSESSMENT" in r1.stdout and "score:" in r1.stdout
    adopted_score = int(r1.stdout.split("score:")[1].split("/")[0]) if "score:" in r1.stdout else -1
    st = json.loads(state.read_text())
    history_ok = any(h.get("summary", "").startswith("adoption assessment") for h in st.get("history", []))
    ok = fresh_ok and auto_ok and adopted_score >= 90 and history_ok
    return check("lifecycle.adoption-assessment",
                 "adoption score: fresh env scores low; first-run completion auto-assesses >=90 and records it in history",
                 ok, f"fresh={fresh_score}; after first-run={adopted_score}; auto-run={auto_ok}; history={history_ok}")


def test_hooks_wiring(tmp):
    root = tmp / "hooksroot"
    root.mkdir()
    (root / "AGENTS.md").write_text("# test contract\n")
    r1 = run_script(tmp, "hooks.py", "check", "--runtime", "claude", "--root", str(root))
    gap_ok = r1.returncode == 10 and "GAP" in r1.stdout
    r2 = run_script(tmp, "hooks.py", "install", "--runtime", "claude", "--root", str(root))
    wired = (root / "CLAUDE.md").read_text() if (root / "CLAUDE.md").exists() else ""
    install_ok = r2.returncode == 0 and "@AGENTS.md" in wired
    r3 = run_script(tmp, "hooks.py", "install", "--runtime", "claude", "--root", str(root))
    idempotent = r3.returncode == 0 and wired.count("@AGENTS.md") == (root / "CLAUDE.md").read_text().count("@AGENTS.md") == 1
    r4 = run_script(tmp, "hooks.py", "check", "--runtime", "openclaw", "--root", str(root))
    native_ok = r4.returncode == 0 and "natively" in r4.stdout
    return check("lifecycle.hooks-wiring",
                 "hooks: claude gap detected (exit 10) -> install wires @AGENTS.md once (idempotent); native runtimes pass without wiring",
                 gap_ok and install_ok and idempotent and native_ok,
                 f"gap exit={r1.returncode}; install exit={r2.returncode}; re-install exit={r3.returncode}; native exit={r4.returncode}")


def main():
    print("=== PixzFlow self-learning lifecycle tests (deterministic, subprocess-isolated) ===")
    with tempfile.TemporaryDirectory(prefix="pixz-lifecycle-") as td:
        tmp = Path(td)
        fresh_root(tmp)  # shared sandboxed root (tests mutate copies, never the repo)
        test_first_activation(tmp)
        test_duplicate_setup_refused(tmp)
        test_reload_and_ready(tmp)
        test_skill_version_change(tmp)
        test_version_only_no_content(tmp)
        test_new_skill_discovered(tmp)
        test_failed_adaptation(tmp)
        test_regression_after_adaptation(tmp)
        test_task_state_adaptation_pointer(tmp)
        test_doctor_measured_baseline(tmp)
        test_verify_installed_integrity(tmp)
        test_sitrep_orientation(tmp)
        test_adoption_assessment(tmp)
        test_hooks_wiring(tmp)
    passed = sum(1 for r in RESULTS if r[2])
    print(f"\n{passed}/{len(RESULTS)} lifecycle tests passed.")
    print("limits: state-machine depth only (verification-depth ladder). The behavioral half —")
    print("a real model reading AGENTS.md and actually adapting — is heuristic-eval + successor-benchmark territory (UNRUN).")
    sys.exit(0 if passed == len(RESULTS) else 1)


if __name__ == "__main__":
    main()
