import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.retriever import Retriever
from backend.responder import Responder
from memory.chat_history import ChatMemory
import pickle
import dotenv
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
            print("👋 Goodbye!")
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
    🔧 Commands:
    /history  - Show previous Q&A
    /export   - Save to 'chat_history.md'
    /clear    - Delete memory
    /exit     - Quit the program
    /help     - Show this help menu
    /summarize - Generate repo summary
    """)
            elif cmd == "/exit":
                print("Exiting.")
                break
            elif cmd == "/summarize":
                print("Summarizing entire repo...")

                # Pull all metadata (already chunked)
                with open("vector_store/metadata.json", "rb") as f:
                    all_chunks = pickle.load(f)

                response = responder.summarize(all_chunks)
                print(f"\n📄 Summary:\n{response}")

                chat_memory.add("Summarize the repo", response)
            continue
        # Retrieve relevant code chunks
        top_chunks = retriever.query(user_query, top_k=5)

        # Send to LLM (Gemini or Ollama)
        response = responder.answer(user_query, top_chunks)
        chat_memory.add(user_query, response)

        print("\n🧠 AI Response:")
        print("————————————————————")
        print(response)
        print("————————————————————")

if __name__ == "__main__":
    main()
