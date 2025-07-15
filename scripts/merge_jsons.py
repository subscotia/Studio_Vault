#!/usr/bin/env python3
"""
merge_vaults.py

🎯 PURPOSE:
Merges two vault JSON files into a single output file. It includes logic to
handle duplicate entries based on a specified conflict resolution rule.

🛡️ SAFE:
- Uses a configurable set of fields (e.g., 'name', 'filename') to identify
  unique entries.
- When a duplicate is found, it keeps the entry from the secondary file only
  if the primary entry is missing a value in a specified 'conflict field'
  (e.g., 'developer').
- Creates a timestamped backup of the output file before overwriting it.

🔧 TWEAKABLE CONFIGURATION:
- All file paths and logical parameters can be changed in the
  '--- CONFIGURATION ---' block below.
"""

import json
from pathlib import Path
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
# The primary vault file. Entries from this file are the default.
PRIMARY_VAULT_FILE = Path("../data/xvault_master.json")

# The secondary vault file to merge into the primary one.
SECONDARY_VAULT_FILE = Path("waves.json")

# The final, merged output file.
OUTPUT_VAULT_FILE = Path("../data/xvault_master.json")

# Directory for backups.
BACKUP_DIR = Path("../backups")

# A list of field names that together define a unique plugin entry.
UNIQUE_ID_FIELDS = ["name", "filename"]

# When a duplicate is found, this field is checked. If the entry from the
# PRIMARY file has an empty value in this field, and the SECONDARY entry
# has a value, the secondary entry will be kept.
CONFLICT_RESOLUTION_FIELD = "developer"


# ---------------------------------------------------------


def get_entry_key(entry: dict, key_fields: list) -> tuple:
    """
    Given a dictionary and a list of key fields, this function retrieves the corresponding values
    from the dictionary for the specified keys and returns them as a tuple. It enables the creation
    of a composite key by looking up values based on the supplied key fields.

    :param entry: A dictionary from which values will be retrieved.
    :param key_fields: A list specifying the keys whose associated values are to be extracted
        from the ``entry`` dictionary.
    :return: A tuple containing the values mapped to the specified ``key_fields`` from the ``entry``.

    """
    return tuple(entry.get(key) for key in key_fields)


def main():
    """
    Main function responsible for merging two JSON-based vault files into a single
    output file. The function reads data from primary and secondary input files,
    resolves conflicts based on a predefined conflict resolution field, and saves
    the merged data to an output file with a backup of the pre-existing output
    file, if any.

    This function ensures a robust merging process by handling cases such as:
    - Nonexistent input files
    - Conflicting entries resolved in favor of the secondary file when the primary
      file's conflict resolution field is empty
    - Backup of the output file before overwriting

    :raises FileNotFoundError: Raised if one or both input files do not exist.
    :raises json.JSONDecodeError: Raised if input files contain invalid JSON.

    :return: None
    """
    if not PRIMARY_VAULT_FILE.exists() or not SECONDARY_VAULT_FILE.exists():
        print(f"❌ Error: One or both input files not found.")
        print(
            f"  - Primary: {PRIMARY_VAULT_FILE.resolve()} {'(found)' if PRIMARY_VAULT_FILE.exists() else '(not found)'}")
        print(
            f"  - Secondary: {SECONDARY_VAULT_FILE.resolve()} {'(found)' if SECONDARY_VAULT_FILE.exists() else '(not found)'}")
        return

    primary_data = json.loads(PRIMARY_VAULT_FILE.read_text(encoding="utf-8"))
    secondary_data = json.loads(SECONDARY_VAULT_FILE.read_text(encoding="utf-8"))

    print(f"Merging vaults...")
    print(f"  - Primary file: '{PRIMARY_VAULT_FILE}' ({len(primary_data)} entries)")
    print(f"  - Secondary file: '{SECONDARY_VAULT_FILE}' ({len(secondary_data)} entries)")
    print(f"  - Conflict resolution field: '{CONFLICT_RESOLUTION_FIELD}'")
    print("-" * 50)

    merged_entries = {}
    conflicts_resolved = 0

    # First, load all entries from the primary file. These are the defaults.
    for entry in primary_data:
        key = get_entry_key(entry, UNIQUE_ID_FIELDS)
        merged_entries[key] = entry

    # Second, merge in the secondary file with the conflict resolution logic.
    for entry in secondary_data:
        key = get_entry_key(entry, UNIQUE_ID_FIELDS)

        # If it's a new entry, just add it.
        if key not in merged_entries:
            merged_entries[key] = entry
        else:
            # It's a duplicate. Apply conflict resolution logic.
            primary_entry = merged_entries[key]
            secondary_entry = entry

            primary_conflict_value = primary_entry.get(CONFLICT_RESOLUTION_FIELD)
            secondary_conflict_value = secondary_entry.get(CONFLICT_RESOLUTION_FIELD)

            # If the primary's conflict field is empty but the secondary's is not,
            # then the secondary entry is "better" and should be kept.
            if not primary_conflict_value and secondary_conflict_value:
                merged_entries[key] = secondary_entry
                conflicts_resolved += 1

    # Convert the dictionary of entries back into a list for saving.
    final_vault_data = list(merged_entries.values())

    print(f"Merge complete.")
    print(f"  - {conflicts_resolved} conflicts resolved in favor of the secondary file.")
    print(f"  - Total unique entries in merged vault: {len(final_vault_data)}")

    # Save the final result using our safe utility function.
    backup_path = save_vault_with_backup(
        vault_path=OUTPUT_VAULT_FILE,
        data_to_save=final_vault_data,
        backup_dir=BACKUP_DIR
    )

    print(f"\n✅ Merged vault saved to: {OUTPUT_VAULT_FILE}")
    if backup_path:
        print(f"🔒 Backup of original output file saved to: {backup_path}")


if __name__ == "__main__":
    main()
