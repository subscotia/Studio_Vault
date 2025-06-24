import json
from pathlib import Path
from datetime import datetime
import os

# Config
base_dir = Path(__file__).resolve().parent
vault_path = base_dir / "vault_instr_wip.json"
logs_dir = base_dir / "logs"
logs_dir.mkdir(exist_ok=True)

# Metadata expectations
required_fields = ["name", "type", "host", "developer", "tags"]
allowed_types = {"Instrument", "FX", "Utility"}
allowed_hosts = {"Kontakt", "vst3", "SINE", "EZDrummer", "MSoundFactory", "Nebula", "Soundpaint", "Opus", "Cube", "Mixbox", "TR5 Suite", "EZBass", "Reaper", "Falcon", "standalone", "CLAP", None}

# Load Vault
vault = json.loads(vault_path.read_text(encoding="utf-8"))
issues = []

for i, entry in enumerate(vault):
    entry_issues = []
    name = entry.get("name", f"[NoName_{i}]")

    # Check required fields exist
    for field in required_fields:
        if field not in entry:
            entry_issues.append(f"❌ Missing field: {field}")
        elif entry[field] in ["", None]:
            entry_issues.append(f"⚠️ Field '{field}' is blank or null")

    # Validate allowed field values
    if "type" in entry and entry["type"] not in allowed_types:
        entry_issues.append(f"🚫 Unexpected type: {entry['type']}")
    if "host" in entry and entry["host"] not in allowed_hosts:
        entry_issues.append(f"🚫 Unexpected host: {entry['host']}")

    if entry_issues:
        issues.append({
            "name": name,
            "index": i,
            "problems": entry_issues
        })

# Output results
if issues:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = logs_dir / f"vault_validation_{ts}.json"
    report_path.write_text(json.dumps(issues, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"🚨 Validation complete — {len(issues)} problematic entries found")
    print(f"📄 Report saved to: {report_path}")
else:
    print("✅ No metadata issues detected in Vault!")
