from parsing.repo_loader import clone_repo, collect_code_files
from parsing.code_chunker import chunk_all_files
from embeddings.embedder import Embedder
from embeddings.vector_Store import VectorStore
import getpass
import sys
if __name__ == "__main__":
    url = input("Enter GitHub Repo URL: ")
    print("\nChoose embedding model:")
    print("1. Gemini (Google AI)")
    print("2. Ollama (local)")
    print("3. local")
    model_choice = input("Your choice (1 or 2): ").strip()
    if model_choice not in ["1", "2","3"]:
        print("Invalid choice.")
        sys.exit(1)

# Set model type and keys
    model = "gemini" if model_choice == "1" else "ollama" if model_choice == "2" else "local"
    
    repo_path = clone_repo(url)
    files = collect_code_files(repo_path)
    print(f"Found {len(files)} code files.")
    if model == "gemini":
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
    else:
        gemini_key = None
    chunks = chunk_all_files(files)
    print(f"Generated {len(chunks)} chunks.")
    # for c in chunks[:5]:
    #     print(f"\n--- Chunk ({c['file']}): {c['start_line']}–{c['end_line']}\n{c['content'][:300]}")
    
    embedder = Embedder(model, gemini_api_key=gemini_key)
    vector_min=738 if model =="ollama" else 768
    store=VectorStore(dim=vector_min)  
    total_embeds=0
    metadata=[]
    embeddings=[]

    print("Generating")

    for chunk in chunks:
        file_path = chunk["file"]
        content = chunk["content"]
        start_line = chunk["start_line"]
        end_line = chunk["end_line"]
        try:
            embedding = embedder.get_embedding(content)
            embeddings.append(embedding)
            metadata.append({
                "file": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "content": content
            })
            total_embeds += 1
        except Exception as e:
            print(f"Skipping chunk in {file_path}:{start_line}-{end_line}: {e}")
        
    print(f"[info] embedded {total_embeds} chunks")
    print("saving vector store...")
    store.add(embeddings, metadata)
    store.save()
    print("[info] saved vector store")
    print("\nDone.")
    print("Embeddings saved to vector_Store")
    