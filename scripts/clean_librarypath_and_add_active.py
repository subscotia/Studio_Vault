#!/usr/bin/env python3
"""
clean_librarypath_and_add_active.py

🧹 Cleans up vault entries by:
- Removing "libraryPath"
- Adding "ACTIVE": true

🎛️ Tweakable section:
You can change the default value of ACTIVE, the target field names, or add additional fields later.

🔁 What it does:
- Loads xvault_master_wking.json
- Removes "libraryPath" if present
- Adds "ACTIVE": true to each entry
- Writes a backup to backups/
- Saves updated vault back to original path
"""

import json
from pathlib import Path

# ── CONFIG ──────────────────────────
VAULT_FILE  = Path("../data/ivault_master.json")
BACKUP_DIR  = Path("../backups")
BACKUP_FILE = BACKUP_DIR / "ivault_master.json.cleaned_active.json"
DEFAULT_ACTIVE_STATE = True  # 🔧 Flip to False if needed
# ────────────────────────────────────

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    cleaned = []

    for entry in data:
        entry.pop("libraryPath", None)  # Safely remove if exists
        entry["ACTIVE"] = DEFAULT_ACTIVE_STATE
        cleaned.append(entry)

    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    VAULT_FILE.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Vault cleaned: removed 'libraryPath', added 'ACTIVE': {DEFAULT_ACTIVE_STATE}")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

if __name__ == "__main__":
    main()