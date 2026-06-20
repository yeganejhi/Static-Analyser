# tests/test_analyzer.py
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','src')))
from core import CustomVisitor, generate_ast

class TestStaticAnalyzer(unittest.TestCase):
    def run_analysis(self,source_code):
        tree = generate_ast(source_code)
        visitor= CustomVisitor()
        visitor.visit(tree)
        return visitor

    def test_naming_convention_violations(self):
        bad_code = """
def badFunction(): 
    pass

class student_info: 
    pass
"""
        visitor = self.run_analysis(bad_code)
        self.assertEqual(len(visitor.naming_errors),2)

        self.assertTrue(any("badFunction" in err for err in visitor.naming_errors))
        self.assertTrue(any("student_info" in err for err in visitor.naming_errors))


    def test_unused_variables(self):
        bad_code = """
def calculate():
    used_var = 10
    unused_var = 50
    return used_var
"""
        
        visitor = self.run_analysis(bad_code)
        unused = visitor.defined_vars - visitor.used_vars
        self.assertIn("unused_var",unused)
        self.assertNotIn("used_var",unused)

    def test_dead_code_detection(self):
        bad_code = """
def check_status():
    return "Active"
    print("dead line") #first dead line 
    x = 100                  #second dead line
"""
        
        visitor = self.run_analysis(bad_code)
        self.assertEqual(len(visitor.dead_code), 2)
if __name__ == "__main__":
    unittest.main()
