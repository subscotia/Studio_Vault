#!/usr/bin/env python3
"""
analyze_scripts.py

🎯 PURPOSE:
Scans the current directory for all Python scripts (*.py) and generates a
summary report for each one. This provides a high-level overview of the
project's tooling, helping to identify the purpose of each script and which
ones may be deprecated or superseded by more modern, configurable versions.

💡 INSIGHTS PROVIDED:
- The script's stated purpose from its docstring.
- The primary vault file it is configured to read from.
- Whether it uses the modern 'vault_utils.py' module for safe backups.
"""

import re
from pathlib import Path

# --- CONFIGURATION ---
# The directory to scan for scripts. '.' means the current directory.
SCRIPT_DIRECTORY = Path('..')


# ---------------------

def analyze_script(script_path: Path):
    """Reads a single script file and extracts key information."""
    try:
        content = script_path.read_text(encoding="utf-8")

        # Extract the purpose from the docstring
        purpose_match = re.search(r"🎯 PURPOSE:\n(.*?)\n\n", content, re.DOTALL)
        purpose = purpose_match.group(1).strip().replace('\n', ' ') if purpose_match else "No purpose defined."

        # Extract the vault file it reads from
        vault_file_match = re.search(r"VAULT_FILE\s*=\s*Path\(\"(.*?)\"\)", content)
        vault_file = vault_file_match.group(1) if vault_file_match else "Not specified."

        # Check if it uses our modern utility module
        uses_vault_utils = "from vault_utils import" in content

        return {
            "purpose": purpose,
            "vault_file": vault_file,
            "is_modern": uses_vault_utils
        }

    except Exception as e:
        return {"error": str(e)}


def main():
    """Main function to find and analyze all scripts."""
    print("🔍 Analyzing all Python scripts in the current directory...")

    # Find all .py files, excluding this script itself
    scripts_to_analyze = [p for p in SCRIPT_DIRECTORY.glob('*.py') if p.name != 'analyze_scripts.py']

    if not scripts_to_analyze:
        print("No scripts found to analyze.")
        return

    for script_path in sorted(scripts_to_analyze):
        print("\n" + "=" * 50)
        print(f"📄 SCRIPT: {script_path.name}")
        print("=" * 50)

        analysis = analyze_script(script_path)

        if "error" in analysis:
            print(f"  ❌ Could not analyze this script: {analysis['error']}")
        else:
            print(f"  - Purpose: {analysis['purpose']}")
            print(f"  - Operates On: {analysis['vault_file']}")
            print(f"  - Modern (uses vault_utils): {'✅ Yes' if analysis['is_modern'] else '❌ No'}")

    print("\n" + "=" * 50)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
