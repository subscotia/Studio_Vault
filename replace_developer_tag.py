#!/usr/bin/env python3
"""
replace_developer_tag.py

Replaces one developer name with another throughout a vault JSON.
Example: "NI" → "Native Instruments"
"""

import json
from pathlib import Path

# 🔧 Config
VAULT_FILE   = Path("ivault_master.json")
OLD_NAME     = "NI"
NEW_NAME     = "Native Instruments"
OUT_FILE     = Path("ivault_master_devrep.json")  # or VAULT_FILE to overwrite

# 📦 Load vault
data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

# 🔁 Replace developers
count = 0
for item in data:
    dev = item.get("developer")
    if dev and dev.strip().lower() == OLD_NAME.lower():
        item["developer"] = NEW_NAME
        count += 1

# 💾 Write updated vault
OUT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✔ Replaced {count} developer entr{'y' if count == 1 else 'ies'}: \"{OLD_NAME}\" → \"{NEW_NAME}\"")
print(f"📁 Output written to: {OUT_FILE}")