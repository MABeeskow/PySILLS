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
import tkinter.font as tkfont

from tkinter import ttk
from ttkthemes import ThemedTk

class PySILLSApp:

    def __init__(self, root, skin="dark"):
        self.root = root
        self.skin = skin
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

    def set_mode(self, value):
            self.radio_var.set(value)
            self.update_toggle_styles()

    def update_toggle_styles(self):
        for value, button in self.toggle_buttons.items():
            if value == self.radio_var.get():
                button.state(["pressed"])
            else:
                button.state(["!pressed"])

    def create_widgets(self):

        # 1st panel (PySILLS)
        self.frame_main = ttk.LabelFrame(self.main_frame, text="General", padding=10)
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

        # Toggle-Buttons
        self.radio_var = tk.StringVar(value="option1")
        self.toggle_buttons = {}
        options = [
            ("Mineral analysis", "option1"),
            ("Fluid inclusion analysis", "option2"),
            ("Melt inclusion analysis", "option3"),]

        for text, value in options:
            btn = ttk.Button(
                self.frame_project, text=text, style="Toggle.TButton", command=lambda v=value: self.set_mode(v))
            btn.pack(fill="x", pady=2)
            self.toggle_buttons[value] = btn

        self.update_toggle_styles()

        # Buttons
        self.btn_frame_project = ttk.Frame(self.frame_project)
        self.btn_frame_project.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_project, text="Setup").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_project, text="Results").pack(fill="x", pady=2)

        # 3rd panel (Standard files)
        self.frame_standard = ttk.LabelFrame(
            self.main_frame, text="Standard reference material (SRM) settings", padding=10)
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
        self.frame_listbox_standard = ttk.LabelFrame(self.main_frame, text="Imported files", padding=10)
        self.frame_listbox_standard.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.file_list_standard = tk.Listbox(self.frame_listbox_standard, height=20)
        self.file_list_standard.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 6):
            self.file_list_standard.insert(tk.END, f"Standard_File_{i}.csv")

        # 4th panel (Sample files)
        self.frame_sample = ttk.LabelFrame(self.main_frame, text="Sample files settings", padding=10)
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
        self.frame_listbox_sample = ttk.LabelFrame(self.main_frame, text="Imported files", padding=10)
        self.frame_listbox_sample.grid(row=1, column=2, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.file_list_sample = tk.Listbox(self.frame_listbox_sample, height=20)
        self.file_list_sample.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 13):
            self.file_list_sample.insert(tk.END, f"Sample_File_{i}.csv")

        # 5th panel (Isotopes)
        self.frame_isotopes = ttk.LabelFrame(self.main_frame, text="Isotope settings", padding=10)
        self.frame_isotopes.grid(row=0, column=3, sticky="nsew", padx=(0, 10), pady=(0, 10))

        # Buttons
        self.btn_frame_isotopes = ttk.Frame(self.frame_isotopes)
        self.btn_frame_isotopes.pack(fill="x", pady=5)

        ttk.Button(self.btn_frame_isotopes, text="Assign SRM").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_isotopes, text="View SRM values").pack(fill="x", pady=2)
        ttk.Button(self.btn_frame_isotopes, text="View isotope results").pack(fill="x", pady=2)

        # Listbox (z.B. für Messfiles)
        self.frame_listbox_isotopes = ttk.LabelFrame(self.main_frame, text="Measured isotopes", padding=10)
        self.frame_listbox_isotopes.grid(row=1, column=3, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.list_isotopes = tk.Listbox(self.frame_listbox_isotopes, height=20)
        self.list_isotopes.pack(fill="both", expand=True)

        # Demo-Daten
        for i in range(1, 43):
            self.list_isotopes.insert(tk.END, f"Isotope_{i}")


        # Toggle.TButton
        style = ttk.Style()
        style.configure("Toggle.TButton",
            relief="flat",
            borderwidth=0,
            padding=6
        )
        if self.skin == "dark":
            listbox_style = {
                "bg": "#3a3a3a",
                "fg": "#e6e6e6",
                "selectbackground": "#e76f51",
                "selectforeground": "#ffffff",
                "highlightthickness": 0,
                "borderwidth": 0,
                "relief": "flat"
            }
            # Toggle.TButton
            style.map("Toggle.TButton",
                background=[
                    ("pressed", "#e76f51"),   # aktiv
                    ("active", "#5c5c5c")     # hover
                ]
            )
        elif self.skin == "light":
            listbox_style = {
                "bg": "#d5d5d5",
                "fg": "#000000",
                "selectbackground": "#e76f51",
                "selectforeground": "#ffffff",
                "highlightthickness": 0,
                "borderwidth": 0,
                "relief": "flat"
            }
            # Toggle.TButton
            style.map("Toggle.TButton",
                background=[
                    ("pressed", "#e76f51"),   # aktiv
                    ("active", "#bbbbbb")     # hover
                ]
            )

        self.file_list_standard.configure(**listbox_style)
        self.file_list_sample.configure(**listbox_style)
        self.list_isotopes.configure(**listbox_style)

        self.file_list_standard.configure(font=("Arial", 14))
        self.file_list_sample.configure(font=("Arial", 14))
        self.list_isotopes.configure(font=("Arial", 14))


# ----------------------------------------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------------------------------------

def style_listboxes(self, dark=True):
    if dark:
        cfg = {
            "bg": "#2b2b2b",
            "fg": "#e6e6e6",
            "selectbackground": "#4a90e2",
            "selectforeground": "#ffffff"
        }
    else:
        cfg = {
            "bg": "#ffffff",
            "fg": "#000000",
            "selectbackground": "#4a90e2",
            "selectforeground": "#ffffff"
        }

    for lb in [self.file_list_standard, self.file_list_sample, self.list_isotopes]:
        lb.configure(**cfg, highlightthickness=0, relief="flat")

def configure_light_theme(root):
    style = ttk.Style(root)
    if "pysillls_light" not in style.theme_names():
        style.theme_create("pysillls_light", parent="clam", settings={
            ".": {
                "configure": {
                    "background": "#e0e0e0",
                    "foreground": "#000000",
                    "font": ("Arial", 14)
                }
            },
            "TFrame": {
                "configure": {
                    "background": "#e0e0e0"
                }
            },
            "TLabel": {
                "configure": {
                    "background": "#e0e0e0",
                    "foreground": "#000000"
                }
            },
            "TLabelFrame": {
                "configure": {
                    "background": "#e0e0e0",
                    "borderwidth": 1,
                    "relief": "solid"
                }
            },
            "TLabelFrame.Label": {
                "configure": {
                    "background": "#e0e0e0",
                    "foreground": "#000000"
                }
            },
            "TButton": {
                "configure": {
                    "background": "#d5d5d5",
                    "foreground": "#000000",
                    "padding": 6,
                    "relief": "flat",
                    "borderwidth": 1
                },
                "map": {
                    "background": [
                        ("active", "#bbbbbb"),
                        ("pressed", "#c0c0c0")
                    ],
                    "foreground": [
                        ("disabled", "#9a9a9a")
                    ]
                }
            },
            "TRadiobutton": {
                "configure": {
                    "background": "#e0e0e0",
                    "foreground": "#000000"
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground": "#d5d5d5",
                    "foreground": "#000000"
                }
            },
            "Treeview": {
                "configure": {
                    "background": "#e0e0e0",
                    "foreground": "#000000",
                    "fieldbackground": "#2b2b2b"
                },
                "map": {
                    "background": [("selected", "#4a90e2")],
                    "foreground": [("selected", "#ffffff")]
                }
            }
        })

    style.theme_use("pysillls_light")
    root.configure(bg="#eaeaea")

def configure_dark_theme(root):
    style = ttk.Style(root)
    if "pysills_dark" not in style.theme_names():
        style.theme_create("pysills_dark", parent="clam", settings={
            ".": {
                "configure": {
                    "background": "#2b2b2b",
                    "foreground": "#e6e6e6",
                    "font": ("Arial", 14)
                }
            },

            "TFrame": {
                "configure": {
                    "background": "#2b2b2b"
                }
            },

            "TLabel": {
                "configure": {
                    "background": "#2b2b2b",
                    "foreground": "#e6e6e6"
                }
            },

            "TLabelFrame": {
                "configure": {
                    "background": "#2b2b2b",
                    "borderwidth": 1,
                    "relief": "solid"
                }
            },

            "TLabelFrame.Label": {
                "configure": {
                    "background": "#2b2b2b",
                    "foreground": "#ffffff"
                }
            },

            "TButton": {
                "configure": {
                    "background": "#3a3a3a",
                    "foreground": "#ffffff",
                    "padding": 6,
                    "relief": "flat",
                    "borderwidth": 1
                },
                "map": {
                    "background": [
                        ("active", "#5c5c5c"),
                        ("pressed", "#353535")
                    ],
                    "foreground": [
                        ("disabled", "#9a9a9a")
                    ]
                }
            },

            "TRadiobutton": {
                "configure": {
                    "background": "#2b2b2b",
                    "foreground": "#e6e6e6"
                }
            },

            "TEntry": {
                "configure": {
                    "fieldbackground": "#3a3a3a",
                    "foreground": "#ffffff"
                }
            },

            "Treeview": {
                "configure": {
                    "background": "#2b2b2b",
                    "foreground": "#e6e6e6",
                    "fieldbackground": "#2b2b2b"
                },
                "map": {
                    "background": [("selected", "#4a90e2")],
                    "foreground": [("selected", "#ffffff")]
                }
            }
        })

    style.theme_use("pysills_dark")
    root.configure(bg="#2b2b2b")

def main():
    root = ThemedTk(theme="clam")
    skin = "dark"

    tkfont.nametofont("TkDefaultFont").configure(size=14)
    tkfont.nametofont("TkTextFont").configure(size=14)
    tkfont.nametofont("TkMenuFont").configure(size=14)


    if skin == "dark":
        configure_dark_theme(root)
    elif skin == "light":
        configure_light_theme(root)

    app = PySILLSApp(root, skin)
    root.mainloop()


if __name__ == "__main__":
    main()