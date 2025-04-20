
import requests
import os
import json
from typing import List, Literal
from google import genai
import numpy as np
from sentence_transformers import SentenceTransformer
import dotenv
dotenv.load_dotenv()

ModelType = Literal["gemini", "ollama", "local"]
class Embedder:
    def __init__(self, model: ModelType, ollama_model_name="nomic-embed-text", gemini_api_key=None,local_model_name:str="all-MiniLM-L6-v2"):
        self.model = model
        self.gemini_key = gemini_api_key
        self.ollama_model = ollama_model_name
        self.local_model_name=local_model_name
        if model == "gemini":
            if not gemini_api_key:
                raise ValueError("Gemini API key required for Gemini embedding.")
            self.client=genai.Client(api_key=gemini_api_key)
        elif model == "ollama":
            if not ollama_model_name:
                raise ValueError("Ollama model name required for Ollama embedding.")
            self.ollama_model = ollama_model_name
        elif model=="local":
            self.local_model = SentenceTransformer(local_model_name)

    def get_embedding(self, text: str) -> List[float]:
        if self.model == "gemini":
            return self._embed_gemini(text)
        elif self.model == "ollama":
            return self._embed_ollama(text)
        elif self.model=="local":
            return self._embed_local(text)
        else:
            raise ValueError("Unsupported embedding model")
    def _embed_gemini(self, text: str) -> List[float]:
        result = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text,
        )
        return np.array(result.embeddings[0].values)
    def _embed_ollama(self, text: str) -> List[float]:
        url = "http://localhost:11434/api/embeddings"
        headers = {"Content-Type": "application/json"}
        body = {"model": self.ollama_model, "prompt": text}

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise RuntimeError(f"Ollama embedding failed: {response.text}")

        return response.json()["embedding"]
    
    def _embed_local(self,text:str)->List[float]:
        return self.local_model.encode(text).tolist()


def select_model_cli() -> Embedder:
    print("\n Choose your embedding model:")
    print("1. Gemini (Google API)")
    print("2. Ollama (Local LLM via API)")
    print("3. Local SentenceTransformer (Fastest)")

    choice = input("Enter choice (1/2/3): ").strip()
    if choice == "1":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        return Embedder(model="gemini", gemini_api_key=api_key)
    elif choice == "2":
        model_name = input("Enter Ollama model name [default: nomic-embed-text]: ").strip() or "nomic-embed-text"
        return Embedder(model="ollama", ollama_model_name=model_name)
    elif choice == "3":
        local_model = input("Enter local model name [default: all-MiniLM-L6-v2]: ").strip() or "all-MiniLM-L6-v2"
        return Embedder(model="local", local_model_name=local_model)
    else:
        raise ValueError("Invalid choice. Please select 1, 2, or 3.")

def select_responder_model_cli() -> Literal["gemini", "ollama", "fast"]:
    print("\n Choose your LLM model:")
    print("1. Gemini (Google API)")
    print("2. Ollama (Local LLM via API)")
    print("3. Local sentence-based (Fast)")

    choice = input("Enter choice (1/2/3): ").strip()
    if choice == "1":
        return "gemini"
    elif choice == "2":
        return "ollama"
    elif choice == "3":
        return "fast"
    else:
        raise ValueError("Invalid choice. Please select 1, 2, or 3.")
