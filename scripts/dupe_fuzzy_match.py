import json
import csv
import os
from itertools import combinations
from difflib import SequenceMatcher

# 🔧 Config
json_path = 'vault_instruments_wip.json'
filter_type = 'Instrument'
dedup_fields = ['developer', 'name']
similarity_threshold = 0.85
log_path = 'logs/fuzzy_matches_log.csv'

# 📥 Load vault
with open(json_path, 'r', encoding='utf-8') as f:
    vault = json.load(f)

# 🧹 Filter by type and required fields
filtered = [
    t for t in vault
    if t.get('type') == filter_type and all(isinstance(t.get(f), str) for f in dedup_fields)
]

# 🧪 Compute pairwise fuzzy matches
def make_key(tool):
    return ' | '.join(t.get(f, '').strip().lower() for f in dedup_fields)

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

matches = []

for a, b in combinations(filtered, 2):
    key_a = make_key(a)
    key_b = make_key(b)
    if key_a == key_b:
        continue
    score = similarity(key_a, key_b)
    if score >= similarity_threshold:
        matches.append((f"{score:.2f}", key_a, key_b))

# 📁 Ensure /logs dir exists
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# 📊 Write fuzzy match log
with open(log_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Score', 'Entry A', 'Entry B'])
    writer.writerows(matches)

# ✅ Report
print(f"🧠 Found {len(matches)} fuzzy match(es) above {similarity_threshold}")
print(f"📁 Saved to {log_path}")