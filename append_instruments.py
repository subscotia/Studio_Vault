import json
from pathlib import Path

# Load current Vault
vault_path = Path("vault_working.json")
vault = json.loads(vault_path.read_text(encoding="utf-8"))

# Load Kontakt instruments
instr_path = Path("soundpaint_instruments_merged.json")
instruments = json.loads(instr_path.read_text(encoding="utf-8"))

# Append and write out a combined Vault
combined = vault + instruments
out_path = Path("vault_with_instruments.json")
out_path.write_text(
    json.dumps(combined, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"✔ Combined Vault written → {out_path}")