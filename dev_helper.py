#!/usr/bin/env python3
"""
dev_helper.py v7.0

• Always loads xvault_raw.json from script’s directory
• Backs up alongside it
• For each DEV_RULE, does a case-insensitive regex search
  over the entire JSON-dumped entry (guaranteed to catch profiler matches)
• Never overwrites an existing developer
• Reports per-rule and total assignments
"""

import json
import re
import shutil
from pathlib import Path

# ─── locate files relative to this script ─────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent
VAULT_FILE  = BASE_DIR / "xvault_skipped.json"
BACKUP_FILE = BASE_DIR / "xvault_raw_bak.json"
REPORT_FILE = BASE_DIR / "logs" / "dev-helper.json"
# ────────────────────────────────────────────────────────────────────────────

DEV_RULES = {
    "M-":     "Techivation",
"T-":     "Techivation",
"TDR ":     "Tokyo Dawn Labs",
"stilwell":     "Stillwell Audio",
"Nugen":     "Nugen Audio",
"MAAT":     "MAAT",
"KHs":     "Kilohearts",
"RX8":     "Izotope",
"Hornet":     "Hornet"







    # …add more as needed
}


def compile_rules(rules):
    """Strip each key, escape it, compile IGNORECASE."""
    out = []
    for raw, dev in rules.items():
        key = raw.strip()
        pat = re.compile(re.escape(key), re.IGNORECASE)
        out.append((raw, dev, pat))
    return out


def main():
    # 1) Load & Backup
    if not VAULT_FILE.exists():
        print(f"❌ Vault not found: {VAULT_FILE}")
        return

    entries = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    shutil.copy2(VAULT_FILE, BACKUP_FILE)
    print(f"🔍 Loaded {len(entries)} entries. Backup → {BACKUP_FILE}")

    # 2) Prepare
    rules = compile_rules(DEV_RULES)
    changes = []

    # 3) Apply each rule over every entry’s full JSON
    for raw, dev, pat in rules:
        matched = 0
        for e in entries:
            # skip ones that already have a developer
            if e.get("developer"):
                continue

            entry_json = json.dumps(e, ensure_ascii=False)
            if pat.search(entry_json):
                e["developer"] = dev
                changes.append({
                    "rule":     raw,
                    "filename": e.get("filename"),
                    "developer": dev
                })
                matched += 1

        print(f"▶ Rule '{raw}' applied to {matched} entries.")

    # 4) Summary & Write
    print(f"✅ Total assignments: {len(changes)}")
    VAULT_FILE.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps({"assigned_count": len(changes), "changes": changes},
                   indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"📝 Report → {REPORT_FILE}")


if __name__ == "__main__":
    main()