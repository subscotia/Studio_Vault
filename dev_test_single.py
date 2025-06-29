import json, re
from pathlib import Path

DEV_RULE = "Newfangled"
entry = {
    "name": "Newfangled Elevate",
    "filename": "Newfangled_Elevate.vst3"
}

def normalize(s: str) -> str:
    return re.sub(r"[_\-]", " ", s.lower())

name_n = normalize(entry["name"])
file_norm = normalize(entry["filename"])
file_raw_l = entry["filename"].lower()
entry_l = json.dumps(entry).lower()

print("name_n     =", name_n)
print("file_norm  =", file_norm)
print("file_raw_l =", file_raw_l)
print("entry_l    =", entry_l)

sub = DEV_RULE.strip().lower()
print("sub        =", sub)
print("sub in name_n?", sub in name_n)
print("sub in file_norm?", sub in file_norm)
print("sub in file_raw_l?", sub in file_raw_l)
print("sub in entry_l?", sub in entry_l)