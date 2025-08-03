#!/usr/bin/env python3
import json
from pathlib import Path

# ────────────────────────────────────────────────
# CONFIGURATION: update these two lines as needed
INPUT  = "vault_instr_wip.json"
OUTPUT = "virtual_instruments_lc_type.json"
# ────────────────────────────────────────────────

def enforce_lowercase_type(input_path: str, output_path: str):
    """
    Reads a JSON array from input_path, lower-cases each entry's "type" field,
    and writes the result to output_path.
    """
    p_in = Path(input_path)
    data = json.loads(p_in.read_text(encoding="utf-8"))

    if isinstance(data, list):
        for obj in data:
            t = obj.get("type")
            if isinstance(t, str):
                obj["type"] = t.strip().lower()
    else:
        # if your JSON is a single object, not a list
        t = data.get("type")
        if isinstance(t, str):
            data["type"] = t.strip().lower()

    p_out = Path(output_path)
    p_out.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"✔ Lower-cased 'type' field written to: {output_path}")

if __name__ == "__main__":
    enforce_lowercase_type(INPUT, OUTPUT)