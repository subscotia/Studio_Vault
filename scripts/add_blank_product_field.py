#!/usr/bin/env python3
"""
add_blank_product_field.py

📝 PURPOSE:
Adds a blank `"product"` field to all vault entries that don’t already have one.
Designed for manual editing: you’ll fill these in yourself after the script runs.

🔧 USE CASE:
You're reviewing unmatched entries in the vault and want a `"product"` key in place
on every entry, even if it's temporarily empty.

🔁 WHAT IT DOES:
- Loads `xvault_master.json`
- Finds entries missing `"product"`
- Adds: `"product": ""` to them
- Reorders the keys so `"product"` is first
- Saves a backup to `/backups/`
- Overwrites the vault in-place

💾 SIDE EFFECTS:
- Overwrites the main vault file
- Creates `backups/xvault_wking_filling.added_blank_product.json`

"""
import json
from pathlib import Path

VAULT_FILE  = Path("../data/xvault_master.json")
BACKUP_DIR  = Path("../backups")
BACKUP_FILE = BACKUP_DIR / "xvault_wking_filling.added_blank_product.json"

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    updated = 0

    for entry in data:
        if "product" not in entry:
            entry["product"] = ""
            updated += 1

    # Reorder: 'product' first
    reordered = []
    for entry in data:
        if "product" in entry:
            prod = {"product": entry.pop("product")}
            reordered.append({**prod, **entry})
        else:
            reordered.append(entry)

    # Ensure backup dir exists
    BACKUP_DIR.mkdir(exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write updated file
    VAULT_FILE.write_text(json.dumps(reordered, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Added blank 'product' to {updated} entries.")
    print(f"🔒 Backup saved to: {BACKUP_FILE}")

if __name__ == "__main__":
    main()