import json
from datetime import datetime
import os

# 📝 FILE PATHS — edit these as needed
base_path = 'vault_instruments.json'
merge_path = 'melda_plugins_merged.json'
output_path = 'vault_instruments.json'

def merge_vaults(base_path, merge_path, output_path, dev_key='developer', name_key='name'):
    try:
        with open(base_path, 'r', encoding='utf-8') as f:
            base = json.load(f)
        with open(merge_path, 'r', encoding='utf-8') as f:
            additions = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ File not found: {e.filename}")
        return

    if not isinstance(base, list) or not isinstance(additions, list):
        print("❌ Both files must be JSON arrays.")
        return

    existing_keys = {
        f"{tool.get(dev_key, '')}|{tool.get(name_key, '')}"
        for tool in base
        if isinstance(tool.get(dev_key), str) and isinstance(tool.get(name_key), str)
    }

    added, skipped = [], []

    for tool in additions:
        dev = tool.get(dev_key)
        name = tool.get(name_key)

        if not isinstance(dev, str) or not isinstance(name, str):
            skipped.append("(missing developer or name)")
            continue

        key = f"{dev.strip()}|{name.strip()}"

        if key not in existing_keys:
            base.append(tool)
            added.append(name)
            existing_keys.add(key)
        else:
            skipped.append(name)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(base, f, indent=2)

    # 📁 Ensure logs/ folder exists
    os.makedirs('../logs', exist_ok=True)

    # 📄 Create log filename based on merged file
    merge_basename = os.path.splitext(os.path.basename(merge_path))[0]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f"logs/vault_merge_{merge_basename}_{timestamp}.log"

    with open(log_filename, 'w', encoding='utf-8') as log:
        log.write(f"[{timestamp}] Merge run\n")
        log.write(f"  Base:   {base_path}\n")
        log.write(f"  Merge:  {merge_path}\n")
        log.write(f"  Output: {output_path}\n")
        log.write(f"  Added:   {len(added)}\n")
        log.write(f"  Skipped: {len(skipped)}\n")
        if skipped:
            log.write("  Skipped duplicates:\n")
            for name in skipped:
                log.write(f"    • {name}\n")

    print(f"\n✅ Merge complete → {output_path}")
    print(f"🗂️ Log saved → {log_filename}")
    print(f"🔹 Added:   {len(added)}")
    print(f"🔸 Skipped: {len(skipped)} duplicate(s)")
    if skipped:
        print("⚠️ Skipped duplicates:")
        for name in skipped:
            print(f" • {name}")

# 🔧 Run it!
merge_vaults(base_path, merge_path, output_path)