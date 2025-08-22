from typing import List, Dict
import json
from .safety import strip_protected_terms

SYSTEM_TEXT = """You are Bridgit Social’s matching assistant. Return ONLY valid JSON per the schema.
Authority: Instructions > Evidence > Demos. If conflict, follow this order.
Priorities: (1) Consent & safety (2) Relevance to context (3) Brevity.

RULES
- Do NOT infer or use protected attributes (race, religion, sexual orientation, health, etc.).
- Never guess facts; use only provided profile fields or EVIDENCE.
- Keep openers respectful, opt-in, and situational. Avoid pickup lines.
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

def render_prompt(demos: List[Dict], evidence_snippets: List[str], profile_a: Dict, profile_b: Dict, context: Dict) -> Dict:
    """
    Returns a dict with 'system' and 'user' ready to feed a chat completion API.
    """
    demos_block = []
    for d in demos:
        demos_block.append(
            f'# Demo\nPROFILES:\nA: {json.dumps(d["A"], ensure_ascii=False)}\nB: {json.dumps(d["B"], ensure_ascii=False)}\nCONTEXT: {json.dumps(d["CONTEXT"], ensure_ascii=False)}\nOUTPUT:\n{json.dumps(d["OUTPUT"], ensure_ascii=False)}'
        )
    demos_text = "\n\n".join(demos_block) if demos_block else "# No demos selected"

    evidence_text = "\n".join([f"[E{i+1}] {e}" for i, e in enumerate(evidence_snippets)]) if evidence_snippets else "(none)"

    # Strip protected terms from suggestions in demos (defensive)
    safe_demos_text = strip_protected_terms(demos_text)

    user_text = f"""### DEMOS
{safe_demos_text}

### EVIDENCE
{evidence_text}

### QUERY
PROFILES:
A: {json.dumps(profile_a, ensure_ascii=False)}
B: {json.dumps(profile_b, ensure_ascii=False)}
CONTEXT: {json.dumps(context, ensure_ascii=False)}

Return ONLY the JSON per SCHEMA.
STOP: ###
"""
    return {"system": SYSTEM_TEXT, "user": user_text}
