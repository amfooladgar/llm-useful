
"""
End-to-end pipeline (CLI):
1) Load config + knowledge
2) Build index
3) Scrub profiles/context
4) Retrieve evidence
5) Select demos via MMR
6) Build prompt
7) Mock LLM generate
8) Print JSON result
"""

import os, json, yaml
from typing import Dict, Any
from .retriever import build_knowledge_index, load_config
from .mmr import mmr_select
from .prompt import build_prompt
from .safety import scrub_profiles_and_context
from .llm import generate

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOW_DIR = os.path.join(DATA_DIR, "knowledge")
DEMOS_PATH = os.path.join(DATA_DIR, "demos.json")
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
SAMPLE_INPUT = os.path.join(BASE_DIR, "sample_input.json")

def build_query_text(obj: Dict[str, Any]) -> str:
    ip = obj.get("initiator_profile", {})
    rp = obj.get("recipient_profile", {})
    cx = obj.get("context", {})
    parts = []
    parts.append("goals:" + ",".join(ip.get("goals", [])))
    parts.append("interests:" + ",".join(ip.get("interests", [])))
    parts.append("goals2:" + ",".join(rp.get("goals", [])))
    parts.append("interests2:" + ",".join(rp.get("interests", [])))
    parts.append("location_type:" + cx.get("location_type", ""))
    parts.append("venue:" + cx.get("venue", ""))
    parts.append("noise:" + cx.get("noise_level", ""))
    return " ".join(parts)

def run_once(input_obj: Dict[str, Any]) -> Dict[str, Any]:
    cfg = load_config(CONFIG_PATH)

    # Safety scrub first
    initiator, recipient, context, risks = scrub_profiles_and_context(
        input_obj.get("initiator_profile", {}),
        input_obj.get("recipient_profile", {}),
        input_obj.get("context", {})
    )
    safe_obj = {
        "initiator_profile": initiator,
        "recipient_profile": recipient,
        "context": context
    }

    # Build index and retrieve
    idx = build_knowledge_index(KNOW_DIR, CONFIG_PATH)
    query_text = build_query_text(safe_obj)
    evidence = idx.search(query_text, top_k=cfg["top_k_docs"])

    # Load demos
    with open(DEMOS_PATH, "r") as f:
        demos = json.load(f)
    selected_demos = mmr_select(demos, query_text, k=cfg["top_k_demos"], lamb=cfg["mmr_lambda"])

    # Build prompt
    prompt = build_prompt(evidence, selected_demos, safe_obj)

    # Call mock LLM
    result = generate(prompt, safe_obj, evidence, selected_demos)
    # Merge safety risks
    if risks:
        result["risks"] = list(set(result.get("risks", []) + risks))
    return result

if __name__ == "__main__":
    with open(SAMPLE_INPUT, "r") as f:
        payload = json.load(f)
    out = run_once(payload)
    print(json.dumps(out, indent=2, ensure_ascii=False))
