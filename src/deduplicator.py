"""
Removes duplicate or near-duplicate articles based on embeddings.
"""
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np

# load model once
_EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')


class Deduplicator:
    @staticmethod
    def dedupe(items: List[Dict[str, Any]], threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Removes near-duplicate articles using cosine similarity on embeddings.
        """
        texts = [it['body'] for it in items]
        embeddings = _EMBED_MODEL.encode(texts, convert_to_numpy=True)
        keep = []
        for idx, emb in enumerate(embeddings):
            if not any(
                np.dot(emb, embeddings[j]) / (np.linalg.norm(emb) * np.linalg.norm(embeddings[j]))
                > threshold
                for j in keep
            ):
                keep.append(idx)
        return [items[i] for i in keep]