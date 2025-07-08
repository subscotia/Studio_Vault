#!/usr/bin/env python3
"""
replace_value.py

🎯 PURPOSE:
Scans a vault and replaces all instances of a target value with a new value.
This script is universal: it works correctly on simple fields (like 'developer')
and on list-based fields (like 'families' or 'tags').

🛡️ SAFE:
- Intelligently detects if a field is a list or a simple value and applies
  the correct replacement logic.
- When replacing in a list, it preserves the other items.
- If the replacement value is set to None when working on a list, the target
  value will be removed from the list entirely.
- Creates a timestamped backup before saving changes.

🔧 TWEAKABLE CONFIGURATION:
- All parameters are in the configuration block for easy editing.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("xvault_wking_filling.json")
BACKUP_DIR = Path("backups")

# The field to inspect and modify.
FIELD_NAME = "families"

# The value to search for (the typo or old value).
TARGET_VALUE = "mic emulations"

# The value to replace it with.
# For lists, setting this to None will REMOVE the target value.
# For simple fields, it will set the field to null.
REPLACEMENT_VALUE = "mics"


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
    print(f"🔎 Replacing '{TARGET_VALUE}' with '{REPLACEMENT_VALUE}' in field '{FIELD_NAME}'.")
    print("-" * 50)

    for entry in vault_data:
        field_value = entry.get(FIELD_NAME)
        entry_modified = False

        # --- Logic for List Fields (e.g., 'families', 'tags') ---
        if isinstance(field_value, list):
            if TARGET_VALUE in field_value:
                # Build a new list, replacing the target value as we go.
                new_list = []
                for item in field_value:
                    if item == TARGET_VALUE:
                        # If replacement is None, we skip adding it, effectively removing it.
                        if REPLACEMENT_VALUE is not None:
                            new_list.append(REPLACEMENT_VALUE)
                    else:
                        new_list.append(item)

                # To prevent duplicates if the replacement already exists
                # we can convert to a dict and back.
                entry[FIELD_NAME] = list(dict.fromkeys(new_list))
                entry_modified = True

        # --- Logic for Simple Fields (e.g., 'developer', 'emulates') ---
        else:
            if field_value == TARGET_VALUE:
                entry[FIELD_NAME] = REPLACEMENT_VALUE
                entry_modified = True

        if entry_modified:
            modified_count += 1
            entry_name = entry.get('name', 'N/A')
            print(f"  -> Modified '{FIELD_NAME}' in entry '{entry_name}'.")

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
        print("\nNo entries were found containing that value. The vault file remains unchanged.")


if __name__ == "__main__":
    main()
