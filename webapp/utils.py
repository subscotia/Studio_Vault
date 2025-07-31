import os
import json
import shutil
from datetime import datetime

# --- File Path Configuration ---
# Assumes this file is in 'webapp', and 'data'/'backups' are siblings of 'webapp'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
BACKUPS_DIR = os.path.join(PROJECT_ROOT, 'backups')
VAULT_FILE_PATH = os.path.join(DATA_DIR, 'vault_master.json')


def save_vault_with_backup(data_to_save):
    """
    Saves the provided data to the master vault JSON file, creating a
    timestamped backup of the original file first.

    Args:
        data_to_save (list): The complete list of plugin objects to be saved.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Ensure the backups directory exists
        os.makedirs(BACKUPS_DIR, exist_ok=True)

        # 1. Create timestamped backup
        if os.path.exists(VAULT_FILE_PATH):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file_name = f"vault_master_{timestamp}.json"
            backup_file_path = os.path.join(BACKUPS_DIR, backup_file_name)
            shutil.copy2(VAULT_FILE_PATH, backup_file_path)
            print(f"Successfully created backup: {backup_file_path}")

        # 2. Write the new data to the master file
        with open(VAULT_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2)

        print(f"Successfully saved updated data to {VAULT_FILE_PATH}")
        return True

    except Exception as e:
        print(f"CRITICAL ERROR: Failed to save vault data. Error: {e}")
        return False
