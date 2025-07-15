# Subscotia Vault: Development Guide & Best Practices

**Document Version:** 1.0
**Date:** 13 July 2025

---

### 1. Core Philosophy

This document outlines the official structure and best practices for the Subscotia Vault project. Adherence to these standards is mandatory to ensure the project remains clear, maintainable, and scalable. Our core philosophy is to treat this project with the same rigor as a professional software development endeavor.

---

### 2. Project Directory Structure

To ensure a clean separation of concerns, the project will adhere to the following directory structure. All files and new directories must be placed in their logically correct location.

```
/vault
│
├── .venv/                # Python virtual environment (managed by IDE)
├── backups/              # Automated, timestamped backups of data files
├── ref/                  # Generated reference lists (e.g., families.txt)
│
├── data/                 # Core data files. The "database" of the project.
│   ├── ivault_master.json
│   └── xvault_master.json
│
├── scripts/              # All Python scripts for data management and analysis.
│   ├── vault_utils.py    # The shared utility module.
│   └── ... (all other .py scripts)
│
├── webapp/               # Future home for the Flask web application.
│   └── ...
│
├── archive/              # Old, deprecated, or single-use scripts.
│
└── README.md             # High-level project overview.
└── DEVELOPMENT_GUIDE.md  # This file.
└── VAULT_GUIDE.md        # Data schema and classification rules.
```

---

### 3. Version Control (Git) Best Practices

* **Branching Strategy:**
    * The `main` branch must always represent a stable, completed state of the project.
    * All new features or significant changes (e.g., building the web app, a major data refactoring) **must** be developed on a separate **feature branch**.
    * Branch names should be descriptive (e.g., `feature/webapp`, `fix/id-cleanup`).
    * Work is only merged back into `main` when the feature is complete and tested.

* **Commit Messages:**
    * Commits should be frequent and logical, representing a single unit of work.
    * Commit messages will follow the "journal entry" format we have established, providing a clear summary of the work done in that commit.

* **Workflow:**
    * All Git operations (commit, push, pull, branch) should be performed from within the PyCharm IDE to maintain an efficient, integrated workflow.

---

### 4. Python Scripting Best Practices

All scripts created for this project must adhere to the following standards.

* **Modularity & Reusability:**
    * Commonly used, repeatable logic (e.g., saving files with backups) **must** be placed in the shared `scripts/vault_utils.py` module.
    * Scripts should be designed to be as generic and reusable as possible. A single `merge_list_values.py` is preferable to separate scripts for merging families and tags.

* **Configuration:**
    * All user-configurable parameters (e.g., file paths, values to search for) **must** be placed in a clearly marked `--- CONFIGURATION ---` block at the top of the script.

* **Safety & Idempotency:**
    * Scripts that modify data **must** use the `save_vault_with_backup` function from `vault_utils.py`.
    * Scripts should be **idempotent**, meaning they can be run multiple times without causing errors or creating duplicate data. They should check if a value already exists before adding it.

* **Documentation (Docstrings):**
    * Every script **must** begin with a multi-line docstring that clearly explains its function using the following format:
        * `🎯 PURPOSE:` A one-sentence summary of what the script does.
        * `🛡️ SAFE:` A description of its safety features.
        * `🔧 TWEAKABLE CONFIGURATION:` A note that parameters can be edited.

* **Terminology:**
    * We will use standard industry terminology. In the context of JSON, we will refer to **keys** and **values**. The process of improving existing code is called **refactoring**.

---

### 5. Data Management Best Practices

* The master JSON files in the `/data` directory are to be treated as the definitive database.
* **Manual editing of the master JSON files is strictly discouraged.** All modifications should be performed via the version-controlled Python scripts in the `/scripts` directory to ensure changes are safe, repeatable, and documented.
