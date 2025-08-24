
# Bridgit Social — RAG + Few‑Shot Matchmaking (Baseline)

This repository is a **minimal, dependency‑light baseline** to enrich Bridgit Social's matchmaking suggestions using a small **RAG (retrieval‑augmented generation)** layer plus a **few‑shot demo selector (MMR)**.

> Goals: safer, more contextual, and research‑informed suggestions that remain **opt‑in** and **consent‑forward**.

## Features
- Ingests markdown knowledge docs into a tiny TF‑IDF style index (no external DB).
- Hybrid retrieval (BM25‑like scoring via TF‑IDF cosine).
- Few‑shot selection via simple **MMR** (diversity‑aware).
- A **safety scrubber** that removes protected attributes and risky claims from prompts.
- Prompt builder that follows: **Instructions > Evidence > Demos > Query**.
- Mock LLM that returns **JSON** (schema‑constrained) so you can wire in a real LLM later.
- CLI demo and optional FastAPI service (commented out to keep deps minimal).

## File Tree
```
bridgit_rag_baseline/
├── README.md
├── config.yaml
├── sample_input.json
├── data/
│   ├── demos.json
│   └── knowledge/
│       ├── consent_and_safety.md
│       ├── general_openers.md
│       ├── professional_events.md
│       ├── coffee_shop.md
│       └── follow_up.md
├── src/
│   ├── retriever.py
│   ├── mmr.py
│   ├── prompt.py
│   ├── safety.py
│   ├── llm.py
│   ├── schemas.py
│   └── main.py
└── tests/
    └── test_demo_runner.py
```

## Quickstart

1) **Run the demo (CLI)**
```bash
python3 -m src.main
```

2) **Modify the knowledge base**
- Add or edit markdown files in `data/knowledge/`.
- Run again; the index rebuilds automatically.

3) **Swap in a real embedding/vector DB later**
- Replace `SimpleVectorIndex` in `src/retriever.py` with FAISS, Milvus, or OpenSearch.
- Replace `MockLLM` in `src/llm.py` with your provider (OpenAI/Cohere/Bedrock).

## Config
`config.yaml` sets chunking and retrieval parameters.

## Notes
- This baseline intentionally avoids heavy dependencies. It should run on plain Python ≥3.9.
- The safety scrubber aims for **conservative redaction**; adapt it to your legal & policy needs.
