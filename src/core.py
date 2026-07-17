# src/core.py
import re
import ast

COMPLEXITY_THRESHOLD = 10

def generate_ast(source_code):
    try:
        tree = ast.parse(source_code)
        return tree
    except SyntaxError as e:
        print(f"[SYNTAX ERROR] Invalid Python syntax: {e.msg} (Line {e.lineno})")        
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
        
class SecurityVisitor(ast.NodeVisitor):
    """تحلیلگر امنیتی"""
    def __init__(self, file_path, issues):
        self.file_path = file_path
        self.issues = issues
        self.in_loop = False
        self.loop_depth = 0
    
    def visit_Call(self, node):
        # تشخیص استفاده از توابع خطرناک
        if isinstance(node.func, ast.Name):
            dangerous_funcs = {
                'eval': 'Use of eval() is dangerous and can lead to code injection',
                'exec': 'Use of exec() is dangerous and can lead to code injection',
                'compile': 'Use of compile() with untrusted input is dangerous',
                '__import__': 'Dynamic imports can be a security risk',
                'input': 'Using input() in Python 2 is dangerous (use raw_input() or Python 3 input with caution)'
            }
            
            if node.func.id in dangerous_funcs:
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': f"Security Issue: {dangerous_funcs[node.func.id]}",
                    'severity': 'ERROR',
                    'category': 'security'
                })
        
        # تشخیص SQL injection احتمالی
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ['execute', 'executemany', 'cursor']:
                for arg in node.args:
                    if isinstance(arg, ast.Name) or isinstance(arg, ast.BinOp):
                        self.issues.append({
                            'file_path': self.file_path,
                            'line': node.lineno,
                            'column': node.col_offset,
                            'message': "Potential SQL Injection: Using dynamic query with user input",
                            'severity': 'WARNING',
                            'category': 'security'
                        })
                        break
        
        self.generic_visit(node)
    
    def visit_While(self, node):
        """تشخیص حلقه‌های بی‌نهایت"""
        self.loop_depth += 1
        self.in_loop = True
        
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            has_break = False
            has_return = False
            
            for child in ast.walk(node):
                if isinstance(child, ast.Break):
                    has_break = True
                elif isinstance(child, ast.Return):
                    has_return = True
            
            if not has_break and not has_return:
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': "Potential infinite loop detected: 'while True' without break or return",
                    'severity': 'WARNING',
                    'category': 'performance'
                })
        
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False
    
    def visit_For(self, node):
        self.loop_depth += 1
        self.in_loop = True
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False

class PerformanceVisitor(ast.NodeVisitor):
    """تحلیلگر عملکرد"""
    def __init__(self, file_path, issues):
        self.file_path = file_path
        self.issues = issues
        self.in_loop = False
        self.loop_depth = 0
    
    def visit_BinOp(self, node):
        if self.in_loop and isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': "Performance Issue: String concatenation inside loop. Use str.join() or list append",
                    'severity': 'WARNING',
                    'category': 'performance'
                })
        self.generic_visit(node)
    
    def visit_For(self, node):
        was_in_loop = self.in_loop
        self.in_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = was_in_loop
    
    def visit_While(self, node):
        was_in_loop = self.in_loop
        self.in_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = was_in_loop
        
class CustomVisitor(ast.NodeVisitor):
    def __init__(self, file_path="sample_code", config=None):
        super().__init__()
        self.file_path = file_path
        self.config = config if config else {"max_complexity": 10, "disable_rules": []}
        self.issues = []

        self.scope_stack = []
        self.current_scope = {
            'defined_vars': {},
            'used_vars': set(),
            'function_name': None
        }

        self.snake_case_pattern = r"^[a-z_][a-z0-9_]*$"
        self.camel_case_pattern = r"^[A-Z][a-zA-Z0-9]*$"

        self.current_function = None

    def _enter_scope(self, function_name=None):
        self.scope_stack.append(self.current_scope)
        self.current_scope = {
            'defined_vars': {},
            'used_vars': set(),
            'function_name': function_name
        }

    def _exit_scope(self):
        if self.current_scope['defined_vars']:
            unused = set(self.current_scope['defined_vars'].keys()) - self.current_scope['used_vars']
            for var_name in unused:
                line, col = self.current_scope['defined_vars'][var_name]
                self.issues.append({
                    'file_path': self.file_path,
                    'line': line,
                    'column': col,
                    'message': f"Variable '{var_name}' is defined but never used.",
                    'severity': 'WARNING',
                    'category': 'code_quality'
                })
        
        if self.scope_stack:
            self.current_scope = self.scope_stack.pop()

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
                'severity': 'WARNING',
                'category': 'code_quality'
            })
            
        if "naming-convention" not in self.config.get("disable_rules", []):
            if not re.match(self.snake_case_pattern, node.name):
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': f"Function name '{node.name}' should be snake_case (e.g., my_function).",
                    'severity': 'ERROR',
                    'category': 'code_quality'
                })

        self._enter_scope(function_name=node.name)

        has_returned = False
        for child_node in node.body:
            if has_returned:
                self.issues.append({
                    'file_path': self.file_path,
                    'line': child_node.lineno,
                    'column': child_node.col_offset,
                    'message': "Unreachable code detected after return/raise statement.",
                    'severity': 'WARNING',
                    'category': 'code_quality'
                })
                continue

            if isinstance(child_node, (ast.Return, ast.Raise)):
                has_returned = True
            elif isinstance(child_node, ast.If):
                if_has_return = any(isinstance(n, (ast.Return, ast.Raise)) for n in child_node.body)
                else_has_return = any(isinstance(n, (ast.Return, ast.Raise)) for n in child_node.orelse)
                
                if if_has_return and else_has_return:
                    has_returned = True

        self.generic_visit(node)
        
        security_visitor = SecurityVisitor(self.file_path, self.issues)
        security_visitor.visit(node)
        
        performance_visitor = PerformanceVisitor(self.file_path, self.issues)
        performance_visitor.visit(node)
        
        self._exit_scope()
        self.current_function = None

    def visit_ClassDef(self, node):
        if "naming-convention" not in self.config.get("disable_rules", []):
            if not re.match(self.camel_case_pattern, node.name):
                self.issues.append({
                    'file_path': self.file_path,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': f"Class name '{node.name}' should be PascalCase (e.g., MyClass).",
                    'severity': 'ERROR',
                    'category': 'code_quality'
                })
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.current_scope['defined_vars'][target.id] = (node.lineno, node.col_offset)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.current_scope['used_vars'].add(node.id)
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        for gen in node.generators:
            if isinstance(gen.target, ast.Name):
                self.current_scope['defined_vars'][gen.target.id] = (node.lineno, node.col_offset)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        for gen in node.generators:
            if isinstance(gen.target, ast.Name):
                self.current_scope['defined_vars'][gen.target.id] = (node.lineno, node.col_offset)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        for gen in node.generators:
            if isinstance(gen.target, ast.Name):
                self.current_scope['defined_vars'][gen.target.id] = (node.lineno, node.col_offset)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        for gen in node.generators:
            if isinstance(gen.target, ast.Name):
                self.current_scope['defined_vars'][gen.target.id] = (node.lineno, node.col_offset)
        self.generic_visit(node)

    def finalize_analysis(self):
        if self.current_scope['defined_vars']:
            unused = set(self.current_scope['defined_vars'].keys()) - self.current_scope['used_vars']
            for var_name in unused:
                line, col = self.current_scope['defined_vars'][var_name]
                self.issues.append({
                    'file_path': self.file_path,
                    'line': line,
                    'column': col,
                    'message': f"Variable '{var_name}' is defined but never used.",
                    'severity': 'WARNING',
                    'category': 'code_quality'
                })
        return self.issues