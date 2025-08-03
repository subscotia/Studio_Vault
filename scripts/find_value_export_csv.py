import json
import csv

# 🔧 Configurable filter
json_path = 'vault_instr_wip.json'
csv_output = 'instruments_with_Arturia.csv'
target_field = 'developer'
target_value = 'Arturia'

with open(json_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

filtered = [
    t for t in vault
    if t.get('type') == 'Instrument' and t.get(target_field) == target_value
]

print(f"🎯 Found {len(filtered)} instruments with {target_field} = '{target_value}'")

# ✍️ Write to CSV
with open(csv_output, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'developer', 'format', 'tags', 'type'])
    writer.writeheader()
    for tool in filtered:
        writer.writerow({
            'name': tool.get('name'),
            'developer': tool.get('developer'),
            'format': tool.get('format'),
            'tags': ', '.join(tool.get('tags', [])) if isinstance(tool.get('tags'), list) else '',
            'type': tool.get('type')
        })

print(f"✅ Exported to {csv_output}")