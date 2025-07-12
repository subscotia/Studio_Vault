#!/usr/bin/env python3
"""
populate_product_field.py

🎯 PURPOSE:
Populates an empty 'product' field by combining the 'developer' and 'name'
fields. For example, if developer is "Spectrasonics" and name is "Omnisphere",
it will set the product to "Spectrasonics Omnisphere".

🛡️ SAFE:
- It will ONLY populate the 'product' field if it is currently empty or null.
  It will NOT overwrite existing product names.
- It requires both the 'developer' and 'name' fields to have values before
  it will create the product name.
- Creates a timestamped backup before saving any changes.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file and the fields used in the configuration block.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")

# The field to populate.
TARGET_FIELD = "product"

# A list of fields to combine, in order, to create the new value.
SOURCE_FIELDS = ["developer", "name"]


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

    print(f"🔍 Scanning '{VAULT_FILE}' to populate empty '{TARGET_FIELD}' fields.")
    print("-" * 50)

    for entry in vault_data:
        # We only proceed if the target field is empty or does not exist.
        # The 'not entry.get(TARGET_FIELD)' check handles null, None, and empty strings "".
        if not entry.get(TARGET_FIELD):

            source_values = [entry.get(field) for field in SOURCE_FIELDS]

            # Ensure all source fields have valid, non-empty string values.
            if all(isinstance(val, str) and val for val in source_values):
                # Combine the source values with a space in between.
                new_product_name = " ".join(source_values)
                entry[TARGET_FIELD] = new_product_name
                modified_count += 1
                print(f"  -> Set product for '{entry.get('name')}' to '{new_product_name}'.")

    print("-" * 50)

    if modified_count > 0:
        print(f"\nPopulated {modified_count} entries. Saving the vault...")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=vault_data,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo entries needed their product field populated.")


if __name__ == "__main__":
    main()
