Custom Python Static Analysis & AST Metrics Engine
https://github.com/yeganejhi/Static-Analyser/actions/workflows/ci.yml/badge.svg
https://img.shields.io/badge/Python-3.13-blue.svg
https://img.shields.io/badge/Field-Software_Engineering_%7C_Compilers-orange.svg

A modular static analyzer that looks at Python code structure, finds potential issues, and helps enforce good coding practices. Built on Python's ast module, it parses source code into abstract syntax trees to analyze control flow and variable usage without actually running the code.

🚀 What It Does
AST-Level Analysis: Instead of using regex or string matching (which can be brittle), this tool works directly with Python's syntax tree to understand code structure at a deeper level.

Metrics Computation: Calculates things like cyclomatic complexity to give you a sense of how complex your functions are.

AI Integration Ready: There's a hook for connecting to LLMs (like OpenAI or Anthropic) if you want automated refactoring suggestions.

Clear Reporting: Outputs both color-coded terminal messages and structured JSON reports.

CI/CD Friendly: Comes with a GitHub Actions pipeline and pytest tests out of the box.

🔍 How It Works Under the Hood
1. Cyclomatic Complexity
This is basically a measure of how many independent paths exist through your code. The more decision points (if statements, loops, etc.), the higher the complexity.

The engine walks through the AST and counts:

if, for, while, and async for statements (each adds 1 to the score)

Boolean expressions with and/or (each condition adds to the complexity)

For example, if a and b or c: adds 2 to the complexity score because there are two decision points.

2. Finding Unreachable Code
Ever written code that can never run? This catches that.

If a function hits a return or raise, any code after that in the same block gets flagged.

For if/else blocks: if both branches end with return or raise, anything after the if/else is unreachable.

3. Tracking Variable Usage
The tool keeps track of which variables are defined and which ones are actually used. After scanning the whole file, it does a simple set difference:

text
Unused Variables = Defined Variables - Used Variables
This helps catch dead code and potential mistakes.

4. Naming Convention Checks
Functions should follow snake_case (e.g., my_function)

Classes should follow PascalCase (e.g., MyClass)

These rules can be turned off via configuration if needed.

🤖 AI Refactoring Integration (src/ai_handler.py)
This is an experimental feature that can send problematic code to an LLM and ask for refactoring suggestions. When the analyzer finds something like a function with complexity > 10, it packages up the code and sends it to an API (OpenAI, Anthropic, etc.) with a prompt like:

text
[SYSTEM]: You are an automated refactoring agent.
[CONTEXT]: Cyclomatic Complexity is 14 (max allowed is 10).
[INPUT CODE]: def process_data(data): ...
[TASK]: Refactor to reduce complexity. Return ONLY valid Python code.
The response is then parsed and validated to make sure it's syntactically correct before being shown to the developer.

📊 Usage Examples
Running the Analyzer
bash
# Default run (analyzes sample files)
python src/analyzer.py

# Analyze a specific directory or file
python src/analyzer.py --path ./my_project --verbose

# Save output as JSON
python src/analyzer.py --path ./src/core.py --output report.json
Sample Input
python
def badFunction(x):
    used_var = 10
    unused_var = 50
    if x > used_var:
        return True
    else:
        return False
    print("This line is completely dead!")  # Unreachable
Output Examples
Console Output (colored):

text
[ERROR] sample_dirty_code.py:1:0 — Function name 'badFunction' should be snake_case.
[WARNING] sample_dirty_code.py:8:4 — Unreachable code after return/raise.
[WARNING] sample_dirty_code.py:?:? — Variable 'unused_var' defined but never used.
JSON Output:

json
[
  {
    "file_path": "sample_dirty_code.py",
    "line": 1,
    "column": 0,
    "message": "Function name 'badFunction' should be snake_case.",
    "severity": "ERROR"
  },
  {
    "file_path": "sample_dirty_code.py",
    "line": 8,
    "column": 4,
    "message": "Unreachable code detected after return/raise.",
    "severity": "WARNING"
  }
]
Custom Configuration
You can adjust settings programmatically:

python
from core import CustomVisitor

config = {
    "max_complexity": 12,
    "disable_rules": ["naming-convention"]  # turn off naming checks
}

visitor = CustomVisitor(config=config)
🏗️ Project Structure
text
Static Analyser/
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI config
├── src/
│   ├── core.py             # AST visitors & metrics
│   ├── analyzer.py         # CLI orchestrator
│   ├── ai_handler.py       # LLM integration
│   └── reporter.py         # Output formatting
├── tests/
│   └── test_analyzer.py    # Unit tests
└── requirements.txt        # Dependencies
⚠️ Known Limitations
Cross-module analysis: The variable tracker only looks at single files. It doesn't analyze imports or global dependencies across modules.

Nested functions: Variables defined inside closures might show up as "unused" incorrectly in some edge cases.

Python version: Optimized for Python 3.10+. Older syntax (Python 2) won't parse.

🧪 Testing & CI
The project uses pytest for regression testing. The test suite isolates specific code snippets and checks that the analyzer catches the right issues.

GitHub Actions runs the full test suite on every push to main:

bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -v
📦 Installation
Requirements:

Python 3.10 or higher

Dependencies listed in requirements.txt

Setup:

bash
git clone https://github.com/yeganejhi/Static-Analyser.git
cd Static-Analyser
pip install -r requirements.txt
pytest -v  # verify everything works
📚 References
This work draws on foundational concepts from program analysis and software metrics:

McCabe, T. J. (1976). A Complexity Measure. IEEE Transactions on Software Engineering. (The classic paper on cyclomatic complexity.)

Nielson, F., Nielson, H. R., & Hankin, C. (2015). Principles of Program Analysis. Springer. (A comprehensive reference on static analysis and data-flow.)