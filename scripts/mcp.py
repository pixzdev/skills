#!/usr/bin/env python3
"""
PIXZ MCP auto-config — vetted, free + no-signup-first MCP server integration.

Stdlib-only. Companion to skill `pixz.core.mcp` and `mcp/catalog.json`.

Commands:
  list      [--tier T] [--transport T] [--category C] [--json]   catalog listing
  tier      <minimal|medium|full>                                 what a setup tier installs
  check     <id>|<id...>|--all [--timeout S] [--json]            LIVE probe: initialize + tools/list
  add       <id>|<id...> --runtime <rt> [--dry-run] [--json]     idempotent, non-destructive config write
  remove    <id>|<id...> --runtime <rt> [--dry-run] [--json]     remove catalog-managed entries
  status    [--runtime <rt>] [--json]                            configured servers + last check evidence
  detect                                                            which runtimes are present here

Evidence: check results are written to .pixz/mcp-check.json (timestamp, per-server
status, tool counts). Docs-verification in the catalog is NOT liveness proof —
the check file is. Exit codes: 0 ok · 10 partial (some checks failed) · 1 error.

Security: the catalog universe is auth-none by construction. This tool never
writes credentials into config artifacts and never overwrites user-modified
config entries (it reports them instead).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "mcp" / "catalog.json"
EVIDENCE_DIR = ROOT / ".pixz"
EVIDENCE_PATH = EVIDENCE_DIR / "mcp-check.json"
PROTOCOL_VERSION = "2025-06-18"
CLIENT_INFO = {"name": "pixz-mcp", "version": "1.0.0"}

RUNTIME_CONFIGS = {
    # runtime -> (project-relative config file, container key, shape)
    "claude": (".mcp.json", "mcpServers", "json"),
    "cursor": (".cursor/mcp.json", "mcpServers", "json"),
    "opencode": ("opencode.json", "mcp", "json"),
    "codex": (None, None, "toml-snippet"),  # printed, never clobbered
    "generic": (".mcp.json", "mcpServers", "json"),
}


# ---------------------------------------------------------------- catalog

def load_catalog():
    if not CATALOG_PATH.exists():
        sys.exit(f"catalog missing: {CATALOG_PATH}")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def servers(catalog=None):
    catalog = catalog or load_catalog()
    return {s["id"]: s for s in catalog["servers"]}


def resolve_server(sid, catalog=None):
    """Resolve a catalog id to a concrete server dict (gitmcp URL auto-filled from git)."""
    catalog = catalog or load_catalog()
    by_id = servers(catalog)
    if sid not in by_id:
        return None
    s = dict(by_id[sid])
    if s.get("url_template"):
        s["url"] = fill_gitmcp_template(s["url_template"])
    return s


def fill_gitmcp_template(template):
    remote = git_remote_url()
    if not remote:
        return None
    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$", remote)
    if not m:
        return None
    return template.format(owner=m.group("owner"), repo=m.group("repo"))


def git_remote_url():
    try:
        out = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10, cwd=str(ROOT),
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return None


def tier_server_ids(tier, catalog=None):
    catalog = catalog or load_catalog()
    spec = catalog["tiers"].get(tier)
    if not spec:
        return None
    ids = spec.get("servers", [])
    if ids == "all":
        return sorted(servers(catalog).keys())
    return ids


# ---------------------------------------------------------------- config files

def config_file(runtime, root=None):
    root = Path(root) if root else Path.cwd()
    entry = RUNTIME_CONFIGS.get(runtime)
    if not entry or not entry[0]:
        return None
    return root / entry[0]


def load_json_config(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"config file {path} is not valid JSON — refusing to merge ({e}). Fix manually; this tool never clobbers.")


def write_json_config(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    # EXISTS + PARSES verification (re-read after write)
    json.loads(path.read_text(encoding="utf-8"))


def spec_for(s, runtime):
    """Emit the runtime-specific spec for a server."""
    if s.get("command"):
        cmd, args = s["command"], list(s.get("args", []))
        if runtime == "opencode":
            return {"type": "local", "command": [cmd] + args, "enabled": True}
        return {"command": cmd, "args": args}
    url = s.get("url")
    if not url:
        return None
    if runtime == "opencode":
        return {"type": "remote", "url": url, "enabled": True}
    return {"url": url}


def codex_snippet(s, sid):
    if s.get("command"):
        args = " ".join([s["command"]] + list(s.get("args", [])))
        return f'[mcp_servers.{sid}]\ncommand = "{args}"'
    return f'[mcp_servers.{sid}]\nurl = "{s.get("url")}"'


# ---------------------------------------------------------------- live checks

def _http_post_jsonrpc(url, method, params, session_id=None, timeout=30):
    """POST one JSON-RPC request to a streamable-HTTP MCP endpoint. Returns (result, detail, error)."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        ctype = r.headers.get("Content-Type", "")
        raw = r.read(200000).decode("utf-8", "replace")
        new_session = r.headers.get("Mcp-Session-Id")
    payload = raw
    if "text/event-stream" in ctype:
        payload = sse_first_data(raw)
    try:
        doc = json.loads(payload)
    except Exception:
        return None, raw[:300], new_session
    if isinstance(doc, dict) and doc.get("error"):
        return None, json.dumps(doc["error"])[:300], new_session
    return (doc.get("result") if isinstance(doc, dict) else None), raw[:300], new_session


def sse_first_data(raw):
    """Extract the first `data:` JSON payload from an SSE body."""
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            candidate = line[5:].strip()
            try:
                json.loads(candidate)
                return candidate
            except Exception:
                continue
    return None


def _http_sse_endpoint(url, timeout=30):
    """For legacy SSE servers: GET the endpoint stream, return the `endpoint` event data (POST target path)."""
    req = urllib.request.Request(url, headers={"Accept": "text/event-stream"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if "text/event-stream" not in r.headers.get("Content-Type", ""):
            raise RuntimeError(f"expected text/event-stream, got {r.headers.get('Content-Type')}")
        buf = b""
        while b"event: endpoint" not in buf:
            chunk = r.read(1024)
            if not chunk:
                raise RuntimeError("SSE stream closed before `endpoint` event")
            buf += chunk
            if len(buf) > 200000:
                raise RuntimeError("SSE endpoint event not found")
    text = buf.decode("utf-8", "replace")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("event: endpoint"):
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].strip().startswith("data:"):
                    return lines[j].strip()[5:].strip()
    raise RuntimeError("endpoint event without data")


def check_remote(s, sid, timeout):
    """Streamable HTTP or legacy SSE: initialize + tools/list. Returns (ok, tools, detail)."""
    url = s.get("url")
    if not url:
        return False, 0, "no resolved URL (is the git remote set?)"
    transport = s.get("transport", "")
    if transport == "remote-sse" or url.endswith("/sse"):
        try:
            target = url
            session = None
            try:
                path = _http_sse_endpoint(url, timeout=timeout)
                target = url.rstrip("/") + ("/" + path.lstrip("/") if not path.startswith("http") else "")
                if path.startswith("http"):
                    target = path
            except Exception:
                # some SSE servers accept POST directly on the /sse URL
                target = url
            result, detail, _ = _http_post_jsonrpc(
                target, "initialize",
                {"protocolVersion": PROTOCOL_VERSION, "capabilities": {}, "clientInfo": CLIENT_INFO},
                session_id=session, timeout=timeout)
            if not result:
                return False, 0, f"initialize failed: {detail}"
            tools_res, detail2, _ = _http_post_jsonrpc(target, "tools/list", {}, session_id=session, timeout=timeout)
            tools = len((tools_res or {}).get("tools", []))
            return True, tools, f"initialize ok; tools/list ok"
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read(300).decode("utf-8", "replace")
            except Exception:
                pass
            return False, 0, f"HTTP {e.code}: {body[:200]}"
        except Exception as e:
            return False, 0, f"{type(e).__name__}: {e}"
    else:
        try:
            result, detail, session = _http_post_jsonrpc(
                url, "initialize",
                {"protocolVersion": PROTOCOL_VERSION, "capabilities": {}, "clientInfo": CLIENT_INFO},
                timeout=timeout)
            if not result:
                return False, 0, f"initialize failed: {detail}"
            tools_res, detail2, _ = _http_post_jsonrpc(url, "tools/list", {}, session_id=session, timeout=timeout)
            tools = len((tools_res or {}).get("tools", []))
            return True, tools, "initialize ok; tools/list ok"
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read(300).decode("utf-8", "replace")
            except Exception:
                pass
            return False, 0, f"HTTP {e.code}: {body[:200]}"
        except Exception as e:
            return False, 0, f"{type(e).__name__}: {e}"


def _read_stdio_response(proc, want_id, lines_out, timeout):
    """Read stdout lines until a JSON-RPC response with `id == want_id` appears."""
    found = threading.Event()

    def reader():
        try:
            for line in iter(proc.stdout.readline, b""):
                lines_out.append(line.decode("utf-8", "replace"))
                if len(lines_out) > 500:
                    break
                stripped = line.decode("utf-8", "replace").strip()
                if not stripped.startswith("{"):
                    continue
                try:
                    doc = json.loads(stripped)
                except Exception:
                    continue
                if isinstance(doc, dict) and doc.get("id") == want_id and ("result" in doc or "error" in doc):
                    found.set()
                    return
        except Exception:
            pass

    t = threading.Thread(target=reader, daemon=True)
    t.start()
    if not found.wait(timeout):
        return None
    for line in lines_out:
        stripped = line.strip()
        if stripped.startswith("{"):
            try:
                doc = json.loads(stripped)
            except Exception:
                continue
            if isinstance(doc, dict) and doc.get("id") == want_id:
                return doc
    return None


def check_stdio(s, sid, timeout):
    """Spawn the stdio server, run initialize + tools/list. Returns (ok, tools, detail)."""
    cmd = [s["command"]] + list(s.get("args", []))
    if cmd and cmd[0].startswith("npx") and not shutil.which(cmd[0]):
        return False, 0, f"runner not found: {cmd[0]} (install Node 18+)"
    proc = None
    try:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=str(ROOT),
        )
        lines_out = []
        init = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {}, "clientInfo": CLIENT_INFO}}
        proc.stdin.write((json.dumps(init) + "\n").encode())
        proc.stdin.flush()
        resp = _read_stdio_response(proc, 1, lines_out, timeout)
        if resp is None:
            stderr = ""
            try:
                if proc.poll() is not None:
                    stderr = (proc.stderr.read() or b"").decode("utf-8", "replace")[:300]
            except Exception:
                pass
            return False, 0, f"no initialize response within {timeout}s (first `npx` run downloads the package — retry with a larger --timeout). stderr: {stderr}"
        if "error" in resp:
            return False, 0, f"initialize error: {json.dumps(resp['error'])[:300]}"
        # initialized notification, then tools/list
        try:
            proc.stdin.write((json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n").encode())
            proc.stdin.flush()
        except Exception:
            pass
        tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        proc.stdin.write((json.dumps(tools_req) + "\n").encode())
        proc.stdin.flush()
        resp2 = _read_stdio_response(proc, 2, lines_out, min(30, timeout))
        if resp2 is None or "result" not in resp2:
            return True, 0, "initialize ok; tools/list not observed (server may require the initialized notification first)"
        tools = len(resp2.get("result", {}).get("tools", []))
        return True, tools, "initialize ok; tools/list ok"
    except Exception as e:
        return False, 0, f"{type(e).__name__}: {e}"
    finally:
        if proc is not None:
            try:
                proc.kill()
                proc.wait(timeout=5)
            except Exception:
                pass


def load_evidence():
    if EVIDENCE_PATH.exists():
        try:
            return json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"checked_at": None, "servers": {}}


def save_evidence(doc):
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def run_check(ids, timeout, as_json=False):
    catalog = load_catalog()
    by_id = servers(catalog)
    results = {}
    failed = 0
    for sid in ids:
        s = resolve_server(sid, catalog)
        if s is None:
            results[sid] = {"status": "FAILED", "tools": 0, "detail": f"not in catalog ({CATALOG_PATH.name})"}
            failed += 1
            continue
        if s.get("command"):
            ok, tools, detail = check_stdio(s, sid, timeout)
        else:
            ok, tools, detail = check_remote(s, sid, timeout)
        results[sid] = {
            "status": "OK" if ok else "FAILED",
            "tools": tools,
            "detail": detail,
            "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "transport": s.get("transport"),
        }
        if not ok:
            failed += 1
    # merge into evidence file
    ev = load_evidence()
    for sid, r in results.items():
        ev["servers"][sid] = r
    ev["checked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_evidence(ev)
    if as_json:
        print(json.dumps({"results": results, "evidence": str(EVIDENCE_PATH)}, indent=2))
    else:
        for sid, r in results.items():
            mark = "OK  " if r["status"] == "OK" else "FAIL"
            extra = f" tools={r['tools']}" if r["status"] == "OK" else ""
            print(f"{mark} {sid:22s} {r['status']}{extra} — {r['detail'][:160]}")
        print(f"evidence: {EVIDENCE_PATH.relative_to(ROOT) if EVIDENCE_PATH.is_relative_to(ROOT) else EVIDENCE_PATH}")
    if failed:
        print(f"partial: {failed}/{len(ids)} live checks failed — failed servers must NOT be wired", file=sys.stderr)
        return 10
    return 0


# ---------------------------------------------------------------- add / remove

def cmd_add(ids, runtime, dry_run, as_json):
    catalog = load_catalog()
    path = config_file(runtime)
    entry = RUNTIME_CONFIGS.get(runtime)
    if not entry:
        sys.exit(f"unknown runtime: {runtime} (known: {', '.join(RUNTIME_CONFIGS)})")
    actions = {}
    cfg = load_json_config(path) if path else {}
    container_key = entry[1]
    for sid in ids:
        s = resolve_server(sid, catalog)
        if s is None:
            actions[sid] = {"action": "skipped", "detail": "not in catalog"}
            continue
        spec = spec_for(s, runtime)
        if spec is None:
            actions[sid] = {"action": "skipped", "detail": "could not resolve a URL for this runtime (git remote missing?)"}
            continue
        if runtime == "codex" or not path:
            actions[sid] = {"action": "printed", "detail": "codex: add this snippet to ~/.codex/config.toml", "snippet": codex_snippet(s, sid)}
            continue
        container = cfg.setdefault(container_key, {})
        if sid in container:
            if container[sid] == spec:
                actions[sid] = {"action": "exists", "detail": "already configured (identical)"}
            else:
                actions[sid] = {"action": "exists", "detail": "user-modified entry present — NOT overwritten (idempotency rule)"}
        else:
            container[sid] = spec
            actions[sid] = {"action": "added", "detail": f"written to {path}"}
    if not dry_run:
        if runtime != "codex" and path:
            write_json_config(path, cfg)
    out = {"runtime": runtime, "config_file": str(path) if path else "(codex: ~/.codex/config.toml)", "dry_run": dry_run, "actions": actions}
    if as_json:
        print(json.dumps(out, indent=2))
    else:
        print(f"runtime: {runtime} · config: {out['config_file']} · dry_run: {dry_run}")
        for sid, a in actions.items():
            print(f"  {a['action']:8s} {sid:22s} {a['detail']}")
            if "snippet" in a:
                print(a["snippet"])
    return 0


def cmd_remove(ids, runtime, dry_run, as_json):
    catalog = load_catalog()
    path = config_file(runtime)
    entry = RUNTIME_CONFIGS.get(runtime)
    if not entry or not path:
        sys.exit(f"runtime {runtime} has no JSON config this tool manages")
    cfg = load_json_config(path)
    container = cfg.get(entry[1], {})
    actions = {}
    for sid in ids:
        if sid in container:
            del container[sid]
            actions[sid] = {"action": "removed", "detail": f"removed from {path}"}
        else:
            actions[sid] = {"action": "absent", "detail": "not in config (nothing removed)"}
    if not dry_run:
        write_json_config(path, cfg)
    out = {"runtime": runtime, "config_file": str(path), "dry_run": dry_run, "actions": actions}
    if as_json:
        print(json.dumps(out, indent=2))
    else:
        for sid, a in actions.items():
            print(f"  {a['action']:8s} {sid:22s} {a['detail']}")
    return 0


# ---------------------------------------------------------------- list / tier / status / detect

def cmd_list(args):
    catalog = load_catalog()
    rows = list(catalog["servers"])
    if args.tier:
        ids = tier_server_ids(args.tier, catalog)
        if ids is None:
            sys.exit(f"unknown tier: {args.tier}")
        rows = [r for r in rows if r["id"] in ids]
    if args.transport:
        rows = [r for r in rows if args.transport in r.get("transport", "")]
    if args.category:
        rows = [r for r in rows if r.get("category") == args.category]
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    print(f"{'ID':22s} {'TRANSPORT':22s} {'TIER':4s} {'CAT':10s} TARGET")
    for r in rows:
        target = r.get("url") or r.get("url_template") or " ".join([r["command"]] + list(r.get("args", [])))
        print(f"{r['id']:22s} {r['transport']:22s} {r['tier']:4s} {r.get('category',''):10s} {target}")
    print(f"\n{len(rows)} server(s) — all free + no signup + no API key. Sources & verification: {CATALOG_PATH.relative_to(ROOT)}")
    return 0


def cmd_tier(args):
    catalog = load_catalog()
    spec = catalog["tiers"].get(args.name)
    if not spec:
        sys.exit(f"unknown tier: {args.name} (known: {', '.join(catalog['tiers'])})")
    if args.json:
        print(json.dumps(spec, indent=2))
        return 0
    print(f"Tier: {args.name}")
    print(f"  {spec['description']}")
    print(f"  skills: {spec.get('skills')}")
    ids = spec.get("servers", [])
    if ids == "all":
        print(f"  mcp servers: ALL ({len(catalog['servers'])} vetted entries)")
    else:
        print(f"  mcp servers: {', '.join(ids) if ids else '(none — native tools only)'}")
    return 0


def cmd_status(args, as_json):
    catalog = load_catalog()
    by_id = servers(catalog)
    runtimes = [args.runtime] if args.runtime else list(RUNTIME_CONFIGS)
    ev = load_evidence()
    out = {"runtimes": {}, "last_check": None}
    for rt in runtimes:
        path = config_file(rt)
        configured = {}
        if path and path.exists():
            cfg = load_json_config(path)
            entry = RUNTIME_CONFIGS[rt]
            for sid, spec in (cfg.get(entry[1]) or {}).items():
                in_catalog = sid in by_id
                last = ev["servers"].get(sid)
                configured[sid] = {
                    "in_catalog": in_catalog,
                    "spec": spec,
                    "last_check": (last["status"] + (f" tools={last['tools']}" if last.get("tools") is not None else "")) if last else None,
                }
        out["runtimes"][rt] = {"config_file": str(path) if path else f"({rt}: no JSON config managed by this tool)", "configured": configured}
    out["last_check"] = ev.get("checked_at")
    if as_json:
        print(json.dumps(out, indent=2))
        return 0
    for rt, info in out["runtimes"].items():
        print(f"runtime {rt}: {info['config_file']}")
        if not info["configured"]:
            print("  (nothing configured)")
        for sid, c in info["configured"].items():
            cat = "" if c["in_catalog"] else "  [NOT in catalog — T3? vet before trusting]"
            print(f"  {sid:22s} last_check={c['last_check'] or '-'}{cat}")
    print(f"last check run: {out['last_check'] or '(never)'} — evidence: .pixz/mcp-check.json")
    return 0


def cmd_detect(_args):
    found = []
    checks = [
        ("claude", Path.cwd() / "CLAUDE.md", shutil.which("claude"), Path.home() / ".claude"),
        ("cursor", Path.cwd() / ".cursor", shutil.which("cursor"), None),
        ("opencode", Path.cwd() / "opencode.json", shutil.which("opencode"), Path.home() / ".config" / "opencode"),
        ("codex", None, shutil.which("codex"), Path.home() / ".codex"),
        ("openclaw", None, shutil.which("openclaw"), Path.home() / ".openclaw"),
    ]
    for name, project, cli, home in checks:
        hits = []
        if project and (project.is_file() or project.is_dir()):
            hits.append(f"project marker: {project.name}")
        if cli:
            hits.append(f"cli: {cli}")
        if home and home.exists():
            hits.append(f"home dir: {home}")
        if hits:
            found.append(name)
            print(f"  ✓ {name:10s} — {', '.join(hits)}")
    if not found:
        print("  no known runtime markers — use --runtime generic (.mcp.json)")
    print(f"detected: {', '.join(found) if found else 'none'}")
    return 0


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="PIXZ MCP auto-config (vetted, free + no-signup-first)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="catalog listing")
    p.add_argument("--tier")
    p.add_argument("--transport")
    p.add_argument("--category")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("tier", help="what a setup tier installs")
    p.add_argument("name", choices=["minimal", "medium", "full"])
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_tier)

    p = sub.add_parser("check", help="live probe: initialize + tools/list")
    p.add_argument("ids", nargs="*", help="server ids, or --all")
    p.add_argument("--all", action="store_true")
    p.add_argument("--timeout", type=int, default=120, help="seconds per server (default 120 — first npx run downloads)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=None)

    p = sub.add_parser("add", help="idempotent, non-destructive config write")
    p.add_argument("ids", nargs="+")
    p.add_argument("--runtime", required=True, choices=list(RUNTIME_CONFIGS))
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=None)

    p = sub.add_parser("remove", help="remove catalog-managed entries")
    p.add_argument("ids", nargs="+")
    p.add_argument("--runtime", required=True, choices=list(RUNTIME_CONFIGS))
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=None)

    p = sub.add_parser("status", help="configured servers + last check evidence")
    p.add_argument("--runtime")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=None)

    p = sub.add_parser("detect", help="which runtimes are present here")
    p.set_defaults(fn=cmd_detect)

    args = ap.parse_args()

    if args.cmd == "check":
        if args.all:
            ids = sorted(servers().keys())
        elif args.ids:
            ids = args.ids
        else:
            ap.error("give server ids or --all")
        sys.exit(run_check(ids, args.timeout, args.json))
    elif args.cmd == "add":
        sys.exit(cmd_add(args.ids, args.runtime, args.dry_run, args.json))
    elif args.cmd == "remove":
        sys.exit(cmd_remove(args.ids, args.runtime, args.dry_run, args.json))
    elif args.cmd == "status":
        sys.exit(cmd_status(args, args.json))
    else:
        sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
