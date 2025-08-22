from fastapi import FastAPI, Query, Header
from typing import Optional
from .models import Profile, Context, MatchOutput
from .prompt import render_prompt, SYSTEM_TEXT
from .llm import MockLLM, extract_json
from .safety import validate_output
from .retrieval import EmbeddingIndex
from .mmr import select_mmr
from .ab import load_config, choose_version
import json, os

app = FastAPI(title="Bridgit Matching API", version="2.0")
DEMO_PATH = os.getenv("DEMO_PATH","data/demos.json")
EVID_PATH = os.getenv("EVID_PATH","data/evidence_store.json")
AB_PATH = os.getenv("AB_PATH","ab_config.yaml")

with open(DEMO_PATH,"r",encoding="utf-8") as f: DEMOS = json.load(f)
with open(EVID_PATH,"r",encoding="utf-8") as f: EVIDENCE = json.load(f)
AB_CFG = load_config(AB_PATH)

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/match", response_model=MatchOutput)
def match(profile_a: Profile, profile_b: Profile, context: Context,
          version: Optional[str] = Query(None), x_prompt_version: Optional[str] = Header(None)):
    selected_version = choose_version(AB_CFG, user_key=(profile_a.currentCompany or "anon"),
                                      override=(version or x_prompt_version))
    query_text = json.dumps({"A":profile_a.model_dump(),"B":profile_b.model_dump(),"C":context.model_dump()}, ensure_ascii=False)
    index = EmbeddingIndex()
    index.add_demos(DEMOS)
    idxs = index.search(query_text, k=4)
    retrieved = [DEMOS[i] for i in idxs]
    demos = select_mmr(query_text, retrieved, k=2, lam=0.7)
    evidence = EVIDENCE[:2]

    prompt = render_prompt(demos, evidence, profile_a.model_dump(), profile_b.model_dump(), context.model_dump(), version=selected_version)
    raw = MockLLM().chat(prompt["system"], prompt["user"])
    obj = json.loads(extract_json(raw))
    validate_output(obj)
    return obj
