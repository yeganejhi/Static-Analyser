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
    def __init__(self):
        super().__init__()
        self.defined_vars = set()
        self.used_vars = set()
        self.naming_errors = []
        self.snake_case_pattern = r"^[a-z_][a-z0-9_]*$"
        self.camel_case_pattern = r"^[A-Z][a-zA-Z0-9]*$"
        self.dead_code = []
        self.function_complexities = {}
        self.complexity_warnings = []  # اینجا غلط املایی complextiy_warning اصلاح شد

    def visit_FunctionDef(self, node):
        self.current_function = node.name

        # محاسبه پیچیدگی با ساب‌ویزیتور
        sub_visitor = ComplexityVisitor()
        sub_visitor.visit(node)
        complexity_score = sub_visitor.complexity

        self.function_complexities[node.name] = complexity_score

        # بررسی آستانه مجاز و ثبت هشدار (منطق روز ۹)
        if complexity_score > COMPLEXITY_THRESHOLD:
            warning_msg = f"Line {node.lineno}: Function '{node.name}' is too complex (Complexity: {complexity_score}). Consider refactoring."
            self.complexity_warnings.append(warning_msg)
            
        if not re.match(self.snake_case_pattern, node.name):
            error_msg = f"Line {node.lineno}: Function name '{node.name}' should be snake_case."
            self.naming_errors.append(error_msg)

        has_returned = False
        for child_node in node.body:
            if has_returned:
                msg = f"Line {child_node.lineno}: Unreachable code detected after return/raise statement."
                self.dead_code.append(msg)

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
        if not re.match(self.camel_case_pattern, node.name):
            error_msg = f"Line {node.lineno}: Class name '{node.name}' should be PascalCase (e.g., MyClass)."
            self.naming_errors.append(error_msg)
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
    
    # متدهای گزارش‌دهی نهایی
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

    def report_dead_code(self):
        if self.dead_code:
            print("\n👻 [Static Analysis Warning] Unreachable/Dead Code Detected:")
            for err in self.dead_code:
                print(f"  - {err}")
        else:
            print("\n✅ No unreachable code detected. Control flow looks healthy!")

    def report_complexity_warnings(self):
        if self.complexity_warnings:
            print("\n⚡ [Static Analysis Warning] High Cyclomatic Complexity Detected:")
            for warning in self.complexity_warnings:
                print(f"  - {warning}")
        else:
            print("\n✅ All functions have an acceptable complexity level!")