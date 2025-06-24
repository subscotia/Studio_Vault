import json
from pathlib import Path

# 1) Read your Orchestral Tools list
txt_path = Path("LibraryList_OrcTools.txt")
lines = [
    line.strip()
    for line in txt_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

# 2) Build Vault entries
entries = []
for name in lines:
    entries.append({
        "name": name,
        "type": "Instrument",
        "host": "Orchestral Tools",
        "developer": "Orchestral Tools",
        "libraryPath": None,
        "tags": []
    })

# 3) Write out the merged JSON
out = Path("orctools_instruments_merged.json")
out.write_text(
    json.dumps(entries, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ {len(entries)} Orchestral Tools libraries written → {out}")