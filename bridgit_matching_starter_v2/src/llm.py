import json
class MockLLM:
    def chat(self, system: str, user: str) -> str:
        out = {
            "score": 0.76,
            "factors": ["Overlapping interests (technology)", "Same city", "Mentorship complement"],
            "risks": ["Initiator is early-career; keep tone mentoring-focused"],
            "suggestions": [
                {"for":"initiator","text":"I’m into ML & startups too—open to a 10‑min chat about projects tonight?"},
                {"for":"recipient","text":"If you’re up for it, share a recent project and ask what they’re exploring."}
            ]
        }
        return json.dumps(out, ensure_ascii=False)

def extract_json(text: str) -> str:
    start = text.find("{"); end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found")
    return text[start:end+1]

# OpenAI/Bedrock stubs commented (ready to wire later)
