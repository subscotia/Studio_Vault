#!/usr/bin/env python3
"""
remove_value_from_list_field.py

🎯 PURPOSE:
Scans a vault and removes a specific value from a specified list-based
field (e.g., 'families', 'tags') in every entry where it is found.

🛡️ SAFE:
- It will only attempt to modify fields that are lists. It will not cause
  errors on fields that are strings, numbers, or null.
- If removing the value results in an empty list, the field will be saved
  as an empty list `[]`, maintaining data type consistency.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file, the target field, and the value to remove
  in the '--- CONFIGURATION ---' block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("xvault_wking_filling.json")
BACKUP_DIR = Path("backups")

# The list-based field to clean up.
FIELD_TO_CLEAN = "families"

# The specific string value you want to remove from that field.
VALUE_TO_REMOVE = "acqua"


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
    print(f"🔎 Criteria: Removing value '{VALUE_TO_REMOVE}' from field '{FIELD_TO_CLEAN}'.")
    print("-" * 50)

    for entry in vault_data:
        # Get the target field's value. We default to None if it doesn't exist.
        field_value = entry.get(FIELD_TO_CLEAN)

        # --- This is the crucial safety check ---
        # We only proceed if the field exists AND it is a list.
        # This prevents errors on fields that are null, strings, etc.
        if isinstance(field_value, list):

            # Check if the value we want to remove is actually in the list.
            if VALUE_TO_REMOVE in field_value:

                # Create a new list, keeping all items EXCEPT the one to remove.
                # This is a safe and efficient way to remove all occurrences.
                original_length = len(field_value)
                cleaned_list = [item for item in field_value if item != VALUE_TO_REMOVE]

                # Update the entry with the new, cleaned list.
                entry[FIELD_TO_CLEAN] = cleaned_list

                # Only count as modified if the list actually changed.
                if len(cleaned_list) < original_length:
                    modified_count += 1
                    entry_name = entry.get('name', 'N/A')
                    print(f"  -> Cleaned '{FIELD_TO_CLEAN}' in entry '{entry_name}'.")

    print("-" * 50)

    if modified_count > 0:
        print(f"\nCleaned {modified_count} entries. Saving the vault...")

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
