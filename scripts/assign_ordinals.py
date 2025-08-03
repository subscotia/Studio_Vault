import json

def assign_ordinals(vault_path, output_path):
    with open(vault_path, 'r', encoding='utf-8') as f:
        vault = json.load(f)

    for idx, tool in enumerate(vault):
        tool["ordinal"] = str(idx).zfill(5)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vault, f, indent=2)

    print(f"✔ Ordinals assigned to {len(vault)} tools → {output_path}")