import json
import os
import sys

VAULT_PATH = "waves.json"  # Change if needed

def validate_json(path):
    print(f"🔍 Checking {path} for JSON syntax issues...")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("✅ JSON parsed successfully!")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e.msg} (Line {e.lineno}, Column {e.colno})")
        return None
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return None

def check_structure(data):
    print("🧠 Running structure checks...")
    if not isinstance(data, list):
        print("⚠️ Expected top-level structure: list of plugin entries.")
        return
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            print(f"⚠️ Entry {i} is not a dict.")
            continue
        required_keys = ["name", "tags"]
        for key in required_keys:
            if key not in entry:
                print(f"⚠️ Entry {i} missing key: '{key}'")
        if "tags" in entry and not isinstance(entry["tags"], list):
            print(f"⚠️ Entry {i} has non-list 'tags': {entry['tags']}")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else VAULT_PATH
    if not os.path.isfile(path):
        print(f"❌ Vault file does not exist: {path}")
        return
    data = validate_json(path)
    if data:
        check_structure(data)

if __name__ == "__main__":
    main()