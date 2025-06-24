import json

vault_path = 'vault_instruments_wip.json'

with open(vault_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

updated = 0

for tool in vault:
    if tool.get('type') == 'Instrument':
        dev = tool.get('format')
        if not isinstance(dev, str) or not dev.strip():
            tool['format'] = 'falcon'
            updated += 1

with open(vault_path, 'w', encoding='utf-8') as f:
    json.dump(vault, f, indent=2)

print(f"✅ Updated {updated} instruments with format = 'falcon'")