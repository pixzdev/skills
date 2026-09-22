#!/usr/bin/env python3
"""
PixzFlow Hooks — runtime contract wiring: check + install (2.2.0).

F4: makes the ACTIVATE step of installation mechanical instead of improvised.
Only runtimes that need wiring get wiring — for runtimes that read AGENTS.md
natively (openclaw, opencode, hermes, codex, generic), `check` confirms the
contract file exists and `install` is a documented no-op. Claude is the one
runtime that needs an import line (CLAUDE.md -> @AGENTS.md).

Commands:
  hooks.py check   --runtime <rt> [--root PATH]   verify the contract is reachable
  hooks.py install --runtime <rt> [--root PATH]   write minimal wiring (append-only,
                                                  refuses to overwrite existing content)

Exit: 0 wired/verified · 10 gap found (not wired) · 1 error.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAUDE_MARKER = "@AGENTS.md"
CLAUDE_FRAGMENT = "# CLAUDE.md — PixzFlow wiring\n@AGENTS.md\n"

NATIVE_RUNTIMES = {
    "openclaw": "reads AGENTS.md natively",
    "opencode": "reads AGENTS.md natively",
    "hermes": "reads AGENTS.md natively",
    "codex": "reads AGENTS.md natively (root->leaf, 32 KiB cap)",
    "cursor": "reads AGENTS.md via standard",
    "generic": "reads AGENTS.md via standard",
}


def check(root, runtime):
    agents = root / "AGENTS.md"
    if not agents.exists():
        print(f"FAIL — AGENTS.md missing at {agents}; the operating contract is unreachable.")
        return 10
    if runtime == "claude":
        claude_md = root / "CLAUDE.md"
        if not claude_md.exists():
            print("GAP — AGENTS.md present, but no CLAUDE.md import for Claude. "
                  "Fix: hooks.py install --runtime claude")
            return 10
        if CLAUDE_MARKER not in claude_md.read_text(encoding="utf-8"):
            print("GAP — CLAUDE.md exists but does not import @AGENTS.md. "
                  "Fix: hooks.py install --runtime claude")
            return 10
        print("PASS — Claude reaches the contract: CLAUDE.md -> @AGENTS.md (AGENTS.md present).")
        return 0
    if runtime in NATIVE_RUNTIMES:
        print(f"PASS — {NATIVE_RUNTIMES[runtime]}; AGENTS.md present at repo root.")
        return 0
    print(f"PASS (assumed) — AGENTS.md present; runtime '{runtime}' has no known extra wiring.")
    return 0


def install(root, runtime):
    if runtime != "claude":
        if runtime in NATIVE_RUNTIMES:
            print(f"NO-OP — {NATIVE_RUNTIMES[runtime]}; nothing to wire. Contract check:")
            return check(root, runtime)
        print(f"NO-OP — no wiring known for runtime '{runtime}'. Contract check:")
        return check(root, runtime)
    if not (root / "AGENTS.md").exists():
        print("FAIL — AGENTS.md missing; nothing to import.")
        return 1
    claude_md = root / "CLAUDE.md"
    if claude_md.exists():
        txt = claude_md.read_text(encoding="utf-8")
        if CLAUDE_MARKER in txt:
            print("ALREADY WIRED — CLAUDE.md already imports @AGENTS.md (no duplicate, no overwrite).")
            return 0
        claude_md.write_text(txt.rstrip() + "\n\n" + CLAUDE_MARKER + "\n", encoding="utf-8")
        print(f"APPENDED '@AGENTS.md' to existing {claude_md} (existing content preserved).")
        return 0
    claude_md.write_text(CLAUDE_FRAGMENT, encoding="utf-8")
    print(f"CREATED {claude_md} with '@AGENTS.md' import.")
    return 0


def main():
    p = argparse.ArgumentParser(description="PixzFlow runtime contract wiring (2.2.0)")
    p.add_argument("cmd", choices=["check", "install"])
    p.add_argument("--runtime", required=True,
                   help="claude|openclaw|opencode|hermes|codex|cursor|generic")
    p.add_argument("--root", help="project root to wire (default: this repo)")
    args = p.parse_args()
    root = Path(args.root) if args.root else ROOT
    if args.cmd == "check":
        return check(root, args.runtime)
    return install(root, args.runtime)


if __name__ == "__main__":
    sys.exit(main())
