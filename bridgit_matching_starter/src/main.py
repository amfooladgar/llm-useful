import json
from .prompt import render_prompt
from .mmr import select_mmr
from .llm import MockLLM, extract_json
from .models import MatchRequest
from .safety import contains_protected

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_match(json_obj):
    # Minimal schema checks
    required_keys = ["score", "factors", "risks", "suggestions"]
    for k in required_keys:
        if k not in json_obj:
            raise ValueError(f"Missing key: {k}")
    if not (0.0 <= float(json_obj["score"]) <= 1.0):
        raise ValueError("score must be between 0.0 and 1.0")
    if not isinstance(json_obj["suggestions"], list) or len(json_obj["suggestions"]) != 2:
        raise ValueError("suggestions must be a list of two items")
    for s in json_obj["suggestions"]:
        if contains_protected(s.get("text","")):
            raise ValueError("Suggestion contains protected attribute terms")
    return True

def stringify_query(profile_a, profile_b, context):
    return f"{profile_a} {profile_b} {context}"

def main():
    demos_bank = load_json("data/demos.json")  # list of demo dicts
    evidence_store = load_json("data/evidence_store.json")  # list of strings

    # Example request
    profile_a = {"goals":["professional_networking"],"interests":["data","startups"],"availability":"today_evening","style":"prefer_to_be_approached"}
    profile_b = {"goals":["professional_networking","mentorship"],"interests":["ml","startups"],"availability":"today_evening","style":"likes_to_initiate"}
    context = {"place":"Cowork Cafe","city":"New York","event":"Tech Mixer","time":"18:30"}

    # Select demos via lightweight MMR
    query_text = stringify_query(profile_a, profile_b, context)
    demos = select_mmr(query_text, demos_bank, k=2, lam=0.7)

    # For this starter, we just take top 1 evidence (pretend retrieval)
    evidence = evidence_store[:1]

    # Build prompt
    prompt = render_prompt(demos=demos, evidence_snippets=evidence, profile_a=profile_a, profile_b=profile_b, context=context)

    # Call LLM (mock)
    llm = MockLLM()
    raw = llm.chat(prompt["system"], prompt["user"])
    json_str = extract_json(raw)
    obj = json.loads(json_str)

    # Validate
    validate_match(obj)

    print("=== PROMPT (system) ===")
    print(prompt["system"])
    print("\n=== PROMPT (user) ===")
    print(prompt["user"])
    print("\n=== LLM OUTPUT ===")
    print(json.dumps(obj, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
