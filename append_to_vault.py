import json
from pathlib import Path

# Load your current Vault
vault_path = Path("vault_working.json")
vault = json.loads(vault_path.read_text(encoding="utf-8"))

# Load Orchestral Tools entries
ot = json.loads(Path("orctools_instruments_merged.json")
                .read_text(encoding="utf-8"))

# Append and overwrite
vault += ot
vault_path.write_text(
    json.dumps(vault, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ Added {len(ot)} Orchestral Tools libraries → vault_working.json")