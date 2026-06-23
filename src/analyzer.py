# src/analyzer.py
import os
from core import generate_ast, CustomVisitor
from reporter import ConsoleReporter

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    target_file = "sample_code.py"
    
    print("--- Reading Target File ---")
    EXPORT_AS_JSON = False
    source_code = read_file(target_file)
    
    if source_code:
        tree = generate_ast(source_code)
        
        print("\n--- Starting AST Traversal (Visitor Pattern) ---")
        visitor = CustomVisitor(file_path=target_file)
        visitor.visit(tree)
        
        issues = visitor.filalize_analysis()
        if EXPORT_AS_JSON:
            ConsoleReporter.report_as_json(issues)
        else:
            print(f"--- Reading Target File: {target_file} ---")
            print("\n--- Starting AST Traversal (Visitor Pattern) ---")
            print("--- Traversal Completed ---")        
            ConsoleReporter.report(issues)
if __name__ == "__main__":
    main()