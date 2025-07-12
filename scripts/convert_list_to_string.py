#!/usr/bin/env python3
"""
convert_list_to_string.py

🎯 PURPOSE:
Converts a field that is mistakenly a list of strings into a single,
space-separated string. For example, it will change
`"product": ["Acustica", "Amber"]` to `"product": "Acustica Amber"`.

🛡️ SAFE:
- Only modifies fields that are lists. It will not affect fields that are
  already strings, null, or other data types.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file and the target field in the configuration block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The field to convert from a list to a string.
FIELD_TO_CONVERT = "product"


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

    print(f"🔍 Scanning '{VAULT_FILE}' to convert '{FIELD_TO_CONVERT}' fields from list to string.")
    print("-" * 50)

    for entry in vault_data:
        field_value = entry.get(FIELD_TO_CONVERT)

        # We only proceed if the field is a list
        if isinstance(field_value, list):
            # Join all items in the list into a single string, separated by spaces.
            # We convert each item to a string first to be safe.
            new_string_value = " ".join(str(item) for item in field_value)

            entry[FIELD_TO_CONVERT] = new_string_value
            modified_count += 1
            entry_name = entry.get('name', 'N/A')
            print(f"  -> Converted '{FIELD_TO_CONVERT}' for '{entry_name}' to '{new_string_value}'.")

    print("-" * 50)

    if modified_count > 0:
        print(f"\nConverted {modified_count} entries. Saving the vault...")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=vault_data,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo list-based fields were found to convert.")


if __name__ == "__main__":
    main()
