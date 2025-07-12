#!/usr/bin/env python3
"""
move_tags_to_families.py

🎯 PURPOSE:
Moves specified values from the 'tags' list to the 'families' list within
each entry of a vault. This is useful for re-categorizing data as the
taxonomy evolves.

🛡️ SAFE:
- Only operates on entries where 'tags' and 'families' are lists.
- When moving a value, it is added to 'families' only if not already present,
  preventing duplicates.
- The value is cleanly removed from the 'tags' list.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- You can specify which values to move in the 'VALUES_TO_MOVE' list.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# A list of the exact string values you want to move from 'tags' to 'families'.
# This is case-sensitive. Add or remove items as needed.
VALUES_TO_MOVE = [

    "electric keys",







]


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

    print(f"🔍 Scanning '{VAULT_FILE}' to move values from 'tags' to 'families'.")
    print(f"   Values to move: {VALUES_TO_MOVE}")
    print("-" * 50)

    for entry in vault_data:
        tags_list = entry.get("tags")
        families_list = entry.get("families")

        # We can only proceed if both fields are lists
        if not isinstance(tags_list, list) or not isinstance(families_list, list):
            continue

        values_that_were_moved = []

        # Find which of our target values are in the current entry's tag list
        for value in VALUES_TO_MOVE:
            if value in tags_list:
                values_that_were_moved.append(value)

                # Add to families if not already there
                if value not in families_list:
                    families_list.append(value)

        # If we found any values to move in this entry, clean up the tags list
        if values_that_were_moved:
            # Create a new tags list, excluding the ones we moved
            entry["tags"] = [tag for tag in tags_list if tag not in values_that_were_moved]
            modified_count += 1
            entry_name = entry.get('name', 'N/A')
            print(f"  -> Moved {values_that_were_moved} for '{entry_name}'.")

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
        print("\nNo entries contained the specified tags to move.")


if __name__ == "__main__":
    main()
