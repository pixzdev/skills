#!/usr/bin/env python3
"""
PIXZ Skill Resolver — dependency-aware, cycle-safe, runtime-aware.
v2.0.0: optional deps are opt-in via --with-optional (audit fix #7/#8); orchestrator aggregates reduced to the evidence floor.

Usage:
  python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
  python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional
  python scripts/resolve.py --list --runtime generic
  python scripts/resolve.py --check-cycles

Lockfile (pixz.lock) — the `pinned` channel, now real:
  python scripts/resolve.py --install X --runtime R --channel stable --lock pixz.lock   # resolve + WRITE/update the lock
  python scripts/resolve.py --install X --runtime R --channel pinned  --lock pixz.lock  # resolve + VERIFY every version against the lock
Pinned + missing lock → fail. Pinned + any version drift (LOCK_MISMATCH) or missing entry
(LOCK_MISSING_ENTRY) → fail. Exit 1. Default lock path: <repo>/pixz.lock.
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"

def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)

def build_graph(registry):
    return {s["id"]: s for s in registry.get("skills", [])}

def load_lock(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["_source"] = str(p)
        return doc
    except Exception as e:
        return {"skills": None, "_source": str(p), "_error": str(e)}


def save_lock(path, graph_versions, install_id, runtime, channel):
    from datetime import datetime, timezone
    p = Path(path)
    doc = load_lock(p)
    skills = (doc or {}).get("skills") or {}
    skills.update(graph_versions)
    p.write_text(json.dumps({
        "schema": "pixz/lock/1",
        "channel": "pinned",
        "created_at": doc.get("created_at") if doc and doc.get("created_at") else datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pinned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pinned_by": f"resolve.py --install {install_id} --runtime {runtime} --channel {channel}",
        "skills": dict(sorted(skills.items())),
    }, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return str(p)


def resolve(install_id, runtime, channel, graph, limits, registry, with_optional=False, lock=None):
    if install_id not in graph:
        return None, f"Skill not found: {install_id}"

    visited = {}  # sid -> True
    order = []
    errors = []
    excluded_optional = []  # list of {id, reason, parent}
    excluded_incompatible = []

    def dfs(sid, path, is_optional_path=False):
        if sid in path:
            cycle = path[path.index(sid):] + [sid]
            errors.append(f"CYCLE_DETECTED: {' -> '.join(cycle)}")
            return
        if sid in visited:
            return
        if sid not in graph:
            if is_optional_path:
                # optional missing is not fatal — record excluded
                excluded_optional.append({"id": sid, "reason": "optional_not_in_registry", "parent": path[-1] if path else None})
                return
            errors.append(f"MISSING_DEPENDENCY: {sid} required but not in registry")
            return
        meta = graph[sid]
        # runtime check — for required/aggregates it's hard fail; for optional it's exclusion
        compat = runtime in meta.get("compatible_runtimes", []) or "generic" in meta.get("compatible_runtimes", [])
        # strict: if runtime not in list, treat as incompatible
        if runtime not in meta.get("compatible_runtimes", []) and "generic" not in meta.get("compatible_runtimes", []):
            if is_optional_path:
                excluded_optional.append({"id": sid, "reason": f"runtime_incompatible_{runtime}", "parent": path[-1] if path else None})
                return
            # for required, record error later but also track as excluded_incompatible
            if not compat:
                # still dfs to collect errors, but will fail
                pass

        # runtime hard failure for non-optional
        if not is_optional_path and runtime not in meta.get("compatible_runtimes", []):
            # allow generic as fallback, else error
            if "generic" not in meta.get("compatible_runtimes", []):
                errors.append(f"RUNTIME_INCOMPATIBLE: {sid} not compatible with {runtime} (supports {meta.get('compatible_runtimes')})")

        path.append(sid)
        # aggregates and requires are always mandatory
        for dep in meta.get("aggregates", []):
            dfs(dep, path, is_optional_path=False)
        for dep in meta.get("requires", []):
            dfs(dep, path, is_optional_path=False)
        # optional: only if with_optional, else collect as excluded
        for dep in meta.get("optional", []):
            if with_optional:
                dfs(dep, path, is_optional_path=True)
            else:
                # record excluded if not already visited and not excluded before
                if dep not in visited and dep not in [e["id"] for e in excluded_optional]:
                    excluded_optional.append({"id": dep, "reason": "optional_not_requested", "parent": sid})
        path.pop()
        # only mark visited if we actually processed (not excluded)
        if sid not in visited:
            visited[sid] = True
            order.append(sid)

    dfs(install_id, [])

    visited_ids = set(visited.keys())

    # Check conflicts across visited set (hard fail)
    for sid in list(visited_ids):
        meta = graph.get(sid, {})
        for c in meta.get("conflicts", []):
            if c in visited_ids:
                errors.append(f"CONFLICT: {sid} conflicts with {c}")
            # also if conflict is in excluded_optional with --with-optional, it's also conflict

    # If with_optional, check conflicts where optional introduces conflict with mandatory
    if with_optional:
        for ex in excluded_optional:
            # shouldn't happen because dfs would have added, but if conflict prevented optional inclusion, we already excluded
            pass

    # Prune excluded_optional that are actually already satisfied via mandatory path
    # e.g., planning's optional environment-awareness is already mandatory via change-safety
    excluded_optional = [e for e in excluded_optional if e["id"] not in visited_ids]

    # Depth limits
    max_chain = (limits or {}).get("max_skill_chain_depth", 12)
    if len(visited_ids) > max_chain:
        errors.append(f"LIMIT_EXCEEDED: skill chain {len(visited_ids)} > max_skill_chain_depth {max_chain}")

    # Topo (post-order reversed)
    topo = list(reversed(order)) if not errors else []
    topo = [x for x in topo if x in visited_ids]

    # Channel validation — pinned verifies against the lockfile (pixz.lock)
    if channel == "pinned" and lock is not None:
        if lock.get("skills") is None:
            errors.append(f"LOCK_INVALID: {lock.get('_source', 'lockfile')} has no skills map")
        else:
            for sid in visited_ids:
                locked = lock["skills"].get(sid)
                current = graph[sid].get("version")
                if locked is None:
                    errors.append(f"LOCK_MISSING_ENTRY: {sid} resolved but not in lock (add it or re-pin)")
                elif locked != current:
                    errors.append(f"LOCK_MISMATCH: {sid} locked at {locked}, registry has {current}")

    if errors:
        return None, "\n".join(errors)

    return {
        "install": install_id,
        "runtime": runtime,
        "channel": channel,
        "with_optional": with_optional,
        "graph": topo,
        "total": len(topo),
        "versions": {sid: graph[sid].get("version") for sid in topo},
        "excluded_optional": excluded_optional,
        "excluded_incompatible": excluded_incompatible,
    }, None

def main():
    p = argparse.ArgumentParser(description="PixzFlow Skill Resolver (v2.0.0)")
    p.add_argument("--install", help="skill id to install")
    p.add_argument("--runtime", default="generic", choices=["claude","openclaw","opencode","hermes","codex","cursor","generic"])
    p.add_argument("--channel", default="stable", choices=["latest","stable","pinned"],
                   help="pinned verifies the resolved graph against --lock (pixz.lock); non-pinned + --lock writes/updates the lock")
    p.add_argument("--lock", help="path to pixz.lock (default: ./pixz.lock when used)")
    p.add_argument("--with-optional", action="store_true", help="include optional dependencies (otherwise they are reported as excluded)")
    p.add_argument("--list", action="store_true", help="list all skills")
    p.add_argument("--check-cycles", action="store_true", help="check all cycles")
    args = p.parse_args()

    reg = load_registry()
    graph = build_graph(reg)
    limits = reg.get("limits", {})

    if args.list:
        for s in reg["skills"]:
            print(f"{s['id']:<32} {s['version']:<8} {s['category']:<12} {','.join(s['compatible_runtimes'])}  # {s['description'][:60]}")
        return

    if args.check_cycles:
        all_errors = []
        state = {}
        path = []
        def dfs_global(sid):
            if state.get(sid) == 1:
                idx = path.index(sid)
                cycle = path[idx:] + [sid]
                all_errors.append(f"CYCLE: {' -> '.join(cycle)}")
                return
            if state.get(sid) == 2:
                return
            state[sid] = 1
            path.append(sid)
            meta = graph.get(sid, {})
            for dep in (meta.get("requires", []) + meta.get("aggregates", [])):
                if dep in graph:
                    dfs_global(dep)
            path.pop()
            state[sid] = 2
        for sid in graph:
            if state.get(sid) is None:
                dfs_global(sid)
        if all_errors:
            print("\n".join(all_errors))
            sys.exit(1)
        else:
            print("No cycles detected.")
        return

    if not args.install:
        p.print_help()
        sys.exit(2)

    lock_path = args.lock or (str(ROOT / "pixz.lock") if args.channel == "pinned" else None)
    lock = load_lock(lock_path) if lock_path else None
    if args.channel == "pinned" and lock is None:
        print(f"RESOLVE FAILED: --channel pinned requires a lockfile (expected {lock_path}); "
              f"run once with --channel stable --lock {lock_path} to pin, or pass --lock PATH", file=sys.stderr)
        sys.exit(1)

    result, err = resolve(args.install, args.runtime, args.channel, graph, limits, reg,
                          with_optional=args.with_optional, lock=lock)
    if err:
        print(f"RESOLVE FAILED for {args.install} (runtime={args.runtime}, channel={args.channel}, with_optional={args.with_optional})", file=sys.stderr)
        print(err, file=sys.stderr)
        # also print current excluded for debugging if any
        sys.exit(1)
    else:
        print(json.dumps(result, indent=2))
        print(f"\n✓ Resolved {result['total']} skills for {result['install']} @ {result['runtime']} ({result['channel']}, with_optional={result['with_optional']}):")
        for i, sid in enumerate(result["graph"], 1):
            meta = graph[sid]
            print(f"  {i:2}. {sid} — {meta['name']} ({meta['path']})")
        if result["excluded_optional"]:
            print(f"\n  Excluded optional ({len(result['excluded_optional'])}):")
            for ex in result["excluded_optional"]:
                print(f"    - {ex['id']} (reason: {ex['reason']}, parent: {ex['parent']})")
            if not result["with_optional"]:
                print(f"    → Re-run with --with-optional to include them (if compatible & non-conflicting).")
        if result["channel"] == "pinned":
            print(f"\n  Pinned channel: graph verified against {lock_path} (all locked versions match the registry).")
        elif lock_path:
            written = save_lock(lock_path, result["versions"], args.install, args.runtime, args.channel)
            print(f"\n  Lock written: {written} ({len(result['versions'])} skill versions pinned)")

if __name__ == "__main__":
    main()
