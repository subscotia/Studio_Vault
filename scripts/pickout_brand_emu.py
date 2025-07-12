#!/usr/bin/env python3
"""
pickout_brand_emu.py

For each FX entry in xvault_raw.json:
 - Finds any "families" value that starts with "BRAND-"
 - Strips off "BRAND-", keeping e.g. "AMEK" in families
 - Sets entry["emulates"] = "AMEK"
 - Leaves other families untouched

Backs up xvault_raw.json → xvault_raw_bak.json,
overwrites the vault file, and writes a machine-friendly report.
"""

import json, shutil
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────
VAULT_FILE   = Path("xvault_raw.json")
BACKUP_FILE  = Path("xvault_raw_bak.json")
JSON_REPORT  = Path("../logs/pickout_brand_emu.json")
PREFIX       = "BRAND-"
# ────────────────────────────────────────────────────────────────────────────

def main():
    # 1) Backup (overwrite)
    shutil.copy2(VAULT_FILE, BACKUP_FILE)
    print(f"🔒 Backed up vault to {BACKUP_FILE}")

    # 2) Load vault
    entries = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

    changed = []
    updated = []

    # 3) Process each entry
    for e in entries:
        fams = e.get("families") or []
        # find all BRAND- items
        brands = [f[len(PREFIX):] for f in fams if f.startswith(PREFIX)]
        if not brands:
            updated.append(e)
            continue

        old_fams = fams.copy()
        # strip PREFIX from all families
        new_fams = [f[len(PREFIX):] if f.startswith(PREFIX) else f
                    for f in fams]
        e["families"] = new_fams
        # set emulates to the first brand found
        e["emulates"] = brands[0] if len(brands) == 1 else brands

        changed.append({
            "name":           e.get("name"),
            "filename":       e.get("filename"),
            "old_families":   old_fams,
            "new_families":   new_fams,
            "emulates":       e["emulates"]
        })
        updated.append(e)

    # 4) Overwrite vault
    VAULT_FILE.write_text(
        json.dumps(updated, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"✅ Updated vault: {len(changed)} entries had BRAND- pulled out")

    # 5) Write JSON report
    JSON_REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "changed_count":   len(changed),
        "changed_entries": changed
    }
    JSON_REPORT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"📝 JSON report written to {JSON_REPORT}")

if __name__ == "__main__":
    main()