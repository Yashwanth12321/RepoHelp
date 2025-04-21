import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.retriever import Retriever
from backend.responder import Responder
from memory.chat_history import ChatMemory
import dotenv
import json
dotenv.load_dotenv()

def main():
    print("Welcome to RepoChat! or type /help")
 

    
    # Let user pick embedding + chat model
    retriever = Retriever()
    responder = Responder(model="gemini", gemini_api_key=os.getenv("GEMINI_API_KEY"))
    chat_memory = ChatMemory()

    while True:
        user_query = input("\nAsk something about the repo (or type 'exit', /help for details): ")
        if user_query.strip().lower() in ["exit", "quit"]:
            print(" Goodbye!")
            break
        if user_query.strip() == "":
            continue
        if user_query.startswith("/"):
            cmd = user_query.strip().lower()

            if cmd == "/history":
                chat_memory.show()
            elif cmd == "/export":
                chat_memory.export()
                print("Chat history exported to chat_history.md")
            elif cmd == "/clear":
                confirm = input("Are you sure? This will delete all history. (yes/no): ")
                if confirm.lower() == "yes":
                    chat_memory.clear()
                    print("🧹 History cleared.")
            elif cmd == "/help":
                print("""
             Commands:
            /history           - Show previous Q&A
            /export            - Save to 'chat_history.md'
            /clear             - Delete memory
            /exit              - Quit the program
            /help              - Show this help menu
            /summarize         - Generate repo summary
            /explain <file>    - Explain what a file does
            /find <function>   - Find function definition and purpose
            /how-does <feat>   - How a feature/logic works in the repo
            """)
            elif cmd == "/exit":
                print("Exiting.")
                break
            elif cmd == "/summarize":
                print("Summarizing entire repo...")

                # Pull all metadata (already chunked)
                with open("vector_store/metadata.json", "rb") as f:
                    all_chunks = json.load(f)

                response = responder.summarize(all_chunks)
                print(f"\n Summary:\n{response}")

                chat_memory.add("Summarize the repo", response)
            elif cmd.startswith("/explain "):
                file_path = user_query[len("/explain "):].strip()
                prompt = f"Explain what the file '{file_path}' does in this repo."
                top_chunks = retriever.query(prompt)
                response = responder.answer(prompt, top_chunks)
                print(f"\n Explanation of {file_path}:\n{response}")
                chat_memory.add(prompt, response)

            elif cmd.startswith("/find "):
                func_name = user_query[len("/find "):].strip()
                prompt = f"Where is the function '{func_name}' defined and what does it do?"
                top_chunks = retriever.query(prompt)
                response = responder.answer(prompt, top_chunks)
                print(f"\nFunction '{func_name}' info:\n{response}")
                chat_memory.add(prompt, response)

            elif cmd.startswith("/how-does "):
                feature = user_query[len("/how-does "):].strip()
                prompt = f"How does the feature '{feature}' work in this codebase?"
                top_chunks = retriever.query(prompt)
                response = responder.answer(prompt, top_chunks)
                print(f"\n How '{feature}' works:\n{response}")
                chat_memory.add(prompt, response)
            else :
                print("Unknown prompt")

            continue
        # Retrieve relevant code chunks
        top_chunks = retriever.query(user_query, top_k=5)

        # Send to LLM (Gemini or Ollama)
        response = responder.answer(user_query, top_chunks)
        chat_memory.add(user_query, response)

        print("\nAI Response:")
        print("————————————————————")
        print(response)
        print("————————————————————")

if __name__ == "__main__":
    main()
