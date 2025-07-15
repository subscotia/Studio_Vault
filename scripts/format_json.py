#!/usr/bin/env python3
"""
format_json.py

🎯 PURPOSE:
Reads a specified JSON file and writes it back to the same location with
standard "pretty-print" formatting (2-space indentation). This is a dedicated
utility for cleaning up JSON files that have inconsistent whitespace or
line breaks.

🛡️ SAFE:
- This script does not alter any data; it only reformats the file structure.
- It uses the standard `save_vault_with_backup` utility to ensure a
  timestamped backup is created before overwriting the file.

🔧 TWEAKABLE CONFIGURATION:
- You can specify which JSON file to format in the configuration block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
# The JSON file you want to format.
FILE_TO_FORMAT = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")


# ---------------------------------------------------------

def main():
    """Main function to run the script."""
    if not FILE_TO_FORMAT.exists():
        print(f"❌ Error: File not found at '{FILE_TO_FORMAT.resolve()}'")
        return

    print(f"🔍 Reading '{FILE_TO_FORMAT.name}' to reformat...")

    try:
        # Load the data from the potentially messy file
        data = json.loads(FILE_TO_FORMAT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the file. It may be invalid JSON. Details: {e}")
        return

    # The save function in vault_utils already handles pretty-printing
    # with indent=2. We just need to call it.
    print("💾 Saving file with clean formatting...")

    backup_path = save_vault_with_backup(
        vault_path=FILE_TO_FORMAT,
        data_to_save=data,
        backup_dir=BACKUP_DIR
    )

    print(f"✅ File formatted successfully.")
    if backup_path:
        print(f"🔒 Backup of original file saved to: {backup_path}")


if __name__ == "__main__":
    main()
