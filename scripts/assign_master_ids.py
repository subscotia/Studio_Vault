#!/usr/bin/env python3
"""
assign_master_ids.py

🎯 PURPOSE:
Performs the final, definitive ID assignment for the entire merged master
vault. It iterates through every object and assigns a new, unique ID based
on the established Subscotia Vault naming convention.

💡 CONVENTION:
[Type Code (1)][Dev Code (2)][Sequential Number (5)] -> e.g., XAC00125

🛡️ SAFE:
- This script will overwrite any existing values in the 'id' key. It should
  only be run after the vault is finalized and old IDs have been nulled.
- It includes error handling for missing 'type' or 'developer' keys.
- It can now handle cases where the 'developer' key mistakenly contains a
  list instead of a string.
- Creates a final timestamped backup before saving the ID'd vault.

🔧 TWEAKABLE CONFIGURATION:
- The starting number for the sequence can be adjusted.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
# The final, merged master vault file.
MASTER_VAULT_FILE = Path("../data/vault_master.json")
BACKUP_DIR = Path("../backups")

# The number to start the global sequential ID from.
STARTING_ID_NUMBER = 1

# Mapping of the 'type' value to its single-character ID code.
TYPE_CODES = {
    "instrument": "I",
    "fx": "X",
    "utility": "U",
    "container": "C",
    "expansion": "E"
}


# ---------------------------------------------------------

def main():
    """Main function to run the script."""
    if not MASTER_VAULT_FILE.exists():
        print(f"❌ Error: Master vault file not found at '{MASTER_VAULT_FILE.resolve()}'")
        return

    try:
        vault_data = json.loads(MASTER_VAULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the vault file. It may be invalid JSON. Details: {e}")
        return

    current_id_number = STARTING_ID_NUMBER
    assigned_count = 0
    skipped_count = 0

    print(f"🔍 Starting ID assignment for '{MASTER_VAULT_FILE.name}'...")
    print("-" * 50)

    for entry in vault_data:
        obj_type = entry.get("type")
        developer_value = entry.get("developer")
        developer_name = ""

        # --- Robust handling for developer key ---
        if isinstance(developer_value, str):
            developer_name = developer_value
        elif isinstance(developer_value, list) and developer_value:
            # If it's a list, use the first item and treat it as the name.
            developer_name = str(developer_value[0])
        # --- End of robust handling ---

        # We need both type and a valid developer name to create an ID.
        if not obj_type or not developer_name:
            skipped_count += 1
            name = entry.get('name', 'N/A')
            print(f"  ⚠️ Skipping '{name}': Missing 'type' or 'developer' key.")
            continue

        # Get the type code, defaulting to 'Z' if not found in our map.
        type_code = TYPE_CODES.get(obj_type, "Z").upper()

        # Get the developer code from the cleaned name.
        dev_code = developer_name[:2].upper().ljust(2, 'X')  # Pad with 'X' if dev name is 1 char

        # Format the sequential number with 5 digits, padded with zeros.
        id_number_str = f"{current_id_number:05d}"

        # Assemble the final ID.
        new_id = f"{type_code}{dev_code}{id_number_str}"

        entry["id"] = new_id
        assigned_count += 1
        current_id_number += 1

    print("-" * 50)
    print(f"Assignment complete.")
    print(f"  - {assigned_count} IDs were successfully assigned.")
    if skipped_count > 0:
        print(f"  - {skipped_count} objects were skipped due to missing data.")

    # Save the final ID'd vault.
    backup_path = save_vault_with_backup(
        vault_path=MASTER_VAULT_FILE,
        data_to_save=vault_data,
        backup_dir=BACKUP_DIR
    )

    print(f"\n✅ Master vault with new IDs saved successfully.")
    if backup_path:
        print(f"🔒 Backup of the pre-ID'd vault saved to: {backup_path}")


if __name__ == "__main__":
    main()
