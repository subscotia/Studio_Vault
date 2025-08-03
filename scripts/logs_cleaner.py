import os
import time

# 🔧 Config
log_folder = 'logs'
retention_days = 7  # Delete logs older than this
allowed_exts = ['.json', '.csv', '.log']  # Extend if needed

now = time.time()
deleted = 0

if os.path.exists(log_folder):
    for fname in os.listdir(log_folder):
        path = os.path.join(log_folder, fname)
        if os.path.isfile(path) and any(fname.endswith(ext) for ext in allowed_exts):
            if os.stat(path).st_mtime < now - retention_days * 86400:
                os.remove(path)
                deleted += 1

print(f"🧹 Removed {deleted} log file(s) older than {retention_days} day(s) from '{log_folder}'")
else:
    print(f"📂 No '/logs' folder found—nothing to clean.")