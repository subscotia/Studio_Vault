import json
from collections import Counter
import csv

# 🔧 Config
json_path = 'vault_instruments_wip.json'
csv_output = 'duplicates_report.csv'  # Set to None if you don't want CSV export
dedup_fields = ['developer', 'name']  # Fields used to determine duplicates

# 📥 Load Vault
with open(json_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

# Filter by Type
vault = [t for t in vault if t.get('type') == 'Instrument']  # 🔧 change to 'Effect', etc.

# 🧮 Build keys for duplicate detection
def make_key(tool, fields):
    return '|'.join(str(tool.get(field, '')).strip().lower() for field in fields)

keys = [make_key(t, dedup_fields) for t in vault]
counts = Counter(keys)

# 🎯 Find duplicates
dupe_keys = [key for key, count in counts.items() if count > 1]
duplicates = [t for t in vault if make_key(t, dedup_fields) in dupe_keys]

print(f"🔎 Found {len(dupe_keys)} duplicate key(s)")
print(f"🧍‍♂️ Total duplicate entries: {len(duplicates)} based on fields: {dedup_fields}")

# 📝 Optional CSV export
if csv_output:
    with open(csv_output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'developer', 'format', 'tags', 'type'])
        writer.writeheader()
        for tool in duplicates:
            writer.writerow({
                'name': tool.get('name'),
                'developer': tool.get('developer'),
                'format': tool.get('format'),
                'tags': ', '.join(tool.get('tags', [])) if isinstance(tool.get('tags'), list) else '',
                'type': tool.get('type')
            })
    print(f"✅ Duplicate report exported to {csv_output}")
