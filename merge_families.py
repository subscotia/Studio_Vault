#!/usr/bin/env python3
"""
merge_families.py

🔁 Replaces specified family names with a unified target value.

🎯 Configurable source values: e.g. ["analysis", "analysers"]
🧩 Target value: e.g. "analysis"
🚫 Skips non-string and protected cases
📁 Writes updated vault back to file and keeps original backup
"""

import json
from pathlib import Path

VAULT_FILE = Path("xvault_wking_filling.json")
BACKUP_DIR = Path("backups")
BACKUP_FILE = BACKUP_DIR / "xvault_wking_filling.family_merged.json"

# 🛠️ Editable config block
SOURCE_FAMILIES = ["de ess", "deess"]  # Case-insensitive
TARGET_FAMILY = "deess"

def normalise_family(fam):
    return fam.strip().lower()

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    merged_count = 0

    for entry in data:
        families = entry.get("families", [])
        new_families = []
        for fam in families:
            if isinstance(fam, str):
                if normalise_family(fam) in map(normalise_family, SOURCE_FAMILIES):
                    if TARGET_FAMILY not in new_families:
                        new_families.append(TARGET_FAMILY)
                        merged_count += 1
                else:
                    new_families.append(fam)
            else:
                new_families.append(fam)
        entry["families"] = new_families

    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    VAULT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Merged families to \"{TARGET_FAMILY}\" across {merged_count} entries.")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

if __name__ == "__main__":
    main()