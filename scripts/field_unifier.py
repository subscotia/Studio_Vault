#- ✅ Dry-run mode — simulate changes without writing to disk
#- ✅ Opt-out toggles for logging and dry-run clearly labeled
#- ✅ Optional unification of tags if you want to normalize string lists
#Everything you might tweak is grouped neatly at the top under # 🔧 Configuration, so it’s easy to spot and adjust.


import json
from pathlib import Path
from datetime import datetime
import os

# 🔧 Configuration
base_dir = Path(__file__).resolve().parent
vault_path = base_dir / "vault_instr_wip.json"
logs_dir = base_dir / "logs"
logs_dir.mkdir(exist_ok=True)

fields_to_unify = ["developer", "host", "format"]  # Add/remove fields here
case_mode = "lower"  # Options: "lower", "upper", "title"
unify_tags = False   # ⬅️ If True, applies unification to string elements inside "tags" list
dry_run = True       # ⬅️ If True, nothing is saved—just shows how many entries *would* change
log_changes = True   # ⬅️ If True, saves change log to /logs/

# 📦 Load Vault
vault = json.loads(vault_path.read_text(encoding="utf-8"))
change_log = []

def unify(text):
    if not isinstance(text, str):
        return text
    if case_mode == "lower":
        return text.lower()
    elif case_mode == "upper":
        return text.upper()
    elif case_mode == "title":
        return text.title()
    return text

# 🧹 Normalize entries
modified_count = 0
for entry in vault:
    updated = {}

    for field in fields_to_unify:
        if field in entry and isinstance(entry[field], str):
            before = entry[field]
            after = unify(before)
            if before != after:
                if not dry_run:
                    entry[field] = after
                updated[field] = {"before": before, "after": after}

    if unify_tags and isinstance(entry.get("tags"), list):
        unified_tags = []
        tag_changes = []
        for tag in entry["tags"]:
            if isinstance(tag, str):
                new_tag = unify(tag)
                unified_tags.append(new_tag)
                if tag != new_tag:
                    tag_changes.append({"before": tag, "after": new_tag})
            else:
                unified_tags.append(tag)

        if tag_changes:
            if not dry_run:
                entry["tags"] = unified_tags
            updated["tags"] = tag_changes

    if updated:
        change_log.append({
            "name": entry.get("name", "[Unnamed]"),
            "changes": updated
        })
        modified_count += 1

# 💾 Write if not dry-run
if dry_run:
    print(f"🧪 Dry run: {modified_count} entries *would* be updated in {vault_path.name}")
else:
    vault_path.write_text(json.dumps(vault, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Unified {modified_count} entries in {vault_path.name}")

# 📝 Write log if enabled
if log_changes and change_log:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"vault_unified_{case_mode}_{ts}.json"
    log_path.write_text(json.dumps(change_log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"📄 Change log saved to: {log_path}")