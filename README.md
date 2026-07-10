# PyAnalyzer - Static Code Analysis Tool for Python

[![CI Status](https://github.com/yeganejhi/Static-Analyser/actions/workflows/ci.yml/badge.svg)](https://github.com/yeganejhi/Static-Analyser/actions)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight static analyzer that looks at Python code structure, finds potential issues, and helps enforce good coding practices. Built on Python's ast module, it parses source code into abstract syntax trees to analyze control flow and variable usage without actually running the code.

---

## Highlights

Here's what this tool can do for you:

- AST-based analysis instead of fragile regex patterns
- No external dependencies besides colorama for terminal output
- Calculates cyclomatic complexity to find overly complex functions
- Detects unused variables, dead code, and naming violations
- Outputs both color-coded terminal messages and structured JSON
- Configurable thresholds and rule toggles
- Comes with GitHub Actions workflow and pytest tests

---

## Overview

This project started as a way to better understand how static analysis works under the hood. Instead of just using existing linters, I wanted to build something from scratch using Python's AST module and learn about things like cyclomatic complexity and control flow analysis.

The tool examines Python code at the AST level, which means it actually understands the structure of your code rather than just matching text patterns. It walks through the syntax tree and looks for:

- Functions that are too complex (cyclomatic complexity above a threshold)
- Code that can never execute (dead code after return or raise)
- Variables that are defined but never used
- Function names that don't follow snake_case
- Class names that don't follow PascalCase

You can run it on a single file or an entire directory, and it will generate a report showing any issues it finds.

---

## Quick Start

Getting started takes just a few seconds:

```bash
# Install the only dependency
pip install -r requirements.txt

# Run on a single file
python src/analyzer.py sample_code.py

# Run on an entire project
python src/analyzer.py ./my_project

# Get JSON output for CI/CD
python src/analyzer.py ./src --format json
```

Here's what the output looks like:

```
-> Analyzing directory: ./my_project
Loaded configuration from analyzer.json

=== STATIC ANALYSIS REPORT ===
--------------------------------------------------
[ERROR] sample_code.py:1:0 - Function name 'badFunction' should be snake_case
[WARNING] sample_code.py:8:4 - Unreachable code after return/raise
[WARNING] sample_code.py:?:? - Variable 'unused_var' defined but never used
--------------------------------------------------
Total issues found: 3
```

---

## How It Works

The tool uses Python's built-in ast module to parse source code into an abstract syntax tree, then walks through that tree to analyze different aspects of the code.

### Cyclomatic Complexity

This measures how many independent paths exist through your code. The more decision points (if statements, loops, etc.), the higher the complexity score. The tool counts:

- Each if, for, while, and async for statement adds 1 to the score
- Boolean expressions with and/or add to the complexity as well

For example, `if a and b or c:` adds 2 to the complexity score because there are two decision points.

### Unused Variable Detection

The tool keeps track of which variables are defined and which ones are actually used. After scanning the whole file, it does a simple set difference:

```
Unused Variables = Defined Variables - Used Variables
```

This helps catch dead code and potential mistakes.

### Unreachable Code Detection

Ever written code that can never run? The tool catches that:

- If a function hits a return or raise, any code after that in the same block gets flagged
- For if/else blocks, if both branches end with return or raise, anything after the whole block is unreachable

### Naming Convention Checks

The tool checks that:

- Functions use snake_case (like my_function)
- Classes use PascalCase (like MyClass)

These checks can be turned off in the configuration if needed.

---

## Configuration

You can customize the tool's behavior by creating a `analyzer.json` file in your project root:

```json
{
  "max_complexity": 12,
  "disable_rules": ["naming-convention"]
}
```

Available options:

- `max_complexity`: Maximum allowed cyclomatic complexity (default is 10)
- `disable_rules`: List of rules to skip, currently only "naming-convention" is available

If no configuration file is found, the tool uses default settings.

---

## Example Usage

Let's say you have this code in `sample.py`:

```python
def badFunction(x):
    used_var = 10
    unused_var = 50
    if x > used_var:
        return True
    else:
        return False
    print("This line is completely dead!")
```

Running the analyzer gives you:

```
=== STATIC ANALYSIS REPORT ===
--------------------------------------------------
[ERROR] sample.py:1:0 - Function name 'badFunction' should be snake_case
[WARNING] sample.py:8:4 - Unreachable code detected after return/raise
[WARNING] sample.py:?:? - Variable 'unused_var' defined but never used
--------------------------------------------------
Total issues found: 3
```

If you need JSON output (useful for CI/CD pipelines):

```json
[
  {
    "file_path": "sample.py",
    "line": 1,
    "column": 0,
    "message": "Function name 'badFunction' should be snake_case",
    "severity": "ERROR"
  },
  {
    "file_path": "sample.py",
    "line": 8,
    "column": 4,
    "message": "Unreachable code detected after return/raise",
    "severity": "WARNING"
  },
  {
    "file_path": "sample.py",
    "line": "?",
    "column": "?",
    "message": "Variable 'unused_var' defined but never used",
    "severity": "WARNING"
  }
]
```

---

## Project Structure

Here's how the code is organized:

```
Static-Analyser/
├── .github/workflows/
│   └── ci.yml              # GitHub Actions configuration
├── src/
│   ├── analyzer.py         # Main orchestrator and file traversal
│   ├── core.py             # AST visitors and metrics
│   ├── cli.py              # Command-line argument parsing
│   └── reporter.py         # Output formatting (console and JSON)
├── tests/
│   └── test_analyzer.py    # Unit tests
├── sample_code.py          # Example code for testing
└── requirements.txt        # Dependencies
```

---

## Installation

You only need Python 3.10 or higher (tested on 3.13). The only external dependency is colorama for colored terminal output.

```bash
git clone https://github.com/yeganejhi/Static-Analyser.git
cd Static-Analyser
pip install -r requirements.txt
```

To verify everything works:

```bash
pytest -v
```

---

## Testing

The project uses pytest for testing. The test suite covers:

- Naming convention violations
- Unused variable detection
- Dead code detection
- Complexity threshold enforcement

GitHub Actions runs the full test suite on every push to the main branch.

```bash
pytest -v
```

---

## Known Limitations

There are a few things the tool doesn't handle perfectly yet:

- Cross-module analysis isn't supported - it only looks at single files and doesn't track variables across imports
- Nested functions might cause some false positives in certain edge cases
- Only supports Python 3.10+ syntax (no Python 2)

These are things I'd like to improve in future versions.

---

## Contributing

If you find a bug or have an idea for improvement, feel free to open an issue or submit a pull request. Here's how you can contribute:

1. Fork the repository
2. Create a branch for your changes
3. Add tests for any new functionality
4. Make sure all tests pass
5. Submit a pull request

For development setup:

```bash
git clone https://github.com/yeganejhi/Static-Analyser.git
cd Static-Analyser
pip install -r requirements.txt
```

---

## Further Reading

If you want to learn more about the concepts behind this tool:

- McCabe's original paper on cyclomatic complexity is a good starting point
- The Python AST documentation explains how Python represents code structure
- There are some good guides online about writing static analysis tools

---

## Author

I'm Yegane Jhi, majoring in computer science, interested in compilers and program analysis. This project was a way to learn more about how static analysis tools work by building one from scratch.

[GitHub](https://github.com/yeganejhi)

---

**If you find this useful, consider giving it a star on GitHub.**
