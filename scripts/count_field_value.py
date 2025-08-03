import json
from pathlib import Path
import sys

# ── CONFIG ─────────────────────────────
VAULT_FILE = Path("../data/xvault_master.json")
FIELD_NAME = "developer"         # e.g. "developer"
TARGET_VAL = "Techivation"       # e.g. value to count
# ──────────────────────────────────────

def main():
    try:
        data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to read {VAULT_FILE}: {e}")
        sys.exit(1)

    count = sum(1 for e in data if e.get(FIELD_NAME) == TARGET_VAL)
    print(f"🔎 {FIELD_NAME} == \"{TARGET_VAL}\": {count} occurrence(s)")

if __name__ == "__main__":
    main()