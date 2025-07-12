import json

VAULT_INPUT = "vault_working.json"
INSTR_OUTPUT = "vault_instr_wip.json"
FX_OUTPUT = "vault_fx_wip.json"

def split_vault_by_type(vault_path, instr_path, fx_path):
    with open(vault_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    instruments = [item for item in data if item.get("type") == "Instrument"]
    fx = [item for item in data if item.get("type") != "Instrument"]

    with open(instr_path, "w", encoding="utf-8") as f:
        json.dump(instruments, f, indent=2)
    print(f"🎹 Exported {len(instruments)} instruments to {instr_path}")

    with open(fx_path, "w", encoding="utf-8") as f:
        json.dump(fx, f, indent=2)
    print(f"🎛️ Exported {len(fx)} FX/other entries to {fx_path}")

if __name__ == "__main__":
    split_vault_by_type(VAULT_INPUT, INSTR_OUTPUT, FX_OUTPUT)