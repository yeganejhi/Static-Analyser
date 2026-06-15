import re
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
    return ast.dump(tree, indent=4)

class CustomVisitor(ast.NodeVisitor):

    def __init__(self):
        super().__init__()
        self.defined_vars = set()
        self.used_vars = set()

        self.naming_errors=[]
        self.snake_case_pattern = r"^[a-z_][a-z0-9_]*$"
        self.camel_case_pattern = r"^[A-Z][a-zA-Z0-9]*$"

    def visit_FunctionDef(self, node):
        print(f"📌 Found function: [ {node.name} ]")

        if not re.match(self.snake_case_pattern,node.name):
            error_msg = f"Line {node.lineno}: Function name '{node.name}' should be snake_case."
            self.naming_errors.append(error_msg)

        self.generic_visit(node)
    def visit_ClassDef(self, node):
        print(f"🏫 Found class: [ {node.name} ]")
        if not re.match(self.camel_case_pattern,node.name):
            error_msg=f"Line {node.lineno}:Class name '{node.name}' should be PascalCase (e.g., MyClass)."
            self.naming_errors.append(error_msg)
        self.generic_visit(node)


    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        print(f"🔍 Found variable/identifier: '{node.id}'")
        
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
            
        self.generic_visit(node)
    
    def report_unused_variables(self):
        unused = self.defined_vars - self.used_vars
        if unused:
            print("\n⚠️  [Static Analysis Warning] Dead/Unused Variables Found:")
            for var in unused:
                print(f"  - Variable '{var}' is defined but never used.")
        else:
            print("\n✅ No unused variables detected. Code is clean!")

    def report_naming_errors(self):
        if self.naming_errors:
            print("\n❌ [Static Analysis Error] Naming Convention Violations Found:")
            for err in self.naming_errors:
                print(f"  - {err}")
        
        else:
            print("\n✅ All functions and classes follow the PEP 8 naming style!")