#!/usr/bin/env python3
"""
dev_rules_profiler.py

For each DEV_RULES key, counts how many entries would match
in name, filename, or anywhere in the JSON.

Usage: python dev_rules_profiler.py
"""

import json, re
from pathlib import Path

VAULT_FILE = Path("xvault_raw.json")

DEV_RULES = {
    "Newfangled":    "Newfangledaudio",
    "Noiz ":         "Kit Plugins",
    "Nolard ":       "Nebula",
    "Amethyst":      "Acustica",
    "Purple":        "Acustica",
    "Neutron":       "Izotope",
    "Ozone":         "Izotope",
    "Neold":         "Neold",
    "Navy":          "Acustica",
    "Mint":          "Acustica",
    "Mindscape":     "Fuseroom",
    "Taupe":         "Acustica",
    "Need ":         "Noiseash",
    "Anvil  ":       "Fuseroom",
    "API_1608_":     "Nebula",
    "Amplifikation ": "Kuassa",
    # …add more to test
}

def normalize(s:str)->str:
    s = s or ""
    s = s.lower()
    # replace underscores & hyphens w/ space
    s = re.sub(r"[_\-]", " ", s)
    return s.strip()

def main():
    if not VAULT_FILE.exists():
        print("ERROR: xvault_raw.json not found")
        return

    data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(data)} entries.\n")

    print(f"{'RULE':20}  {'#name':>6}  {'#file':>6}  {'#entry':>6}")
    print("-"*44)

    for raw in DEV_RULES:
        sub = raw.strip().lower()
        cnt_name = cnt_file = cnt_entry = 0

        for e in data:
            name_n = normalize(e.get("name", ""))
            file_n = normalize(e.get("filename", ""))
            entry_n = json.dumps(e).lower()

            if sub in name_n:
                cnt_name += 1
            if sub in file_n:
                cnt_file += 1
            if sub in entry_n:
                cnt_entry += 1

        print(f"{raw[:20]:20}  {cnt_name:6}  {cnt_file:6}  {cnt_entry:6}")

if __name__ == "__main__":
    main()