#!/usr/bin/env python3
"""
vault_utils.py

A shared module for common, reusable functions used across the Vault project.
This module lives in the /scripts directory and uses relative paths to access
data and backup directories.
"""

import json
from pathlib import Path
from datetime import datetime

def save_vault_with_backup(vault_path: Path, data_to_save: list, backup_dir: Path):
    """
    Safely saves new data to a vault file and creates a timestamped backup first.

    Args:
        vault_path (Path): The path to the main vault JSON file (e.g., ../data/ivault.json).
        data_to_save (list): The list of dictionary objects (the vault data) to save.
        backup_dir (Path): The path to the directory where backups should be stored (e.g., ../backups).
    """
    # Ensure the backup directory exists.
    backup_dir.mkdir(exist_ok=True)

    backup_file_path = None

    if vault_path.exists():
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{vault_path.stem}_{timestamp}{vault_path.suffix}"
        backup_file_path = backup_dir / backup_filename

        original_content = vault_path.read_text(encoding="utf-8")
        backup_file_path.write_text(original_content, encoding="utf-8")

    vault_path.write_text(
        json.dumps(data_to_save, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return backup_file_path
