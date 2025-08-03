import json
from pathlib import Path

# load your existing Vault
vault = json.loads(Path("vault_with_instruments.json").read_text(encoding="utf-8"))
# load expansions
exp = json.loads(Path("expansions_instruments_merged.json").read_text(encoding="utf-8"))

combined = vault + exp
out = Path("vault_with_expansions.json")
out.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✔ New combined Vault → {out}")