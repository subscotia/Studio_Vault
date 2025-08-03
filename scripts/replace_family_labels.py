#!/usr/bin/env python3
"""
replace_family_labels.py

📝 PURPOSE:
Standardizes and expands specific values in the "families" field.

🔧 USE CASE:
You imported legacy Reaper labels (e.g. "---STUDIO-Cocteau") and want to replace them with
one or more modern equivalents (e.g. "studios", "guthrie").

🔁 WHAT IT DOES:
- Loads `xvault_master.json`
- Scans entries with a "families" list
- Replaces mapped values (supports 1:1 or 1:many mappings)
- Adds new values, removes old ones, avoids duplicates
- Saves backup to `/backups/`
- Overwrites the vault in-place

💾 SIDE EFFECTS:
- Vault overwritten
- Backup saved: `/backups/xvault_wking_filling.relabel_families.json`

📂 CONFIGURATION:
Edit `family_replacements` to map old → new label(s).
Each value can be a string or a list of strings.

🧠 NOTES:
- Case-sensitive matches
- Won’t add duplicates if new labels already exist
"""

import json
from pathlib import Path

# ── CONFIG ─────────────────────────────────────────────
VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")
BACKUP_FILE = BACKUP_DIR / "ivault_master.relabel_families.json"

family_replacements = {
    "vocal": "vocals"


    # Add more as needed
}
# ──────────────────────────────────────────────────────

def main():
    vault = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(vault, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

    changes = 0

    for entry in vault:
        families = entry.get("families")
        if isinstance(families, list):
            new_list = families.copy()
            for old, replacement in family_replacements.items():
                if old in new_list:
                    new_list.remove(old)
                    if isinstance(replacement, str):
                        replacement = [replacement]
                    for val in replacement:
                        if val not in new_list:
                            new_list.append(val)
                    changes += 1
            entry["families"] = new_list

    VAULT_FILE.write_text(json.dumps(vault, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Applied replacements to {changes} entries.")

if __name__ == "__main__":
    main()