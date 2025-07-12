import json
import csv

VAULT_PATH = "vault_working.json"
CSV_EXPORT_PATH = "vault_export.csv"

def export_vault_to_csv(json_path, csv_path):
    with open(json_path, "r", encoding="utf-8") as f:
        vault = json.load(f)

    if not vault:
        print("⚠️  Vault is empty.")
        return

    # Collect all unique keys across entries to handle schema variability
    all_keys = set()
    for entry in vault:
        all_keys.update(entry.keys())
    headers = sorted(all_keys)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for entry in vault:
            writer.writerow(entry)

    print(f"📤 Vault successfully exported to: {csv_path}")

if __name__ == "__main__":
    export_vault_to_csv(VAULT_PATH, CSV_EXPORT_PATH)