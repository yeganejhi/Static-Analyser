# src/analyzer.py
import os
from core import generate_ast, CustomVisitor

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    target_file = "sample_code.py"
    
    print("--- Reading Target File ---")
    source_code = read_file(target_file)
    
    if source_code:
        tree = generate_ast(source_code)
        
        print("\n--- Starting AST Traversal (Visitor Pattern) ---")
        visitor = CustomVisitor()
        
        visitor.visit(tree)
        print("------------------------------------------------")

if __name__ == "__main__":
    main()