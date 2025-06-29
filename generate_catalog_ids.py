#!/usr/bin/env python3
"""
generate_catalog_ids.py

Assign unique IDs to catalog entries and emit:
  • Updated JSON
  • CSV index (id,name,type,developer)
  • Optional detailed log file

Now supports:
  --start-seq N     # Begin numbering at N instead of 1

Usage:
  python generate_catalog_ids.py \
    input.json    output.json \
    [--index-file IDX.csv] \
    [--log-file LOG.txt] \
    [--include-skipped] \
    [--no-sort] \
    [--start-seq N]
"""

import json
import shutil
import logging
import csv
import argparse
from pathlib import Path
from typing import Optional

# ─── Logging Setup ────────────────────────────────────────────────────────────
logger = logging.getLogger("catalog_id_gen")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(
    "%(asctime)s  %(levelname)-5s  %(message)s", "%Y-%m-%d %H:%M:%S"
)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(fmt)
logger.addHandler(ch)

# ─── Backup Utility ───────────────────────────────────────────────────────────
def backup(src: Path) -> None:
    """Copy src → src.bak if not already present."""
    bak = src.with_suffix(src.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(src, bak)
        logger.info(f"Backup created: {bak.name}")
    else:
        logger.info(f"Backup already exists: {bak.name}")

# ─── Core ID Generator ────────────────────────────────────────────────────────
def generate_ids(
    input_file: Path,
    output_file: Path,
    index_file: Optional[Path] = None,
    log_file:   Optional[Path] = None,
    sort_by_id: bool = True,
    include_skipped: bool = False,
    start_seq: int = 1
):
    # 1) Backup
    backup(input_file)

    # 2) Load data
    try:
        data = json.loads(input_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Failed to read/parse JSON: {e}")
        return

    processed, skipped = [], []
    sequence = start_seq

    logger.info(f"=== Starting ID assignment (start_seq={start_seq}) ===")
    for entry in data:
        name = entry.get("name", "<Unnamed>")
        t    = entry.get("type")
        d    = entry.get("developer")

        # skip if missing type or developer
        if not t or not d:
            logger.warning(f"SKIP  missing type/developer → {name}")
            skipped.append(entry.copy())
            continue

        # build prefix from first two letters of type & developer
        prefix = (t.strip().lower()[:2] + d.strip().lower()[:2]).upper()
        new_id = f"{prefix}{sequence:05d}"
        entry["id"] = new_id

        logger.info(f"OK    {new_id} assigned to {name}")
        processed.append(entry)
        sequence += 1

    # 3) Sort?
    if sort_by_id:
        processed.sort(key=lambda x: x["id"])

    # 4) Combine
    output_list = processed + (skipped if include_skipped else [])

    # 5) Write JSON
    try:
        output_file.write_text(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info(f"Updated JSON written to: {output_file.name}")
    except Exception as e:
        logger.error(f"Failed to write JSON: {e}")

    # 6) Write CSV index
    if index_file:
        try:
            with index_file.open("w", newline="", encoding="utf-8") as csvf:
                writer = csv.writer(csvf)
                writer.writerow(["id","name","type","developer"])
                for e in processed:
                    writer.writerow([
                        e["id"],
                        e.get("name",""),
                        e.get("type",""),
                        e.get("developer","")
                    ])
            logger.info(f"CSV index written to: {index_file.name}")
        except Exception as e:
            logger.error(f"Failed to write CSV: {e}")

    # 7) Write detailed log
    if log_file:
        try:
            with log_file.open("w", encoding="utf-8") as lf:
                lf.write("=== Catalog ID Assignment Log ===\n\n")
                lf.write(f"Processed: {len(processed)} entries\n")
                lf.write(f"Skipped:   {len(skipped)} entries\n\n")
                for e in processed:
                    lf.write(f"OK    {e['id']} → {e.get('name','')}\n")
                for e in skipped:
                    lf.write(f"SKIP  {e.get('name','')} (missing fields)\n")
            logger.info(f"Log file saved to: {log_file.name}")
        except Exception as e:
            logger.error(f"Failed to write log: {e}")

# ─── CLI Entrypoint ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Assign IDs to catalog entries and emit JSON/CSV/logs"
    )
    p.add_argument("input_file",  type=Path,
                   help="Source JSON (e.g. new_tools.json)")
    p.add_argument("output_file", type=Path,
                   help="Destination JSON (e.g. new_tools_with_ids.json)")
    p.add_argument("--index-file", "-i", type=Path,
                   help="CSV index file (default: <output_stem>_index.csv)")
    p.add_argument("--log-file", "-l", type=Path,
                   help="Detailed text log file")
    p.add_argument("--include-skipped", "-s", action="store_true",
                   help="Also include skipped entries at end of JSON")
    p.add_argument("--no-sort", action="store_true",
                   help="Do not sort processed entries by ID")
    p.add_argument("--start-seq", "-S", type=int, default=1,
                   help="Sequence number to start from (default: 1)")

    args = p.parse_args()

    # default index name if none given
    if not args.index_file:
        args.index_file = args.output_file.with_name(
            f"{args.output_file.stem}_index.csv"
        )

    generate_ids(
        input_file      = args.input_file,
        output_file     = args.output_file,
        index_file      = args.index_file,
        log_file        = args.log_file,
        sort_by_id      = not args.no_sort,
        include_skipped = args.include_skipped,
        start_seq       = args.start_seq
    )