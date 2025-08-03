#!/usr/bin/env python3
"""
dupe_remove_vst2.py

Removes redundant .dll FX entries when a .vst3 sibling exists,
and writes a machine-friendly JSON report of removals.

• Backup: xvault_raw.json → xvault_raw_bak.json
• Removal logic: same filename-stem, keep .vst3, drop .dll
• Report: logs/vst-vst3-removed.json
"""

import json
import shutil
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────
VAULT_FILE   = Path("xvault_raw.json")
BACKUP_FILE  = Path("xvault_raw_bak.json")
JSON_REPORT  = Path("../logs/vst-vst3-removed.json")
# ────────────────────────────────────────────────────────────────────────────

def main():
    # 1) Backup
    shutil.copy2(VAULT_FILE, BACKUP_FILE)
    print(f"🔒 Backed up vault to {BACKUP_FILE}")

    # 2) Load vault
    entries = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

    # 3) Group by filename-stem
    groups = {}
    for e in entries:
        fn = e.get("filename", "")
        stem = Path(fn).stem
        groups.setdefault(stem, []).append(e)

    # 4) Determine .dll entries to remove
    removed = []
    for stem, items in groups.items():
        exts = {Path(i["filename"]).suffix.lower() for i in items}
        if ".dll" in exts and ".vst3" in exts:
            for i in items:
                if Path(i["filename"]).suffix.lower() == ".dll":
                    removed.append({
                        "name":     i.get("name"),
                        "filename": i.get("filename")
                    })

    # 5) Filter out the removed entries
    cleaned = [e for e in entries if {
        "name": e.get("name"), "filename": e.get("filename")
    } not in removed]

    # 6) Overwrite vault
    VAULT_FILE.write_text(
        json.dumps(cleaned, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"✅ Removed {len(removed)} entries; updated {VAULT_FILE}")

    # 7) Write JSON report
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


#Walk-through:
#- We copy xvault_raw.json to xvault_raw_bak.json for safety.
#- We group entries by the filename’s stem (Delay_BRIGADE).
#- If both .dll and .vst3 exist for a stem, we collect the .dll entries into a removed list.
#- We rewrite xvault_raw.json without those .dll items.
#- Instead of a plain-text log, we produce logs/vst-vst3-removed.json

