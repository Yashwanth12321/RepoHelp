import os
from typing import List

def chunk_code_file(file_path: str, max_lines: int = 20, overlap: int = 5) -> List[dict]:
    chunks = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    for i in range(0, len(lines), max_lines - overlap):
        chunk = lines[i:i + max_lines]
        text = ''.join(chunk).strip()
        if text:
            chunks.append({
                "file": file_path,
                "start_line": i + 1,
                "end_line": i + len(chunk),
                "content": text
            })
    return chunks

def chunk_all_files(file_list: List[str]) -> List[dict]:
    all_chunks = []
    for file_path in file_list:
        chunks = chunk_code_file(file_path)
        all_chunks.extend(chunks)
    return all_chunks
