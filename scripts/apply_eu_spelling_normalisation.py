#!/usr/bin/env python3
"""
apply_eu_spelling_normalisation.py

🇪🇺 Applies EU-style spelling normalisation directly to vault entries.

✅ Converts strings and list items (e.g. "color" → "colour")
🚫 Skips protected fields: "Product", "Name", "Filename"
📁 Input: xvault_master.json
💾 Backup saved to: backups/xvault_wking_filling.spell_eu_normalised.json
"""

import json
from pathlib import Path
import re

VAULT_FILE = Path("../data/ivault_master.json")
BACKUP_DIR = Path("../backups")
BACKUP_FILE = BACKUP_DIR / "ivault_master.spell_eu_normalised.json"

PROTECTED_FIELDS = {"Product", "Name", "Filename"}

SPELLING_MAP = {
    "color": "colour",
    "colors": "colours",
    "favorite": "favourite",
    "favorites": "favourites",
    "analyze": "analyse",
    "analyzing": "analysing",
    "organize": "organise",
    "organizing": "organising",
    "optimize": "optimise",
    "optimization": "optimisation",
    "equalizer": "equaliser",
    "equalizers": "equalisers",
    "center": "centre",
    "meters": "metres",
    "behavior": "behaviour",
    "catalog": "catalogue",
    "license": "licence"
}

def normalise_text(text):
    for us, eu in SPELLING_MAP.items():
        text = re.sub(rf"\b{us}\b", eu, text, flags=re.IGNORECASE)
    return text

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    modified = 0

    for entry in data:
        for field, value in entry.items():
            if field in PROTECTED_FIELDS:
                continue
            if isinstance(value, str):
                updated = normalise_text(value)
                if updated != value:
                    entry[field] = updated
                    modified += 1
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, str):
                        new_item = normalise_text(item)
                        new_list.append(new_item)
                        if new_item != item:
                            modified += 1
                    else:
                        new_list.append(item)
                entry[field] = new_list

    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    VAULT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ EU normalisation applied. {modified} field values updated.")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

if __name__ == "__main__":
    main()