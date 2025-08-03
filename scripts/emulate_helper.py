#!/usr/bin/env python3
"""
emulate_helper.py

General-purpose “emulates” tagger:
  – If a substring appears in ANY string field of an entry,
    append a configured value to that entry’s 'emulates' field.

CONFIGURE:
  EMULATE_RULES = {
    "substring1": "EmulateValue1",
    "substring2": "EmulateValue2",
    ...
  }

• Backs up xvault_raw.json → xvault_raw_bak.json (overwrite)
• Preserves existing emulates (appends when needed)
• Reports changes in machine-friendly logs/emulate-helper.json
"""

import json, shutil
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────
VAULT_FILE    = Path("xvault_raw.json")
BACKUP_FILE   = Path("xvault_raw_bak.json")
REPORT_FILE   = Path("../logs/emulate-helper.json")

# substring (lowercase) → emulates value
EMULATE_RULES = {
    "33609":                "33609",
#    "memory man":          "Electro-Harmonix Memory Man",
 #   "la-2a":               "Teletronix LA-2A",
  #  "ssl":                  "SSL",
   # "N4Kent":               "Vox AC30"
    # add more as needed…
}
# ────────────────────────────────────────────────────────────────────────────

def matches_any_field(entry, substr):
    """Return True if substr found in any string or list-of-strings field."""
    substr = substr.lower()
    for k, v in entry.items():
        if isinstance(v, str):
            if substr in v.lower():
                return True
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, str) and substr in item.lower():
                    return True
    return False

def append_emulates(entry, value):
    """Append value into entry['emulates'], preserving existing."""
    old = entry.get("emulates")
    if not old:
        entry["emulates"] = value
    elif isinstance(old, list):
        if value not in old:
            old.append(value)
            entry["emulates"] = old
    elif isinstance(old, str):
        if old != value:
            entry["emulates"] = [old, value]

def main():
    # 1) Backup
    shutil.copy2(VAULT_FILE, BACKUP_FILE)
    print(f"🔒 Backed up vault to {BACKUP_FILE}")

    # 2) Load data
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

    changes = []

    # 3) Process entries
    for e in data:
        before = e.get("emulates")
        for substr, emulate_val in EMULATE_RULES.items():
            if matches_any_field(e, substr):
                append_emulates(e, emulate_val)
        after = e.get("emulates")
        if before != after:
            changes.append({
                "name":      e.get("name"),
                "filename":  e.get("filename"),
                "before":    before,
                "after":     after
            })

    # 4) Overwrite vault
    VAULT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                          encoding="utf-8")
    print(f"✅ Updated {len(changes)} entries with emulates values")

    # 5) Write report
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