#!/usr/bin/env python3
"""
find_key_value.py

🎯 PURPOSE:
Scans a vault JSON file and reports all entries that match a specific
key-value query. This is a read-only script for finding data.

💡 HOW IT WORKS:
- It can search within simple string keys (like 'developer') or list-based
  keys (like 'families' or 'tags').
- It supports different search modes: 'exact' match or 'contains' for partial matches.
- It can output the results to the console or save them to a specified text or
  Markdown file.

🔧 TWEAKABLE CONFIGURATION:
- You can change the vault file, the key to search, the value to find,
  the search mode, and the output file in the configuration block below.
"""

import json
from pathlib import Path

# --- CONFIGURATION (Tweak these values as needed) ---
VAULT_FILE = Path("../data/ivault_master.json")
REF_DIR = Path("../ref")

# The key you want to search within.
KEY_TO_SEARCH = "families"

# The value you are looking for. This is case-insensitive.
VALUE_TO_FIND = "soundscapes"

# The search mode. Options:
# "exact": The value must be an exact match.
# "contains": The value must contain the search term.
SEARCH_MODE = "exact"

# The file to save the report to. Use .md for Markdown formatting.
# Leave as None to print to the console instead.
OUTPUT_FILE = REF_DIR / "search_results.md"


# ---------------------------------------------------------

def main():
    """Main function to run the script."""
    if not VAULT_FILE.exists():
        print(f"❌ Error: Vault file not found at '{VAULT_FILE.resolve()}'")
        return

    try:
        data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the vault file. It may be invalid JSON. Details: {e}")
        return

    found_count = 0
    # Normalize the search term by stripping whitespace and converting to lowercase
    search_term = VALUE_TO_FIND.strip().lower()
    output_lines = []

    report_header = f"Search Results for '{search_term}' in key '{KEY_TO_SEARCH}' (mode: {SEARCH_MODE})"
    output_lines.append(f"# {report_header}\n")

    for index, entry in enumerate(data):
        value = entry.get(KEY_TO_SEARCH)
        match_found = False

        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    # Normalize the item from the data in the same way
                    item_normalized = item.strip().lower()
                    if SEARCH_MODE == 'exact' and item_normalized == search_term:
                        match_found = True
                        break
                    elif SEARCH_MODE == 'contains' and search_term in item_normalized:
                        match_found = True
                        break

        elif isinstance(value, str):
            # Normalize the value from the data in the same way
            value_normalized = value.strip().lower()
            if SEARCH_MODE == 'exact' and value_normalized == search_term:
                match_found = True
            elif SEARCH_MODE == 'contains' and search_term in value_normalized:
                match_found = True

        if match_found:
            found_count += 1
            product_name = entry.get('product', 'N/A')

            result_line = (
                f"## Match #{found_count} (Object Index: {index})\n"
                f"- **Product:** {product_name}\n"
                f"- **Found Value:** `{value}`\n"
            )
            output_lines.append(result_line)

    if found_count > 0:
        summary = f"\nFound {found_count} matching entries."
        output_lines.append(summary)

        if OUTPUT_FILE:
            OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT_FILE.write_text("\n".join(output_lines), encoding="utf-8")
            print(f"✅ Report saved to: {OUTPUT_FILE.resolve()}")
        else:
            print("-" * 50)
            print("\n".join(output_lines))
            print("-" * 50)

    else:
        print("🤷 No matching entries found.")


if __name__ == "__main__":
    main()
