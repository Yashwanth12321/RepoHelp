
import json
import os
from datetime import datetime

class ChatMemory:
    def __init__(self, path="chat_history.json"):
        self.path = path
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return []

    def add(self, question, answer):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer
        })
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.history, f, indent=2)

    def show(self):
        for idx, entry in enumerate(self.history, 1):
            print(f"\n--- Chat {idx} ---")
            print(f"> Q: {entry['question']}")
            print(f"A: {entry['answer']}")

    def clear(self):
        self.history = []
        self._save()

    def export(self, out_file="chat_history.md"):
        with open(out_file, "w") as f:
            for idx, entry in enumerate(self.history, 1):
                f.write(f"### Chat {idx}\n")
                f.write(f"**Q:** {entry['question']}\n\n")
                f.write(f"**A:** {entry['answer']}\n\n")
