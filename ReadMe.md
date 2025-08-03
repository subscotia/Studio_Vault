Subscotia Sound Vault Project
Project Lead: Drew Campbell (Subscotia Sound)
Production Assistant: Google Gemini 2.5 Pro (AI)

1. Project Overview
The Subscotia Sound Vault is a comprehensive, custom-built database designed to catalog every audio plugin, virtual instrument, and utility owned by the studio. The project's primary goal is to create a powerful, searchable, and efficient system for managing the studio's extensive digital toolbox, streamlining the creative workflow during composition, mixing, and mastering.

2. End Goals
The project is divided into two main development phases:

Local Web Application: A fast, modern, and interactive single-page web application. It will run on a dedicated local server within the studio network, providing a powerful interface for searching, filtering, and exploring the plugin vault.

Native Windows Application: A bespoke desktop application with deep integration into the studio's primary DAW, Cockos Reaper. The long-term vision for this app includes features like the ability to directly insert a selected plugin onto a track in Reaper.

3. Current Status
The project is currently in the Backend Data Population & Cleaning phase. The primary focus is on building out two master JSON files (ivault.json for instruments, xvault.json for effects/utilities) with complete and accurate metadata for every tool.

4. Repository Structure
The project is organized within this Git repository with the following structure:

/vault
│
├── backups/              # Contains timestamped backups of vault files
├── logs/                 # For future logging output
├── ref/                  # Reference documents (e.g., families.txt, VAULT_GUIDE.md)
│
├── ivault.json           # (Example name) Master JSON for instruments
├── xvault.json           # (Example name) Master JSON for effects/utilities
│
├── vault_utils.py        # Shared module for common, reusable Python functions
├── *.py                  # Various Python scripts for data management
│
└── README.md             # This file

5. Workflow & Tooling
Version Control: The project is managed using Git, with this repository as the central source of truth.

Development Environment: Primary development is done in Python 3 using the PyCharm Professional IDE.

Data Management: A suite of custom Python scripts is used to perform data cleaning, enrichment, and management tasks on the core JSON files. These scripts are designed to be modular, configurable, and safe, utilizing a shared vault_utils.py module for common operations like creating timestamped backups.

Documentation:

VAULT_GUIDE.md: A living document in the /ref directory that outlines the core principles, data schemas, and conventions for the vault to ensure consistency.

Commit Messages: Daily work is summarized in clear journal-style commit messages.

6. Key Data Conventions
The vault is built on a set of clearly defined principles to ensure data integrity and searchability. Key conventions include:

ID Schema: A unique ID is assigned to each entry (Type-Developer-Sequence, e.g., INOR00025).

Product vs. Plugin: Each JSON entry represents a single plugin, not a product bundle.

Modular Families: The families field uses modular, single-purpose tags (e.g., ["compressors", "opto"]) rather than hyper-specific ones.

Primary type: Each entry has a primary type of "instrument", "container", "fx", "utility" or "expansion.

For a complete list of all conventions, please refer to the VAULT_GUIDE.md file.
