import json, re
from collections import defaultdict
import os

# ----- Adjust these paths if you're NOT moving the INIs into the project -----
fxfolders_fn = r"F:\py\reaper-fxfolders.ini"
fxtags_fn    = r"F:\py\reaper-fxtags.ini"

# 1) Parse custom FX folders
plugin_folders = defaultdict(list)
current_folder = None
with open(fxfolders_fn, encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line: continue
        folder = re.match(r'^\[(.+)\]$', line)
        if folder:
            current_folder = folder.group(1)
        elif current_folder:
            plugin_folders[line].append(current_folder)

# 2) Parse plugin tags
plugin_tags = defaultdict(list)
current_plug = None
with open(fxtags_fn, encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line: continue
        head = re.match(r'^\[(.+)\]$', line)
        if head:
            current_plug = head.group(1)
        elif current_plug and line.startswith("Tags="):
            plugin_tags[current_plug] = [
                t.strip() for t in line.split("=", 1)[1].split(",") if t.strip()
            ]

# 3) Build plugin-centric vault
all_names = set(plugin_folders) | set(plugin_tags)
vault = []
for name in sorted(all_names):
    vault.append({
        "name": name,
        "customFolders": plugin_folders.get(name, []),
        "tags": plugin_tags.get(name, [])
    })

# 4) Export to JSON
out_fn = os.path.join(os.getcwd(), "plugins_vault.json")
with open(out_fn, "w", encoding="utf-8") as out:
    json.dump(vault, out, indent=2, ensure_ascii=False)

print(f"Exported {len(vault)} plugins → {out_fn}")