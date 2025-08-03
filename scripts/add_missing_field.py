#!/usr/bin/env python3
"""
add_missing_field.py

🎯 PURPOSE:
Ensures every entry in a vault JSON file has a specific field. If the field
is missing from an entry, it is added with a specified default value.

🛡️ SAFE:
- It will NOT overwrite the field if it already exists in an entry, even if
  the existing value is different from the default.
- Creates a timestamped backup of the original vault before saving changes.
- Only writes to the file if at least one entry was modified.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file, the field to add, and the default value
  in the '--- CONFIGURATION ---' block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The field to add to each entry if it is missing.
FIELD_TO_ADD = "product"

# The default value to assign to the new field.
# For a list field, use []. For a text field, use "" or None.
DEFAULT_VALUE = []


# ---------------------------------------------------------

def main():
    """Main function to run the script."""
    if not VAULT_FILE.exists():
        print(f"❌ Error: Vault file not found at '{VAULT_FILE}'")
        return

    try:
        vault_data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the vault file. It may be invalid JSON. Details: {e}")
        return

    modified_count = 0

    print(f"🔍 Scanning '{VAULT_FILE}' to ensure field '{FIELD_TO_ADD}' exists.")
    print("-" * 50)

    for entry in vault_data:
        # Check if the field does NOT exist in the entry
        if FIELD_TO_ADD not in entry:
            entry[FIELD_TO_ADD] = DEFAULT_VALUE
            modified_count += 1
            entry_name = entry.get('name', 'N/A')
            print(f"  -> Added missing '{FIELD_TO_ADD}' field to '{entry_name}'.")

    print("-" * 50)

    if modified_count > 0:
        print(f"\nAdded field to {modified_count} entries. Saving the vault...")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=vault_data,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo entries were missing the specified field. The vault file remains unchanged.")


if __name__ == "__main__":
    main()
