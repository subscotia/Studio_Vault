#!/usr/bin/env python3
"""
fill_empty_developer.py

🎯 PURPOSE:
Interactively prompts the user to fill in empty 'developer' fields in a
vault JSON file. It shows the user the product and name for context.

🛡️ SAFE:
- Processes one entry at a time, waiting for user input.
- If the user just presses Enter (provides no input), the field is skipped.
- Creates a single timestamped backup of the original vault before saving
  all changes at the end of the session.
- Only writes to the file if at least one entry was updated.

🔧 TWEAKABLE CONFIGURATION:
- You can easily change the vault file and the target field in the
  '--- CONFIGURATION ---' block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/xvault_master_wking.json")
BACKUP_DIR = Path("../backups")

# The field you want to interactively fill.
FIELD_TO_FILL = "developer"


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

    print(f"🔍 Scanning '{VAULT_FILE}' for entries with an empty '{FIELD_TO_FILL}' field.")
    print("Press Enter without typing to skip an entry.")
    print("-" * 50)

    # We iterate over a copy of the list to ensure we can modify it safely
    for entry in vault_data:
        # The condition 'if not entry.get(FIELD_TO_FILL):' checks for null, None, or empty strings ""
        if not entry.get(FIELD_TO_FILL):

            # Provide context to the user
            product = entry.get('product', 'N/A')
            name = entry.get('name', 'N/A')

            print(f"\nFound empty developer for:")
            print(f"  - Product: {product}")
            print(f"  - Name:    {name}")

            # Prompt for user input
            user_input = input(f"Enter developer name: ").strip()

            # If the user provided a value, update the entry
            if user_input:
                entry[FIELD_TO_FILL] = user_input
                modified_count += 1
                print(f"  -> Set developer to '{user_input}'")
            else:
                print("  -> Skipped.")

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
        print("\nNo entries were modified.")


if __name__ == "__main__":
    main()
