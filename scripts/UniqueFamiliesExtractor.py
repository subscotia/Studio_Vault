#!/usr/bin/env python3
"""
list_unique_families.py

📜 Outputs all unique 'families' from the vault as:
"family-name"
Each on its own line, lowercased, quoted.

🗂 File written to: ref/families.text (unless --console flag is used)
"""

import json
import argparse
from pathlib import Path

VAULT_FILE = Path("../data/xvault_master_wking.json")
REF_DIR = Path("../ref")
OUTPUT_FILE = REF_DIR / "families.txt"

def main():
    parser = argparse.ArgumentParser(description="List unique families from the vault")
    parser.add_argument("--console", action="store_true", 
                       help="Output to console only (skip writing to file)")
    args = parser.parse_args()

    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    families_set = set()

    for entry in data:
        families = entry.get("families", [])
        for fam in families:
            if isinstance(fam, str):
                families_set.add(fam.lower())

    formatted_families = "\n".join(f'"{fam}"' for fam in sorted(families_set))

    if args.console:
        print(formatted_families)
    else:
        REF_DIR.mkdir(exist_ok=True)
        OUTPUT_FILE.write_text(formatted_families, encoding="utf-8")
        print(f"✅ Families list written to: {OUTPUT_FILE}")

    # Optional count output — uncomment when needed
    # print(f"\nTotal unique families: {len(families_set)}")

if __name__ == "__main__":
    main()
