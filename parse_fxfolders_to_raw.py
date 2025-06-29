#!/usr/bin/env python3
"""
parse_fxfolders_to_raw.py

Reads a Reaper fxfolders.txt/ini and emits a baseline JSON array of FX entries,
extracting:
  • filename (pre-dot + extension)
  • host     (extension)
  • raw family hint (post-equals)

We humanize the "name" by replacing underscores with spaces and uppercasing.
All other fields are placeholders to be filled in later (developer, id, etc.)
"""

import json
import re
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────
IN_FILE  = Path("reaper-fxfolders.txt")
OUT_FILE = Path("xvault_raw.json")
# ──────────────────────────────────────────────────────────────────────

def humanize(s: str) -> str:
    # replace underscores, remove extension, title-case
    base = Path(s).stem
    return base.replace("_", " ").title()

def parse_line(line: str):
    # match: filename.ext=rawHint
    m = re.match(r'^([^.=]+?\.[^.=]+)=(.+)$', line.strip())
    if not m:
        return None
    filename, raw = m.groups()
    # split host from filename
    host = filename.split(".", 1)[1]
    # families hint: remove leading '-' if present, split on '|' into list
    raw = raw.lstrip("-")
    families = [f.strip() for f in raw.split("|") if f.strip()]
    return {
        "name":        humanize(filename),
        "filename":    filename,
        "type":        "fx",
        "host":        host,
        "developer":   None,
        "families":    families or None,
        "libraryPath": None,
        "tags":        [],
        "emulates":    None,
        "id":          None
    }

def main():
    if not IN_FILE.exists():
        print(f"❌ Cannot find {IN_FILE}")
        return

    entries = []
    for raw in IN_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith(";") or line.startswith("["):
            continue
        obj = parse_line(line)
        if obj:
            entries.append(obj)

    OUT_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"✔ Parsed {len(entries)} FX entries → {OUT_FILE}")

if __name__ == "__main__":
    main()