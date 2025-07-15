#!/usr/bin/env python3
"""
inject_product_by_filename.py

Backs up xvault_master.json, then for each entry:
- extracts the filename stem (lowercased)
- looks up that stem in suite_map.json
- injects/overwrites "product": "<mapped name>"
- writes everything back in-place
"""

import json
import shutil
from pathlib import Path

# ── CONFIG ─────────────────────────────────────────────────────
VAULT       = Path("../data/xvault_master.json")
BACKUP      = Path("xvault_wking_filling.backup.json")
SUITE_MAP   = Path("suite_map.json")
# ────────────────────────────────────────────────────────────────

def make_backup(src: Path, dst: Path):
    shutil.copy(src, dst)
    print(f"🔒 Backup created: {dst}")

def main():
    # Prechecks
    if not VAULT.exists():
        print(f"❌ Vault file not found: {VAULT}")
        return
    if not SUITE_MAP.exists():
        print(f"❌ suite_map.json not found: {SUITE_MAP}")
        return

    # 1) Backup
    make_backup(VAULT, BACKUP)

    # 2) Load suite map and vault
    suite_dict = json.loads(SUITE_MAP.read_text(encoding="utf-8"))
    entries    = json.loads(VAULT.read_text(encoding="utf-8"))

    # 3) Inject product field
    updated = 0
    for entry in entries:
        fn_stem = Path(entry.get("filename", "")).stem.lower()
        if fn_stem in suite_dict:
            entry["product"] = suite_dict[fn_stem]
            updated += 1

    # 4) Reorder so "product" is first key in each object
    def reorder(e: dict) -> dict:
        if "product" in e:
            prod_val = e.pop("product")
            return {"product": prod_val, **e}
        return e

    reordered = [reorder(e) for e in entries]

    # 5) Overwrite vault
    VAULT.write_text(
        json.dumps(reordered, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"✅ Injected 'product' into {updated}/{len(entries)} entries.")
    print(f"💾 Overwritten vault: {VAULT}")

if __name__ == "__main__":
    main()