#!/usr/bin/env python3
"""
list_unique_types.py

📜 PURPOSE:
Scans the master vault and outputs all unique 'type' values found. This is
useful for verifying the high-level categorization of the entire library
after a merge.

🗂️ OUTPUT:
A clean list of types, each on its own line, written to ref/types.txt.
"""

import json
from pathlib import Path

# --- CONFIGURATION (Tweak these values as needed) ---
# Point this to your new, merged master vault file.
VAULT_FILE = Path("../data/vault_master.json")
REF_DIR = Path("../ref")
OUTPUT_FILE = REF_DIR / "types.txt"


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

    type_set = set()

    for entry in data:
        # Get the type string from the object.
        type_value = entry.get("type")

        # We only want to add it if it's a non-empty string.
        if isinstance(type_value, str) and type_value:
            type_set.add(type_value)

    # Ensure the 'ref' directory exists before writing to it.
    REF_DIR.mkdir(parents=True, exist_ok=True)

    # Write the sorted, unique type names to the output file.
    OUTPUT_FILE.write_text("\n".join(sorted(type_set)), encoding="utf-8")

    print(f"✅ Unique types list written to: {OUTPUT_FILE.resolve()}")
    print(f"\nFound the following types: {sorted(type_set)}")
    print(f"Total unique types: {len(type_set)}")


if __name__ == "__main__":
    main()
