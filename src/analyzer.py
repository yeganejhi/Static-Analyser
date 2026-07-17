# src/analyzer.py
import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import generate_ast, CustomVisitor
from reporter import ConsoleReporter
from cli import parse_arguments

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def load_config(config_path=None):
    default_config = {
        "max_complexity": 10,
        "disable_rules": [],
        "enable_security": True,
        "enable_performance": True
    }
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                user_config = json.load(file)
                default_config.update(user_config)
                print(f"Loaded configuration from {config_path}")
                return default_config
        except json.JSONDecodeError:
            print(f"Warning: {config_path} is invalid. Using default configurations.")
    
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

def analyze_single_file(file_path, config):
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
            "severity": "ERROR",
            "category": "syntax"
        }]

    visitor = CustomVisitor(file_path=file_path, config=config)
    visitor.visit(tree)
    return visitor.finalize_analysis()

def get_python_files(directory, config):
    python_files = []
    exclude_patterns = config.get("exclude_patterns", [".venv", "__pycache__", "test_*.py"])
    
    for root, dirs, files in os.walk(directory):
        should_skip = False
        for pattern in exclude_patterns:
            if pattern in root:
                should_skip = True
                break
        if should_skip:
            continue
            
        for file in files:
            if file.endswith(".py"):
                skip_file = False
                for pattern in exclude_patterns:
                    if pattern in file:
                        skip_file = True
                        break
                if not skip_file:
                    python_files.append(os.path.join(root, file))
    
    return python_files

def main():
    arg = parse_arguments()
    target_path = arg.path
    export_format = arg.format
    output_file = arg.output

    config = load_config(arg.config)

    all_issues = []
    if os.path.isdir(target_path):
        print(f"-> Analyzing directory: {target_path}")
        python_files = get_python_files(target_path, config)
        print(f"-> Found {len(python_files)} Python files")
        
        for file_path in python_files:
            file_issues = analyze_single_file(file_path, config)
            all_issues.extend(file_issues)

    elif os.path.isfile(target_path):
        print(f"-> Analyzing single file: {target_path}")
        all_issues = analyze_single_file(target_path, config)
    else:
        print(f"Error: Path '{target_path}' does not exist.")
        return
    
    if export_format == "json":
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_issues, f, indent=2)
            print(f"✓ JSON report saved to {output_file}")
        else:
            ConsoleReporter.report_as_json(all_issues)
    elif export_format == "sarif":
        if output_file:
            ConsoleReporter.report_as_sarif(all_issues, output_file)
        else:
            ConsoleReporter.report_as_sarif(all_issues, "report.sarif")
    else:
        print("-" * 50)       
        ConsoleReporter.report(all_issues)

if __name__ == "__main__":
    main()