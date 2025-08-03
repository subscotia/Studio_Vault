import shutil

source = 'vault_instruments.json'
destination = 'vault_instruments_wip.json'

shutil.copyfile(source, destination)
print(f"✅ Copied {source} → {destination}")