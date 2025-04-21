
import ast

def extract_defs_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    elements = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            docstring = ast.get_docstring(node)
            args = []
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
            elements.append({
                "type": "class" if isinstance(node, ast.ClassDef) else "function",
                "name": name,
                "args": args,
                "docstring": docstring or "No docstring provided."
            })
    return elements

def format_for_llm(elements, file_path):
    prompt = f"# AutoDoc Request for {file_path}\n\n"
    for el in elements:
        prompt += f"### {el['type'].capitalize()}: `{el['name']}`\n"
        prompt += f"**Arguments**: {', '.join(el['args']) if el['args'] else 'None'}\n"
        prompt += f"**Docstring**: {el['docstring']}\n\n"
    prompt += "\nGenerate a markdown-style technical documentation from the above code."
    return prompt
