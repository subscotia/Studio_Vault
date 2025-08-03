# append_falcon_to_vault.py

import json
from pathlib import Path

# Load the current working Vault
vault_path = Path("vault_working.json")
vault = json.loads(vault_path.read_text(encoding="utf-8"))

# Load Falcon instruments
falcon_path = Path("falcon_instruments_merged.json")
falcon = json.loads(falcon_path.read_text(encoding="utf-8"))

# Append Falcon entries
vault += falcon

# Overwrite vault_working.json in place
vault_path.write_text(
    json.dumps(vault, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ Added {len(falcon)} Falcon libraries → vault_working.json")