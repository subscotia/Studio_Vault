#!/usr/bin/env python3
"""
split_list_item.py

🎯 PURPOSE:
Finds an item in a list-based field that contains a specific keyword,
and replaces that single item with multiple new items derived from splitting
the original. For example, it can find "solo cello" in the 'families' list
and replace it with ["solo", "cello"].

🛡️ SAFE:
- Only operates on the specified field if it is a list.
- After splitting, it ensures no duplicate values are added to the list.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- All parameters are in the configuration block for easy editing.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The list-based field to modify.
FIELD_TO_MODIFY = "tags"

# The script will find list items that contain this keyword.
# This is case-sensitive.
SEARCH_TERM = "violin"


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
    print(f"🔎 Criteria: Splitting items in '{FIELD_TO_MODIFY}' that contain '{SEARCH_TERM}'.")
    print("-" * 50)

    for entry in vault_data:
        target_list = entry.get(FIELD_TO_MODIFY)

        if not isinstance(target_list, list):
            continue

        # We build a new list rather than modifying the original while iterating
        new_list = []
        entry_was_modified = False

        for item in target_list:
            # Check if the item is a string and contains our search term
            if isinstance(item, str) and SEARCH_TERM in item:
                # Split the string into words and add them to our new list
                split_values = item.split()
                new_list.extend(split_values)
                entry_was_modified = True
            else:
                # If it doesn't match, just keep the original item
                new_list.append(item)

        if entry_was_modified:
            # To prevent duplicates (e.g., if 'solo' was already in the list),
            # we convert the list to a dictionary's keys and back to a list.
            deduplicated_list = list(dict.fromkeys(new_list))

            # Update the entry with the new, corrected list
            entry[FIELD_TO_MODIFY] = deduplicated_list
            modified_count += 1
            entry_name = entry.get('name', 'N/A')
            print(f"  -> Split items in '{FIELD_TO_MODIFY}' for '{entry_name}'.")

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
        print("\nNo entries contained list items matching the criteria.")


if __name__ == "__main__":
    main()
