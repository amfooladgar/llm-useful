import json
from .prompt import render_prompt
from .retrieval import EmbeddingIndex
from .mmr import select_mmr
from .llm import MockLLM, extract_json
from .safety import validate_output

def main():
    with open("data/demos.json","r",encoding="utf-8") as f:
        demos_bank = json.load(f)
    with open("data/evidence_store.json","r",encoding="utf-8") as f:
        evidence_store = json.load(f)

    profile_a = {"currentCompany":"SDot LLC","gender":"male","homeLocation":"New York, NY, USA",
                 "industry":["Technology"],"interests":["data","startups"],"occupation":"Bioengineering",
                 "pitches":["Exploring ML x biology"],"realTimeAvailability": True}
    profile_b = {"currentCompany":"Bridgit","gender":"male","homeLocation":"New York City, NY, USA",
                 "industry":["Technology"],"interests":["programming","startups"],"occupation":"Founder",
                 "pitches":["Mentoring early‑career engineers"],"realTimeAvailability": True}
    context = {"place":"Cowork Cafe","city":"New York","event":"Tech Mixer","time":"18:30"}

    query_text = json.dumps({"A":profile_a,"B":profile_b,"C":context}, ensure_ascii=False)
    index = EmbeddingIndex()
    index.add_demos(demos_bank)
    idxs = index.search(query_text, k=4)
    retrieved = [demos_bank[i] for i in idxs]
    demos = select_mmr(query_text, retrieved, k=2, lam=0.7)
    evidence = evidence_store[:2]
    prompt = render_prompt(demos, evidence, profile_a, profile_b, context, version="v1")

    raw = MockLLM().chat(prompt["system"], prompt["user"])
    obj = json.loads(extract_json(raw))
    validate_output(obj)

    print("=== PROMPT (system) ===")
    print(prompt["system"][:500] + ("..." if len(prompt["system"])>500 else ""))
    print("\n=== PROMPT (user) ===")
    print(prompt["user"][:900] + ("..." if len(prompt["user"])>900 else ""))
    print("\n=== LLM OUTPUT ===")
    print(json.dumps(obj, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
