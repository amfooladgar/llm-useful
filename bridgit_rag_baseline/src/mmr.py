
"""
Simple MMR (Maximal Marginal Relevance) selector over a tiny bag-of-words space.
No external dependencies; cosine over normalized term counts.
"""

from typing import List, Tuple
import math
from collections import Counter

def bow(text: str) -> Counter:
    tokens = [t.lower() for t in text.split() if t.isalpha() or t.isalnum()]
    return Counter(tokens)

def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[t] * b.get(t, 0) for t in a)
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def mmr_select(candidates: List[dict], query_text: str, k: int = 2, lamb: float = 0.7) -> List[dict]:
    """
    candidates: demo dicts with keys 'id', 'situation', 'query_features', 'suggestion', 'response'
    """
    qv = bow(query_text)
    selected = []
    remaining = candidates[:]
    while remaining and len(selected) < k:
        best = None
        best_score = -1.0
        for cand in remaining:
            # relevance
            cand_text = " ".join(cand.get("query_features", [])) + " " + cand.get("situation", "")
            rv = bow(cand_text)
            rel = cosine(qv, rv)
            # diversity penalty w.r.t selected
            if not selected:
                div = 0.0
            else:
                div = max(cosine(bow(" ".join(s.get("query_features", [])) + " " + s.get("situation", "")), rv) for s in selected)
            score = lamb * rel - (1 - lamb) * div
            if score > best_score:
                best_score = score
                best = cand
        selected.append(best)
        remaining = [c for c in remaining if c["id"] != best["id"]]
    return selected
