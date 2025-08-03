import json
from pathlib import Path

INPUT_FILE = Path("../data/developer_catalog.json")
OUTPUT_FILE = Path("developers_only.txt")

def main():
    if not INPUT_FILE.exists():
        print("❌ Input file not found.")
        return

    raw = INPUT_FILE.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return

    dev_list = data.get("developer", [])
    if not isinstance(dev_list, list):
        print("⚠️ 'developer' key not a list.")
        return

    cleaned = [d.strip() for d in dev_list if isinstance(d, str) and d.strip()]
    OUTPUT_FILE.write_text("\n".join(sorted(set(cleaned))), encoding="utf-8")
    print(f"✅ Extracted {len(cleaned)} developers to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()