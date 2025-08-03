from pathlib import Path

src = Path("vault_with_expansions.json")
dst = Path("vault_working.json")

# Backup the current vault first
if dst.exists():
    dst.rename("vault_working_backup.json")

# Promote the new combined vault
src.rename(dst)
print(f"✔ Promoted {dst.name}; backup: vault_working_backup.json")