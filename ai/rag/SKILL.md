---
name: RAG Systems
description: Grounded retrieval-augmented generation — chunking, hybrid retrieval, citation, UNKNOWN handling and eval. Use when answers must come from a corpus. Do not invent citations. For system-level RAG work, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.ai.rag
category: ai
triggers: [rag, retrieval, vector, grounding, knowledge base]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# RAG Systems — `pixz.ai.rag`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when building or evaluating a retrieval system.

## Purpose

Answers grounded in retrieved evidence with hallucination resistance. Every factual sentence must **cite**. If retrieval is insufficient, the answer is **UNKNOWN** — never fabricated.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Q&A over docs, policies, tickets, code, knowledge bases | Tasks the model should not retrieve for (pure code edit in the open repo) |
| Designing chunk/index/retrieve/rerank pipelines | "Search the web once" — that's research, not a RAG system |

## Methodology

### 1. Chunk & index

- Chunk by semantic units (headings, functions), not naive 512-char slices when structure exists.
- Overlap tuned; too much overlap = near-duplicate hits. Dedup.
- Metadata on every chunk: source URI, title, section, timestamp, access control, authority (official vs comment).
- Embeddings: pin the model id; changing it requires re-index. Store the model id next to the index.

### 2. Retrieve

- Hybrid: vector + BM25 (or equivalent lexical). Vector-only fails on identifiers, error codes, names.
- Rerank the union. Threshold + max-k with diversity (don't return 8 near-duplicates).
- Honor ACL metadata *before* sending chunks to the model.
- Query rewrite for follow-ups; do not retrieve with a pronoun-only query.

### 3. Ground

- Every factual sentence **cite**s chunk id(s). No synthesis without source.
- Distinguish retrieved fact vs model inference (label them).
- Quote when numbers, legal language, or API signatures are involved.
- If top chunks disagree, surface the contradiction — do not average them.

### 4. Discipline

- Confidence per sentence with basis (which chunks, score).
- **UNKNOWN** when retrieval insufficient — do not fabricate. Offer what would make it answerable (missing doc, stale index).
- Never invent citations, URLs, or chunk ids.

### 5. Eval

- retrieval: recall@k, MRR, on a frozen question set.
- generation: faithfulness (supported by chunks), citation fidelity (cited chunk actually contains the claim), answer relevance.
- freshness regression: new docs appear in retrieval within the SLA.
- cost/latency budget per query.

Treat eval numbers as evidence with a basis (`pixz.core.epistemic-reasoning`). No decorative scores.

## Failure Conditions

- Answer with no citations on a factual claim → invalid; redo or UNKNOWN.
- Invented citation → critical failure.
- Vector-only on identifier-heavy corpora → expected miss; add lexical.

## Example

> Pricing bot. Chunk price tables as whole tables (not split mid-row). Hybrid retrieve. Question "what's the team plan in EUR?" — if chunks are USD-only, answer UNKNOWN + point to the USD table, do not convert without a source. Faithfulness eval on 50 gold questions.

## Structured Output

```yaml
rag_report:
  pipeline: {chunk, index, retrieve, rerank, generate}
  grounding_evidence: [{sentence, chunk_ids, quote}]
  unknowns: [...]
  faithfulness: {score, basis, n}
  evals: {recall_at_k, citation_fidelity, freshness, latency}
  residual_unknowns: [...]
```

## Main Skill

Standing up RAG (ingest → index → eval → ship) is orchestrator work. Activate `pixz.core.orchestrator`.
