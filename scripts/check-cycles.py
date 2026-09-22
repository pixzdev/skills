#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
reg = json.loads((ROOT/"registry.json").read_text())
graph = {s["id"]: s for s in reg["skills"]}
state = {}
path = []
errors = []

def dfs(sid):
    if state.get(sid)==1:
        idx = path.index(sid)
        cycle = path[idx:] + [sid]
        errors.append(" -> ".join(cycle))
        return
    if state.get(sid)==2:
        return
    state[sid]=1
    path.append(sid)
    for dep in graph[sid].get("requires",[]) + graph[sid].get("aggregates",[]):
        if dep in graph:
            dfs(dep)
    path.pop()
    state[sid]=2

for sid in graph:
    if state.get(sid) is None:
        dfs(sid)

if errors:
    print("CYCLE DETECTED:")
    for c in errors:
        print(f"  {c}")
    sys.exit(1)
else:
    print(f"✓ No circular dependencies detected across {len(graph)} skills.")
    # also check orchestrator self-reference
    # ensure limits
    limits = reg.get("limits",{})
    print(f"  Limits: chain={limits.get('max_skill_chain_depth')} orchestration={limits.get('max_orchestration_depth')} iterations={limits.get('max_iterations')}")
