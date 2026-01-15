#!/usr/bin/env python3
"""
Hook to enforce using uv instead of pip or other package managers.
Blocks commands that use pip, pip3, pipx, conda, or poetry.
"""
import json
import re
import sys

# Main execution
try:
    input_data = json.load(sys.stdin)
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    if tool_name != 'Bash':
        sys.exit(0)  # Only check Bash commands

    command = tool_input.get('command', '')

    # Pattern to detect package manager commands
    blocked_patterns = [
        r'\bpip\s+(install|uninstall|freeze|list|show|download)',
        r'\bpip3\s+(install|uninstall|freeze|list|show|download)',
        r'\bpipx\s+(install|uninstall|run)',
        r'\bconda\s+(install|remove|create|update)',
        r'\bpoetry\s+(add|remove|install|update)',
        r'\bpython\s+-m\s+pip\b',
        r'\bpython3\s+-m\s+pip\b',
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            print("BLOCKED: Use 'uv' instead of other package managers.")
            print("Examples:")
            print("  uv add <package>        # Add a dependency")
            print("  uv remove <package>     # Remove a dependency")
            print("  uv pip install <pkg>    # If you need pip compatibility")
            print("  uv run <command>        # Run with project dependencies")
            sys.exit(2)  # Exit code 2 blocks the tool

    sys.exit(0)

except Exception as e:
    print(f"Error in enforce_uv hook: {e}", file=sys.stderr)
    sys.exit(1)
