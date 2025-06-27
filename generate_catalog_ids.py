#!/usr/bin/env python3
"""
generate_catalog_ids.py

Assign unique IDs to catalog entries (instruments, FX, DAWs, utilities, etc.)
and optionally produce:
  • a CSV index (id → name → type → developer)
  • a detailed log file of actions

ID format: <2-letter type prefix><2-letter developer prefix><zero-padded 5-digit seq>
"""

import json
import shutil
import logging
import csv
from pathlib import Path
from typing import Optional

# ──────── 1) Logging Setup ────────
logger = logging.getLogger("catalog_id_gen")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s  %(levelname)-5s  %(message)s", "%Y-%m-%d %H:%M:%S")
ch = logging.StreamHandler()           # console handler
ch.setLevel(logging.INFO)
ch.setFormatter(fmt)
logger.addHandler(ch)

# ──────── 2) Backup Utility ────────
def backup(src: Path) -> None:
    """Copy src → src.bak if not already present."""
    bak = src.with_suffix(src.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(src, bak)
        logger.info(f"Backup created: {bak.name}")
    else:
        logger.info(f"Backup already exists: {bak.name}")

# ──────── 3) Core ID Generator ────────
def generate_ids(
    input_file: str,
    output_file: str,
    index_file: Optional[str] = None,
    log_file:   Optional[str] = None,
    sort_by_id: bool = True,
    include_skipped: bool = False
):
    """
    Reads JSON array from input_file, assigns each entry a unique `id`:
      <first2(type)><first2(developer)><5-digit sequence>
    Writes:
      - updated JSON to output_file
      - optional CSV index (id,name,type,developer) to index_file
      - optional detailed log to log_file
    """

    src  = Path(input_file)
    dest = Path(output_file)

    # 3.1 Backup original
    backup(src)

    # 3.2 Load data
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Failed to read/parse JSON: {e}")
        return

    processed, skipped = [], []
    sequence = 1

    # 3.3 Assign IDs
    logger.info("=== Starting ID assignment ===")
    for entry in data:
        name = entry.get("name", "<Unnamed>")
        t    = entry.get("type")
        d    = entry.get("developer")

        # Validation
        if not t or not d:
            msg = f"SKIP  missing type/developer → {name}"
            logger.warning(msg)
            skipped.append(entry.copy())
            continue

        # Build prefix + ID
        prefix = t.strip().lower()[:2] + d.strip().lower()[:2]
        new_id = f"{prefix}{sequence:05d}"
        entry["id"] = new_id

        logger.info(f"OK    {new_id} assigned to {name}")
        processed.append(entry)
        sequence += 1

    # 3.4 Sort if requested
    if sort_by_id:
        processed.sort(key=lambda x: x["id"])

    # 3.5 Prepare final output list
    output_list = processed + (skipped if include_skipped else [])

    # 3.6 Write updated JSON
    try:
        dest.write_text(json.dumps(output_list, indent=2, ensure_ascii=False),
                        encoding="utf-8")
        logger.info(f"Updated JSON written to: {dest.name}")
    except Exception as e:
        logger.error(f"Failed to write JSON: {e}")

    # 3.7 Optional: CSV index
    if index_file:
        idx = Path(index_file)
        try:
            with idx.open("w", newline="", encoding="utf-8") as csvf:
                writer = csv.writer(csvf)
                writer.writerow(["id", "name", "type", "developer"])
                for e in processed:
                    writer.writerow([ e["id"], e.get("name",""), e.get("type",""), e.get("developer","") ])
            logger.info(f"CSV index written to: {idx.name}")
        except Exception as e:
            logger.error(f"Failed to write CSV: {e}")

    # 3.8 Optional: Detailed log file
    if log_file:
        lg = Path(log_file)
        try:
            with lg.open("w", encoding="utf-8") as lf:
                lf.write("=== Catalog ID Assignment Log ===\n\n")
                lf.write(f"Processed: {len(processed)} entries\n")
                lf.write(f"Skipped:   {len(skipped)} entries\n\n")
                for e in processed:
                    lf.write(f"OK    {e['id']} → {e.get('name','')}\n")
                for e in skipped:
                    lf.write(f"SKIP  {e.get('name','')} (missing fields)\n")
            logger.info(f"Log file saved to: {lg.name}")
        except Exception as e:
            logger.error(f"Failed to write log: {e}")

# ──────── 4) Example Usage ────────
if __name__ == "__main__":
    # Simply call generate_ids() with file paths.
    # You can ignore CLI—just edit these variables or call from another script.
    generate_ids(
        input_file     = "vault_instr.json",
        output_file    ="vault_instr_master.json",
        index_file     = "instrument_index.csv",    # set to None to skip CSV
        log_file    ="logs/id_assignment.log",       # set to None to skip log
        sort_by_id     = True,
        include_skipped= False
    )

#Legend & Use:
#1.	Backup: Creates input.json.bak if none exists.
#2.	ID Logic:
#• type_prefix = first 2 chars of "type" (lowercased)
#• dev_prefix = first 2 chars of "developer"
#• sequence = 5-digit, zero-padded counter only for valid entries
#3.	Skip Handling: Entries missing type/developer go into skipped and are dropped by default.
#4.	Outputs:
#– Updated JSON (always)
#– Optional CSV for quick lookup (--index_file)
#- Optional detailed text log (--log_file)
#5.	Customization: Toggle sorting or include skipped entries by changing flags in the final generate_ids() call.
