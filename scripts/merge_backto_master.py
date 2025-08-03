#!/usr/bin/env python3

import json
from pathlib import Path

def key(item):
    return (item.get("name", "").strip().lower(),
            item.get("developer", "").strip().lower())

def merge_vault(master_path: Path, untagged_path: Path, output_path: Path):
    master = json.loads(master_path.read_text(encoding="utf-8"))
    untagged = json.loads(untagged_path.read_text(encoding="utf-8"))

    updated_map = { key(item): item for item in untagged }

    merged = []
    overwritten = 0
    existing_keys = set()

    for item in master:
        k = key(item)
        existing_keys.add(k)
        if k in updated_map:
            merged.append(updated_map[k])
            overwritten += 1
        else:
            merged.append(item)

    # If untagged contains brand-new entries, add those too
    new_entries = [item for k, item in updated_map.items() if k not in existing_keys]
    if new_entries:
        print(f"⚠️  Appending {len(new_entries)} brand-new entries from untagged.json.")
        merged.extend(new_entries)

    output_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✔ Merged {untagged_path.name} into {master_path.name} → {output_path.name}")
    print(f"↻ {overwritten} entries were overwritten. {len(new_entries)} new entries added.")

if __name__ == "__main__":
    merge_vault(
        Path("vault_instr_master.json"),
        Path("../data/untagged.json"),
        Path("vault_instr_merged.json")
    )