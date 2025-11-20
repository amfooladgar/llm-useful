import os, json
from typing import List, Dict
import numpy as np
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SK = True
except Exception:
    HAS_SK = False

def _stringify_demo(d: Dict) -> str:
    return json.dumps({"A": d.get("A"), "B": d.get("B"), "CONTEXT": d.get("CONTEXT")}, ensure_ascii=False)

class EmbeddingIndex:
    def __init__(self, backend: str = None):
        self.backend = backend or os.getenv("EMBED_BACKEND","tfidf")
        self.docs = []
        self._tfidf = None
        self._vecs = None

    def add_demos(self, demos: List[Dict]):
        self.docs = [_stringify_demo(d) for d in demos]
        if self.backend == "tfidf" and HAS_SK:
            self._tfidf = TfidfVectorizer(min_df=1, max_features=2048)
            self._vecs = self._tfidf.fit_transform(self.docs)
        # Note: FAISS/OpenSearch stubs can be added here later.

    def search(self, query: str, k: int = 3) -> List[int]:
        if self.backend == "tfidf" and HAS_SK and self._tfidf is not None:
            qv = self._tfidf.transform([query])
            sims = cosine_similarity(qv, self._vecs)[0]
            order = np.argsort(-sims)[:k]
            return list(order)
        # Fallback naive: return first k
        return list(range(min(k, len(self.docs))))
