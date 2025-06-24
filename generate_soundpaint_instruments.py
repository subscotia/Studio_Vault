import json
from pathlib import Path

# 1) Read your Soundpaint list file
txt_path = Path("LibraryList_012.txt")
lines = [l.strip() for l in txt_path.read_text(encoding="utf-8").splitlines() if l.strip()]

# 2) Build structured entries
instruments = []
for entry in lines:
    # If you have a "Dev – Library" pattern, split on the dash:
    if "–" in entry:
        dev, lib = [s.strip() for s in entry.split("–", 1)]
    else:
        dev, lib = None, entry
    instruments.append({
        "name": lib,
        "type": "Instrument",
        "host": "Soundpaint",
        "developer": "Soundpaint",
        "libraryPath": None,
        "tags": []
    })

# 3) Write out the merged JSON
out_path = Path("soundpaint_instruments_merged.json")
out_path.write_text(
    json.dumps(instruments, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"✔ {len(instruments)} Soundpaint libraries written → {out_path}")