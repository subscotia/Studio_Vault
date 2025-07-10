#!/usr/bin/env python3
"""
page_monitor.py

🎯 PURPOSE:
Monitors a list of webpages for content changes. If a change is detected,
it fetches the new content, converts it to Markdown, and saves it to a
specified local file.

🛡️ SAFE:
- Uses a hash (a digital fingerprint) to detect changes, which is highly reliable.
- Only overwrites local files when a change has actually occurred.
- Handles plain text files and HTML pages differently and safely.
- Stores the state (the last known hashes) in a separate `snapshots.json` file.

🔧 TWEAKABLE CONFIGURATION:
- The list of pages to monitor is in the `PAGES_TO_MONITOR` block. You can
  easily add, remove, or edit targets here.
"""

import requests
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

# --- CONFIGURATION (Tweak these values) ---

# This is the main configuration list. Add or remove dictionaries as needed.
PAGES_TO_MONITOR = [
    {
        "name": "Airwindopedia",
        "url": "https://www.airwindows.com/wp-content/uploads/Airwindopedia.txt",
        "local_file": Path("F:/Studio/Admin Ops/Operations/git/vault/ref/Airwindopedia.md"),
        "content_selector": None  # No selector needed for a plain .txt file
    },
    {
        "name": "Acqua Plugin Guide",
        "url": "https://justpaste.it/AcquaPluginGuide",
        "local_file": Path("F:/Studio/Admin Ops/Operations/git/vault/ref/Acustica Audio Acqua Plugins Guide .md"),
        "content_selector": "#articleContent"  # Grabs the main body of the article
    },
    {
        "name": "Acqua Recommendations",
        "url": "https://justpaste.it/AcquaRecommendations",
        "local_file": Path("F:/Studio/Admin Ops/Operations/git/vault/ref/Acustica Audio Acqua Recommendations.md"),
        "content_selector": "#articleContent"
    },
    {
        "name": "Acqua Master List",
        "url": "https://justpaste.it/AcusticaAudioAcquaMasterList",
        "local_file": Path(
            "F:/Studio/Admin Ops/Operations/git/vault/ref/Unofficial Acustica Audio Acqua Master Plugins List.md"),
        "content_selector": "#articleContent"
    }
]

# The file where we store the last known hashes of the pages.
SNAPSHOT_FILE = Path("page_snapshots.json")


# ---------------------------------------------------------

def get_snapshots():
    """Loads the last known hashes from the snapshot file."""
    if not SNAPSHOT_FILE.exists():
        return {}
    return json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))


def save_snapshots(snapshots):
    """Saves the updated hashes to the snapshot file."""
    SNAPSHOT_FILE.write_text(json.dumps(snapshots, indent=2), encoding="utf-8")


def get_content_hash(content: str) -> str:
    """Calculates the SHA-256 hash of the content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def main():
    """Main function to run the monitor."""
    print("Starting webpage monitor...")
    snapshots = get_snapshots()
    changes_found = False

    for page in PAGES_TO_MONITOR:
        name = page["name"]
        url = page["url"]
        local_file = page["local_file"]
        selector = page["content_selector"]

        print(f"\nChecking '{name}'...")

        try:
            # highlight-start
            # Add a User-Agent header to mimic a standard browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers)
            # highlight-end
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        except requests.RequestException as e:
            print(f"  ❌ Error fetching page: {e}")
            continue

        raw_content = response.text
        content_to_check = ""

        if selector:  # This is an HTML page
            soup = BeautifulSoup(raw_content, 'html.parser')
            content_element = soup.select_one(selector)
            if content_element:
                content_to_check = str(content_element)
            else:
                print(f"  ⚠️ Warning: Could not find content with selector '{selector}'. Skipping.")
                continue
        else:  # This is a plain text file
            content_to_check = raw_content

        # Calculate the hash of the new content
        new_hash = get_content_hash(content_to_check)
        last_hash = snapshots.get(url)

        if new_hash == last_hash:
            print("  ✅ No changes detected.")
        else:
            print(f"  🚨 Change detected! Updating local file...")
            changes_found = True

            # Convert to Markdown
            if selector:  # It was HTML
                h = html2text.HTML2Text()
                h.body_width = 0  # Don't wrap lines
                markdown_content = h.handle(content_to_check)
            else:  # It was plain text
                markdown_content = content_to_check

            # Save the new content to the local file
            try:
                # Ensure the directory exists
                local_file.parent.mkdir(parents=True, exist_ok=True)
                local_file.write_text(markdown_content, encoding="utf-8")
                print(f"  -> Successfully updated '{local_file.name}'")
                # Update the snapshot with the new hash
                snapshots[url] = new_hash
            except IOError as e:
                print(f"  ❌ Error writing to file: {e}")

    if changes_found:
        save_snapshots(snapshots)
        print("\nAll changes processed and snapshots updated.")
    else:
        print("\nMonitoring complete. No changes found on any page.")


if __name__ == "__main__":
    main()
