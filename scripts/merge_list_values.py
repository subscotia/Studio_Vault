#!/usr/bin/env python3
"""
merge_list_values.py

🎯 PURPOSE:
Scans a specified list-based key (e.g., 'families', 'tags') and replaces
multiple source values with a single, unified target value. This is ideal for
consolidating typos or variations (e.g., merging ["synth", "synthesizer"]
into "synths").

🛡️ SAFE:
- Only operates on the specified key if it is a list.
- The comparison is case-insensitive to catch more variations.
- Ensures the final list has no duplicate values.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file, the target key, the source values to find,
  and the target value to replace them with, all in the configuration block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The list-based key you want to clean up.
KEY_TO_MODIFY = "tags"  # Can be "families", "tags", etc.

# A list of the source values you want to find and replace.
# This check is case-insensitive.
SOURCE_VALUES = ["cdsm", "c d s m"]

# The single, unified value that will replace all of the source values.
TARGET_VALUE = "cdsm"


# ---------------------------------------------------------

def normalise_value(value: str) -> str:
    """Helper function to make string comparisons case-insensitive and clean."""
    return value.strip().lower()


def main():
    """Main function to run the script."""
    if not VAULT_FILE.exists():
        print(f"❌ Error: Vault file not found at '{VAULT_FILE}'")
        return

    try:
        data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the vault file. It may be invalid JSON. Details: {e}")
        return

    modified_count = 0
    # Normalize the source values once for efficiency
    normalised_sources = {normalise_value(val) for val in SOURCE_VALUES}

    print(f"🔍 Scanning '{VAULT_FILE}' to merge values in the '{KEY_TO_MODIFY}' key.")
    print(f"   Merging {SOURCE_VALUES} into '{TARGET_VALUE}'.")
    print("-" * 50)

    for entry in data:
        original_list = entry.get(KEY_TO_MODIFY)

        if not isinstance(original_list, list):
            continue

        new_list = []
        entry_was_modified = False

        # We build a new list to avoid issues with modifying a list while iterating
        for item in original_list:
            if isinstance(item, str):
                # If the item is one of our source values, add the target instead
                if normalise_value(item) in normalised_sources:
                    if TARGET_VALUE not in new_list:
                        new_list.append(TARGET_VALUE)
                    entry_was_modified = True
                # Otherwise, keep the original item
                else:
                    new_list.append(item)
            else:
                # Keep non-string items as they are
                new_list.append(item)

        if entry_was_modified:
            # Use dict.fromkeys to ensure the final list is free of any duplicates
            entry[KEY_TO_MODIFY] = list(dict.fromkeys(new_list))
            modified_count += 1

    if modified_count > 0:
        print(f"\n✅ Merged values in {modified_count} entries.")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=data,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo entries were found that required merging.")


if __name__ == "__main__":
    main()
