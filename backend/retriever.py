import faiss
import numpy as np
import json
from embeddings.embedder import select_model_cli

class Retriever:
    def __init__(self, index_path="vector_store/faiss.index", metadata_path="vector_store/metadata.json"):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        self.embedder = select_model_cli()

    def query(self, user_query: str, top_k=5):
        print(f"\n🔍 Embedding query: {user_query}")
        embedding = self.embedder.get_embedding(user_query)
        embedding = np.array(embedding).astype("float32").reshape(1, -1)

        _, indices = self.index.search(embedding, top_k)

        results = []
        for i in indices[0]:
            if i < len(self.metadata):
                results.append(self.metadata[i])
        
        return results
