#!/usr/bin/env python3
"""
correct_phaser_family.py

🎯 PURPOSE:
Scans the vault and corrects entries where the 'families' list contains
'phase' (indicating a phaser effect) but not 'correction' (indicating a
phase utility). It renames 'phase' to 'phasers' and ensures the parent
category 'modulation' is also present.

🛡️ SAFE:
- Only operates on the 'families' field if it is a list.
- The conditional logic is strict, preventing accidental changes to phase
  correction utilities.
- Will not add 'modulation' if it already exists, preventing duplicates.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- All parameters are in the configuration block for easy editing.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/xvault_master.json")
BACKUP_DIR = Path("../backups")

# --- The Condition ---
# In this field...
FIELD_TO_CHECK = "families"
# ...find this value...
VALUE_TO_FIND = "phase"
# ...but ONLY if this value is NOT present.
EXCLUSION_VALUE = "correction"

# --- The Action ---
# Replace the found value with this...
REPLACEMENT_VALUE = "phasers"
# ...and also ensure this value is present.
VALUE_TO_ADD = "modulation"


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

    print(f"🔍 Scanning '{VAULT_FILE}' for 'phase' correction...")
    print(f"🔎 Criteria: If '{FIELD_TO_CHECK}' has '{VALUE_TO_FIND}' but not '{EXCLUSION_VALUE}'.")
    print("-" * 50)

    for entry in vault_data:
        families_list = entry.get(FIELD_TO_CHECK)

        # We can only proceed if the field is a list
        if not isinstance(families_list, list):
            continue

        # Check for the specific condition: 'phase' is present AND 'correction' is absent
        if VALUE_TO_FIND in families_list and EXCLUSION_VALUE not in families_list:

            # Build a new list to hold the corrected values
            new_list = []
            entry_was_changed = False

            # 1. Replace 'phase' with 'phasers'
            for item in families_list:
                if item == VALUE_TO_FIND:
                    new_list.append(REPLACEMENT_VALUE)
                    entry_was_changed = True
                else:
                    new_list.append(item)

            # 2. Add 'modulation' if it's not already there
            if VALUE_TO_ADD not in new_list:
                new_list.append(VALUE_TO_ADD)
                entry_was_changed = True

            # 3. If any changes were made, update the entry
            if entry_was_changed:
                # Using dict.fromkeys to handle any potential duplicate creation cleanly
                entry[FIELD_TO_CHECK] = list(dict.fromkeys(new_list))
                modified_count += 1
                entry_name = entry.get('name', 'N/A')
                print(f"  -> Corrected families for '{entry_name}'.")

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
        print("\nNo entries matched the criteria for correction.")


if __name__ == "__main__":
    main()
