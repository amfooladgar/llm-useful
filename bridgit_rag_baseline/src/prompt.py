
"""
Prompt builder: Instructions > Evidence > Demos > Query
Returns a single string to feed to an LLM.
"""

import json
from typing import List, Dict, Any

SYSTEM_RULES = """
You are Bridgit Social’s matching assistant.
Authority: Instructions > Evidence > Demos.
Priorities: (1) Consent & safety (2) Relevance to context (3) Brevity.

RULES
- Do NOT infer or use protected attributes (race, religion, sexual orientation, health, etc.).
- Never guess facts; use only provided profile fields or EVIDENCE.
- Keep openers respectful, opt‑in, and situational. Avoid pickup lines.
- If data is insufficient, return score=0.0 with "insufficient_data" in risks.

SCHEMA (return exactly these keys)
{
  "score": <float 0.0-1.0>,
  "factors": [ "<short bullet>", ... ],
  "risks": [ "<short bullet>", ... ],
  "suggestions": [
    {"for":"initiator","text":"<one sentence>"},
    {"for":"recipient","text":"<one sentence>"}
  ]
}
"""

def build_prompt(evidence_chunks: List[Dict[str, Any]], demos: List[Dict[str, Any]], query_obj: Dict[str, Any]) -> str:
    evidence_txt = []
    for e in evidence_chunks:
        src = e["metadata"].get("source")
        evidence_txt.append(f"- [{src}] {e['text'].strip()[:500]}")
    demos_txt = []
    for d in demos:
        demos_txt.append(json.dumps({
            "situation": d.get("situation"),
            "suggestion": d.get("suggestion"),
            "response": d.get("response"),
            "factors": d.get("factors", []),
            "risks": d.get("risks", [])
        }))

    prompt = f"""{SYSTEM_RULES}

### EVIDENCE
{chr(10).join(evidence_txt)}

### DEMOS
{chr(10).join(demos_txt)}

### QUERY
{json.dumps(query_obj, ensure_ascii=False, indent=2)}

Return only valid JSON for the SCHEMA. Do not include extra keys or explanations.
"""
    return prompt
