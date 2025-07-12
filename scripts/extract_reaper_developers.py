#!/usr/bin/env python3
"""
extract_local_reaper_developers.py

Scans a local copy of REAPER's VST plugin cache file (INI format)
to extract likely developer names based on plugin paths.

Looks for:
  • reaper-vstplugins64.ini
  • reaper-vstplugins.ini
in the current working directory.
"""

import configparser
from pathlib import Path
import re

FILES = ["reaper-vstplugins64.ini", "reaper-vstplugins.ini"]
OUTPUT = Path("known_developers_from_local_reaper.txt")

def extract_developer_from_path(path):
    parts = Path(path).parts
    for i in range(len(parts)-1, 0, -1):
        if parts[i].lower().endswith((".dll", ".vst3")):
            return parts[i-1]
    return None

def main():
    devs = set()

    for fname in FILES:
        fpath = Path(fname)
        if not fpath.exists():
            continue

        config = configparser.ConfigParser()
        config.read(fpath, encoding="utf-8", errors="ignore")

        for section in config.sections():
            for key, val in config.items(section):
                match = re.search(r"(?:\\|/)([^\\/:]+)(?:\\|/)[^\\/:]+\.(?:dll|vst3)", val, re.IGNORECASE)
                if match:
                    devs.add(match.group(1))

    if not devs:
        print("❌ No developers found in local INI files.")
        return

    sorted_devs = sorted(devs)
    OUTPUT.write_text("\n".join(sorted_devs), encoding="utf-8")
    print(f"✅ Extracted {len(sorted_devs)} developer names to: {OUTPUT}")

if __name__ == "__main__":
    main()