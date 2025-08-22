# Bridgit Social — Matching Prompt Starter (v2)

Implements Matching with **Instructions > Evidence > Demos > Query**.
Includes: TF‑IDF retrieval (FAISS optional), MMR, FastAPI `/match`, prompt bank,
unit tests, and a canary A/B harness.

## Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_local.py
```

## API
```bash
uvicorn src.app:app --reload --port 8080
curl -s -X POST http://localhost:8080/match -H "Content-Type: application/json" -d @data/sample_request.json | jq
```

See `ab_config.yaml` for canary rollout.
