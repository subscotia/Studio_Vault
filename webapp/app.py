import os
import json
import time
import re  # Import the regular expression module
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from utils import save_vault_with_backup, VAULT_FILE_PATH

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

# --- Path Configuration ---
DATA_DIR = os.path.dirname(VAULT_FILE_PATH)


@app.route('/')
def index():
    """
    Serves the main index.html page and injects the vault data directly.
    """
    try:
        with open(VAULT_FILE_PATH, 'r', encoding='utf-8') as f:
            vault_data = json.load(f)
    except Exception as e:
        print(f"Error reading vault data: {e}")
        vault_data = []

    cache_buster = int(time.time())
    return render_template('index.html', vault_data=vault_data, cache_buster=cache_buster)


def generate_new_id(new_plugin_type, new_plugin_developer, existing_data):
    """
    Generates a new, globally unique ID based on the VAULT_GUIDE.md convention.
    """
    type_code_map = {
        "instrument": "I", "fx": "X", "utility": "U",
        "container": "C", "expansion": "E"
    }
    type_code = type_code_map.get(new_plugin_type, "X")

    # Bug Fix: Sanitize the developer name to remove non-alphabetic characters
    # before creating the two-letter code.
    sanitized_dev = ""
    if new_plugin_developer:
        sanitized_dev = re.sub(r'[^A-Z]', '', new_plugin_developer.upper())

    dev_code = (sanitized_dev + "XX")[:2]  # Pad with XX and take the first two letters

    max_seq = 0
    for plugin in existing_data:
        if "id" in plugin and plugin["id"]:
            try:
                seq_num = int(plugin["id"][3:])
                if seq_num > max_seq:
                    max_seq = seq_num
            except (ValueError, IndexError):
                continue

    new_seq = max_seq + 1
    return f"{type_code}{dev_code}{new_seq:05d}"


@app.route('/api/plugin', methods=['POST'])
def add_plugin():
    """
    API endpoint to receive new plugin data, generate an ID, and save it.
    """
    try:
        new_plugin = request.get_json()

        try:
            with open(VAULT_FILE_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        new_id = generate_new_id(
            new_plugin.get("type"),
            new_plugin.get("developer"),
            existing_data
        )
        new_plugin['id'] = new_id

        existing_data.append(new_plugin)

        save_successful = save_vault_with_backup(existing_data)

        if save_successful:
            return jsonify({
                'status': 'success',
                'message': 'Plugin added successfully.',
                'new_plugin': new_plugin
            }), 201
        else:
            raise IOError("Failed to save the vault file.")

    except Exception as e:
        print(f"Error in add_plugin: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
