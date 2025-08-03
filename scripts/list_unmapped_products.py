""""""
#✅ What You’ll Get
#- It scans the vault
#- Extracts all entries missing a "product"
#- Writes a simple tab-separated list to unmapped_entries.txt:
""""""

import json
from pathlib import Path

VAULT_FILE = Path("../data/xvault_master.json")
OUT_FILE   = Path("unmapped_entries.txt")

with VAULT_FILE.open(encoding="utf-8") as f:
    data = json.load(f)

missing = [e for e in data if "product" not in e]

with OUT_FILE.open("w", encoding="utf-8") as f:
    for e in missing:
        filename = e.get("filename", "???")
        name     = e.get("name", "???")
        f.write(f"📄 Filename: {filename}\n")
        f.write(f"   Name:     {name}\n\n")

print(f"📝 {len(missing)} unmapped entries written to {OUT_FILE}")