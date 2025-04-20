# vector_store.py

import faiss
import os
import json
import numpy as np
from typing import List, Dict

class VectorStore:
    def __init__(self, dim: int, store_path: str = "vector_store/"):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.store_path = store_path
        self.metadata: List[Dict] = []

        if not os.path.exists(store_path):
            os.makedirs(store_path)

    def add(self, embeddings: List[List[float]], metadata: List[Dict]):
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata count must match")

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def save(self):
        faiss.write_index(self.index, os.path.join(self.store_path, "faiss.index"))
        with open(os.path.join(self.store_path, "metadata.json"), "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self):
        self.index = faiss.read_index(os.path.join(self.store_path, "faiss.index"))
        with open(os.path.join(self.store_path, "metadata.json")) as f:
            self.metadata = json.load(f)

    def search(self, query_embedding: List[float], top_k: int = 5):
        query = np.array([query_embedding]).astype("float32")
        D, I = self.index.search(query, top_k)
        results = [self.metadata[i] for i in I[0]]
        return results
