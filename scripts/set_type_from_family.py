#!/usr/bin/env python3
"""
set_type_from_family.py

🎯 PURPOSE:
Scans the vault and sets a single-value field (like 'type') based on the
presence of a specific value in a list-based field (like 'families').
For example, if 'families' contains 'utilities', it sets 'type' to 'utility'.

🛡️ SAFE:
- Only checks for the condition in fields that are lists.
- Only overwrites the target field if the value needs to be changed.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- The file paths, fields, and values are all configurable below.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/xvault_master_wking.json")
BACKUP_DIR = Path("../backups")

# --- The Condition ---
# If this field...
CONDITION_FIELD = "families"
# ...contains this value...
CONDITION_VALUE = "utilities"

# --- The Action ---
# ...then set this field...
TARGET_FIELD = "type"
# ...to this new value.
NEW_VALUE = "utility"


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
    print(f"🔎 Criteria: If '{CONDITION_FIELD}' contains '{CONDITION_VALUE}', set '{TARGET_FIELD}' to '{NEW_VALUE}'.")
    print("-" * 50)

    for entry in vault_data:
        # Get the list from the condition field
        condition_list = entry.get(CONDITION_FIELD)

        # We can only proceed if the field is a list and contains our target value
        if isinstance(condition_list, list) and CONDITION_VALUE in condition_list:

            # Check if the target field needs to be updated
            if entry.get(TARGET_FIELD) != NEW_VALUE:
                entry[TARGET_FIELD] = NEW_VALUE
                modified_count += 1
                entry_name = entry.get('name', 'N/A')
                print(f"  -> Set '{TARGET_FIELD}' for '{entry_name}' to '{NEW_VALUE}'.")

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
        print("\nNo entries matched the criteria or needed updating.")


if __name__ == "__main__":
    main()
