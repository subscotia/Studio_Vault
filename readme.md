# Vault Toolkit

A growing collection of focused Python utilities for cleaning, inspecting, and maintaining a large JSON-based audio production and engineering vault (e.g. sample libraries, plugins, virtual instruments). Each script is modular, editable, and designed for rapid data triage with minimal overhead.

Current features include:

- 🔍 `dupe_checker.py`: Find exact duplicates based on configurable fields
- 🧠 `fuzzy_dupe_finder.py`: Surface near-duplicate entries using fuzzy matching
- 🧹 `dupe_remover.py`: Remove duplicate entries while retaining the first match
- 📝 Logging: Clean logs exported to `/logs/` in either `.json` or `.csv` format
- 🎯 Type scoping: Easily target subsets (e.g. only `"Instrument"` entries)
- 🎨 CLI-friendly output with emoji-enhanced summaries

This project reflects a real-world cleanup effort and is evolving script by script, with each tool representing a specific functional need in managing sample metadata.

💡 Designed for clarity, efficiency, and step-by-step learning.