#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Name:        pysills_main.py
# Author:      Maximilian A. Beeskow
# Version:     v1.0.0 (GUI prototype)
# Date:        30.03.2026
# ----------------------------------------------------------------------------------------------------------------------

# MODULES
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class PySILLSApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PySILLS")
        self.root.geometry("900x600")

        # --- Main container ---
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        # Layout konfigurieren
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        # UI initialisieren
        self.create_widgets()

    # ------------------------------------------------------------------------------------------------------------------

    def create_widgets(self):

        # --- Left Panel (Project / Files) ---
        self.left_frame = ttk.LabelFrame(self.main_frame, text="Project Files", padding=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Listbox (z.B. für Messfiles)
        self.file_list = tk.Listbox(self.left_frame, height=20)
        self.file_list.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 6):
            self.file_list.insert(tk.END, f"Sample_File_{i}.csv")

        # Buttons
        self.btn_frame = ttk.Frame(self.left_frame)
        self.btn_frame.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame, text="Add").pack(side="left", padx=2)
        ttk.Button(self.btn_frame, text="Remove").pack(side="left", padx=2)

        # --- Right Panel (Controls / Settings) ---
        self.right_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Beispiel Widgets
        ttk.Label(self.right_frame, text="Parameter A:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_a = ttk.Entry(self.right_frame)
        self.entry_a.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(self.right_frame, text="Option:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo = ttk.Combobox(self.right_frame, values=["Option 1", "Option 2", "Option 3"])
        self.combo.grid(row=1, column=1, sticky="ew", pady=5)

        self.check_var = tk.BooleanVar()
        ttk.Checkbutton(self.right_frame, text="Enable Feature", variable=self.check_var)\
            .grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Button(self.right_frame, text="Run").grid(row=3, column=0, columnspan=2, pady=10)

        # Grid Verhalten
        self.right_frame.columnconfigure(1, weight=1)


# ----------------------------------------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------------------------------------

def main():
    root = ThemedTk(theme="clearlooks")  # später: "equilux", "black", "radiance"
    app = PySILLSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()