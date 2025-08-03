#!/usr/bin/env python3
"""
extract_untagged.py

Modes:
  extract: pull out all entries where `tags` is empty or missing
  merge:   merge manually-updated entries back into the master,
           matching on (name, developer) and overwriting those entries.

Usage:
  python extract_untagged.py extract master.json untagged.json
  python extract_untagged.py merge  master.json untagged.json merged.json
"""

import sys, json
from pathlib import Path

def extract(master_path: Path, out_path: Path):
    data = json.loads(master_path.read_text(encoding="utf-8"))
    untagged = [item for item in data if not item.get("tags")]
    out_path.write_text(json.dumps(untagged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✔ Extracted {len(untagged)} untagged entries to {out_path}")

def merge(master_path: Path, updated_path: Path, out_path: Path):
    master = json.loads(master_path.read_text(encoding="utf-8"))
    updated = json.loads(updated_path.read_text(encoding="utf-8"))

    # build a lookup for updated entries by (name, developer)
    def key(item):
        return (item.get("name","").strip().lower(),
                item.get("developer","").strip().lower())
    updated_map = { key(item): item for item in updated }

    merged = []
    replaced = 0
    for item in master:
        k = key(item)
        if k in updated_map:
            merged.append(updated_map[k])
            replaced += 1
        else:
            merged.append(item)

    # also, if updated has brand-new entries not in master, append them
    new_keys = set(updated_map.keys()) - { key(item) for item in master }
    if new_keys:
        for k in new_keys:
            merged.append(updated_map[k])
        print(f"⚠️  {len(new_keys)} new entries in updated not found in master; appended.")

    out_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✔ Merged vault written to {out_path} ({replaced} entries overwritten)")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "extract" and len(sys.argv) == 4:
        extract(Path(sys.argv[2]), Path(sys.argv[3]))
    elif mode == "merge" and len(sys.argv) == 5:
        merge(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        print("❌ Invalid arguments.\n" + __doc__)
        sys.exit(1)