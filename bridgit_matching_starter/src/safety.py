from typing import List
import re

# Simple protected attributes keyword list (expand as needed)
PROTECTED_TERMS = [
    "race", "religion", "sexual orientation", "disability", "health",
    "ethnicity", "nationality", "political", "age", "gender", "pregnant"
]

def contains_protected(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in PROTECTED_TERMS)

def strip_protected_terms(text: str) -> str:
    # remove mentions of protected terms (defensive for demo prompts)
    safe = text
    for term in PROTECTED_TERMS:
        safe = re.sub(term, "[REDACTED]", safe, flags=re.IGNORECASE)
    return safe
