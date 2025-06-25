#Here’s a Python utility that:
#Loads your existing JSON Vault
#Appends new plugin entries from a separate input JSON
#Validates basic fields to avoid junk data
#Saves a timestamped backup of the original file
#Writes the updated Vault back with proper indentation



import json
import os
from datetime import datetime

VAULT_PATH = "vault_instr_wip.json"
NEW_ENTRIES_PATH = "Generic_instruments_merged.json"

REQUIRED_FIELDS = ["name", "type", "host", "developer", "libraryPath", "tags"]

def is_valid_plugin(entry):
    return all(field in entry for field in REQUIRED_FIELDS)

def backup_vault(path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}.backup_{ts}"
    os.rename(path, backup_path)
    print(f"🛡️  Vault backed up to: {backup_path}")

def validate_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {path}: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return False

def append_entries(vault_path, entries_path):
    with open(vault_path, "r", encoding="utf-8") as f:
        vault = json.load(f)

    with open(entries_path, "r", encoding="utf-8") as f:
        new_entries = json.load(f)

    added = 0
    for entry in new_entries:
        if is_valid_plugin(entry):
            vault.append(entry)
            added += 1
        else:
            print(f"⚠️  Skipped invalid entry: {entry.get('name', '[Unnamed]')}")

    backup_vault(vault_path)

    with open(vault_path, "w", encoding="utf-8") as f:
        json.dump(vault, f, indent=2)

    print(f"✅ Added {added} plugins to the Vault.")

if __name__ == "__main__":
    if not validate_json_file(VAULT_PATH) or not validate_json_file(NEW_ENTRIES_PATH):
        print("🚫 Import halted due to invalid input file(s).")
    else:
        append_entries(VAULT_PATH, NEW_ENTRIES_PATH)