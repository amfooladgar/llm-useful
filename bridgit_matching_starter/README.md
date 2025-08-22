# Bridgit Social — Matching Prompt Starter (v1.0)

This starter shows **how to implement the Matching workload** with:
- Prompt assembly (Instructions > Evidence > Demos > Query)
- MMR-based demo selection
- Basic safety checks and JSON schema validation
- A mock LLM client you can swap for OpenAI/Bedrock
- Minimal, dependency-free Python

## Quick Start

```bash
python3 src/main.py
```

This will:
1) Load sample profiles and context
2) Select demos via MMR
3) Build the prompt (matching schema)
4) Call a *mock* LLM and parse/validate the JSON
5) Print the structured result

## Files

- `src/prompt.py` — prompt template and rendering
- `src/mmr.py` — very small MMR demo selector (cosine on bag-of-words)
- `src/llm.py` — mock LLM client (swap with OpenAI / Bedrock)
- `src/models.py` — simple data classes and validation
- `src/safety.py` — protected attribute keywords and safety checks
- `src/main.py` — demo runner
- `data/demos.json` — example demo bank
- `data/evidence_store.json` — example evidence snippets for events

## Swapping in a real LLM

Replace `MockLLM` in `src/llm.py` with one of the stubs:

- **OpenAI (example)**:
```python
# pip install openai
from openai import OpenAI
client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system","content": system_text},{"role":"user","content": user_text}],
    temperature=0.2,
    stop=["###"]
)
```

- **AWS Bedrock (Claude)**:
```python
# boto3 bedrock-runtime (refer to AWS docs)
# bedrock = boto3.client("bedrock-runtime")
# resp = bedrock.invoke_model(body={...})
```

Ensure your response is **ONLY** the JSON per schema. If the model returns extra text, truncate between the first `{` and the last `}` and then validate.

## Production Tips

- Keep prompt text in versioned files (e.g., S3) and load at runtime.
- Use real embeddings (e.g., Titan, OpenAI text-embedding) for demo retrieval.
- Log: prompt version, selected demos, evidence IDs, and parsed output.
- Guardrails: reject outputs with protected attributes or malformed JSON.
- A/B test new prompt versions; canary rollout with auto-rollback.
