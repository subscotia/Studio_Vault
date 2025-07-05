#!/usr/bin/env python3
"""
replace_field_value.py

📝 PURPOSE:
Scans a JSON list (e.g. xvault_wking_filling.json) and replaces all instances
of a specific value in a given field with another value—or nulls them out.

🏗️ EXAMPLE USE CASE:
You've accidentally assigned "Techivation" as developer to 1181 entries,
but only meant to assign it to 4. This script will help clean that up in bulk.

🔁 WHAT IT DOES:
- Loads the vault JSON file
- For each entry, checks if entry[FIELD_NAME] == TARGET_VALUE
- If it matches, replaces it with REPLACEMENT (or sets to null)
- Saves the updated vault back in-place
"""

import json
from pathlib import Path

# ── CONFIG ─────────────────────────────────────────────────────
VAULT_FILE    = Path("xvault_wking_filling.json")
FIELD_NAME    = "developer"         # field to inspect
TARGET_VALUE  = "Techivation"       # value to search for
REPLACEMENT   = None                # use a string, or None to null it out
# ────────────────────────────────────────────────────────────────

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    updated = 0

    for entry in data:
        if entry.get(FIELD_NAME) == TARGET_VALUE:
            entry[FIELD_NAME] = REPLACEMENT
            updated += 1

    # Save backup before overwriting
    backup = VAULT_FILE.with_suffix(".before_replace.json")
    backup.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write the cleaned version back
    VAULT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Replaced {updated} occurrence(s) of '{TARGET_VALUE}' in field '{FIELD_NAME}'.")
    print(f"💾 Backup saved to: {backup}")

if __name__ == "__main__":
    main()