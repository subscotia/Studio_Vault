#!/usr/bin/env python3
"""
fx_function_vocab.py

A configurable, centralized list of allowed FX functions.
Used to validate or auto-suggest tags for FX-type vault entries.
"""

# ─── Configure Your Controlled Vocabulary Here ──────────────
# Use lowercase strings only; match Reaper categories if needed

FX_FUNCTIONS = [
    "reverb",
    "delay",
    "distortion",
    "modulation",      # chorus / flanger / phaser / tremolo
    "eq",              # equalizers, filters
    "compressor",
    "limiter",
    "gate",            # noise gate / transient designer
    "pitch",           # pitch shift, octave, harmonizer
    "spatial",         # stereo tools / MS / imaging
    "resonator",       # combs, physical models
    "saturator",
    "multi-fx",        # bundles, processors with many types
    "utility",         # gain / routing / dry-wet / phase invert
    "analyzer",        # spectral, metering, visualization
    "exciter",
    "bitcrusher",
    "transient",
    "de-esser",
    "tape",
    "amp sim",
    "cab sim",
    "vocoder",
    "formant"
]
# ─────────────────────────────────────────────────────────────

# This script isn’t meant to be run directly—it’s imported by others
# For testing or previewing, you can uncomment below:

if __name__ == "__main__":
    print("🎛️  FX Function Vocabulary")
    print(f"Total categories: {len(FX_FUNCTIONS)}\n")
    for fn in FX_FUNCTIONS:
        print(f" • {fn}")