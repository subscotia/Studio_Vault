#!/usr/bin/env python3
"""
add_parent_category.py

🎯 PURPOSE:
Scans the vault and adds a parent category to a list-based field if a
child category is present. For example, if 'families' contains 'connectivity',
it adds 'utility' to ensure proper classification.

🛡️ SAFE:
- Only operates on fields that are lists.
- Will not add the new value if it already exists, preventing duplicates.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- The file paths, fields, and values are all configurable below.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/xvault_master.json")
BACKUP_DIR = Path("../backups")

# --- The Condition ---
# If this field...
CONDITION_FIELD = "families"
# ...contains this value...
CONDITION_VALUE = "atmos"

# --- The Action ---
# ...then add a new value to this field.
TARGET_FIELD = "families"
# This is the new value to add.
VALUE_TO_ADD = "utilities"


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

    print(f"🔍 Scanning '{VAULT_FILE}'...")
    print(f"🔎 Criteria: If '{CONDITION_FIELD}' contains '{CONDITION_VALUE}', add '{VALUE_TO_ADD}' to '{TARGET_FIELD}'.")
    print("-" * 50)

    for entry in vault_data:
        # Get the list from the condition field
        condition_list = entry.get(CONDITION_FIELD)

        # We can only proceed if the field is a list and contains our target value
        if isinstance(condition_list, list) and CONDITION_VALUE in condition_list:

            # Since the target field is the same, we can work on the same list
            # Check if the value to add is already present
            if VALUE_TO_ADD not in condition_list:
                condition_list.append(VALUE_TO_ADD)
                modified_count += 1
                entry_name = entry.get('name', 'N/A')
                print(f"  -> Added '{VALUE_TO_ADD}' to '{entry_name}'.")

    print("-" * 50)

    if modified_count > 0:
        print(f"\nUpdated {modified_count} entries. Saving the vault...")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=vault_data,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo entries matched the criteria. The vault file remains unchanged.")


if __name__ == "__main__":
    main()
