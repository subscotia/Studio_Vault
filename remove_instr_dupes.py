#!/usr/bin/env python3
"""
remove_instr_dupes.py

Strips out FX entries that belong to instrument families ("INSTR--…"),
since those live in the instruments vault already.

• Backup: xvault_raw.json → xvault_raw_bak.json (overwrite)
• Removal logic: drop entries where any family startswith "INSTR--"
• Report: logs/instr-dupes-removed.json
"""

import json
import shutil
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────
VAULT_FILE    = Path("xvault_raw.json")
BACKUP_FILE   = Path("xvault_raw_bak.json")
JSON_REPORT   = Path("logs/instr-dupes-removed.json")
FAMILY_PREFIX = "INSTR--"
# ────────────────────────────────────────────────────────────────────────────

def main():
    # 1) Backup (overwrite)
    shutil.copy2(VAULT_FILE, BACKUP_FILE)
    print(f"🔒 Backed up vault to {BACKUP_FILE}")

    # 2) Load vault
    entries = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

    # 3) Partition entries
    removed = []
    kept    = []
    for e in entries:
        fams = e.get("families") or []
        if any(f.startswith(FAMILY_PREFIX) for f in fams):
            removed.append({"name": e.get("name"), "filename": e.get("filename"), "families": fams})
        else:
            kept.append(e)

    # 4) Overwrite vault with kept entries
    VAULT_FILE.write_text(
        json.dumps(kept, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"✅ Removed {len(removed)} instrument-family entries; {len(kept)} remain")

    # 5) Write JSON report
    JSON_REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "removed_count": len(removed),
        "removed_entries": removed
    }
    JSON_REPORT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"📝 JSON report written to {JSON_REPORT}")

if __name__ == "__main__":
    main()