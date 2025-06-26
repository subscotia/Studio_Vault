#- backs up the original json file
#- appends a new field (e.g., "emulation") to each item
#- optionally sets a value for that field—if you skip the value, it’ll just be null (which is valid json)


import json
import shutil
import os

# configuration
json_path = "kontakt_instruments_merged.json"  # original json file
new_field = "emulates"       # field to add
new_value = None              # set to a list like ["prophet-5"] or leave as None

# back up the original file
backup_path = f"{json_path}.bak"
shutil.copy(json_path, backup_path)
print(f"backup created at {backup_path}")

# load, modify, and overwrite in place
with open(json_path, "r+", encoding="utf-8") as file:
    data = json.load(file)
    for item in data:
        item[new_field] = new_value
    file.seek(0)
    json.dump(data, file, indent=2)
    file.truncate()
    print(f'field "{new_field}" added to all items in {json_path}')