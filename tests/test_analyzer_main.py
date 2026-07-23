import sys
import os
import json
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import read_file, load_config, get_python_files, main

def test_read_file(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')", encoding='utf-8')
    assert read_file(str(test_file)) == "print('hello')"
    
    assert read_file(str(tmp_path / "missing.py")) is None

def test_load_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    config_file = tmp_path / "config.json"
    config_file.write_text('{"max_complexity": 20}')
    config = load_config(str(config_file))
    assert config["max_complexity"] == 20
    
    bad_config = tmp_path / "bad.json"
    bad_config.write_text('{invalid_json}')
    config_bad = load_config(str(bad_config))
    assert config_bad["max_complexity"] == 10  
def test_get_python_files(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("x = 1")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "ignore.py").write_text("y = 2")
    
    config = {"exclude_patterns": [".venv", "test_*.py"]}
    files = get_python_files(str(tmp_path), config)
    
    assert len(files) == 1
    assert "main.py" in files[0]

def test_main_integration(tmp_path):
    test_py = tmp_path / "app.py"
    test_py.write_text("x = 1\n", encoding='utf-8')
    
    with patch('sys.argv', ['analyzer.py', str(tmp_path)]):
        main() 
        
    json_out = tmp_path / "out.json"
    with patch('sys.argv', ['analyzer.py', str(test_py), '--format', 'json', '--output', str(json_out)]):
        main()
        assert json_out.exists()  

    with patch('sys.argv', ['analyzer.py', 'does_not_exist_path']):
        main()