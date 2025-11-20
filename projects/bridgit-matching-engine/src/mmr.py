from typing import List, Dict
from collections import Counter
def _bow(text: str) -> Counter:
    toks = [t.lower() for t in text.split()]
    return Counter(toks)
def _cos(a: Counter, b: Counter) -> float:
    inter = set(a)&set(b)
    num = sum(a[t]*b[t] for t in inter)
    den = (sum(v*v for v in a.values()))**0.5 * (sum(v*v for v in b.values()))**0.5
    return 0.0 if den==0 else num/den
def select_mmr(query_text: str, candidates: List[Dict], k: int = 2, lam: float = 0.7) -> List[Dict]:
    qv = _bow(query_text)
    pool = [(c, _cos(qv, _bow(f'{c["A"]} {c["B"]} {c["CONTEXT"]}'))) for c in candidates]
    selected = []
    while pool and len(selected) < k:
        best, best_mmr = None, -1
        for c, rel in pool:
            if not selected:
                mmr = rel
            else:
                max_sim = max(_cos(_bow(str(c)), _bow(str(s))) for s in selected)
                mmr = lam*rel - (1-lam)*max_sim
            if mmr > best_mmr:
                best, best_mmr = c, mmr
        selected.append(best)
        pool = [(c, rel) for (c, rel) in pool if c is not best]
    return selected
