# src/cli.py
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Static Analyser: A professional code quality analysis tool for Python."
    )

    parser.add_argument(
        "path",
        type=str,
        help="Path to the Python file or directory to analyze"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json", "sarif"],
        default="text",
        help="Output format for the analysis report (default: text)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for SARIF or JSON reports"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to custom configuration file"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    print(f"Target Path: {args.path}")
    print(f"Selected Format: {args.format}")