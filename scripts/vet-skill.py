#!/usr/bin/env python3
"""
PIXZ skill quarantine scanner — vet an EXTERNAL skill bundle before it is imported.

Part of the skill-import quarantine protocol (see skill `pixz.core.mcp`,
section "External skill imports"): never trust a skill's self-description.
This tool scans a bundle (directory with SKILL.md, or a .zip of one) for:

  1. structural   — SKILL.md present, frontmatter complete (name/description/version/category/triggers/id)
  2. injection    — prompt-injection & exfiltration patterns (blockers)
  3. secrets      — credential patterns and secret-file paths (blockers)
  4. consistency  — description/triggers/body coherence (warnings)
  5. budget       — size/cost metrics + bundled executable inventory (warnings)

Exit codes: 0 pass · 10 warnings (human review required) · 1 fail (import blocked).
Stdlib-only. Read-only — never modifies the scanned bundle.
"""
import argparse
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

# ---------------------------------------------------------------- patterns

# BLOCKER patterns: prompt injection / exfiltration / credential theft.
# Matched case-insensitively against SKILL.md + bundled script text.
FAIL_PATTERNS = [
    ("injection.ignore-prior",    r"ignore\s+(all\s+|any\s+)?(previous|prior|above|earlier|preceding)\s+(instructions|rules|guidelines|prompts|context)"),
    ("injection.disregard",       r"disregard\s+(your\s+|all\s+)?(instructions|rules|guidelines|training|policy)"),
    ("injection.hide-from-user",  r"do\s+not\s+(tell|inform|notify|reveal|show)\s+(the\s+)?user"),
    ("injection.hide-from-user2", r"without\s+(telling|informing|letting|asking)\s+(the\s+)?user"),
    ("injection.hide-from-dev",   r"(hide|conceal|suppress)\s+this\s+(from|from\s+)(the\s+)?(user|developer)"),
    ("injection.reveal-system",   r"reveal\s+(your\s+|the\s+)?(system\s+prompt|instructions|guidelines|developer\s+message)"),
    ("injection.new-persona",     r"(you\s+are\s+now|pretend\s+(you\s+are|to\s+be))"),
    ("injection.override",        r"override\s+(your\s+|the\s+)?(system|safety|security|guardrail)"),
    ("injection.exfiltrate",      r"exfiltrat"),
    ("injection.send-remote",     r"(send|post|upload|transmit)\s+.{0,60}\s+to\s+(a\s+)?(remote|external|third-party|untrusted)"),
    ("exfil.curl-pipe-sh",        r"curl\s+[^\n|]{0,200}\|\s*(ba|z)?sh"),
    ("exfil.wget-pipe-sh",        r"wget\s+[^\n|]{0,200}\|\s*(ba|z)?sh"),
    ("exfil.base64-decode",       r"base64\s+(-d|--decode)"),
    ("exfil.atob",                r"atob\("),
    ("exfil.nw-transfer",         r"(transfer\.sh|file\.io|ngrok\.(io|app)|localtunnel|serveo\.net|requestbin)"),
    ("secret.ssh",                r"(?:~|\$HOME|[A-Z]:\\|/home/[^/\s]+)?[/\\.]ssh"),
    ("secret.id-rsa",             r"id_(rsa|ed25519|ecdsa)"),
    ("secret.aws-cred",           r"\.aws/credentials"),
    ("secret.netrc",              r"\.netrc"),
    ("secret.gh-pat",             r"\bgh[pousr]_[A-Za-z0-9]{16,}\b"),
    ("secret.aws-key",            r"\bAKIA[0-9A-Z]{16}\b"),
    ("secret.openai-key",         r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ("secret.slack-token",        r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    ("secret.env-access",         r"process\.env\.(API_KEY|API_TOKEN|SECRET|ACCESS_TOKEN|AUTH_TOKEN|DB_|DATABASE)"),
    ("secret.env-access2",        r"os\.environ(?:\.get)?\(\s*['\"](API_KEY|API_TOKEN|SECRET_KEY|ACCESS_TOKEN|AUTH_TOKEN|DATABASE_URL)"),
    ("secret.env-file-read",      r"(cat|read|open|copy)\s+[^\n]{0,40}\.env\b"),
]

# WARNING patterns: suspicious but reviewable.
WARN_PATTERNS = [
    ("danger.sudo",               r"(^|\s)sudo\s+"),
    ("danger.rm-rf",              r"rm\s+-rf\s+(?!/tmp/|/var/folders/)"),
    ("danger.eval",               r"\beval\s*\("),
    ("danger.exec",               r"\bexec\s*\("),
    ("danger.chmod-777",          r"chmod\s+(-R\s+)?777"),
    ("blob.base64-long",          r"[A-Za-z0-9+/]{200,}={0,2}"),
    ("blob.hex-long",             r"\b(?:[0-9a-f]{4}\s){20,}"),
    ("url.suspicious",            r"https?://(?!github\.com|githubusercontent\.com|raw\.gitmirror|registry\.npmjs\.org|docs\.[a-z0-9.-]+\.[a-z]{2,})[a-z0-9.-]+\.[a-z]{2,}[^\s\"')\]]*"),
]

STRUCT_REQUIRES = ["name", "description", "version", "category", "triggers", "id"]
MAX_BODY_CHARS = 20000
MIN_BODY_CHARS = 1500


# ---------------------------------------------------------------- parsing

def parse_frontmatter(text):
    """Minimal YAML-ish frontmatter parser: scalar `key: value` and `key:` + `- item` lists."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[3:end]
    data = {}
    current_key = None
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                data[key] = []
                current_key = key
            else:
                if val.startswith("[") and val.endswith("]"):
                    data[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
                    current_key = None
                else:
                    data[key] = val.strip("'\"")
                    current_key = None
        elif line.strip().startswith("- ") and current_key:
            data[current_key].append(line.strip()[2:].strip().strip("'\""))
    return data


def iter_files(bundle: Path):
    """Yield (relative_path, text) for scannable text files in the bundle."""
    for p in sorted(bundle.rglob("*")):
        if p.is_dir() or any(part.startswith(".") for part in p.parts):
            continue
        if p.suffix.lower() in {".md", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml", ".txt"}:
            try:
                yield p.relative_to(bundle).as_posix(), p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue


def extract_bundle(src: Path):
    """Return the bundle root directory (temp dir for zips, cleaned up by caller)."""
    if src.is_dir():
        return src, None
    if src.suffix.lower() == ".zip":
        tmp = Path(tempfile.mkdtemp(prefix="vet-skill-"))
        with zipfile.ZipFile(src) as z:
            z.extractall(tmp, pwd=None)
        # if the zip wraps everything in one folder, descend into it
        entries = [p for p in tmp.iterdir() if not p.name.startswith(".")]
        if len(entries) == 1 and entries[0].is_dir():
            return entries[0], tmp
        return tmp, tmp
    return None, None


# ---------------------------------------------------------------- checks

def check_bundle(bundle: Path):
    findings = []
    metrics = {}

    def add(severity, check, detail, file=None, line=None):
        f = {"severity": severity, "check": check, "detail": detail}
        if file:
            f["file"] = file
        if line is not None:
            f["line"] = line
        findings.append(f)

    skill_md = bundle / "SKILL.md"
    if not skill_md.exists():
        add("fail", "structure.no-skill-md", "bundle has no SKILL.md", "SKILL.md")
        return findings, metrics
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    metrics["chars"] = len(text)
    metrics["lines"] = len(lines)

    # ---- structure
    fm = parse_frontmatter(text)
    if fm is None:
        add("fail", "structure.no-frontmatter", "SKILL.md has no frontmatter block")
        fm = {}
    for key in STRUCT_REQUIRES:
        if key not in fm or fm[key] in (None, "", []):
            add("warn" if key in ("version", "id") else "fail", f"structure.missing-{key}",
                f"frontmatter missing required key `{key}`", "SKILL.md")
    triggers = fm.get("triggers", [])
    if isinstance(triggers, list) and len(triggers) < 3:
        add("warn", "structure.thin-triggers",
            f"only {len(triggers)} trigger(s); router match quality depends on them", "SKILL.md")
    description = fm.get("description", "") if isinstance(fm.get("description"), str) else ""
    if len(description) > 500:
        add("warn", "budget.long-description",
            f"description is {len(description)} chars (>500) — costs context on every activation", "SKILL.md")

    # body = text after frontmatter
    body = text[text.find("\n---", 3) + 4:] if fm else text
    metrics["body_chars"] = len(body)
    if len(body) < MIN_BODY_CHARS:
        add("warn", "budget.thin-body", f"body is {len(body)} chars (<{MIN_BODY_CHARS}) — may be a stub", "SKILL.md")
    if len(body) > MAX_BODY_CHARS:
        add("warn", "budget.heavy-body",
             f"body is {len(body)} chars (>{MAX_BODY_CHARS}) — heavy context cost; consider references/", "SKILL.md")

    # id vs path consistency (warning — path convention differs across installs)
    skill_id = fm.get("id", "")
    if isinstance(skill_id, str) and skill_id:
        expect_dir = skill_id.replace("pixz.", "").replace(".", "/")
        if bundle.name and bundle.name != expect_dir.replace("/", "") and bundle.name != Path(expect_dir).name:
            add("info", "consistency.id-path",
                f"frontmatter id `{skill_id}` vs bundle dir `{bundle.name}` (convention: {expect_dir})", "SKILL.md")

    # ---- injection + secrets over all scannable files
    files = list(iter_files(bundle))
    for rel, ftext in files:
        for lineno, line in enumerate(ftext.splitlines(), 1):
            for name, pattern in FAIL_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    add("fail", name, f"{line.strip()[:120]}", rel, lineno)
            for name, pattern in WARN_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    snippet = line.strip()[:120]
                    if name == "url.suspicious":
                        m = re.search(pattern, line, re.IGNORECASE)
                        snippet = m.group(0)[:80] if m else snippet
                    add("warn", name, snippet, rel, lineno)

    # ---- consistency: triggers vs description keywords
    if isinstance(triggers, list) and description:
        desc_words = set(re.findall(r"[a-z]{4,}", description.lower()))
        trig_words = set(re.findall(r"[a-z]{3,}", " ".join(triggers).lower()))
        if desc_words and not (desc_words & trig_words):
            add("warn", "consistency.triggers-description",
                "no shared keywords between triggers and description — router and human mismatch", "SKILL.md")

    # ---- bundled executables inventory (budget / review)
    scripts = [rel for rel, _ in files if Path(rel).suffix.lower() in {".sh", ".py", ".js", ".ts"}]
    metrics["bundled_scripts"] = scripts
    if scripts:
        add("info", "inventory.scripts",
            f"bundle ships {len(scripts)} script(s): {', '.join(scripts)} — review each before import", "SKILL.md")

    metrics["est_tokens"] = max(1, len(text) // 4)
    return findings, metrics


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="PIXZ skill quarantine scanner")
    ap.add_argument("bundle", help="path to a skill bundle (directory with SKILL.md) or .zip")
    ap.add_argument("--json", action="store_true", help="JSON report on stdout")
    args = ap.parse_args()

    src = Path(args.bundle)
    if not src.exists():
        print(f"bundle not found: {src}", file=sys.stderr)
        sys.exit(1)
    bundle, tmp = extract_bundle(src)
    if bundle is None:
        print(f"unsupported bundle: {src} (need directory or .zip)", file=sys.stderr)
        sys.exit(1)
    try:
        findings, metrics = check_bundle(bundle)
    finally:
        if tmp:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    fails = [f for f in findings if f["severity"] == "fail"]
    warns = [f for f in findings if f["severity"] == "warn"]
    verdict = "FAIL" if fails else ("REVIEW" if warns else "PASS")

    if args.json:
        print(json.dumps({"bundle": str(src), "verdict": verdict,
                          "metrics": metrics,
                          "fail": fails, "warn": warns,
                          "info": [f for f in findings if f["severity"] == "info"]}, indent=2))
    else:
        print(f"vet-skill: {src} → {verdict}  (fail={len(fails)} warn={len(warns)})")
        for f in fails:
            loc = f"{f['file']}:{f['line']}" if f.get("line") else f.get("file", "")
            print(f"  FAIL  [{f['check']}] {loc} — {f['detail']}")
        for f in warns:
            loc = f"{f['file']}:{f['line']}" if f.get("line") else f.get("file", "")
            print(f"  WARN  [{f['check']}] {loc} — {f['detail']}")
        for f in findings:
            if f["severity"] == "info":
                print(f"  INFO  [{f['check']}] {f['detail']}")
        print(f"  metrics: {metrics.get('chars', 0)} chars · est ~{metrics.get('est_tokens', 0)} tokens"
              + (f" · scripts: {', '.join(metrics['bundled_scripts'])}" if metrics.get("bundled_scripts") else ""))
    sys.exit(1 if fails else (10 if warns else 0))


if __name__ == "__main__":
    main()
