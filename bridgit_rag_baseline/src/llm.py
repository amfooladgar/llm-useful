
"""
Mock LLM that produces JSON following the schema.
Replace with a real LLM later if desired.
"""

import json
from typing import Dict, Any, List
from .safety import ensure_opt_in

def _simple_score(context: Dict[str, Any], evidence_count: int) -> float:
    # Silly heuristic: more evidence + context match => higher score (capped)
    score = 0.4 + min(0.6, 0.1 * evidence_count)
    # More time pressure => slightly lower
    if context.get("time_pressure_minutes", 5) <= 3:
        score -= 0.05
    return max(0.0, min(1.0, score))

def generate(prompt: str, query_obj: Dict[str, Any], evidence_chunks: List[Dict[str, Any]], demos: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Build a minimal, deterministic response using the first demo as a template.
    if not evidence_chunks:
        return {
            "score": 0.0,
            "factors": ["insufficient_evidence"],
            "risks": ["insufficient_data"],
            "suggestions": [
                {"for":"initiator","text":"Not enough context to suggest an opener."},
                {"for":"recipient","text":"N/A"}
            ]
        }

    initiator_tone = (query_obj.get("initiator_profile", {}).get("tone") or "friendly").split(",")[0]
    recipient_tone = (query_obj.get("recipient_profile", {}).get("tone") or "open").split(",")[0]
    context = query_obj.get("context", {})

    # Use top demo for structure, ensure opt-in phrasing
    base_demo = demos[0] if demos else {
        "suggestion": {"for":"initiator","text":"Hi—quick intro?"},
        "response": {"for":"recipient","text":"Sure, what are you building?"}
    }

    init_text = ensure_opt_in(base_demo["suggestion"]["text"])
    rec_text = base_demo["response"]["text"]

    result = {
        "score": _simple_score(context, len(evidence_chunks)),
        "factors": ["opt-in", "context-aware", "time-bounded"],
        "risks": [],
        "suggestions": [
            {"for":"initiator","text": init_text},
            {"for":"recipient","text": rec_text}
        ]
    }
    return result
