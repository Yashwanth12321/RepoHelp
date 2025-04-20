import os
import git

SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.md', '.txt', '.c', '.cpp','.tsx','.jsx','.rs','.go','.rb','.php','.swift','.kotlin'}

def clone_repo(github_url: str, clone_path: str = "./cloned_repo") -> str:
    if os.path.exists(clone_path):
        print(f"[INFO] Removing old repo at {clone_path}")
        import shutil
        shutil.rmtree(clone_path)
    print(f"[INFO] Cloning {github_url}...")
    git.Repo.clone_from(github_url, clone_path)
    return clone_path

def collect_code_files(repo_path: str) -> list:
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                full_path = os.path.join(root, file)
                code_files.append(full_path)
    return code_files

