# src/analyzer.py
import os
import json
from core import generate_ast, CustomVisitor
from reporter import ConsoleReporter
from cli import parse_arguments
from ai_handler import AIReviewer  

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def load_config():
    default_config = {
        "max_complexity": 10,
        "disable_rules": []
    }
    config_path = "analyzer.json" 
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                user_config = json.load(file)
                default_config.update(user_config)
                print(f"Loaded configuration from {config_path}")
        except json.JSONDecodeError:
            print("Warning: analyzer.json is invalid. Using default configurations.")
    else:
        print("No analyzer.json found. Using default internal configs.")

    return default_config
def analyze_single_file(file_path,config):
    source_code = read_file(file_path)
    if source_code is None:
        return []
    tree = generate_ast(source_code)
    if tree is None:
        return [{
            "file_path": file_path,
            "line": "?",
            "column": "?", 
            "message": "Critical: File contains syntax errors and cannot be analyzed.",
            "severity": "ERROR"
        }]

    visitor = CustomVisitor(file_path=file_path,config=config)
    visitor.visit(tree)
    return visitor.finalize_analysis()
def main():
    arg = parse_arguments()
    target_path = arg.path
    export_format = arg.format

    
    config = load_config()

    all_issues = []
    if os.path.isdir(target_path):
        print(f"-> Analyzing directory: {target_path}")

        for root,dirs,files in os.walk(target_path):
            if ".venv" in root:
                continue
            for file in files :
                if file.endswith(".py"):
                    full_path = os.path.join(root,file)
                    file_issues = analyze_single_file(full_path,config)
                    all_issues.extend(file_issues)

    elif os.path.isfile(target_path):
        print(f"-> Recognizing a SINGLE FILE: {target_path}")
        all_issues = analyze_single_file(target_path,config)
    else:
        print(f"Error: Path '{target_path}' does not exist.")
        return
    
        
    if export_format == "json":
        ConsoleReporter.report_as_json(all_issues)
    else:
        print("-" * 50)       
        ConsoleReporter.report(all_issues)

        if arg.ai:
            print(f"\n🤖 Calling Gemini AI Code Reviewer...")
            ai_suggestions = AIReviewer.get_suggestions(all_issues)
            print("\n=== AI OPTIMIZATION SUGGESTIONS ===")
            print(ai_suggestions)
            print("=" * 50)
        
if __name__ == "__main__":
    main()