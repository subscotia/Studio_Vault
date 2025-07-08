#!/usr/bin/env python3
"""
populate_field_by_criteria.py (v2)

🎯 PURPOSE:
Finds entries based on a condition in a source field and updates a target
field within the same entry. This version includes multiple update modes.

🛡️ SAFE:
- 'append' mode will only add values to lists and will not overwrite other data types.
- 'replace' mode is powerful but use with care as it overwrites existing data.
- Creates a timestamped backup of the original vault before saving changes.
- Only writes to the file if at least one entry was modified.

🔧 TWEAKABLE CONFIGURATION:
- All operational parameters can be changed in the '--- CONFIGURATION ---' block.
- A new 'UPDATE_MODE' setting controls how the target field is modified.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("waves.json")
BACKUP_DIR = Path("backups")

# --- Condition to find entries ---
# The JSON key to inspect in each entry.
SOURCE_FIELD = "developer"
# The matching method. Options: "endswith", "startswith", "contains", "exact"
MATCH_CRITERION = "exact"
# The string value to use for the match. This is case-sensitive.
VALUE_TO_MATCH = "Waves Audio"

# --- Action to perform on matched entries ---
# The field to be updated.
TARGET_FIELD = "filename"
# The value to add/set in the target field.
VALUE_TO_ADD = "WaveShell1-VST3 14.vst3"

# How to update the target field. Options: "append", "replace"
# "append":  Adds the value to a list. Creates the list if it doesn't exist.
#            Will NOT modify fields that exist but are not lists (e.g., strings).
# "replace": Overwrites the existing value in the target field completely.
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
    print(
        f"🔎 Criteria: If field '{SOURCE_FIELD}' {MATCH_CRITERION} '{VALUE_TO_MATCH}', then '{UPDATE_MODE}' field '{TARGET_FIELD}' with '{VALUE_TO_ADD}'.")
    print("-" * 50)

    for entry in vault_data:
        source_value = entry.get(SOURCE_FIELD, "")

        if not isinstance(source_value, str):
            continue

        match_found = False
        if MATCH_CRITERION == "endswith" and source_value.endswith(VALUE_TO_MATCH):
            match_found = True
        elif MATCH_CRITERION == "startswith" and source_value.startswith(VALUE_TO_MATCH):
            match_found = True
        elif MATCH_CRITERION == "contains" and VALUE_TO_MATCH in source_value:
            match_found = True
        elif MATCH_CRITERION == "exact" and source_value == VALUE_TO_MATCH:
            match_found = True

        if match_found:
            # --- New logic for handling update modes ---
            entry_name = entry.get('name', 'N/A')

            if UPDATE_MODE == "replace":
                if entry.get(TARGET_FIELD) != VALUE_TO_ADD:
                    entry[TARGET_FIELD] = VALUE_TO_ADD
                    modified_count += 1
                    print(f"  -> Replaced '{TARGET_FIELD}' in '{entry_name}'.")

            elif UPDATE_MODE == "append":
                target_value = entry.get(TARGET_FIELD)

                if target_value is None:
                    entry[TARGET_FIELD] = [VALUE_TO_ADD]
                    modified_count += 1
                    print(f"  -> Created '{TARGET_FIELD}' in '{entry_name}' and added value.")

                elif isinstance(target_value, list):
                    if VALUE_TO_ADD not in target_value:
                        target_value.append(VALUE_TO_ADD)
                        modified_count += 1
                        print(f"  -> Appended to '{TARGET_FIELD}' in '{entry_name}'.")

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
        print("\nNo entries were modified. The vault file remains unchanged.")


if __name__ == "__main__":
    main()
