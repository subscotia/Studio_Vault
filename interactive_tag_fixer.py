#!/usr/bin/env python3
"""
interactive_tag_fixer.py

Lets you interactively assign missing 'developer' or 'type' fields
for entries in a vault JSON (e.g. xvault_skipped.json).
Pulls developer suggestions from a developer list text file.
"""

import json
from pathlib import Path
import readline  # enables up-arrow history on Unix/WSL

# 🔧 Configurable paths
VAULT_FILE = Path("xvault_skipped.json")
OUTPUT_FILE = Path("xvault_skipped_filled.json")
DEVLIST_FILE = Path("known_developers.txt")

def load_devs():
    if not DEVLIST_FILE.exists():
        return []
    return [line.strip() for line in DEVLIST_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]

def suggest_developers(entry_name: str, dev_list):
    name_lower = entry_name.lower()
    suggestions = [
        d for d in dev_list
        if d.lower() in name_lower
    ]
    return sorted(set(suggestions))

def prompt(prompt_text, current_val=None):
    hint = f" [{current_val}]" if current_val else ""
    val = input(f"{prompt_text}{hint}: ").strip()
    return val or current_val

def main():
    if not VAULT_FILE.exists():
        print(f"❌ File not found: {VAULT_FILE}")
        return

    entries = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    dev_list = load_devs()
    updated = 0

    for idx, entry in enumerate(entries):
        name = entry.get("name", "<Unnamed>")
        dev = entry.get("developer")
        typ = entry.get("type")

        if dev and typ:
            continue  # already complete

        print("\n" + "="*60)
        print(f"{idx+1}/{len(entries)}   🎛️  {name}")
        print(f"Developer: {dev or '[none]'}")
        print(f"Type:      {typ or '[none]'}")

        # Dev suggestions
        suggestions = suggest_developers(name, dev_list)
        if suggestions:
            print("Suggestions:", ", ".join(suggestions))

        action = input("→ What do you want to update? [d]eveloper / [t]ype / [s]kip / [q]uit > ").strip().lower()
        if action == "q":
            break
        if action == "s":
            continue
        if action == "d":
            new_dev = prompt("Enter developer", dev)
            entry["developer"] = new_dev
        if action == "t":
            new_type = prompt("Enter type", typ)
            entry["type"] = new_type

        updated += 1

    print(f"\n💾 Saving {updated} updated entries to: {OUTPUT_FILE}")
    OUTPUT_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()