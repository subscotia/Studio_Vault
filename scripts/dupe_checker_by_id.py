#!/usr/bin/env python3
"""
check_duplicate_ids.py

Scans a vault JSON for duplicate 'id' fields.
Set vault path, output destination, and format via the CONFIG block.

Outputs:
  • Console report
  • Optional log file (.log or .json) with locations of each duplicate ID

No command-line args needed—just edit CONFIG.
"""

import json
from pathlib import Path
from collections import defaultdict, Counter

# ─── CONFIG: Set these as needed ─────────────────────────────────────────────
VAULT_PATH     = Path("vault_merged.json")               # your vault file
OUTPUT_FOLDER = Path("../logs")                  # where to save the report (or None)
OUTPUT_FORMAT  = "log"                                  # "json", "log", or None
FILTER_TYPE    = None                                    # e.g. "Instrument", or None for all
# ─────────────────────────────────────────────────────────────────────────────

def load_vault(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data
    except Exception as e:
        print(f"❌ Failed to load vault: {e}")
        exit(1)

def find_duplicate_ids(vault):
    id_map = defaultdict(list)
    for i, entry in enumerate(vault):
        id_ = entry.get("id")
        if id_:
            id_map[id_].append((i, entry))
    dupes = {k: v for k, v in id_map.items() if len(v) > 1}
    return dupes

def report_to_console(dupes):
    print(f"🆔 Found {len(dupes)} duplicated IDs\n")
    for id_, instances in dupes.items():
        print(f" • {id_}  → {len(instances)} entries")
        for i, entry in instances:
            print(f"    └─ #{i+1}: {entry.get('name')} ({entry.get('developer')})")

def write_report(dupes):
    if not OUTPUT_FOLDER:
        return
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FORMAT == "json":
        out = OUTPUT_FOLDER / "duplicate_id_report.json"
        dupe_dict = {
            id_: [
                {
                    "index": i,
                    "name": e.get("name"),
                    "developer": e.get("developer"),
                    "type": e.get("type"),
                    "tags": e.get("tags"),
                }
                for i, e in entries
            ]
            for id_, entries in dupes.items()
        }
        out.write_text(json.dumps(dupe_dict, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n📝 Duplicate report written to: {out}")

    elif OUTPUT_FORMAT == "log":
        out = OUTPUT_FOLDER / "duplicate_id_report.log"
        with out.open("w", encoding="utf-8") as f:
            for id_, entries in dupes.items():
                f.write(f"{id_} → {len(entries)} entries:\n")
                for i, e in entries:
                    f.write(f"  #{i+1}: {e.get('name')} ({e.get('developer')})\n")
                f.write("\n")
        print(f"\n📝 Duplicate report written to: {out}")

if __name__ == "__main__":
    vault = load_vault(VAULT_PATH)
    if FILTER_TYPE:
        vault = [e for e in vault if e.get("type", "").lower() == FILTER_TYPE.lower()]
        print(f"📦 Filtered by type: {FILTER_TYPE} → {len(vault)} entries")

    dupes = find_duplicate_ids(vault)
    if not dupes:
        print("✅ No duplicate IDs found.")
    else:
        report_to_console(dupes)
        write_report(dupes)