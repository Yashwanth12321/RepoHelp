import requests
from typing import List, Literal
import google.generativeai as genai
import sys
from google import genai
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../embeddings")))
from embedder import select_responder_model_cli
import dotenv
dotenv.load_dotenv()
ModelType = Literal["gemini", "ollama", "fast"]

class Responder:
    def __init__(self, model: ModelType, gemini_api_key, ollama_model_name="llama3"):
        self.model = model
        self.ollama_model = ollama_model_name
        self.gemini_key = gemini_api_key

        if self.model == "gemini":
            if not gemini_api_key:
                raise ValueError("Gemini API key is required for Gemini response generation.")

    def summarize(self, chunks: List[dict]) -> str:
        context = "\n\n".join(chunk["content"] for chunk in chunks)

        prompt = (
            "You are a helpful assistant. Summarize the following source code and files into a high-level overview. "
            "Explain what this repository is about, major components, and how everything fits together.\n\n"
            f"{context}"
        )

        Client = genai.Client(api_key=self.gemini_key)

        response = Client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    def answer(self, query: str, chunks: List[dict]) -> str:
        context =  "\n\n".join(chunk["content"] for chunk in chunks)
        prompt = f"""
You're a helpful AI assistant for understanding codebases. 
The user asked: "{query}"

Here are relevant code snippets from a GitHub repository:

{context}

Using the above context, answer the user's query clearly and concisely.
"""
        if self.model == "gemini":
            return self._gemini_generate(prompt)
        elif self.model == "ollama":
            return self._ollama_generate(prompt)
        else:
            print("wrong")
            raise ValueError("Unsupported model selected.")

    def _gemini_generate(self, prompt: str) -> str:
        Client = genai.Client(api_key=self.gemini_key)

        response = Client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    def _ollama_generate(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise RuntimeError(f"Ollama generation failed: {response.text}")
        return response.json()["response"]


# if __name__ == "__main__":
#     model = select_responder_model_cli()
#     responder = Responder(model=model, gemini_api_key=os.getenv("GEMINI_API_KEY"))

#     chunks = [
#         "def add(x, y): return x + y",
#         "def subtract(x, y): return x - y"
#     ]
#     question = "What does the code do?"
#     answer = responder.answer(question, chunks)
#     print(f"\n🧠 AI Response:\n{answer}")
