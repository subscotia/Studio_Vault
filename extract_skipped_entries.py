#!/usr/bin/env python3
"""
extract_skipped_entries.py

Given:
  • the original vault file (e.g. xvault_raw.json)
  • and the one with assigned IDs (e.g. xvault_with_ids.json)

…produces a file like xvault_skipped.json containing only entries without IDs.
"""

import json
from pathlib import Path

ORIGINAL_FILE = Path("xvault_raw.json")
TAGGED_FILE   = Path("xvault_with_ids.json")
OUTPUT_FILE   = Path("xvault_skipped.json")

def main():
    if not ORIGINAL_FILE.exists() or not TAGGED_FILE.exists():
        print("❌ One or both source files not found.")
        return

    original = json.loads(ORIGINAL_FILE.read_text(encoding="utf-8"))
    tagged   = json.loads(TAGGED_FILE.read_text(encoding="utf-8"))

    # gather all known IDs
    assigned_ids = {e["id"] for e in tagged if "id" in e}

    skipped = [
        e for e in original
        if not e.get("id") or e.get("id") not in assigned_ids
    ]

    OUTPUT_FILE.write_text(json.dumps(skipped, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Skipped entries saved to: {OUTPUT_FILE} ({len(skipped)} entries)")

if __name__ == "__main__":
    main()