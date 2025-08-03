#!/usr/bin/env python3
"""
uppercase_ids.py

Reads a vault JSON and uppercases all 'id' fields in-place.

Usage:
  python uppercase_ids.py
"""

import json
from pathlib import Path

# 🔧 Config
INPUT_FILE  = Path("../data/ivault_master.json")
OUTPUT_FILE = Path("ivault_master_caps.json")  # Set to INPUT_FILE to overwrite

# 📥 Load data
data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

# 🔁 Update IDs
fixed = 0
for item in data:
    if "id" in item and isinstance(item["id"], str):
        orig = item["id"]
        upper = orig.upper()
        if orig != upper:
            item["id"] = upper
            fixed += 1

# 💾 Save updated vault
OUTPUT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✔ Updated {fixed} id fields")
print(f"📦 Written to: {OUTPUT_FILE}")