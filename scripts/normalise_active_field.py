#!/usr/bin/env python3
"""
normalize_active_field.py

🛠️ PURPOSE:
Cleans up inconsistent "ACTIVE" fields across the vault:
- Converts string values like "TRUE", "FALSE", "true", "false"
  to proper Boolean values: true / false
- Ignores entries where "ACTIVE" is already a Boolean
- Leaves entries untouched if "ACTIVE" is missing (unless you want to default those too)

📁 INPUT:
- xvault_master.json

📁 OUTPUT:
- Overwrites the original vault file
- Creates a backup in: backups/xvault_wking_filling.active_normalized.json
"""

import json
from pathlib import Path

VAULT_FILE   = Path("../data/xvault_master.json")
BACKUP_DIR   = Path("../backups")
BACKUP_FILE  = BACKUP_DIR / "xvault_wking_filling.active_normalized.json"

def normalize_active(value):
    """Convert stringified booleans to actual booleans"""
    if isinstance(value, str):
        val_lower = value.strip().lower()
        if val_lower == "true":
            return True
        elif val_lower == "false":
            return False
    return value  # leave unchanged if already boolean or unknown type

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    updated = 0

    for entry in data:
        if "ACTIVE" in entry:
            original = entry["ACTIVE"]
            normalized = normalize_active(original)
            if normalized != original:
                entry["ACTIVE"] = normalized
                updated += 1

    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    VAULT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Normalized 'ACTIVE' field in {updated} entries.")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

if __name__ == "__main__":
    main()