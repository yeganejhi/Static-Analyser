import ast

def generate_ast(source_code):
    try:
        tree = ast.parse(source_code)
        return tree
    except SyntaxError as e:
        print(f"Syntax Error detected while parsing: {e}")
        return None
    
def get_ast_dump(tree):
    if tree is None:
        return "No tree to dump."
    return ast.dump(tree,indent=4)


