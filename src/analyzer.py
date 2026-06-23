# src/analyzer.py
import os
import json
from core import generate_ast, CustomVisitor
from reporter import ConsoleReporter

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

def main():
    target_file = "sample_code.py"
    EXPORT_AS_JSON = False
    
    config = load_config()
    source_code = read_file(target_file)
    
    if source_code:
        tree = generate_ast(source_code)
        
        visitor = CustomVisitor(file_path=target_file, config=config)
        visitor.visit(tree)
        
        issues = visitor.finalize_analysis()
        
        if EXPORT_AS_JSON:
            ConsoleReporter.report_as_json(issues)
        else:      
            ConsoleReporter.report(issues)

if __name__ == "__main__":
    main()