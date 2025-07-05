import json
from pathlib import Path

INPUT_A = Path("xvault_skipped_filled.json")
INPUT_B = Path("xvault_skipped.json")
OUTPUT_FILE = Path("xvault_wking_filling.json")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    a_entries = load_json(INPUT_A)
    b_entries = load_json(INPUT_B)

    merged = {}

    # First pass: load all from A
    for entry in a_entries:
        key = (entry.get("name"), entry.get("filename"))
        merged[key] = entry

    # Second pass: merge B with overwrite logic
    for entry in b_entries:
        key = (entry.get("name"), entry.get("filename"))
        if key in merged:
            a_dev = merged[key].get("developer")
            b_dev = entry.get("developer")
            # Keep the one that has a non-empty developer
            if not a_dev and b_dev:
                merged[key] = entry
        else:
            merged[key] = entry

    out = list(merged.values())
    OUTPUT_FILE.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Merged {len(out)} entries to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()