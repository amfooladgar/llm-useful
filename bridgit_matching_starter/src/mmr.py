from typing import List, Dict
import math
from collections import Counter

def _bow(text: str) -> Counter:
    # tiny bag-of-words tokenizer
    tokens = [t.lower() for t in text.split()]
    return Counter(tokens)

def _cosine(a: Counter, b: Counter) -> float:
    # cosine similarity for BoW
    inter = set(a.keys()) & set(b.keys())
    num = sum(a[t]*b[t] for t in inter)
    den = (sum(v*v for v in a.values()))**0.5 * (sum(v*v for v in b.values()))**0.5
    return 0.0 if den == 0 else num/den

def select_mmr(query_text: str, candidates: List[Dict], k: int = 2, lam: float = 0.7) -> List[Dict]:
    """
    Very small MMR selector on top of BoW cosine (for demo).
    candidates are demo dicts with A/B/CONTEXT; we stringify to text.
    """
    qv = _bow(query_text)
    scored = []
    for c in candidates:
        txt = f'{c["A"]} {c["B"]} {c["CONTEXT"]}'
        scored.append((c, _cosine(qv, _bow(txt))))
    selected = []
    while scored and len(selected) < k:
        best_item, best_score = None, -1
        for c, rel in scored:
            if not selected:
                mmr = rel
            else:
                max_sim = max(_cosine(_bow(str(c)), _bow(str(s))) for s in selected)
                mmr = lam*rel - (1-lam)*max_sim
            if mmr > best_score:
                best_item, best_score = c, mmr
        selected.append(best_item)
        scored = [(c, rel) for (c, rel) in scored if c is not best_item]
    return selected
