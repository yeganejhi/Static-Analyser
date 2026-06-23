# src/core.py
import re
import ast

COMPLEXITY_THRESHOLD = 10

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

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if isinstance(node.op, (ast.And, ast.Or)):
            self.complexity += len(node.values) - 1
        self.generic_visit(node)
        
class CustomVisitor(ast.NodeVisitor):
    def __init__(self, file_path="sample_code", config=None):
        super().__init__()
        self.file_path = file_path
        self.config = config if config else {"max_complexity": 10, "disable_rules": []}
        self.issues = []

        self.defined_vars = set()
        self.used_vars = set()

        self.snake_case_pattern = r"^[a-z_][a-z0-9_]*$"
        self.camel_case_pattern = r"^[A-Z][a-zA-Z0-9]*$"

        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name

        sub_visitor = ComplexityVisitor()
        sub_visitor.visit(node)
        complexity_score = sub_visitor.complexity

        max_allowed_complexity = self.config.get("max_complexity", 10)
        if complexity_score > max_allowed_complexity:
            self.issues.append({
                'file_path': self.file_path,
                'line': node.lineno,
                'column': node.col_offset,
                'message': f"Function '{node.name}' is too complex (Cyclomatic Complexity: {complexity_score}). Max allowed is {max_allowed_complexity}.",
                'severity': 'WARNING' 
            })
            
        if "naming-convention" not in self.config.get("disable_rules", []):
            if not re.match(self.snake_case_pattern, node.name):
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': f"Function name '{node.name}' should be snake_case (e.g., my_function).",
                    'severity': 'ERROR'
                })

        has_returned = False
        for child_node in node.body:
            if has_returned:
                self.issues.append({
                    'file_path': self.file_path,
                    'line': child_node.lineno,
                    'column': child_node.col_offset,
                    'message': "Unreachable code detected after return/raise statement.",
                    'severity': 'WARNING' 
                })

            if isinstance(child_node, (ast.Return, ast.Raise)):
                has_returned = True
            elif isinstance(child_node, ast.If):
                if_has_return = any(isinstance(n, (ast.Return, ast.Raise)) for n in child_node.body)
                else_has_return = any(isinstance(n, (ast.Return, ast.Raise)) for n in child_node.orelse)
                
                if if_has_return and else_has_return:
                    has_returned = True

        self.generic_visit(node)
        self.current_function = None

    def visit_ClassDef(self, node):
        if "naming-convention" not in self.config.get("disable_rules", []):
            if not re.match(self.camel_case_pattern, node.name):
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': f"Class name '{node.name}' should be PascalCase (e.g., MyClass).",
                    'severity': 'ERROR'
                })
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)
    
    def finalize_analysis(self):
        unsed_vars = self.defined_vars - self.used_vars

        for var in unsed_vars:
            self.issues.append({
                'file_path': self.file_path,
                'line': '?',
                'column': '?',
                'message': f"Variable '{var}' is defined but never used.",
                'severity': 'WARNING'
            })
        return self.issues