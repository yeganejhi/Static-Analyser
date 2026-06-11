import os
from core import generate_ast,get_ast_dump
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
        print("\n--- Generating and Dumping Complete AST ---")
        
        tree = generate_ast(source_code)
        full_ast_text = get_ast_dump(tree)

        print(full_ast_text)
if __name__ == "__main__":
    main()


    
