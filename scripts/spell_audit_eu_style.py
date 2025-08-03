#!/usr/bin/env python3
"""
spell_audit_eu_style_expanded.py

🇪🇺 Vault metadata spell audit for American vs EU variants.

🧠 NEW:
- Handles plural forms and embedded strings in lists
- Scans inside fields: "description", "families", "tags", "notes", etc.
- Excludes protected fields: "Product", "Name", "Filename"

📋 Reports US spelling → EU suggestion without modifying entries

📁 INPUT: xvault_master.json
📁 OUTPUT: backups/eu_spelling_report_expanded.txt
"""

import json
from pathlib import Path
import re

# ── CONFIG ───────────────────────────
VAULT_FILE = Path("../data/xvault_master.json")
REPORT_FILE = Path("backups/eu_spelling_report_expanded.txt")
SAVE_REPORT = True
IGNORE_FIELDS = {"Product", "Name", "Filename"}

SPELLING_PAIRS = {
    "color": "colour",
    "colors": "colours",
    "favorite": "favourite",
    "favorites": "favourites",
    "analyze": "analyse",
    "analyzing": "analysing",
    "organize": "organise",
    "organizing": "organising",
    "optimize": "optimise",
    "optimization": "optimisation",
    "equalizer": "equaliser",
    "equalizers": "equalisers",
    "center": "centre",
    "meters": "metres",
    "behavior": "behaviour",
    "catalog": "catalogue",
    "license": "licence"
}
# ──────────────────────────────────────

def scan_text(text):
    hits = []
    for us, eu in SPELLING_PAIRS.items():
        pattern = re.compile(rf"\b{us}\b", re.IGNORECASE)
        if pattern.search(text):
            hits.append((us, eu))
    return hits

def main():
    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    report = []
    total_hits = 0

    for i, entry in enumerate(data):
        for field, value in entry.items():
            if field in IGNORE_FIELDS:
                continue

            if isinstance(value, str):
                found = scan_text(value)
                if found:
                    for us, eu in found:
                        report.append(f"[Entry {i}] Field '{field}': '{us}' → suggest '{eu}'")
                        total_hits += 1

            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, str):
                        found = scan_text(item)
                        if found:
                            for us, eu in found:
                                report.append(f"[Entry {i}] Field '{field}'[{idx}]: '{us}' → suggest '{eu}'")
                                total_hits += 1

    if SAVE_REPORT:
        REPORT_FILE.parent.mkdir(exist_ok=True)
        REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print(f"✅ EU spell audit complete. Found {total_hits} Americanisms.")
    if SAVE_REPORT:
        print(f"📄 Report saved to: {REPORT_FILE}")
    else:
        for line in report:
            print(line)

if __name__ == "__main__":
    main()