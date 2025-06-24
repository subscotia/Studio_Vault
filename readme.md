# Vault Toolkit

A growing collection of focused Python utilities for cleaning, inspecting, and maintaining a large JSON-based audio production and engineering vault (e.g. sample libraries, plugins, virtual instruments). Each script is modular, editable, and designed for rapid data triage with minimal overhead.

Current features include:

- 🔍 `dupe_checker.py`: Find exact duplicates based on configurable fields
- 🧠 `fuzzy_dupe_finder.py`: Surface near-duplicate entries using fuzzy matching
- 🧹 `dupe_remover.py`: Remove duplicate entries while retaining the first match
- 📝 Logging: Clean logs exported to `/logs/` in either `.json` or `.csv` format
- 🎯 Type scoping: Easily target subsets (e.g. only `"Instrument"` entries)
- 🎨 CLI-friendly output with emoji-enhanced summaries
> 💡 This repo includes a `.gitignore` to keep things clean—vault files, log exports, and intermediate data are excluded, so the focus stays on the tools, not the noise.

This project reflects a real-world cleanup effort and is evolving script by script, with each tool representing a specific functional need in managing sample metadata.

💡 Designed for clarity, efficiency, and step-by-step learning.

## Usage

Each script is standalone and focused. To run them, make sure you have Python 3 installed.

Example: checking for duplicate instruments based on developer + name:

```bash
python dupe_checker_argparse.py --input vault_instruments_wip.json --type Instrument --fields developer,name --csv logs/dupes_found.csv

## Contributing

Contributions, ideas, and improvements are welcome! Whether it's a bug fix, feature request, or script enhancement, feel free to fork this repo and open a pull request.

If you're using these tools on your own JSON vaults and come up with better matching strategies or workflows—I'd love to hear from you.



