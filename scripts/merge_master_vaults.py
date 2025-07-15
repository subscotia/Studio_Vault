#!/usr/bin/env python3
"""
merge_master_vaults_with_logging.py

🎯 PURPOSE:
Performs the final merge of the instrument vault (ivault) and the effects
vault (xvault) into a single, master vault file. It handles duplicate
entries using a defined conflict resolution strategy and creates a detailed
log of all duplicates found and the actions taken.

🛡️ SAFE:
- Uses a combination of keys (e.g., 'name', 'filename') to uniquely identify
  each plugin and detect duplicates.
- Prioritizes the entry with a non-empty 'developer' key in case of a duplicate.
- Creates a timestamped backup of the final output file before saving.
- Generates a clear, human-readable log file in the /logs directory.

🔧 TWEAKABLE CONFIGURATION:
- The input files, output file, and conflict resolution logic can all be
  adjusted in the configuration block.
"""

import json
from pathlib import Path
from datetime import datetime
from vault_utils import save_vault_with_backup

# --- CONFIGURATION (Tweak these values as needed) ---
# The two source vault files to merge.
INSTRUMENT_VAULT = Path("../data/ivault_master.json")
EFFECTS_VAULT = Path("../data/xvault_master.json")

# The final, combined master vault file.
MASTER_VAULT_OUTPUT = Path("../data/vault_master.json")

# Directories for backups and logs.
BACKUP_DIR = Path("../backups")
LOG_DIR = Path("../logs")

# A list of key names that together define a unique plugin object.
UNIQUE_ID_KEYS = ["name", "filename"]

# When a duplicate is found, this key is checked. The entry with a non-empty
# value for this key will be prioritized.
CONFLICT_RESOLUTION_KEY = "developer"


# ---------------------------------------------------------

def get_entry_key(entry: dict, key_fields: list) -> tuple:
    """Creates a unique, hashable key from an entry's specified keys."""
    return tuple(entry.get(key) for key in key_fields)


def main():
    """Main function to run the script."""
    if not INSTRUMENT_VAULT.exists() or not EFFECTS_VAULT.exists():
        print(f"❌ Error: One or both input files not found.")
        return

    # Ensure log directory exists
    LOG_DIR.mkdir(exist_ok=True)
    log_file_path = LOG_DIR / f"merge_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    log_lines = []

    ivault_data = json.loads(INSTRUMENT_VAULT.read_text(encoding="utf-8"))
    xvault_data = json.loads(EFFECTS_VAULT.read_text(encoding="utf-8"))

    print(f"Merging vaults...")
    log_lines.append("--- Subscotia Vault Merge Log ---")
    log_lines.append(f"Merge started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_lines.append(f"Primary Vault (ivault): {len(ivault_data)} objects")
    log_lines.append(f"Secondary Vault (xvault): {len(xvault_data)} objects")
    log_lines.append("-" * 40)

    merged_objects = {}
    duplicates_found = 0

    # Combine both lists into one for processing
    all_entries = ivault_data + xvault_data

    for entry in all_entries:
        key = get_entry_key(entry, UNIQUE_ID_KEYS)

        if key not in merged_objects:
            merged_objects[key] = entry
        else:
            # A duplicate was found. Log it and resolve the conflict.
            duplicates_found += 1
            existing_entry = merged_objects[key]
            new_entry = entry

            log_lines.append(f"\nDUPLICATE #{duplicates_found}: Name='{key[0]}', Filename='{key[1]}'")
            log_lines.append("  - Existing Object:")
            log_lines.append(f"    - Developer: {existing_entry.get(CONFLICT_RESOLUTION_KEY, 'N/A')}")
            log_lines.append(f"    - Type: {existing_entry.get('type', 'N/A')}")
            log_lines.append("  - New Object:")
            log_lines.append(f"    - Developer: {new_entry.get(CONFLICT_RESOLUTION_KEY, 'N/A')}")
            log_lines.append(f"    - Type: {new_entry.get('type', 'N/A')}")

            existing_has_dev = bool(existing_entry.get(CONFLICT_RESOLUTION_KEY))
            new_has_dev = bool(new_entry.get(CONFLICT_RESOLUTION_KEY))

            # Conflict resolution logic
            if not existing_has_dev and new_has_dev:
                merged_objects[key] = new_entry
                log_lines.append("  - RESOLUTION: Kept New Object (had developer, existing did not).")
            else:
                # Default to keeping the existing object
                log_lines.append("  - RESOLUTION: Kept Existing Object (default action).")

    final_vault_data = list(merged_objects.values())

    print(f"Merge complete.")
    if duplicates_found > 0:
        print(f"  - {duplicates_found} duplicates found and resolved. See log for details.")
    print(f"  - Total unique objects in master vault: {len(final_vault_data)}")

    # Write the log file
    log_lines.append("\n" + "-" * 40)
    log_lines.append("Merge process finished.")
    log_file_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"📝 Merge log saved to: {log_file_path.resolve()}")

    # Save the final result
    backup_path = save_vault_with_backup(
        vault_path=MASTER_VAULT_OUTPUT,
        data_to_save=final_vault_data,
        backup_dir=BACKUP_DIR
    )

    print(f"\n✅ Master vault saved to: {MASTER_VAULT_OUTPUT.resolve()}")
    if backup_path:
        print(f"🔒 Backup of original output file saved to: {backup_path}")


if __name__ == "__main__":
    main()
