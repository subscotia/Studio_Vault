import json
from pathlib import Path
from datetime import datetime
import os

# 🛠 Base setup
base_dir = Path(__file__).resolve().parent
vault_path = base_dir / "vault_instr_wip.json"
ot_path = base_dir / "orctools_instruments_merged.json"
logs_dir = base_dir / "logs"
logs_dir.mkdir(exist_ok=True)

# 🎚️ Control flags
dry_run = False
log_changes = True
skip_conditionals = True  # ⬅️ Toggle this to True/False

# 📦 Override fields
unconditional_overrides = {
    "developer": "Orchestral Tools",
    "host": "SINE",
    "type": "Instrument"
}

conditional_overrides = {} if skip_conditionals else {
    "origin": "MergedImport_20240624"
}

# 🧠 Load data
vault = json.loads(vault_path.read_text(encoding="utf-8"))
new_entries = json.loads(ot_path.read_text(encoding="utf-8"))
change_log = []

# ⚙️ Apply overrides
for entry in new_entries:
    updated_fields = {}

    for key, value in unconditional_overrides.items():
        before = entry.get(key)
        entry[key] = value
        updated_fields[key] = {"before": before, "after": value}

    for key, value in conditional_overrides.items():
        if entry.get(key) in [None, ""]:
            before = entry.get(key)
            entry[key] = value
            updated_fields[key] = {"before": before, "after": value}

    change_log.append({
        "name": entry.get("name", "[Unnamed]"),
        "applied": updated_fields
    })

# 🚀 Finalize
if dry_run:
    print(f"🧪 Dry run: {len(new_entries)} entries *would* be appended to {vault_path.name}")
else:
    merged = vault + new_entries
    vault_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Appended {len(new_entries)} entries to {vault_path.name}")

if log_changes:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"import_log_{ts}.json"
    log_path.write_text(json.dumps(change_log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"📄 Log written to: {log_path}")