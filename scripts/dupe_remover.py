import json
import os
from collections import defaultdict

# 🔧 Config
json_path = 'vault_instr_wip.json'
output_path = 'vault_instr_wip.json'
log_path = 'logs/dupes_removed_log.json'  # Where removed entries get saved
dedup_fields = ['developer', 'name']
filter_type = 'Instrument'

# 📥 Load vault
with open(json_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

seen_keys = set()
unique_entries = []
removed_entries = []

# 🧠 Build deduped list
for t in vault:
    if t.get('type') != filter_type:
        unique_entries.append(t)
        continue

    key = '|'.join(str(t.get(field, '')).strip().lower() for field in dedup_fields)

    if key not in seen_keys:
        unique_entries.append(t)
        seen_keys.add(key)
    else:
        removed_entries.append(t)

# 💾 Save cleaned vault
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(unique_entries, f, indent=2)

# 📁 Ensure /logs directory exists
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# 📝 Save removed entries log
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(removed_entries, f, indent=2)

print(f"✅ Removed {len(removed_entries)} duplicates based on {dedup_fields} within type = '{filter_type}'")
print(f"💾 Cleaned vault saved to {output_path}")
print(f"📁 Removal log saved to {log_path}")