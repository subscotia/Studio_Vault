#!/usr/bin/env python3
"""
list_unique_tags.py

📜 Outputs all unique 'tags' from the vault as:
"tag-name"
Each on its own line, lowercased, and quoted.

🗂 File written to: ref/tags.txt
"""

import json
from pathlib import Path

# --- CONFIGURATION (Tweak these values as needed) ---
# You can point this to ivault_master.json, xvault_master.json, or a merged file.
VAULT_FILE = Path("../data/ivault_master.json")
REF_DIR = Path("../ref")
OUTPUT_FILE = REF_DIR / "tags.txt"


# ---------------------------------------------------------

def main():
    """Main function to run the script."""
    if not VAULT_FILE.exists():
        print(f"❌ Error: Vault file not found at '{VAULT_FILE}'")
        return

    try:
        data = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not read the vault file. It may be invalid JSON. Details: {e}")
        return

    tags_set = set()

    for entry in data:
        # Get the list of tags from the entry.
        tags = entry.get("tags", [])

        # We only proceed if it's a list.
        if isinstance(tags, list):
            for tag in tags:
                # Ensure the item itself is a string before processing.
                if isinstance(tag, str):
                    tags_set.add(tag.lower())

    # Ensure the 'ref' directory exists before writing to it.
    REF_DIR.mkdir(exist_ok=True)

    # Write the sorted, unique tags to the output file.
    # Each tag is wrapped in quotes and placed on a new line.
    OUTPUT_FILE.write_text("\n".join(f'"{tag}"' for tag in sorted(tags_set)), encoding="utf-8")

    print(f"✅ Tags list written to: {OUTPUT_FILE}")
    print(f"\nTotal unique tags: {len(tags_set)}")


if __name__ == "__main__":
    main()
