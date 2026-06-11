import ast
import os

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    with open(file_path,'r',encoding='utf-8') as file:
        return file.read()
    
def main():
    target_file ="sample_code.py"
    print("--- Step 1: Reading File Content ---")

    source_code = read_file(target_file)
    if(source_code):
        print(source_code)
        print("-" * 36)

        print("\n--- Step 2: Testing AST Parsing ---")
        try:
            tree = ast.parse(source_code)
            print("Successfully parsed code into AST!")
            print("Root node fields:", ast.dump(tree, indent=2)[:300] + "...\n[Truncated]")

        except SyntaxError as e:
            print(f"Syntax Error in target file: {e}")
if __name__ == "__main__":
    main()


    
