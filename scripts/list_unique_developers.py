#!/usr/bin/env python3
"""
list_unique_developers.py

📜 Outputs all unique 'developer' names from the vault as:
"Developer Name"
Each on its own line, quoted.

🗂 File written to: ref/developers.txt
"""

import json
from pathlib import Path

# --- CONFIGURATION (Tweak these values as needed) ---
# You can point this to ivault_master.json, xvault_master.json, or a merged file.
VAULT_FILE = Path("../data/ivault_master.json")
REF_DIR = Path("../ref")
OUTPUT_FILE = REF_DIR / "developers.txt"


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

    developer_set = set()

    for entry in data:
        # Get the developer value from the entry
        developer = entry.get("developer")
        
        # Handle string case
        if isinstance(developer, str) and developer:
            developer_set.add(developer)
        # Handle list case    
        elif isinstance(developer, list):
            for dev in developer:
                if isinstance(dev, str) and dev:
                    developer_set.add(dev)

    # Ensure the 'ref' directory exists before writing to it.
    REF_DIR.mkdir(exist_ok=True)

    # Write the sorted, unique developer names to the output file.
    # Each name is wrapped in quotes and placed on a new line.
    OUTPUT_FILE.write_text("\n".join(f'"{dev}"' for dev in sorted(developer_set)), encoding="utf-8")

    print(f"✅ Developers list written to: {OUTPUT_FILE}")
    print(f"\nTotal unique developers: {len(developer_set)}")


if __name__ == "__main__":
    main()