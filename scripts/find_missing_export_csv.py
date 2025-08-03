import json
import csv

json_path = 'vault_instruments_wip.json'
csv_output = 'instruments_missing_format.csv'
target_field = 'format'  # 🔧 Change this to the field you're inspecting (e.g. 'developer', 'tags')

with open(json_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

filtered = [
    t for t in vault
    if t.get('type') == 'Instrument' and not isinstance(t.get(target_field), str)
]

print(f"🧹 Found {len(filtered)} instruments with null/missing '{target_field}'")

# Export to CSV
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