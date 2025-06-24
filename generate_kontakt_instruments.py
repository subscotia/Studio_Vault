import glob
import json
from pathlib import Path

# 1) Find all your LibraryList_*.txt files
txt_files = sorted(glob.glob("LibraryList_*.txt"))

# 2) Read every line from each file, strip whitespace, skip blanks & duplicates
names = []
for fn in txt_files:
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            n = line.strip()
            if n and n not in names:
                names.append(n)

# 3) Build structured entries
instruments = []
for entry in names:
    if "–" in entry:
        dev, lib = [s.strip() for s in entry.split("–", 1)]
    else:
        dev, lib = None, entry
    instruments.append({
        "name": lib,
        "type": "Instrument",
        "host": "Kontakt",
        "developer": dev,
        "libraryPath": None,
        "tags": []
    })

# 4) Write out the merged JSON via pathlib
out_path = Path("kontakt_instruments_merged.json")
out_path.write_text(
    json.dumps(instruments, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ {len(instruments)} Kontakt libraries written → {out_path}")