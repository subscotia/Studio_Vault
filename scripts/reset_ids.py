#!/usr/bin/env python3
"""
reset_ids.py

🎯 PURPOSE:
Iterates through a vault JSON file and resets the 'id' key for every
entry to null. This is a preparatory step before re-assigning a new,
globally unique set of IDs to a merged vault.
"""

import json
from pathlib import Path
# Note: We assume vault_utils is in the same directory, so this import works.
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
# The paths are now relative to the /scripts directory.
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The key to reset to null.
KEY_TO_RESET = "id"


# ---------------------------------------------------------

def main():
    """Main function to run the script."""
    if not VAULT_FILE.exists():
        print(f"❌ Error: Vault file not found at '{VAULT_FILE.resolve()}'")
        return

    try:
        vault_data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the vault file. It may be invalid JSON. Details: {e}")
        return

    modified_count = 0

    print(f"🔍 Scanning '{VAULT_FILE.name}' to reset the '{KEY_TO_RESET}' key.")
    print("-" * 50)

    for entry in vault_data:
        if KEY_TO_RESET in entry and entry[KEY_TO_RESET] is not None:
            entry[KEY_TO_RESET] = None
            modified_count += 1

    print(f"Found {modified_count} entries with existing IDs to reset.")

    if modified_count > 0:
        print(f"\nResetting IDs and saving the vault...")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=vault_data,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo entries needed their IDs reset. The vault file remains unchanged.")


if __name__ == "__main__":
    main()
