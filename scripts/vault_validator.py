import json
from pathlib import Path
from datetime import datetime
from field_rules import field_rules
import os

# Config
base_dir = Path(__file__).resolve().parent
vault_path = base_dir / "kontakt_instruments_merged.json"
logs_dir = base_dir / "logs"
logs_dir.mkdir(exist_ok=True)

# Metadata expectations
required_fields = ["name", "type", "host", "developer", "tags", "emulates"]
allowed_types = {"Instrument", "FX", "Utility", "Container", "Expansion"}
allowed_hosts = {"vst3i", "Kontakt", "vst3", "vst2", "SINE", "EZDrummer",
                 "MSoundFactory", "Nebula", "Soundpaint", "Opus", "Cube", "Mixbox",
                 "TR5 Suite", "EZBass", "Reaper", "Falcon", "standalone", "CLAP", None}

# Load Vault
vault = json.loads(vault_path.read_text(encoding="utf-8"))
issues = []

for i, entry in enumerate(vault):
    entry_issues = []
    name = entry.get("name", f"[NoName_{i}]")

    # Check required fields exist
    for field, rules in field_rules.items():
        if rules.get("required") and field not in entry:
            level = rules.get("severity", "error")
            symbol = "❌" if level == "error" else "⚠️"
            entry_issues.append(f"{symbol} Missing field: {field} [{level}]")
        elif field in entry:
            if rules.get("non_blank") and entry[field] in ["", None]:
                level = rules.get("severity", "warning")
                symbol = "❌" if level == "error" else "⚠️"
                entry_issues.append(f"{symbol} Field '{field}' is blank or null [{level}]")

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
