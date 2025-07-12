import os
import shutil
from datetime import datetime

# Name of the file you're versioning
input_filename = "vault_working.json"

# Where to put backups
backup_dir = "../Vault_Backups"
os.makedirs(backup_dir, exist_ok=True)

# Create timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
versioned_name = f"vault_{timestamp}.json"
dest_path = os.path.join(backup_dir, versioned_name)

# Copy the working file into backups
shutil.copyfile(input_filename, dest_path)

print(f"✔ Backup created: {dest_path}")