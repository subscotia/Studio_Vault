#!/usr/bin/env python3
"""
fill_instrument_format.py

📝 PURPOSE:
Ensures every entry in the vault with `"type": "Instrument"` has a `"format"` value.
If a format is missing or blank, it assigns `"falcon"` as the default.

🔧 USE CASE:
For vaults containing instrument metadata where the `format` field may be null, empty,
or missing—this script helps normalize those entries for downstream consistency.

🔁 WHAT IT DOES:
- Loads `vault_instruments_wip.json`
- Scans all entries where `"type"` is `"Instrument"`
- If `format` is missing, empty, or not a string → sets `"format": "falcon"`
- Writes the updated vault back, overwriting the original

💾 SIDE EFFECTS:
- Overwrites `vault_instruments_wip.json` in-place

📂 INPUT FILES:
- vault_instruments_wip.json

📂 OUTPUT FILES:
- Updated `vault_instruments_wip.json` with corrected instrument formats

🧠 NOTES:
- Entries with any non-blank format are left unchanged
- Reported count only includes newly updated entries
"""


import json

vault_path = 'vault_instruments_wip.json'

with open(vault_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

updated = 0

for tool in vault:
    if tool.get('type') == 'Instrument':
        dev = tool.get('format')
        if not isinstance(dev, str) or not dev.strip():
            tool['format'] = 'falcon'
            updated += 1

with open(vault_path, 'w', encoding='utf-8') as f:
    json.dump(vault, f, indent=2)

print(f"✅ Updated {updated} instruments with format = 'falcon'")