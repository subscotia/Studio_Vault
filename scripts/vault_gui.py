#!/usr/bin/env python3
"""
vault_gui.py

A simple Tkinter GUI to:
  • Select your master vault JSON
  • Select a new-tools JSON
  • Select the ID'd-tools JSON
  • Assign IDs to new tools
  • Merge into the master vault
  • Backup the master vault
  • Rebuild the HTML catalog

Requires:
  - Python 3.x
  - Your helper scripts in the same folder:
      generate_catalog_ids.py
      manage_untagged.py
      backup_vault.py
      build_html_catalog.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
from pathlib import Path

class VaultManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Subscotia Vault Manager")
        self.geometry("620x580")
        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # 1) Master vault selector
        tk.Label(frame, text="Master vault JSON:").grid(row=0, column=0, sticky="w")
        self.master_entry = tk.Entry(frame)
        self.master_entry.grid(row=0, column=1, sticky="we", padx=5)
        self.master_entry.insert(0, "vault_instr_master.json")
        tk.Button(frame, text="Browse…", command=self._pick_master) \
          .grid(row=0, column=2, padx=(5,0))

        tk.Label(frame,
                 text="(This file is your MASTER vault – change its name as needed)",
                 fg="gray", font=("Arial", 8)) \
          .grid(row=1, column=1, sticky="w", pady=(2,10))

        # 2) New tools selector
        tk.Label(frame, text="New tools JSON:").grid(row=2, column=0, sticky="w")
        self.new_entry = tk.Entry(frame)
        self.new_entry.grid(row=2, column=1, sticky="we", padx=5)
        tk.Button(frame, text="Browse…", command=self._pick_new) \
          .grid(row=2, column=2, padx=(5,0))

        # 3) ID'd tools selector
        tk.Label(frame, text="ID'd tools JSON:").grid(row=3, column=0, sticky="w")
        self.new_ids_entry = tk.Entry(frame)
        self.new_ids_entry.grid(row=3, column=1, sticky="we", padx=5)
        tk.Button(frame, text="Browse…", command=self._pick_new_ids) \
          .grid(row=3, column=2, padx=(5,0))

        # 4) Action buttons
        btn_frame = tk.Frame(frame, pady=10)
        btn_frame.grid(row=4, column=0, columnspan=3)
        tk.Button(btn_frame, text="1) Assign IDs",   width=15,
                  command=self.assign_ids).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="2) Merge Tools",  width=15,
                  command=self.merge_tools).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="3) Backup Vault", width=15,
                  command=self.backup_vault).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="4) Rebuild HTML", width=15,
                  command=self.rebuild_html).grid(row=0, column=3, padx=5)

        # 5) Log output
        tk.Label(frame, text="Log:").grid(row=5, column=0, sticky="nw", pady=(10,0))
        self.log = scrolledtext.ScrolledText(frame, height=15, state="disabled")
        self.log.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=5)

        # allow resizing
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(6, weight=1)

    def _pick_master(self):
        path = filedialog.askopenfilename(
            title="Select master vault JSON",
            filetypes=[("JSON files","*.json"),("All files","*.*")]
        )
        if path:
            self.master_entry.delete(0, tk.END)
            self.master_entry.insert(0, path)

    def _pick_new(self):
        path = filedialog.askopenfilename(
            title="Select new-tools JSON",
            filetypes=[("JSON files","*.json"),("All files","*.*")]
        )
        if path:
            self.new_entry.delete(0, tk.END)
            self.new_entry.insert(0, path)

    def _pick_new_ids(self):
        path = filedialog.askopenfilename(
            title="Select ID'd-tools JSON",
            filetypes=[("JSON files","*.json"),("All files","*.*")]
        )
        if path:
            self.new_ids_entry.delete(0, tk.END)
            self.new_ids_entry.insert(0, path)

    def _run_script(self, script, args):
        cmd = ["python", script] + args
        self._log(f"▶ Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stdout.strip():
                self._log(result.stdout.strip())
            if result.stderr.strip():
                self._log("⚠ stderr:\n" + result.stderr.strip())
        except subprocess.CalledProcessError as e:
            self._log(f"❌ Error running {script}:\n{e.stdout}\n{e.stderr}")
            messagebox.showerror("Script Error", f"Failed to run {script}")
            return False
        return True

    def assign_ids(self):
        master = self.master_entry.get().strip()
        newf   = self.new_entry.get().strip()
        if not master or not newf:
            messagebox.showwarning("Missing files", "Select both vault and new-tools JSON first.")
            return
        out = Path(newf).with_name("new_tools_with_ids.json")
        if self._run_script("generate_catalog_ids.py", [ newf, str(out) ]):
            self._log(f"✔ IDs assigned → {out.name}")
            # auto-populate the ID'd field
            self.new_ids_entry.delete(0, tk.END)
            self.new_ids_entry.insert(0, str(out))

    def merge_tools(self):
        master   = self.master_entry.get().strip()
        new_ids  = self.new_ids_entry.get().strip()
        if not master or not new_ids:
            messagebox.showwarning("Missing files", "Select both vault and ID'd-tools JSON first.")
            return
        merged = Path(master).with_name("vault_merged.json")
        if self._run_script("manage_untagged.py",
                            ["merge", master, new_ids, str(merged)]):
            self._log(f"✔ Merged vault → {merged.name}")

    def backup_vault(self):
        master = self.master_entry.get().strip()
        if not master:
            messagebox.showwarning("Missing file", "Select your master vault JSON first.")
            return
        if self._run_script("backup_vault.py", [ master ]):
            self._log("✔ Backup complete.")

    def rebuild_html(self):
        if self._run_script("publish_html_catalog.py", []):
            self._log("✔ HTML regenerated: subscotia_vault.html")

    def _log(self, txt):
        self.log.configure(state="normal")
        self.log.insert(tk.END, txt + "\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")


if __name__ == "__main__":
    app = VaultManagerApp()
    app.mainloop()