import json
from pathlib import Path

# Load current Vault
vault_path = Path("vault_working.json")
vault = json.loads(vault_path.read_text(encoding="utf-8"))

# Load AnalogX FX entries
fx = json.loads(Path("analogx_effects_merged.json").read_text(encoding="utf-8"))

# Append and overwrite
vault += fx
vault_path.write_text(
    json.dumps(vault, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ Added {len(fx)} AnalogX FX → vault_working.json")