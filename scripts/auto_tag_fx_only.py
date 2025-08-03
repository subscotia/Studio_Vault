import json
import re
from pathlib import Path

# Load your full Vault
vault = json.loads(Path("vault_working.json").read_text(encoding="utf-8"))

# Define FX tag rules (regex → tag)
FX_TAG_RULES = {
    r"\bEQ\b|\bEqualizer\b": "eq",
    r"\bCompressor\b": "compressor",
    r"\bLimiter\b": "limiter",
    r"\bSaturat": "saturation",
    r"\bDistort": "distortion",
    r"\bReverb\b|\bVerb\b": "reverb",
    r"\bDelay\b": "delay",
    r"\bChorus\b|\bFlanger\b|\bPhaser\b|\bModulat": "modulation",
    r"\bPitch\b|\bTune\b|\bHarmon": "pitch",
    r"\bTransient\b": "transient",
    r"\bFilter\b|\bLPF\b|\bHPF\b": "filter",
    r"\bMulti[-\s]?FX\b|\bRack\b": "multi-fx",
    r"\bMeter\b|\bAnalyzer\b": "metering",
    r"\bGain\b|\bPan\b|\bUtility\b": "utility",
    r"\bSpatial\b|\b3D\b|\bPanner\b": "spatial",
    r"\bMaster\b": "mastering",
    r"\bAmp Sim\b|\bAmp\b(?=.*Sim)": "amp sim",
    r"\bCab\b|\bCabinet\b|\bIR\b": "amp cab sim",
    r"\bScaler\b|\bRiff\b|\bCreative\b|\bChord\b": "creative",
}

tagged = []

for entry in vault:
    if entry.get("type", "").lower() != "effect":
        tagged.append(entry)
        continue

    name = entry["name"]
    tags = set(entry.get("tags", []))
    tags.add("fx")  # Ensure FX tag is present

    for pattern, tag in FX_TAG_RULES.items():
        if re.search(pattern, name, re.IGNORECASE):
            tags.add(tag)

    entry["tags"] = sorted(tags)
    tagged.append(entry)

# Write out the FX-tagged Vault
Path("vault_fx_tagged.json").write_text(
    json.dumps(tagged, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("✔ FX tagging complete → vault_fx_tagged.json")
print(f"File written to: {Path('vault_fx_tagged.json').absolute()}")