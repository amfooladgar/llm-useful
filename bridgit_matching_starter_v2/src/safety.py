import re
from typing import Dict

PROTECTED_TERMS = ["race","religion","sexual orientation","disability","health","ethnicity","nationality","political","age","gender","pregnant"]

def contains_protected(text: str) -> bool:
    t = (text or "").lower()
    return any(term in t for term in PROTECTED_TERMS)

def strip_protected_terms(text: str) -> str:
    safe = text
    for term in PROTECTED_TERMS:
        safe = re.sub(term, "[REDACTED]", safe, flags=re.IGNORECASE)
    return safe

def validate_output(obj: Dict) -> None:
    for k in ["score","factors","risks","suggestions"]:
        if k not in obj: raise ValueError(f"Missing key: {k}")
    if not (0.0 <= float(obj["score"]) <= 1.0):
        raise ValueError("score must be 0.0–1.0")
    if not isinstance(obj["suggestions"], list) or len(obj["suggestions"]) != 2:
        raise ValueError("suggestions must be length 2")
    for s in obj["suggestions"]:
        if contains_protected(s.get("text","")):
            raise ValueError("Suggestion contains protected terms")
