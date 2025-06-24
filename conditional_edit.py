#reads from the vault_working.json,
# check for entries where "match_attr" equals value "match_value",
# and then set or update attribute "target_attr" to a new value "target_value".
#lastest version here has
#- ✅ Optional dry_run mode — shows changes without saving
#- 📄 Optional logging to a timestamped file in /logs/
#- 🎛️ Pre-filtering by type (e.g. only apply rules to Instruments
#- An optional second condition (e.g. "host" == "vst3" and "developer" == "UAD")
#- Multiple key-value updates on matching entries (e.g. set both "host" and "format")

import json
import os
from datetime import datetime

VAULT_PATH = "vault_instr_wip.json"
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

def conditional_multi_edit(path, match_conditions, updates, type_filter=None, dry_run=False, log_changes=False):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    changes = []
    for entry in data:
        if type_filter and entry.get("type") != type_filter:
            continue

        if all(entry.get(k) == v for k, v in match_conditions.items()):
            before_snapshot = {k: entry.get(k) for k in updates}
            for update_key, update_val in updates.items():
                entry[update_key] = update_val
            after_snapshot = {k: entry.get(k) for k in updates}
            changes.append({
                "name": entry.get("name", "[Unnamed]"),
                "type": entry.get("type"),
                "before": before_snapshot,
                "after": after_snapshot
            })

    if dry_run:
        print(f"🧪 Dry run: {len(changes)} entries *would* be updated. No changes saved.")
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Updated {len(changes)} entries in-place in {path}")

    if log_changes and changes:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(LOGS_DIR, f"vault_multi_edit_{ts}.json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(changes, f, indent=2)
        print(f"📄 Log file written to: {log_path}")

if __name__ == "__main__":
    # Example: If developer == "UAD" and host == "vst3", set host = "UADx" and format = "UADPlugin"
    conditional_multi_edit(
        path=VAULT_PATH,
        match_conditions={"type": "Instrument", "host": "Falcon"},
        updates={"developer": "UVI"},
        type_filter="Instrument",     # Optional filter on entry["type"]
        dry_run=False,        # True = preview only
        log_changes=True      # True = write change log to /logs
    )