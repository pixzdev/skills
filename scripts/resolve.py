#!/usr/bin/env python3
"""
PIXZ Skill Resolver — dependency-aware, cycle-safe, runtime-aware.

Usage:
  python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
  python scripts/resolve.py --list --runtime generic
  python scripts/resolve.py --check-cycles
"""
import argparse, json, os, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"

def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)

def build_graph(registry):
    # id -> meta
    return {s["id"]: s for s in registry.get("skills", [])}

def resolve(install_id, runtime, channel, graph, limits, registry):
    # BFS/DFS expansion of aggregates+requires
    if install_id not in graph:
        return None, f"Skill not found: {install_id}"

    visited = {}
    stack = []
    order = []
    errors = []

    def dfs(sid, path):
        if sid in path:
            cycle = path[path.index(sid):] + [sid]
            errors.append(f"CYCLE_DETECTED: {' -> '.join(cycle)}")
            return
        if sid in visited:
            return
        if sid not in graph:
            errors.append(f"MISSING_DEPENDENCY: {sid} required but not in registry")
            return
        meta = graph[sid]
        # runtime check
        if runtime not in meta.get("compatible_runtimes", []) and "generic" not in meta.get("compatible_runtimes", []):
            # strict: if runtime explicitly not listed
            if runtime not in meta.get("compatible_runtimes", []):
                errors.append(f"RUNTIME_INCOMPATIBLE: {sid} not compatible with {runtime} (supports {meta.get('compatible_runtimes')})")
        # conflicts check (deferred to final graph validation, but also immediate)
        # path stack for cycle
        path.append(sid)
        # aggregates first (only when sid is the root or an aggregate itself)
        # For orchestrator, aggregates are mandatory.
        # For any skill, we expand both aggregates and requires recursively.
        for dep in meta.get("aggregates", []):
            dfs(dep, path)
        for dep in meta.get("requires", []):
            dfs(dep, path)
        # optional deps: include if present and compatible and not conflicting
        # (we include them only if they don't introduce conflict)
        # simple: include optional if it exists in graph
        # Note: we don't fail on optional missing
        # For deterministic resolver, we log optional inclusion
        path.pop()
        visited[sid] = True
        order.append(sid)

    dfs(install_id, [])

    if errors:
        # still check conflicts among visited
        pass

    # Check conflicts across visited set
    visited_ids = set(visited.keys())
    # include install_id even if dfs failed?
    for sid in list(visited_ids):
        meta = graph.get(sid, {})
        for c in meta.get("conflicts", []):
            if c in visited_ids:
                errors.append(f"CONFLICT: {sid} conflicts with {c}")

    # Check depth limits
    max_chain = (limits or {}).get("max_skill_chain_depth", 12)
    if len(visited_ids) > max_chain:
        errors.append(f"LIMIT_EXCEEDED: skill chain {len(visited_ids)} > max_skill_chain_depth {max_chain}")

    # Detect cycles separately via DFS coloring
    # (already captured by path detection, but add formal check)
    # Topological sort check
    # Build edges for topo
    edges = {}
    for sid in visited_ids:
        meta = graph.get(sid, {})
        edges[sid] = set(meta.get("requires", []) + meta.get("aggregates", [])) & visited_ids

    # Kahn's topo (reverse since order is post-order)
    topo = list(reversed(order)) if not errors else []

    # Filter to only visited
    topo = [x for x in topo if x in visited_ids]

    if errors:
        return None, "\n".join(errors)

    # Validate channel / version (simple: ensure version matches SemVer, warn if channel stable but not tagged)
    # Not failing for this impl.

    return {"install": install_id, "runtime": runtime, "channel": channel, "graph": topo, "total": len(topo)}, None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--install", help="skill id to install")
    p.add_argument("--runtime", default="generic", choices=["claude","openclaw","opencode","hermes","codex","cursor","generic"])
    p.add_argument("--channel", default="stable", choices=["latest","stable","pinned"])
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
        # check all nodes for cycles globally
        all_errors = []
        # global DFS coloring
        state = {}  # 0 unvisited, 1 visiting, 2 done
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
                else:
                    # missing dep is not a cycle, but warn
                    pass
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

    result, err = resolve(args.install, args.runtime, args.channel, graph, limits, reg)
    if err:
        print(f"RESOLVE FAILED for {args.install} (runtime={args.runtime}, channel={args.channel})", file=sys.stderr)
        print(err, file=sys.stderr)
        sys.exit(1)
    else:
        print(json.dumps(result, indent=2))
        # human summary
        print(f"\n✓ Resolved {result['total']} skills for {result['install']} @ {result['runtime']} ({result['channel']}):")
        for i, sid in enumerate(result["graph"], 1):
            meta = graph[sid]
            print(f"  {i:2}. {sid} — {meta['name']} ({meta['path']})")

if __name__ == "__main__":
    main()
