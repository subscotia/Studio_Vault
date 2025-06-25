# Extract Unique Field Values and Export to JSO
#- Extracts all the unique values from a specific field (like "developer").
#- Then it writes those into a new JSON file where the field name becomes the key, and the list of unique values becomes the content.


import json
from pathlib import Path


def extract_unique_field_values(vault_path, field_name, output_path):
    """
    Extracts all unique values from a specific field across a list of plugin entries in a JSON vault.
    Saves the results as a new JSON file with the field name as the key.

    Args:
        vault_path (str): Path to the JSON vault you're scanning.
        field_name (str): The field whose values you want to extract (e.g. "developer", "host", "tags").
        output_path (str): The path to write the results (e.g. "developers.json").
    """
    try:
        with open(vault_path, "r", encoding="utf-8") as f:
            vault_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading vault: {e}")
        return

    values = set()
    for item in vault_data:
        val = item.get(field_name)
        if isinstance(val, list):
            values.update(val)  # Handles fields like "tags"
        elif val is not None:
            values.add(val)

    sorted_values = sorted(values)
    output_data = {field_name: sorted_values}

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        print(f"✅ Extracted {len(sorted_values)} unique '{field_name}' entries to {output_path}")
    except Exception as e:
        print(f"❌ Error writing output: {e}")


# === 🔧 USAGE ===
# Enter the file path of your vault here:
vault_file = "vault_instr_wip.json"

# Enter the field you want to scan for unique values:
target_field = "developer"  # You can change this to "host", "tags", "type", etc.

# This will be your output file:
output_file = f"{target_field}_catalog.json"

# Run the extraction:
extract_unique_field_values(vault_file, target_field, output_file)