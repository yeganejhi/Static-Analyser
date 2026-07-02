# tests/test_analyzer.py
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core import CustomVisitor, generate_ast

class TestStaticAnalyzer(unittest.TestCase):
    def run_analysis(self, source_code):
        tree = generate_ast(source_code)
        visitor = CustomVisitor()
        visitor.visit(tree)
        visitor.finalize_analysis()
        return visitor

    def test_naming_convention_violations(self):
        bad_code = "def badFunction():\n    pass\n\nclass student_info:\n    pass\n"
        visitor = self.run_analysis(bad_code)
        
        messages = [issue['message'] for issue in visitor.issues]
        
        self.assertEqual(len(messages), 2)
        self.assertTrue(any("badFunction" in msg for msg in messages))
        self.assertTrue(any("student_info" in msg for msg in messages))

    def test_unused_variables(self):
        bad_code = "def calculate():\n    used_var = 10\n    unused_var = 50\n    return used_var\n"
        visitor = self.run_analysis(bad_code)
        
        # استفاده از همان منطق تفاضل مجموعه‌های خودت در core.py
        unused = visitor.defined_vars - visitor.used_vars
        self.assertIn("unused_var", unused)
        self.assertNotIn("used_var", unused)

    def test_dead_code_detection(self):
        bad_code = "def check_status():\n    return 'Active'\n    print('dead line')\n    x = 100\n"
        visitor = self.run_analysis(bad_code)
        
        # فیلتر کردن خطاهای کد غیرقابل دسترس بر اساس متنی که خودت در core.py نوشتی
        unreachable_messages = [issue['message'] for issue in visitor.issues if "Unreachable code" in issue['message']]
        self.assertEqual(len(unreachable_messages), 2)

if __name__ == "__main__":
    unittest.main()