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

    # Sanitize the developer name to remove non-alphabetic characters
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

@app.route('/api/plugin/<string:plugin_id>', methods=['DELETE'])
def delete_plugin(plugin_id):
    """
    API endpoint to delete a plugin by its ID.
    """
    try:
        # Load the existing vault data
        try:
            with open(VAULT_FILE_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({'status': 'error', 'message': 'Vault file not found or is empty.'}), 404

        # Find the plugin and create a new list without it
        original_count = len(existing_data)
        # This is a safe way to remove the item: build a new list of all items that *don't* match the ID
        updated_data = [p for p in existing_data if p.get('id') != plugin_id]

        # Check if a plugin was actually removed
        if len(updated_data) == original_count:
            return jsonify({'status': 'error', 'message': 'Plugin not found.'}), 404

        # Save the updated data back to the file
        save_successful = save_vault_with_backup(updated_data)

        if save_successful:
            return jsonify({
                'status': 'success',
                'message': 'Plugin deleted successfully.'
            }), 200
        else:
            raise IOError("Failed to save the vault file after deletion.")

    except Exception as e:
        print(f"Error in delete_plugin: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/plugin/<string:plugin_id>', methods=['PUT'])
def update_plugin(plugin_id):
    """
    API endpoint to update an existing plugin by its ID.
    """
    try:
        updated_plugin = request.get_json()

        # Load the existing vault data
        try:
            with open(VAULT_FILE_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({'status': 'error', 'message': 'Vault file not found or is empty.'}), 404

        # Find the plugin and update it
        plugin_found = False
        for i, plugin in enumerate(existing_data):
            if plugin.get('id') == plugin_id:
                # Preserve the original ID
                updated_plugin['id'] = plugin_id
                existing_data[i] = updated_plugin
                plugin_found = True
                break

        if not plugin_found:
            return jsonify({'status': 'error', 'message': 'Plugin not found.'}), 404

        # Save the updated data back to the file
        save_successful = save_vault_with_backup(existing_data)

        if save_successful:
            return jsonify({
                'status': 'success',
                'message': 'Plugin updated successfully.',
                'updated_plugin': updated_plugin
            }), 200
        else:
            raise IOError("Failed to save the vault file after update.")

    except Exception as e:
        print(f"Error in update_plugin: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
