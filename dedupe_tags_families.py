#!/usr/bin/env python3
"""
deduplicate_tags_families.py

🎯 PURPOSE:
Removes exact duplicate values from "tags" and "families" fields
in the vault JSON. Leaves other fields untouched.

🛡️ SAFE:
- Only modifies "tags" and "families" if they are lists
- Ignores missing or malformed fields
- Writes a backup before making changes

📁 INPUT:
- xvault_wking_filling.json

📁 OUTPUT:
- Updated vault with cleaned lists
- Backup saved in: backups/xvault_wking_filling.deduped_tags_families.json
"""

import json
from pathlib import Path

VAULT_FILE = Path("ivault_master.json")
BACKUP_DIR = Path("backups")
BACKUP_FILE = BACKUP_DIR / "ivault_master.deduped_tags_families.json"

def deduplicate_list(values):
    return list(dict.fromkeys(values)) if isinstance(values, list) else values

def main():
    vault = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    cleaned_count = 0

    for entry in vault:
        for field in ["tags", "families"]:
            original = entry.get(field)
            if isinstance(original, list):
                deduped = deduplicate_list(original)
                if len(deduped) != len(original):
                    entry[field] = deduped
                    cleaned_count += 1

    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(vault, indent=2, ensure_ascii=False), encoding="utf-8")
    VAULT_FILE.write_text(json.dumps(vault, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Deduplication complete. Cleaned {cleaned_count} entries.")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

if __name__ == "__main__":
    main()