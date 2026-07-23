import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cli import parse_arguments

def test_parse_arguments_default():
    with patch('sys.argv', ['cli.py', 'sample_code.py']):
        args = parse_arguments()
        assert args.path == 'sample_code.py'
        assert args.format == 'text'   
        assert args.output is None
        assert args.config is None

def test_parse_arguments_with_options():
    with patch('sys.argv', ['cli.py', 'my_folder', '--format', 'json', '--output', 'report.json', '--config', 'config.yaml']):
        args = parse_arguments()
        assert args.path == 'my_folder'
        assert args.format == 'json'
        assert args.output == 'report.json'
        assert args.config == 'config.yaml'