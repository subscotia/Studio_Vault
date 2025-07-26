import os
import json
import time
from flask import Flask, jsonify, render_template
from flask_cors import CORS

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

# --- Path Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
VAULT_FILE = os.path.join(DATA_DIR, 'vault_master.json')


@app.route('/')
def index():
    """
    Serves the main index.html page and injects the vault data directly.
    """
    try:
        with open(VAULT_FILE, 'r', encoding='utf-8') as f:
            vault_data = json.load(f)
    except Exception as e:
        print(f"Error reading vault data: {e}")
        vault_data = [] # Send an empty list on error

    cache_buster = int(time.time())
    # Pass both the vault_data and cache_buster to the template
    return render_template('index.html', vault_data=vault_data, cache_buster=cache_buster)


@app.route('/api/vault')
def get_vault_data():
    """
    API endpoint to read and return the entire contents of the vault master JSON file.
    This remains for potential future use or direct testing.
    """
    try:
        with open(VAULT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "The vault_master.json file was not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
