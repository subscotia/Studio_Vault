"""
Here's a script that does exactly what you're after: it scans your vault JSON, finds entries with the same "id", and collapses them into a single entry—favoring the one that has non-empty "tags".
It assumes:
- All duplicates share the same "id" (this is your merging key)
- If there’s only one duplicate with populated "tags", it wins
- If none have tags, it keeps the first one
- If both have tags, it keeps the one with more tags (fallback logic)
"""
#!/usr/bin/env python3
"""
dedupe_by_id_keep_tags.py

Finds duplicate entries in a vault JSON based on identical "id" fields.
Keeps the version of each duplicate that has populated "tags".

Usage:
  python dedupe_by_id_keep_tags.py
"""

import json
from pathlib import Path
from collections import defaultdict

# 🔧 Config
VAULT_PATH     = Path("vault_merged.json")            # Your input vault
OUTPUT_PATH    = Path("vault_deduped.json")           # Where to save the cleaned vault
REPORT_PATH    = Path("logs/deduped_ids_report.log")  # Optional text report

# 📥 Load vault
vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))

# 🧮 Group entries by ID
id_map = defaultdict(list)
for entry in vault:
    id_ = entry.get("id")
    if id_:
        id_map[id_].append(entry)

# 🔎 Deduplicate
deduped = []
duplicates_found = []

for id_, entries in id_map.items():
    if len(entries) == 1:
        deduped.append(entries[0])
    else:
        # Sort by tag count (desc), then take the one with most tags
        sorted_entries = sorted(
            entries,
            key=lambda e: len(e.get("tags") or []),
            reverse=True
        )
        deduped.append(sorted_entries[0])
        duplicates_found.append((id_, len(entries)))

# 💾 Save output
OUTPUT_PATH.write_text(json.dumps(deduped, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✔ Deduplicated vault written to: {OUTPUT_PATH} ({len(deduped)} entries)")

# 📝 Save report
if duplicates_found:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("== Deduplicated IDs (tag-rich entry retained) ==\n\n")
        for id_, count in duplicates_found:
            f.write(f"{id_} → {count} copies → 1 kept\n")
    print(f"📝 Duplicate ID report written to: {REPORT_PATH}")
else:
    print("✅ No duplicate IDs found — vault unchanged")

