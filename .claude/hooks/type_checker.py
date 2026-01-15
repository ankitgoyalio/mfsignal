#!/usr/bin/env python3
"""
Type checker hook for Claude Code.
Runs mypy with strict mode on Python files.
"""
import json
import subprocess
import sys

# Main execution
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get('tool_input', {}).get('file_path', '')

    if not file_path.endswith('.py'):
        sys.exit(0)  # Not a Python file

    result = subprocess.run(
        ['uv', 'run', 'mypy', '--strict', '.'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✓ mypy type check passed")
    else:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

except Exception as e:
    print(f"Error running mypy: {e}", file=sys.stderr)
    sys.exit(1)
