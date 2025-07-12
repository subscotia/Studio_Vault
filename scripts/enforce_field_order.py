#!/usr/bin/env python3
"""
enforce_field_order.py

🎯 PURPOSE:
Rewrites a vault JSON file to ensure that the keys (fields) within each
entry are in a specific, consistent order. This improves readability and
makes manual comparison of entries easier.

🛡️ SAFE:
- Does not alter any data values; it only changes the order of the keys.
- If an entry has keys that are not in the specified order list, they will be
  preserved and moved to the end of the entry. No data is lost.
- Creates a timestamped backup of the original vault before saving changes.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file and the desired field order in the
  '--- CONFIGURATION ---' block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The desired order of fields for each entry.
# The script will also preserve any fields not in this list.
FIELD_ORDER = [
    "product",  # Added product to the list as it was missing
    "name",
    "type",
    "host",
    "developer",
    "families",
    "tags",
    "emulates",
    "id",
    "ACTIVE"
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

    reordered_vault = []

    print(f"🔍 Scanning '{VAULT_FILE}' to reorder fields...")
    print("-" * 50)

    for original_entry in vault_data:
        reordered_entry = {}

        # Add fields in the desired order
        for field in FIELD_ORDER:
            if field in original_entry:
                reordered_entry[field] = original_entry[field]

        # Add any remaining fields that were not in our order list
        for field, value in original_entry.items():
            if field not in reordered_entry:
                reordered_entry[field] = value

        reordered_vault.append(reordered_entry)

    print(f"✅ All {len(reordered_vault)} entries processed for reordering.")

    # Save the reordered data back to the file
    backup_path = save_vault_with_backup(
        vault_path=VAULT_FILE,
        data_to_save=reordered_vault,
        backup_dir=BACKUP_DIR
    )

    print(f"✅ Vault reordered and saved successfully.")
    if backup_path:
        print(f"🔒 Backup of original vault saved to: {backup_path}")


if __name__ == "__main__":
    main()
