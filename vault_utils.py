# F:\Studio\Admin Ops\Operations\git\vault\vault_utils.py

import json
from pathlib import Path
from datetime import datetime

def save_vault_with_backup(vault_path: Path, data_to_save: list, backup_dir: Path):
    """
    Safely saves new data to a vault file and creates a timestamped backup first.

    Args:
        vault_path (Path): The path to the main vault JSON file.
        data_to_save (list): The list of dictionary objects (the vault data) to save.
        backup_dir (Path): The path to the directory where backups should be stored.

    Returns:
        Path: The path to the newly created backup file, or None if no backup was made.
    """
    # 1. Ensure the backup directory exists.
    backup_dir.mkdir(exist_ok=True)

    backup_file_path = None

    # 2. Only create a backup if the original file actually exists to be backed up.
    if vault_path.exists():
        # Create a unique, timestamped backup filename.
        # e.g., "xvault_master_2025-07-05_12-30-00.json"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{vault_path.stem}_{timestamp}{vault_path.suffix}"
        backup_file_path = backup_dir / backup_filename

        # Read the original content and write it to the backup file.
        original_content = vault_path.read_text(encoding="utf-8")
        backup_file_path.write_text(original_content, encoding="utf-8")

    # 3. Now, write the new, updated data to the main vault file.
    # The 'indent=2' makes the JSON file human-readable.
    # 'ensure_ascii=False' is important for special characters in names.
    vault_path.write_text(
        json.dumps(data_to_save, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return backup_file_path


# This block demonstrates how to use the function.
# You can run this file directly (`python vault_utils.py`) to test it.
if __name__ == "__main__":
    print("--- Testing vault_utils.py ---")

    # Create dummy files and data for the test.
    TEST_VAULT_DIR = Path("./test_run")
    TEST_VAULT_DIR.mkdir(exist_ok=True)

    TEST_VAULT_FILE = TEST_VAULT_DIR / "test_vault.json"
    TEST_BACKUP_DIR = TEST_VAULT_DIR / "backups"

    # Create some initial data in the vault.
    initial_data = [{"id": 1, "name": "Old Plugin"}]
    TEST_VAULT_FILE.write_text(json.dumps(initial_data, indent=2))
    print(f"Created a dummy vault at: {TEST_VAULT_FILE}")

    # Prepare the new data we want to save.
    new_data = [{"id": 1, "name": "Old Plugin"}, {"id": 2, "name": "New Plugin"}]

    # Use the new utility function to save and backup.
    print("\nCalling save_vault_with_backup...")
    backup_path = save_vault_with_backup(
        vault_path=TEST_VAULT_FILE,
        data_to_save=new_data,
        backup_dir=TEST_BACKUP_DIR
    )

    # Report the results.
    if backup_path:
        print(f"✅ Backup created at: {backup_path}")
    else:
        print("🤔 No original file existed, so no backup was made.")

    print(f"✅ Vault updated successfully at: {TEST_VAULT_FILE}")
    print("\n--- Test complete ---")