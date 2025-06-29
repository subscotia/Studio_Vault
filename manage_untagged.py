#!/usr/bin/env python3
"""
manage_untagged.py

Extracts entries missing "tags" into a separate file for editing,
then merges them back into the main vault using name+developer as keys.

Usage:
  # Extract untagged:
  python manage_untagged.py extract vault_instr_master.json untagged.json

  # Merge edited entries back:
  python manage_untagged.py merge vault_instr_master.json untagged.json merged_vault.json
"""

import json, sys
from pathlib import Path

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(data, path: Path):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def extract_untagged(input_file: Path, output_file: Path):
    vault = load_json(input_file)
    untagged = [entry for entry in vault
                if not entry.get("tags") or not isinstance(entry["tags"], list)]
    save_json(untagged, output_file)
    print(f"✔ Extracted {len(untagged)} untagged entries → {output_file.name}")

def merge_fixed_tags(master_file: Path, patch_file: Path, output_file: Path):
    master = load_json(master_file)
    patch  = load_json(patch_file)

    patch_map = {
        (e.get("name","").lower(), e.get("developer","").lower()): e
        for e in patch
    }

    updated = []
    replaced = 0
    seen_keys = set()

    for entry in master:
        key = (entry.get("name","").lower(), entry.get("developer","").lower())
        if key in patch_map:
            updated.append(patch_map[key])
            replaced += 1
            seen_keys.add(key)
        else:
            updated.append(entry)

    # Add new entries (not in master at all)
    for key, entry in patch_map.items():
        if key not in seen_keys:
            updated.append(entry)
            print(f"➕ Appended new entry: {entry.get('name')}")

    save_json(updated, output_file)
    print(f"✔ Merged vault written to: {output_file.name} ({replaced} entries replaced)")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:\n  extract input.json untagged.json\n  merge input.json fixes.json output.json")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "extract":
        extract_untagged(Path(sys.argv[2]), Path(sys.argv[3]))
    elif mode == "merge":
        merge_fixed_tags(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)