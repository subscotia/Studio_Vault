import json
from pathlib import Path

TARGET_FILE = Path("xvault_skipped_filled.json")  # Replace with actual filename

def main():
    if not TARGET_FILE.exists():
        print("❌ File not found.")
        return

    data = json.loads(TARGET_FILE.read_text(encoding="utf-8"))

    modified = 0
    for entry in data:
        if isinstance(entry, dict) and entry.get("developer") == "Techivation":
            entry["developer"] = None
            modified += 1

    TARGET_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Replaced 'Techivation' with null in {modified} entries.")
    print(f"💾 Overwritten: {TARGET_FILE}")

if __name__ == "__main__":
    main()