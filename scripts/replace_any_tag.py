#!/usr/bin/env python3
"""
replace_field_value.py

Replaces one value with another throughout a vault JSON for any specified field.
Example: Can replace values in any field like "developer", "product", "type", etc.
"""

import json
from pathlib import Path

# 🔧 Config
VAULT_FILE   = Path("../data/ivault_master.json")
FIELD_NAME   = "families"     # Can be any field: "developer", "product", "type", etc.
OLD_VALUE    = "guitar"
NEW_VALUE    = "guitars"
OUT_FILE     = Path("../data/ivault_master.json")  # or VAULT_FILE to overwrite

# 📦 Load vault
data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))

# 🔁 Replace values
count = 0
for item in data:
    field_value = item.get(FIELD_NAME)
    if field_value:
        if isinstance(field_value, str) and field_value.strip().lower() == OLD_VALUE.lower():
            item[FIELD_NAME] = NEW_VALUE
            count += 1
        elif isinstance(field_value, list):
            # Handle case where field contains a list
            for idx, val in enumerate(field_value):
                if isinstance(val, str) and val.strip().lower() == OLD_VALUE.lower():
                    field_value[idx] = NEW_VALUE
                    count += 1

# 💾 Write updated vault
OUT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✔ Replaced {count} {FIELD_NAME} entr{'y' if count == 1 else 'ies'}: \"{OLD_VALUE}\" → \"{NEW_VALUE}\"")
print(f"📁 Output written to: {OUT_FILE}")