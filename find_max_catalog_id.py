#!/usr/bin/env python3
"""
find_max_catalog_id.py

Scans a catalog JSON and finds the highest numeric suffix among IDs.
"""

import json
import re
from pathlib import Path

VAULT = Path("ivault_master.json")  # <-- point this to your instrument vault

def extract_suffix(id_str):
    if not isinstance(id_str, str):
        return None
    match = re.search(r"(\d{5})$", id_str)
    return int(match.group(1)) if match else None

def main():
    if not VAULT.exists():
        print(f"❌ File not found: {VAULT}")
        return

    data = json.loads(VAULT.read_text(encoding="utf-8"))
    suffixes = [extract_suffix(e.get("id")) for e in data]
    suffixes = [s for s in suffixes if s is not None]

    if not suffixes:
        print("⚠️  No valid IDs with 5-digit suffixes found.")
        return

    highest = max(suffixes)
    print(f"✅ Highest catalog ID suffix found: {highest}")
    print(f"👉 Start next ID sequence from: {highest + 1}")

if __name__ == "__main__":
    main()