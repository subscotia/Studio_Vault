#!/usr/bin/env python3
"""
backup_vault.py

Creates a timestamped backup of your vault JSON.

Usage:
  python backup_vault.py vault_instr_master.json
  python backup_vault.py vault_instr_master.json --dest my_backups
"""

import shutil
import argparse
from pathlib import Path
from datetime import datetime

def backup(input_file: Path, backup_dir: Path):
    # ensure input exists
    if not input_file.exists():
        print(f"❌ ERROR: {input_file} not found.")
        return

    # create backup dir
    backup_dir.mkdir(parents=True, exist_ok=True)

    # build timestamped filename
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_file = backup_dir / f"{input_file.stem}_{ts}{input_file.suffix}"

    # copy
    shutil.copy2(input_file, dest_file)
    print(f"✔ Backed up {input_file.name} → {dest_file}")

def main():
    p = argparse.ArgumentParser(description="Backup your vault JSON.")
    p.add_argument("vault",              type=Path,
                   help="Path to your vault JSON (e.g. vault_instr_master.json)")
    p.add_argument("--dest", "-d", type=Path, default=Path("../backups"),
                   help="Directory where backups are saved")
    args = p.parse_args()

    backup(args.vault, args.dest)

if __name__ == "__main__":
    main()