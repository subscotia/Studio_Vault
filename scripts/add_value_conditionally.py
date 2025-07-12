#!/usr/bin/env python3
"""
enrich_data_conditionally.py

🎯 PURPOSE:
A universal tool to enrich vault data. It adds a specified value to a target
field if an entry meets a configurable condition. This script can handle
conditions on both simple string fields and list-based fields.

🛡️ SAFE:
- The action (adding a value) is always list-safe, preventing duplicates
  and handling non-existent fields correctly.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- All parameters are in the configuration block.
- A new 'CONDITION_TYPE' setting lets you define the logic for finding matches.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/xvault_master_wking.json")
BACKUP_DIR = Path("../backups")

# --- The Condition ---
# The field to check for the condition.
CONDITION_FIELD = "product"

# How to check the condition. Options:
# "exact_match":     The field's value is exactly equal to CONDITION_VALUE.
# "contains_string": The string field contains CONDITION_VALUE as a substring.
# "in_list":         The list field contains CONDITION_VALUE as an item.
CONDITION_TYPE = "exact_match"

# The value to use for the condition check.
CONDITION_VALUE = "TNT Dynamics Nebula"

# --- The Action ---
# The field to add the new value to.
TARGET_FIELD = "emulates"
# The new value to add.
VALUE_TO_ADD = "Valley People Dyna-mite"


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
        f"🔎 Criteria: If '{CONDITION_FIELD}' has '{CONDITION_TYPE}' with '{CONDITION_VALUE}', then add '{VALUE_TO_ADD}' to '{TARGET_FIELD}'.")
    print("-" * 50)

    for entry in vault_data:
        condition_field_value = entry.get(CONDITION_FIELD)
        match_found = False

        # --- New Universal Condition Logic ---
        if CONDITION_TYPE == "exact_match":
            if condition_field_value == CONDITION_VALUE:
                match_found = True

        elif CONDITION_TYPE == "contains_string":
            if isinstance(condition_field_value, str) and CONDITION_VALUE in condition_field_value:
                match_found = True

        elif CONDITION_TYPE == "in_list":
            if isinstance(condition_field_value, list) and CONDITION_VALUE in condition_field_value:
                match_found = True

        else:
            print(f"❌ Error: Invalid CONDITION_TYPE '{CONDITION_TYPE}' in config. Aborting.")
            return

        # --- Action Logic (if condition was met) ---
        if match_found:
            target_list = entry.get(TARGET_FIELD)
            entry_name = entry.get('name', 'N/A')

            if target_list is None:
                entry[TARGET_FIELD] = [VALUE_TO_ADD]
                modified_count += 1
                print(f"  -> Created '{TARGET_FIELD}' in '{entry_name}' and added value.")

            elif isinstance(target_list, list):
                if VALUE_TO_ADD not in target_list:
                    target_list.append(VALUE_TO_ADD)
                    modified_count += 1
                    print(f"  -> Appended to '{TARGET_FIELD}' in '{entry_name}'.")

            else:
                print(f"⚠️ Warning: Target field '{TARGET_FIELD}' in '{entry_name}' is not a list. Skipping.")

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
