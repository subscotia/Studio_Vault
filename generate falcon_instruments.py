# generate_falcon_instruments.py

import json
from pathlib import Path

# ←── Paste your Falcon libraries here ──→
FALCON_LIBRARIES = [
    # e.g. "UVI Falcon – Cinematic Pads",
    #      "UVI Falcon – Epic Guitars",
    #      "Sound Cell – Negro Spirituals",
"Austrian Grand",
"Key Suite Acoustic",
"Key Suite Digital",
"Key Suite Electric",
"Mosaiq",
"World Suite 3",
"Aurora",
"Digital Synsations",
"EGP",
"Ether Fields",
"Falcon Factory rev2",
"Noctua by Venus Theory",
"Orchestral Suite",
"Organic Arps",
"Retro Organ Suite",
"TagLibrary"
]

# Build structured entries
entries = []
for entry in FALCON_LIBRARIES:
    if "–" in entry:
        dev, lib = [s.strip() for s in entry.split("–", 1)]
    else:
        dev, lib = None, entry
    entries.append({
        "name": lib,
        "type": "Instrument",
        "host": "Falcon",
        "developer": dev,
        "libraryPath": None,
        "tags": []
    })

# Write out JSON
out = Path("falcon_instruments_merged.json")
out.write_text(
    json.dumps(entries, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ {len(entries)} Falcon libraries written → {out}")