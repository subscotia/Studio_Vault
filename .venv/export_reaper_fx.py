import re
import json
from collections import defaultdict

# 1. Read the REAPER tags file
fn = r'F:\py\reaper-fxtags.ini'
with open(fn, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 2. Parse sections: each [PluginName] starts a block
plugins = []
current = None
for L in lines:
    L = L.rstrip('\n')
    # New plugin block
    m = re.match(r'^\[(.+)\]$', L)
    if m:
        current = m.group(1)
        plugins.append({ 'name': current, 'tags': [] })
        continue
    # Grab any Tags= line
    if current and L.startswith('Tags='):
        tags = L.split('=',1)[1].split(',')
        plugins[-1]['tags'] = [t.strip() for t in tags if t.strip()]

# 3. Example: group by your existing “Developer” tags
by_dev = defaultdict(list)
for p in plugins:
    devs = [t for t in p['tags'] if t in [
        'Aly James Lab','Ample Sound','Arturia','FabFilter',
        'AnalogX','Teletone Audio','Wavesfactory'
    ]]
    # if you haven’t tagged by developer,
    # you’ll need to map plugin→dev manually or via another file
    if devs:
        for d in devs:
            by_dev[d].append(p['name'])
    else:
        by_dev['Unknown'].append(p['name'])

# 4. Dump to master JSON
with open('master_plugins.json', 'w', encoding='utf-8') as out:
    json.dump(by_dev, out, indent=2, ensure_ascii=False)

print(f"Found {len(plugins)} total plugins, grouped by developer.")