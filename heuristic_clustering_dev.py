#!/usr/bin/env python3
"""
Heuristic clustering script to generate suite_map.json.
Groups plugins by shared filename prefix and assigns an official suite name.
Now includes:
- [S]kip per cluster
- Auto-saving after each confirmation
"""

import json
import os
from collections import defaultdict
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────
VAULT_FILE   = Path("xvault_wking_filling.json")
OUTPUT_MAP   = Path("suite_map.json")
MIN_PREFIX   = 4   # minimal shared chars to form a cluster
# ───────────────────────────────────────────────────────────────────

def common_prefix(strs):
    """Return longest common prefix among all strings in list."""
    if not strs: return ""
    s1, s2 = min(strs), max(strs)
    for i, ch in enumerate(s1):
        if ch != s2[i]:
            return s1[:i]
    return s1

def main():
    if not VAULT_FILE.exists():
        print(f"❌ Cannot find vault file: {VAULT_FILE}")
        return

    try:
        suite_map = json.loads(OUTPUT_MAP.read_text(encoding="utf-8"))
    except FileNotFoundError:
        suite_map = {}

    entries = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    clusters = defaultdict(list)

    for e in entries:
        stem = os.path.splitext(e["filename"])[0].lower()
        key  = stem[:MIN_PREFIX]
        clusters[key].append(stem)

    # Only consider clusters with 2+ modules and not already saved
    for key, mods in clusters.items():
        unique = sorted(set(mods))
        if len(unique) < 2:
            continue

        # Skip if already mapped
        if all(mod in suite_map for mod in unique):
            continue

        prefix = common_prefix(unique)
        if len(prefix) < MIN_PREFIX:
            continue

        suggested = prefix.title()
        print("\n🔹 Cluster:", unique)
        resp = input(f"✔️  Official suite name [{suggested}] (type S to skip)> ").strip()

        if resp.lower() == "s":
            print("⏭️  Skipped this cluster.")
            continue

        name = resp or suggested
        for mod in unique:
            suite_map[mod] = name

        # Save progress after each batch
        OUTPUT_MAP.write_text(json.dumps(suite_map, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"💾 Saved {len(unique)} entries under: {name}")

    print(f"\n✅ Finished. Full suite map written to: {OUTPUT_MAP} ({len(suite_map)} entries)")

if __name__ == "__main__":
    main()