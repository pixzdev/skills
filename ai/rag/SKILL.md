---
name: RAG Systems
description: Grounded retrieval-augmented generation — chunking, grounding, citation discipline and eval.
version: 1.1.0
id: pixz.ai.rag
category: ai
triggers: [rag, retrieval, vector, grounding, knowledge base]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# RAG Systems — `pixz.ai.rag`

## Purpose
Answers grounded in retrieved evidence with hallucination resistance.

## Methodology
1. **Chunk & Index:** semantic chunking, overlap tuned, dedup, metadata (source, freshness, authority).
2. **Retrieve:** hybrid (vector + BM25), rerank, threshold, max-k with diversity.
3. **Ground:** every factual sentence cites chunk(s); no synthesis without source; distinguish retrieved fact vs model inference.
4. **Discipline:** confidence per sentence with basis; UNKNOWN when retrieval insufficient — do not fabricate.
5. **Eval:** recall@k, faithfulness, citation fidelity, freshness regression, cost/latency.

## Outputs
`rag_report` {pipeline, grounding_evidence[], faithfulness_score, evals, residual_unknowns}

---
