#!/usr/bin/env python3
"""
family_helper.py

Assigns families by simple substring rules against 'name' or 'filename'.

CONFIGURE:
  RULES = {
      "substring1": "FamilyName1",
      "substring2": "FamilyName2",
      ...
  }

• Backup xvault_raw.json → xvault_raw_bak.json (overwrite)
• Append matching families—never remove or overwrite existing ones
• Report changes in logs/family-helper.json
"""

import json, shutil
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────
VAULT_FILE  = Path("xvault_raw.json")
BACKUP_FILE = Path("xvault_raw_bak.json")
REPORT_FILE = Path("../logs/family-helper.json")

# Define your substring → family mappings here:
RULES = {
    "ratio":       "compression",
    "comp":          "compression",
    "saturat":              "saturation",
    "N4":               "nebula",
    "Pwrcab":                "amp cabinet sims",
    "Preamp":        "preamp",
    "Nectar 4":                "vocals"
    # add more rules as you go…
}
# ────────────────────────────────────────────────────────────────────────────

def main():
    # 1) Backup (overwrite)
    shutil.copy2(VAULT_FILE, BACKUP_FILE)
    print(f"🔒 Backed up vault to {BACKUP_FILE}")

    # 2) Load vault
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

    changes = []

    # 3) Process entries
    for e in data:
        name     = e.get("name", "").lower()
        fname    = e.get("filename", "").lower()
        fams     = e.get("families") or []
        added    = []

        for substr, family in RULES.items():
            if substr.lower() in name or substr.lower() in fname:
                if family not in fams:
                    fams.append(family)
                    added.append(family)

        if added:
            e["families"] = fams
            changes.append({
                "name":     e.get("name"),
                "filename": e.get("filename"),
                "added":    added
            })

    # 4) Overwrite vault with updates
    VAULT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    print(f"✅ Applied family rules to {len(changes)} entries")

    # 5) Write JSON report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "changed_count": len(changes),
        "changes":       changes
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                           encoding="utf-8")
    print(f"📝 JSON report written to {REPORT_FILE}")

if __name__ == "__main__":
    main()