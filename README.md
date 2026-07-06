# Custom Python Static Analysis and AST Metrics Engine

[![Build Status](https://github.com/yeganejhi/Static-Analyser/actions/workflows/ci.yml/badge.svg)](https://github.com/yeganejhi/Static-Analyser/actions)

![Python Version](https://img.shields.io/badge/Python-3.13-blue.svg)

This tool is an lightweight static program analyzer. It is designed to evaluate software metrics and enforce syntactic and architectural guidelines. The Custom Python Static Analysis and AST Metrics Engine is built directly on top of Pythons native ast compiler modules. This tool parses source code into a tree representation to inspect control flow and lexical state without runtime execution.

---

## Technical Deep Dive and Implementation Details

The Custom Python Static Analysis and AST Metrics Engine does not rely on naive string pattern matching. Instead it operates at the syntax level. This engine resolves code structures into tree nodes.

### 1. Cyclomatic. Ast Traversal

The complexity calculation is isolated inside a ComplexityVisitor. The ComplexityVisitor tracks decision points within function scopes to map branching overhead:

* Node Coverage: The Custom Python Static Analysis and AST Metrics Engine intercepts ast.If, ast.For, ast.. Ast.AsyncFor. It increments the base complexity score for each branching event.

* Boolean Short-Circuit Analysis: The Custom Python Static Analysis and AST Metrics Engine explicitly intercepts ast.BoolOp nodes. When evaluating And or Or operators it calculates the length of the values chain to accurately register the compound complexity of conditions.

### 2. Control Flow Interruption and Unreachable Code

The Custom Python Static Analysis and AST Metrics Engine detects code after early exits inside ast.FunctionDef scopes. It tracks control-flow termination:

* Sequential Verification: The Custom Python Static Analysis and AST Metrics Engine iterates through the functions node.body statements. A boolean state flag is flipped to True immediately upon encountering an instance of ast.. Ast.Raise. Any subsequent sibling nodes processed within that scope are automatically flagged as code.

* Bidirectional Conditional Splitting: The Custom Python Static Analysis and AST Metrics Engine handles block terminations inside ast.If nodes. It evaluates if both branches independently return or raise. If both the body and orelse sub-trees terminate the control flow, any code following the if-else block in the parent scope is flagged as unreachable.

### 3. Lexical State Analysis and Variable Lifecycles

The Custom Python Static Analysis and AST Metrics Engine tracks usage trends across local and global scopes. It maps mutations during the single-pass traversal:

* Target Mapping: The Custom Python Static Analysis and AST Metrics Engine unrolls node.targets. If a target is bound as an ast.Name its identifier is injected into the defined_vars set.

* Reference Resolving: The Custom Python Static Analysis and AST Metrics Engine checks the nodes context. If the variable identifier is added to the used_vars set it is used.

* Set-Difference Finalization: Because usage maps cannot be evaluated safely until the entire tree has been fully traversed the finalize_analysis method must be invoked explicitly. It performs a set-difference operation to find variables.

### 4. Regular Expression Constraints

* Functions: The Custom Python Static Analysis and AST Metrics Engine validates functions against style guides.

* Classes: The Custom Python Static Analysis and AST Metrics Engine validates classes against PascalCase style guides.

Rules can be dynamically disabled at instantiation by passing a rule-bypassing dictionary into the config payload.

---

## Architecture and Component Layout

The repository enforces a separation of concerns by isolating parsing, state visitation and reporting layers:

```text

Static Analyser/

├──.github/workflows/

│   └── ci.yml            # GitHub Actions CI pipeline configuration

├── src/

│   ├── core.py           # AST Visitors, complexity mapping and analytics core

│   ├── analyzer.py       # Main analyzer orchestration layer

│   └── reporter.py       # Console formatters and JSON encoders

└── tests/

└── test_analyzer.py  # Automated regression test suite

```

Testing and Automated SQA Pipeline

The Custom Python Static Analysis and AST Metrics Engine uses unit testing via pytest. The systems compiler visitors are protected against regression using a test suite.

Continuous Integration

A continuous integration pipeline is fully configured via GitHub Actions. Upon every push or pull_request targeting the branch an ephemeral Linux container runs the following steps to block defective code from hitting production:

```bash

# Executed automatically in GitHub Actions virtual environment:

python -m pip install --upgrade pip

pip install pytest

pytest

```

Local Usage

To execute the Custom Python Static Analysis and AST Metrics Engine locally and run evaluations against your files:

```bash

python src/analyzer.py

```

To run the automated validation suite locally:

```bash

pip install pytest

pytest -v

```

Research and Academic Relevance

The Custom Python Static Analysis and AST Metrics Engine addresses real-world challenges in Static Program Analysis, SQA Automation and Compiler Intermediates. It showcases an understanding of building custom linting utilities manipulating tree structures parsing algorithmic complexities and designing deterministic testing suites suitable for software architecture research. The Custom Python Static Analysis and AST Metrics Engine is a tool, for researchers and developers.