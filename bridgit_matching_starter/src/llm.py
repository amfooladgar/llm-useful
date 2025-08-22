import json
from typing import Dict

class MockLLM:
    """
    Returns a safe, static JSON to demonstrate end-to-end flow.
    Replace with real LLM calls (OpenAI/Bedrock) in production.
    """
    def chat(self, system: str, user: str) -> str:
        # Always return a minimal valid JSON conforming to schema
        out = {
            "score": 0.72,
            "factors": ["Overlapping 'startups' interest", "Same evening availability"],
            "risks": ["A prefers to be approached; suggest gentle opener"],
            "suggestions": [
                {"for":"initiator","text":"Also into startups—open to a 10-min chat about projects this evening?"},
                {"for":"recipient","text":"If you’re up for it, happy to exchange quick intros."}
            ]
        }
        return json.dumps(out, ensure_ascii=False)

def extract_json(text: str) -> str:
    """
    Extract JSON substring from a potentially noisy response.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in response")
    return text[start:end+1]
