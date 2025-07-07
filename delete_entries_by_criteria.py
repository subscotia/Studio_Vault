#!/usr/bin/env python3
"""
delete_entries_by_criteria.py

🎯 PURPOSE:
Finds and interactively deletes entries from a vault JSON file based on
user-defined criteria.

🛡️ SAFE:
- Processes all entries first and finds matches.
- Asks for confirmation (y/n) before flagging an entry for deletion.
- Creates a timestamped backup of the original vault before saving changes.
- Only writes to the file if at least one entry was deleted.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file, the field to check, the matching method,
  and the value to match against in the '--- CONFIGURATION ---' block below.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("xvault_wking_filling.json")
BACKUP_DIR = Path("backups")

# The JSON key to inspect in each entry.
FIELD_TO_CHECK = "name"

# The matching method. Options: "endswith", "startswith", "contains", "exact"
MATCH_CRITERION = "startswith"

# The string value to use for the match. This is case-sensitive.
VALUE_TO_MATCH = "Amber3"


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

    entries_to_keep = []
    deleted_count = 0

    print(f"🔍 Scanning '{VAULT_FILE}'...")
    print(f"🔎 Criteria: Field '{FIELD_TO_CHECK}' {MATCH_CRITERION} '{VALUE_TO_MATCH}'")
    print("-" * 50)

    # Loop through a copy of the list to safely modify
    for entry in vault_data:
        # Get the value from the specified field, default to an empty string if not found
        value_to_check = entry.get(FIELD_TO_CHECK, "")

        # Ensure we are working with a string before calling string methods
        if not isinstance(value_to_check, str):
            entries_to_keep.append(entry)
            continue

        # Check if the entry matches the criteria
        match_found = False
        if MATCH_CRITERION == "endswith" and value_to_check.endswith(VALUE_TO_MATCH):
            match_found = True
        elif MATCH_CRITERION == "startswith" and value_to_check.startswith(VALUE_TO_MATCH):
            match_found = True
        elif MATCH_CRITERION == "contains" and VALUE_TO_MATCH in value_to_check:
            match_found = True
        elif MATCH_CRITERION == "exact" and value_to_check == VALUE_TO_MATCH:
            match_found = True

        if match_found:
            print("\n🚨 Match Found:")
            # Pretty-print the matched entry for readability
            print(json.dumps(entry, indent=2))

            # Ask for user confirmation
            user_input = input("Delete this entry? (y/n): ").strip().lower()

            if user_input == 'y':
                deleted_count += 1
                print("✅ Marked for deletion.")
            else:
                entries_to_keep.append(entry)
                print("❌ Kept.")
        else:
            # If it doesn't match, keep it
            entries_to_keep.append(entry)

    print("-" * 50)

    # Only save if changes were actually made
    if deleted_count > 0:
        print(f"\n🔥 Deleting {deleted_count} entries and saving the vault...")

        backup_path = save_vault_with_backup(
            vault_path=VAULT_FILE,
            data_to_save=entries_to_keep,
            backup_dir=BACKUP_DIR
        )

        print(f"✅ Vault updated successfully.")
        if backup_path:
            print(f"🔒 Backup of original vault saved to: {backup_path}")
    else:
        print("\nNo entries were deleted. The vault file remains unchanged.")


if __name__ == "__main__":
    main()
