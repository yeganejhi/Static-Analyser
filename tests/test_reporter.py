import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.reporter import ConsoleReporter

def test_report_empty_issues():
    ConsoleReporter.report([])

def test_report_with_various_severities():
    issues = [
        {'file_path': 'main.py', 'line': 10, 'column': 5, 'message': 'Syntax error', 'severity': 'ERROR'},
        {'file_path': 'utils.py', 'line': 20, 'column': 2, 'message': 'Variable unused', 'severity': 'WARNING'},
        {'file_path': 'config.py', 'line': 30, 'column': 0, 'message': 'Just an info', 'severity': 'INFO'},
        # تست حالتی که اطلاعات ناقص است
        {'message': 'Unknown issue'}
    ]
    ConsoleReporter.report(issues)

def test_report_as_json():
    issues = [
        {'file_path': 'app.py', 'line': 5, 'column': 1, 'message': 'Bad practice', 'type': 'WARNING'}
    ]
    ConsoleReporter.report_as_json(issues)