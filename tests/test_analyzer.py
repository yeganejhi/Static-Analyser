# tests/test_analyzer.py
import os
import sys
import unittest
import ast

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core import CustomVisitor, generate_ast

class TestStaticAnalyzer(unittest.TestCase):
    def run_analysis(self, source_code):
        tree = generate_ast(source_code)
        visitor = CustomVisitor(file_path="test.py")
        visitor.visit(tree)
        visitor.finalize_analysis()
        return visitor

    def test_unused_variables_with_line_numbers(self):
        bad_code = """
def calculate():
    used_var = 10
    unused_var = 50  
    return used_var
"""
        visitor = self.run_analysis(bad_code)
        
        unused_issues = [
            issue for issue in visitor.issues 
            if "unused_var" in issue['message']
        ]
        
        self.assertEqual(len(unused_issues), 1)
        self.assertNotEqual(unused_issues[0]['line'], '?')
        self.assertEqual(unused_issues[0]['line'], 4)    
        
    def test_variable_scopes(self):
        bad_code = """
def function1():
    x = 10
    return x

def function2():
    y = 20  
    return 5
"""
        visitor = self.run_analysis(bad_code)
        
        y_issues = [
            issue for issue in visitor.issues 
            if "y" in issue['message'] and "defined but never used" in issue['message']
        ]
        self.assertEqual(len(y_issues), 1)
        
        x_issues = [
            issue for issue in visitor.issues 
            if "x" in issue['message'] and "defined but never used" in issue['message']
        ]
        self.assertEqual(len(x_issues), 0)

    def test_list_comprehension_variables(self):
        code = """
def process():
    result = [x * 2 for x in range(10)]
    return result
"""
        visitor = self.run_analysis(code)
        x_issues = [
            issue for issue in visitor.issues 
            if "x" in issue['message'] and "defined but never used" in issue['message']
        ]
        self.assertEqual(len(x_issues), 0)

    def test_dead_code_detection_basic(self):
        bad_code = """
def check_status():
    return 'Active'
    print('dead line')
    x = 100
"""
        visitor = self.run_analysis(bad_code)
        unreachable_messages = [
            issue['message'] for issue in visitor.issues 
            if "Unreachable code" in issue['message']
        ]
        self.assertEqual(len(unreachable_messages), 2)
    
    def test_dead_code_with_if_else(self):
        bad_code = """
def process(value):
    if value > 10:
        return "High"
    else:
        return "Low"
    print("This is dead")
"""
        visitor = self.run_analysis(bad_code)
        unreachable_messages = [
            issue['message'] for issue in visitor.issues 
            if "Unreachable code" in issue['message']
        ]
        self.assertEqual(len(unreachable_messages), 1)
    
    def test_no_false_positive(self):
        good_code = """
def process(value):
    if value > 10:
        return "High"
    else:
        print("Low")
    return "Done"
"""
        visitor = self.run_analysis(good_code)
        unreachable_messages = [
            issue['message'] for issue in visitor.issues 
            if "Unreachable code" in issue['message']
        ]
        self.assertEqual(len(unreachable_messages), 0)

    def test_naming_convention_violations(self):
        bad_code = "def badFunction():\n    pass\n\nclass student_info:\n    pass\n"
        visitor = self.run_analysis(bad_code)
        
        messages = [issue['message'] for issue in visitor.issues]
        
        self.assertEqual(len(messages), 2)
        self.assertTrue(any("badFunction" in msg for msg in messages))
        self.assertTrue(any("student_info" in msg for msg in messages))

if __name__ == "__main__":
    unittest.main()