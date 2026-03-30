#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Name:        pysills_main.py
# Author:      Maximilian A. Beeskow
# Version:     v1.0.0 (GUI prototype)
# Date:        31.03.2026
# ----------------------------------------------------------------------------------------------------------------------

# MODULES
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class PySILLSApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PySILLS")
        self.root.geometry("1250x750")

        # --- Main container ---
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        # Layout konfigurieren
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.columnconfigure(2, weight=3)
        self.main_frame.columnconfigure(3, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=3)
        self.main_frame.rowconfigure(2, weight=1)

        # UI initialisieren
        self.create_widgets()

    # ------------------------------------------------------------------------------------------------------------------

    def create_widgets(self):

        # 1st panel (PySILLS)
        self.frame_main = ttk.LabelFrame(self.main_frame, text="PySILLS", padding=10)
        self.frame_main.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))

        # Buttons
        self.btn_frame_main = ttk.Frame(self.frame_main)
        self.btn_frame_main.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_main, text="New project").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="Open project").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="Save project").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="Close project").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="Settings").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="Documentation").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="About").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_main, text="Quit").pack(fill="x", pady=2)

        # 2nd panel (Project setup)
        self.frame_project = ttk.LabelFrame(self.main_frame, text="Project settings", padding=10)
        self.frame_project.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))

        # Radiobuttons
        self.radio_var = tk.StringVar(value="option1")

        ttk.Radiobutton(self.frame_project,
                        text="Mineral analysis",
                        variable=self.radio_var,
                        value="option1").pack(fill="x", pady=2)
        ttk.Radiobutton(self.frame_project,
                        text="Fluid inclusion analysis",
                        variable=self.radio_var,
                        value="option2").pack(fill="x", pady=2)
        ttk.Radiobutton(self.frame_project,
                        text="Melt inclusion analysis",
                        variable=self.radio_var,
                        value="option3").pack(fill="x", pady=2)

        # Buttons
        self.btn_frame_project = ttk.Frame(self.frame_project)
        self.btn_frame_project.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_project, text="Setup").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_project, text="Results").pack(fill="x", pady=2)

        # 3rd panel (Standard files)
        self.frame_standard = ttk.LabelFrame(self.main_frame, text="Standard reference material (SRM)", padding=10)
        self.frame_standard.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))

        # Buttons
        self.btn_frame_standard = ttk.Frame(self.frame_standard)
        self.btn_frame_standard.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_standard, text="Add file").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_standard, text="Copy file").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_standard, text="Remove file").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_standard, text="View file data").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_standard, text="Interval setup").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_standard, text="Spike elimination").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_standard, text="View file results").pack(fill="x", pady=2)

        # Listbox (z.B. für Messfiles)
        self.frame_listbox_standard = ttk.LabelFrame(self.main_frame, text="Standard files", padding=10)
        self.frame_listbox_standard.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.file_list_standard = tk.Listbox(self.frame_listbox_standard, height=20)
        self.file_list_standard.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 6):
            self.file_list_standard.insert(tk.END, f"Standard_File_{i}.csv")

        # 4th panel (Sample files)
        self.frame_sample = ttk.LabelFrame(self.main_frame, text="Sample files", padding=10)
        self.frame_sample.grid(row=0, column=2, sticky="nsew", padx=(0, 10), pady=(0, 10))

        # Buttons
        self.btn_frame_sample = ttk.Frame(self.frame_sample)
        self.btn_frame_sample.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_sample, text="Add file").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_sample, text="Copy file").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_sample, text="Remove file").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_sample, text="View file data").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_sample, text="Interval setup").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_sample, text="Spike elimination").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_sample, text="View file results").pack(fill="x", pady=2)

        # Listbox (z.B. für Messfiles)
        self.frame_listbox_sample = ttk.LabelFrame(self.main_frame, text="Sample files", padding=10)
        self.frame_listbox_sample.grid(row=1, column=2, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.file_list_sample = tk.Listbox(self.frame_listbox_sample, height=20)
        self.file_list_sample.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 13):
            self.file_list_sample.insert(tk.END, f"Sample_File_{i}.csv")

        # 5th panel (Isotopes)
        self.frame_isotopes = ttk.LabelFrame(self.main_frame, text="Isotopes", padding=10)
        self.frame_isotopes.grid(row=0, column=3, sticky="nsew", padx=(0, 10), pady=(0, 10))

        # Buttons
        self.btn_frame_isotopes = ttk.Frame(self.frame_isotopes)
        self.btn_frame_isotopes.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_isotopes, text="Assign SRM").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_isotopes, text="View SRM values").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_isotopes, text="View isotope results").pack(fill="x", pady=2)

        # Listbox (z.B. für Messfiles)
        self.frame_listbox_isotopes = ttk.LabelFrame(self.main_frame, text="Sample files", padding=10)
        self.frame_listbox_isotopes.grid(row=1, column=3, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.list_isotopes = tk.Listbox(self.frame_listbox_isotopes, height=20)
        self.list_isotopes.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 43):
            self.list_isotopes.insert(tk.END, f"Isotope_{i}")


# ----------------------------------------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------------------------------------

def main():
    root = ThemedTk(theme="ubuntu")  # später: "black", "radiance", "clearlooks", "ubuntu", "azure", "default"
    app = PySILLSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()