import json
from pathlib import Path

# 1) Load your Melda plugin names
txt_path = Path("LibraryList_Melda.txt")
lines = [l.strip() for l in txt_path.read_text(encoding="utf-8").splitlines() if l.strip()]

# 2) Format into Vault entries
melda_plugins = []
for name in lines:
    melda_plugins.append({
        "name": name,
        "type": "Plugin",
        "host": None,
        "developer": "MeldaProduction",
        "libraryPath": None,
        "tags": []
    })

# 3) Write to JSON
out_path = Path("melda_plugins_merged.json")
out_path.write_text(json.dumps(melda_plugins, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✔ {len(melda_plugins)} Melda plugins written → {out_path}")