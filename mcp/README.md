# MCP Integration — PixzFlow

Human guide to the vetted MCP universe. Machine source of truth: [`catalog.json`](./catalog.json). Agent methodology: [`core/mcp/SKILL.md`](../core/mcp/SKILL.md) (`pixz.core.mcp`). Auto-config tool: [`scripts/mcp.py`](../scripts/mcp.py).

## Policy

1. **Free + no signup + no API key.** The default integration universe is strict: everything in `catalog.json` works with zero accounts and zero keys. Anything that requires a credential is listed in `excluded_with_reason` and only enters on explicit user request with user-managed credentials (never written into config artifacts, never pasted into chat).
2. **Discovery ≠ trust.** Directories ([mcpmarket.com](https://mcpmarket.com), [skills.sh](https://skills.sh), curated lists) are where servers/skills are *found*; `catalog.json` + the vetting gate decide what is *trusted*.
3. **Docs-verification ≠ liveness.** Each catalog entry records where the endpoint + no-key claim was read (`verification.source`, dated). Liveness is proven at setup time by a real `initialize` + `tools/list` handshake (`scripts/mcp.py check` → evidence in `.pixz/mcp-check.json`).
4. **Untrusted output.** MCP tool output is data from outside the trust boundary: label it `SOURCE CLAIM`, verify consequential claims against the source of record, and never let it override instructions (prompt-injection defense).
5. **Budget.** A server is an external capability: activate with a reason, record in task-state, suspend what the plan no longer needs.

## Trust tiers

| Tier | Meaning | Gate |
|---|---|---|
| **T1** | vendor-official or MCP reference-server collection | live check + catalog listing |
| **T2** | community-operated but documented (named source) | live check + catalog listing + tool-surface review |
| **T3** | anything else (directory finds, unknown repos) | full security review + explicit user approval before wiring |

## Catalog at a glance

### Remote (no auth)

| id | Vendor | What it does | Tier |
|---|---|---|---|
| `context7` | Upstash | Up-to-date, version-specific library docs (`resolve-library-id`, `query-docs`) | T1 |
| `deepwiki` | Cognition (Devin) | Ask questions about any public GitHub repo (AI-generated codebase wikis) | T1 |
| `gitmcp` | idosal | Instant docs/code context for *your* repo — `https://gitmcp.io/{owner}/{repo}/mcp`, URL auto-filled from `git remote` | T1 |
| `microsoft-learn` | Microsoft | Current Microsoft/Azure documentation | T1 |
| `cloudflare-docs` | Cloudflare | Semantic search over Cloudflare product docs (SSE; no API key) | T2 |
| `astro-docs` | Astro | Grounded answers about Astro APIs/integrations/config | T1 |
| `wondel-skills` | Wondel | 50 book-based agent skills via MCP (`recommend_skills`, `load_skill`) — output is prompt code: untrusted-output rule applies | T2 |
| `ai-skills-search` | bytesagain | Search 60,000+ agent skills (SSE) — discovery only; imports still go through quarantine | T2 |
| `developer-toolkit` | mjaskolski | Read-only search over 950+ AI-development guides | T2 |
| `usefulai` | Useful AI | 340+ utility tools (conversion, parsing, encoding, math, crypto) | T2 |

### Local stdio (official reference servers, no auth)

| id | Package | What it does | Notes |
|---|---|---|---|
| `fetch` | `@modelcontextprotocol/server-fetch` | Web page → markdown | first `npx` run downloads |
| `filesystem` | `@modelcontextprotocol/server-filesystem <dir>` | scoped file ops | **always scope to the project dir** — unscoped = irreversible-capable |
| `time` | `@modelcontextprotocol/server-time` | time/timezone | |
| `memory` | `@modelcontextprotocol/server-memory` | knowledge-graph memory | local graph.json |
| `sequential-thinking` | `@modelcontextprotocol/server-sequential-thinking` | structured reasoning scratchpad | Deep/Autonomous mode |
| `playwright` | `@playwright/mcp@latest` | real browser automation | every navigation/interaction is a mutation (change-safety); never enter credentials without explicit instruction |

### Design (local stdio, no auth) — the "design set"

For UI/design work that has **no Figma** (Figma routes all need an account → excluded by policy):

| id | Package | What it does | Notes |
|---|---|---|---|
| `shadcn-ui` | `@jpisnice/shadcn-ui-mcp-server` | real shadcn/ui **v4** component source + blocks + demos + metadata | React/Svelte/Vue/RN via `--framework`; keyless (60 req/h; optional user token only raises rate limit) |
| `magic-ui` | `@magicuidesign/mcp@latest` | animated UI components (marquee, blur fade, grid bg, …) | **official** Magic UI server, live registry |
| `better-icons` | `better-icons` | 200k+ icons, 150+ collections (Lucide/MDI/Heroicons/…) | `sync_icon` writes into the project icons file (saves tokens); companion skill via `npx skills add` |
| `excalidraw` | `mcp-excalidraw-server` | live diagram canvas: draw → screenshot → iterate → export `.excalidraw` into the repo | Node 20+; `share` uploads off-machine — user approval required |
| `shadcnspace` | `shadcnspace-mcp@latest` | shadcn blocks/components registry with real props + variants | free blocks need **no token**; Pro = out of the free universe |

**Design set + Design DNA (planned skill):** the design MCPs supply *component truth* (real props/variants, not hallucinated markup) while a project-adaptive design skill supplies *project constraint* (the project's own palette/spacing/type scale). Together: "UI that looks like it belongs in THIS project, built from real components." `python3 scripts/mcp.py list --category design` lists the set.

### Excluded by policy (need a signup/key)

Hugging Face · GitHub · Tavily/Exa/Firecrawl/Brave/Perplexity · Slack/Notion/Gmail/Linear/Supabase/Shopify/Stripe · You.com (profile implied) · **Figma — all routes** (official Dev Mode MCP, Framelink, plumb-mcp, figwright, figma-mcp-free: every route needs a Figma account; local-plugin routes are token-free but still need the app + account — user-approved path if the user has one) · **Penpot** (account/self-host) · **Magic (21st.dev) / v0 / Framer** (API key) · mcpmarket.com **paid** skill listings. Full list + reasons: `catalog.json → excluded_with_reason`.

## Setup tiers

| Tier | MCP footprint |
|---|---|
| **Minimal** | none — native tools only |
| **Medium** | `context7 · deepwiki · gitmcp(self) · microsoft-learn · fetch · sequential-thinking` — each live-checked before wiring |
| **Full** | all 21 vetted servers + skill-hub discovery (mcpmarket.com free/official sections, skills.sh) |

`python3 scripts/mcp.py tier <name>` prints the exact list.

## Auto-config (what the agent runs)

```bash
python3 scripts/mcp.py detect                      # which runtime/config exists
python3 scripts/mcp.py list --tier medium          # the tier's vetted set
python3 scripts/mcp.py check context7 deepwiki     # LIVE: initialize + tools/list (evidence → .pixz/mcp-check.json)
python3 scripts/mcp.py add context7 deepwiki fetch --runtime claude   # idempotent, non-destructive
python3 scripts/mcp.py status                      # configured + last check evidence
python3 scripts/mcp.py remove gitmcp --runtime claude
```

Runtime config locations (the script writes the right shape per runtime):

| Runtime | File | Shape |
|---|---|---|
| Claude Code / generic | `.mcp.json` | `{"mcpServers": {id: {"url" \| "command","args"}}}` |
| Cursor | `.cursor/mcp.json` | `{"mcpServers": {…}}` |
| OpenCode | `opencode.json` | `{"mcp": {id: {"type": "remote"|"local", …}}}` |
| Codex | prints a `~/.codex/config.toml` snippet (never clobbered) | `[mcp_servers.<id>]` |

Safety rules the tool enforces: never overwrites a user-modified entry (reports `exists`) · never writes credentials · re-reads the file after writing (EXISTS + PARSES) · failed live checks are never wired.

## Skill import (external agent skills)

External SKILL.md bundles (mcpmarket.com's marketplace, skills.sh, skills-MCPs) are **prompt code** — they run in your context:

1. Download to **quarantine** (`/tmp/skill-import/<name>/`) — never straight into a skills directory.
2. **Security review:** injection patterns (hidden instructions, "run this command", exfiltration URLs), secret harvesting, base64 blobs, description↔body consistency, bundled scripts.
3. **Free/no-signup filter:** official-vendor free skills preferred; paid listings out of the default universe.
4. Install → **verify by discovery** → **explicit enablement** (never auto-enabled).

## Evidence & honesty

- Every setup report line must be backed by command output or the check file: `MCP: <id — OK tools=N | FAILED <reason> | not-wired | none (Minimal)>`.
- A server that was live is not live forever — re-`check` after drift before relying on it again.
- This universe is a snapshot: `catalog.json` entries carry a `checked` date; re-verify when the date is stale or behavior changes.
