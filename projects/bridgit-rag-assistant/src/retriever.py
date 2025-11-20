
"""
Tiny TF-IDF-ish retriever over markdown docs in data/knowledge.
- Splits documents into overlapping chunks.
- Builds a simple DF map and computes cosine similarity on TF-IDF vectors.
"""

import os, math, re, json, yaml
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple

DEFAULT_CONFIG = {
    "chunk_size": 800,
    "chunk_overlap": 120,
    "top_k_docs": 4
}

def load_config(path: str = None) -> Dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    if path and os.path.exists(path):
        with open(path, "r") as f:
            try:
                cfg.update(yaml.safe_load(f))
            except Exception:
                pass
    return cfg

def chunk_text(s: str, size: int, overlap: int) -> List[str]:
    chunks = []
    i = 0
    while i < len(s):
        chunk = s[i:i+size]
        chunks.append(chunk)
        i += max(1, size - overlap)
    return chunks

def tokenize(s: str) -> List[str]:
    return [t.lower() for t in re.findall(r"[a-zA-Z0-9']+", s)]

def tf(counter: Counter) -> Dict[str, float]:
    total = sum(counter.values())
    return {k: v/total for k, v in counter.items()} if total > 0 else {}

class SimpleVectorIndex:
    def __init__(self):
        self.docs: List[Dict[str, Any]] = []
        self.df = Counter()
        self.N = 0

    def add(self, doc_id: str, text: str, metadata: Dict[str, Any]):
        tokens = tokenize(text)
        self.docs.append({"id": doc_id, "text": text, "metadata": metadata, "tokens": Counter(tokens)})
        self.N += 1

    def finalize(self):
        # compute DF
        seen = defaultdict(set)
        for i, d in enumerate(self.docs):
            for t in d["tokens"]:
                seen[t].add(i)
        self.df = Counter({t: len(ixs) for t, ixs in seen.items()})

    def vectorize(self, tokens: Counter) -> Dict[str, float]:
        v = {}
        for t, c in tokens.items():
            idf = math.log((self.N + 1) / (1 + self.df.get(t, 0))) + 1.0
            v[t] = c * idf
        # L2 normalize
        norm = math.sqrt(sum(val*val for val in v.values()))
        if norm > 0:
            v = {k: val/norm for k, val in v.items()}
        return v

    def cosine(self, a: Dict[str, float], b: Dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        # iterate over smaller dict for speed
        if len(a) > len(b):
            a, b = b, a
        dot = sum(val * b.get(k, 0.0) for k, val in a.items())
        return dot

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        qtokens = Counter(tokenize(query))
        qv = self.vectorize(qtokens)
        scored = []
        for d in self.docs:
            dv = self.vectorize(d["tokens"])
            s = self.cosine(qv, dv)
            scored.append((s, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"score": s, **d} for s, d in scored[:top_k]]

def build_knowledge_index(knowledge_dir: str, config_path: str = None) -> SimpleVectorIndex:
    cfg = load_config(config_path)
    idx = SimpleVectorIndex()
    for fname in os.listdir(knowledge_dir):
        if not fname.endswith(".md"):
            continue
        full = os.path.join(knowledge_dir, fname)
        with open(full, "r") as f:
            text = f.read()
        chunks = chunk_text(text, cfg["chunk_size"], cfg["chunk_overlap"])
        for j, ch in enumerate(chunks):
            idx.add(doc_id=f"{fname}::chunk{j}", text=ch, metadata={"source": fname, "chunk": j})
    idx.finalize()
    return idx
