import json
from pathlib import Path

# 1) Read your Musio list file
txt_path = Path("List_Generic.txt")
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
        "host": "vst3i",
        "developer": "GForce",
        "libraryPath": None,
        "tags": ["synth", "vintage"]
    })

# 3) Write out the merged JSON
out_path = Path("Generic_instruments_merged.json")
out_path.write_text(
    json.dumps(instruments, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"✔ {len(instruments)} Generic libraries written → {out_path}")