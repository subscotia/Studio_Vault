import json

with open('vault_working.json', 'r', encoding='utf-8') as f:
    vault = json.load(f)

print(f"Total tools in vault: {len(vault)}")