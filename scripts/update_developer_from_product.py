#!/usr/bin/env python3
"""
update_developer_from_product.py

🎯 PURPOSE:
Corrects the 'developer' field based on a keyword found at the end of the
'product' field. For example, if a product name is "Some Compressor Nebula",
this script can set the developer to "Nebula".

🛡️ SAFE:
- Includes a configurable 'UPDATE_MODE' ('replace' or 'append') to prevent
  accidental data destruction.
- Creates a timestamped backup of the original vault before saving changes.
- Only writes to the file if at least one entry was modified.

🔧 TWEAKABLE CONFIGURATION:
- All operational parameters can be changed in the '--- CONFIGURATION ---' block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/xvault_master.json")
BACKUP_DIR = Path("../backups")

# The field to check for the keyword (e.g., "product").
SOURCE_FIELD = "product"

# The script will find entries where the SOURCE_FIELD ends with this string.
# This is case-sensitive.
MATCH_SUFFIX = "Nebula"

# The field to be updated with the keyword (e.g., "developer").
TARGET_FIELD = "developer"

# How to update the target field.
# "replace": Overwrites the existing value in the target field completely.
# "append":  Adds the value to a list (useful for 'tags' or 'families').
UPDATE_MODE = "replace"


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
    print(f"🔎 Criteria: If '{SOURCE_FIELD}' ends with '{MATCH_SUFFIX}', then '{UPDATE_MODE}' '{TARGET_FIELD}'.")
    print("-" * 50)

    for entry in vault_data:
        source_value = entry.get(SOURCE_FIELD, "")

        # Ensure we are working with a string and it ends with our suffix
        if isinstance(source_value, str) and source_value.endswith(MATCH_SUFFIX):

            # The new value is the suffix itself.
            new_value = MATCH_SUFFIX
            entry_name = entry.get('name', 'N/A')

            # --- Apply the update based on the chosen mode ---
            if UPDATE_MODE == "replace":
                # Only update if the value is actually different
                if entry.get(TARGET_FIELD) != new_value:
                    entry[TARGET_FIELD] = new_value
                    modified_count += 1
                    print(f"  -> Replaced '{TARGET_FIELD}' in '{entry_name}' with '{new_value}'.")

            elif UPDATE_MODE == "append":
                target_list = entry.get(TARGET_FIELD)
                if target_list is None:
                    entry[TARGET_FIELD] = [new_value]
                    modified_count += 1
                    print(f"  -> Created '{TARGET_FIELD}' in '{entry_name}' and added '{new_value}'.")
                elif isinstance(target_list, list):
                    if new_value not in target_list:
                        target_list.append(new_value)
                        modified_count += 1
                        print(f"  -> Appended '{new_value}' to '{TARGET_FIELD}' in '{entry_name}'.")
                else:
                    print(
                        f"⚠️ Warning: Target field '{TARGET_FIELD}' in '{entry_name}' is not a list. Skipping append.")

            else:
                print(f"❌ Error: Invalid UPDATE_MODE '{UPDATE_MODE}' in config. Aborting.")
                return

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
