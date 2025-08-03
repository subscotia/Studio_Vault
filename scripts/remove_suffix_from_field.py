#!/usr/bin/env python3
"""
remove_suffix_from_field.py

🎯 PURPOSE:
Scans a vault and cleans up a specified string field by removing a specific
word if it appears at the very end of the string. For example, it can change
"Spitfire Audio Albion One Library" to "Spitfire Audio Albion One".

🛡️ SAFE:
- Only modifies the field if it is a string and ends with the exact word.
- The comparison is case-sensitive.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file, the target field, and the suffix to remove
  in the '--- CONFIGURATION ---' block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The single-string field to clean up.
FIELD_TO_CLEAN = "product"

# The specific word to remove if it appears at the end of the string.
# This is case-sensitive.
SUFFIX_TO_REMOVE = "Library"


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

    print(f"🔍 Scanning '{VAULT_FILE}' to remove suffix '{SUFFIX_TO_REMOVE}' from field '{FIELD_TO_CLEAN}'.")
    print("-" * 50)

    for entry in vault_data:
        field_value = entry.get(FIELD_TO_CLEAN)

        # We only proceed if the field is a non-empty string
        if isinstance(field_value, str) and field_value:

            # Check if the string ends with our target word.
            # We add a space before it to ensure we match a whole word.
            if field_value.endswith(f" {SUFFIX_TO_REMOVE}"):
                # Use rsplit to remove only the last occurrence of the suffix.
                # This is safer than a simple replace.
                new_value = field_value.rsplit(f" {SUFFIX_TO_REMOVE}", 1)[0]

                entry[FIELD_TO_CLEAN] = new_value
                modified_count += 1
                entry_name = entry.get('name', 'N/A')
                print(f"  -> Cleaned '{FIELD_TO_CLEAN}' for '{entry_name}'. New value: '{new_value}'")

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
        print("\nNo entries were found that required cleaning.")


if __name__ == "__main__":
    main()
