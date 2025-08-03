# F:\Studio\Admin Ops\Operations\git\vault\dedupe_tags_families.py (Refactored)

import json
from pathlib import Path
# highlight-next-line
from vault_utils import save_vault_with_backup # <-- Import our new function

# --- Configuration ---
VAULT_FILE = Path("../data/xvault_master.json")
BACKUP_DIR = Path("../backups")

def deduplicate_list(values):
    # This is a good candidate to move into vault_utils.py later!
    return list(dict.fromkeys(values)) if isinstance(values, list) else values

def main():
    vault = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    cleaned_count = 0

    for entry in vault:
        for field in ["tags", "families"]:
            original = entry.get(field)
            if isinstance(original, list):
                deduped = deduplicate_list(original)
                if len(deduped) != len(original):
                    entry[field] = deduped
                    cleaned_count += 1

    # highlight-start
    # --- Simplified save and backup ---
    print(f"Deduplication complete. Cleaned {cleaned_count} entries.")
    print("Saving vault and creating backup...")
    backup_path = save_vault_with_backup(
        vault_path=VAULT_FILE,
        data_to_save=vault,
        backup_dir=BACKUP_DIR
    )
    print(f"✅ Vault updated successfully.")
    print(f"🔒 Backup saved to: {backup_path}")
    # highlight-end


if __name__ == "__main__":
    main()