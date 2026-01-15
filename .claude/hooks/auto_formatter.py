#!/usr/bin/env python3
"""
Python formatter hook for Claude Code.
Formats Python files using ruff.
"""

import json
import subprocess
import sys

# Main execution
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith(".py"):
        sys.exit(0)  # Not a Python file

    # Run ruff check --select I --fix (import sorting)
    subprocess.run(
        ["uv", "run", "ruff", "check", "--select", "I", "--fix", file_path],
        capture_output=True,
        text=True,
    )

    # Run ruff format
    result = subprocess.run(
        ["uv", "run", "ruff", "format", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"✓ Formatted {file_path} with ruff")
    else:
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.stdout:
            print(result.stdout)

except Exception as e:
    print(f"Error formatting Python file: {e}", file=sys.stderr)
    sys.exit(1)
