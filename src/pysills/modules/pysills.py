#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		pysills.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		05.07.2022

#-----------------------------------------------

## MODULES
import os, pathlib
import re, datetime, csv, string
import tkinter as tk
from tkinter import filedialog
import numpy as np
from modules.gui_elements import SimpleElements as SE
from modules.essential_functions import EssentialDataProcessing as EDP
from modules.essential_functions import EssentialsSRM as ESRM
from modules.essential_functions import Essentials as ES
from modules.chemistry import PeriodicSystemOfElements as PSE
from modules.chemistry import PeriodicSystem
from modules.data import Data
from modules.fluid_inclusions import FluidInclusions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
from modules import data
import colorsys

## GUI
class PySILLS(tk.Frame):
    #
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #
        ## Colors
        self.green_dark = "#282D28"
        self.green_medium = "#616D61"
        self.green_light = "#CFD3CF"
        self.red_dark = "#E76F51"
        self.red_medium = "#F1A896"
        self.red_light = "#FDF0ED"
        self.font_dark = "#000000"
        self.font_light = "#FFFFFF"
        self.yellow_dark = "#E9C46A"
        self.yellow_medium = "#F3DFAE"
        self.yellow_light = "#FDFAF2"
        self.blue_dark = "#5B828E"
        self.blue_medium = "#8CA7AF"
        self.blue_light = "#CDD9DD"
        self.brown_dark = "#AC7E62"
        self.brown_medium = "#C4A491"
        self.brown_light = "#EEE5DF"
        self.slate_grey_dark = "#6E7894"
        self.slate_grey_medium = "#9AA1B4"
        self.slate_grey_light = "#E2E4EA"
        self.sign_red = "#E84258"
        self.sign_green = "#B0D8A4"
        #
        ## Constants
        self.list_std = []
        self.list_smpl = []
        #
        # General Settings
        self.parent = parent
        self.parent.title("PySILLS")
        self.parent.geometry("1800x1000+0+0")
        self.parent.resizable(False, False)
        self.parent["bg"] = self.green_light
        #
        self.list_alphabet = list(string.ascii_uppercase)
        #
        ## Data Container
        self.container_elements = {}
        self.gui_elements = {}
        self.container_gui = {}
        self.window_created = {}
        menu_list = ["SRM", "ma_setting", "ma_datareduction", "ma_dataexploration", "fi_setting", "fi_datareduction",
                     "fi_dataexploration", "mi_setting", "mi_datareduction", "mi_dataexploration", "plotting", "PSE",
                     "salt_correction", "fi_method_setting", "mi_method_setting", "se_method_setting", "dwell_times"]
        gui_categories = ["Label", "Button", "Option Menu", "Entry", "Frame", "Radiobutton", "Checkbox", "Listbox",
                          "Canvas"]
        for menu in menu_list:
            self.container_elements[menu] = {}
            self.container_elements[menu]["Label"] = []
            self.container_elements[menu]["Button"] = []
            self.container_elements[menu]["Option Menu"] = []
            self.container_elements[menu]["Entry"] = []
            self.container_elements[menu]["Frame"] = []
            self.container_elements[menu]["Radiobutton"] = []
            self.container_elements[menu]["Checkbox"] = []
            self.container_elements[menu]["Listbox"] = []
            self.container_elements[menu]["Canvas"] = []
            self.container_gui[menu] = {}
            self.window_created[menu] = False
            #
            self.gui_elements[menu] = {}
            for gui_category in gui_categories:
                self.gui_elements[menu][gui_category] = {}
                self.gui_elements[menu][gui_category]["General"] = []
                self.gui_elements[menu][gui_category]["Specific"] = []
                self.container_gui[menu][gui_category] = {}
                self.container_gui[menu][gui_category]["General"] = []
                self.container_gui[menu][gui_category]["Specific"] = []
        self.container_var = {}
        self.container_var["SRM"] = {}
        self.container_var["SRM"]["default"] = [tk.StringVar(), tk.StringVar()]
        for variable in self.container_var["SRM"]["default"]:
            variable.set("Select SRM")
        self.container_var["isotopes"] = {}
        self.container_var["isotopes"]["default"] = tk.StringVar()
        self.container_var["mineral"] = tk.StringVar()
        self.container_var["mineral"].set("Select Mineral")
        self.container_var["ma_setting"] = []
        self.container_var["fi_setting"] = []
        self.container_var["mi_setting"] = []
        self.container_var["settings"] = {}
        self.container_var["fi_setting"] = {}
        self.container_var["mi_setting"] = {}
        self.container_var["salt_correction"] = {}
        self.container_var["salt_correction"]["Checkboxes"] = {}
        self.container_var["salt_correction"]["Salinity"] = tk.StringVar()
        self.container_var["salt_correction"]["Salinity"].set("Set salinity")
        self.container_var["salt_correction"]["Concentration"] = {}
        self.container_var["dwell_times"] = {}
        self.container_var["dwell_times"]["Entry"] = {}
        self.container_var["dwell_times"]["Entry"]["Default"] = tk.StringVar()
        self.container_var["dwell_times"]["Entry"]["Default"].set("0.01")
        #
        ## MINERAL ANALYSIS
        self.container_var["settings"]["Time BG Start"] = tk.StringVar()
        self.container_var["settings"]["Time BG Start"].set("Set start time")
        self.container_var["settings"]["Time BG End"] = tk.StringVar()
        self.container_var["settings"]["Time BG End"].set("Set end time")
        self.container_var["settings"]["Time SIG Start"] = tk.StringVar()
        self.container_var["settings"]["Time SIG Start"].set("Set start time")
        self.container_var["settings"]["Time SIG End"] = tk.StringVar()
        self.container_var["settings"]["Time SIG End"].set("Set end time")
        self.container_var["settings"]["Author"] = tk.StringVar()
        self.container_var["settings"]["Source ID"] = tk.StringVar()
        self.container_var["ma_datareduction"] = {}
        self.container_var["ma_dataexploration"] = {}
        #
        ## FLUID/MELT INCLUSION ANALYSIS
        self.container_var["fi_setting"]["Time BG Start"] = tk.StringVar()
        self.container_var["fi_setting"]["Time BG Start"].set("Set start time")
        self.container_var["fi_setting"]["Time BG End"] = tk.StringVar()
        self.container_var["fi_setting"]["Time BG End"].set("Set end time")
        self.container_var["fi_setting"]["Time MAT Start"] = tk.StringVar()
        self.container_var["fi_setting"]["Time MAT Start"].set("Set start time")
        self.container_var["fi_setting"]["Time MAT End"] = tk.StringVar()
        self.container_var["fi_setting"]["Time MAT End"].set("Set end time")
        self.container_var["fi_setting"]["Time INCL Start"] = tk.StringVar()
        self.container_var["fi_setting"]["Time INCL Start"].set("Set start time")
        self.container_var["fi_setting"]["Time INCL End"] = tk.StringVar()
        self.container_var["fi_setting"]["Time INCL End"].set("Set end time")
        self.container_var["fi_setting"]["Author"] = tk.StringVar()
        self.container_var["fi_setting"]["Source ID"] = tk.StringVar()
        self.container_var["fi_setting"]["Method"] = tk.StringVar()
        self.container_var["fi_setting"]["Method"].set("Select Method")
        self.container_var["fi_setting"]["Host Setup Selection"] = tk.IntVar()
        self.container_var["fi_setting"]["Host Setup Selection"].set(1)
        self.container_var["fi_setting"]["Oxide"] = tk.StringVar()
        self.container_var["fi_setting"]["Oxide"].set("Select Oxide")
        self.container_var["fi_setting"]["Oxide Concentration"] = tk.StringVar()
        self.container_var["fi_setting"]["Oxide Concentration"].set("100")
        self.container_var["fi_setting"]["Sulfide"] = tk.StringVar()
        self.container_var["fi_setting"]["Sulfide"].set("Select Sulfide")
        self.container_var["fi_setting"]["Sulfide Concentration"] = tk.StringVar()
        self.container_var["fi_setting"]["Sulfide Concentration"].set("100")
        self.container_var["fi_setting"]["Halide"] = tk.StringVar()
        self.container_var["fi_setting"]["Halide"].set("Select Halide")
        self.container_var["fi_setting"]["Halide Concentration"] = tk.StringVar()
        self.container_var["fi_setting"]["Halide Concentration"].set("100")
        self.container_var["fi_setting"]["Mineral Concentration"] = tk.StringVar()
        self.container_var["fi_setting"]["Mineral Concentration"].set("100")
        self.container_var["fi_setting"]["Host Only"] = tk.StringVar()
        self.container_var["fi_setting"]["Host Only"].set("Select Isotope")
        self.container_var["fi_setting"]["2nd Internal"] = tk.StringVar()
        self.container_var["fi_setting"]["2nd Internal"].set("Select Isotope")
        self.container_var["fi_setting"]["2nd Internal Concentration"] = tk.StringVar()
        self.container_var["fi_setting"]["IS Selection"] = tk.IntVar()
        self.container_var["fi_setting"]["IS Selection"].set(1)
        self.container_var["fi_datareduction"] = {}
        self.container_var["fi_dataexploration"] = {}
        #
        self.container_var["mi_setting"]["Time BG Start"] = tk.StringVar()
        self.container_var["mi_setting"]["Time BG Start"].set("Set start time")
        self.container_var["mi_setting"]["Time BG End"] = tk.StringVar()
        self.container_var["mi_setting"]["Time BG End"].set("Set end time")
        self.container_var["mi_setting"]["Time MAT Start"] = tk.StringVar()
        self.container_var["mi_setting"]["Time MAT Start"].set("Set start time")
        self.container_var["mi_setting"]["Time MAT End"] = tk.StringVar()
        self.container_var["mi_setting"]["Time MAT End"].set("Set end time")
        self.container_var["mi_setting"]["Time INCL Start"] = tk.StringVar()
        self.container_var["mi_setting"]["Time INCL Start"].set("Set start time")
        self.container_var["mi_setting"]["Time INCL End"] = tk.StringVar()
        self.container_var["mi_setting"]["Time INCL End"].set("Set end time")
        self.container_var["mi_setting"]["Author"] = tk.StringVar()
        self.container_var["mi_setting"]["Source ID"] = tk.StringVar()
        self.container_var["mi_datareduction"] = {}
        self.container_var["mi_dataexploration"] = {}
        #
        self.container_var["mineralchemistry"] = []
        self.container_var["plotting"] = {}
        self.container_var["IS"] = {}
        self.container_var["IS"]["Default STD"] = tk.StringVar()
        self.container_var["IS"]["Default STD"].set("Select IS")
        self.container_var["IS"]["Default SMPL"] = tk.StringVar()
        self.container_var["IS"]["Default SMPL"].set("Select IS")
        self.container_var["ID"] = {}
        self.container_var["ID"]["Default STD"] = tk.StringVar()
        self.container_var["ID"]["Default STD"].set("A")
        self.container_var["ID"]["Default SMPL"] = tk.StringVar()
        self.container_var["ID"]["Default SMPL"].set("B")
        self.container_var["STD"] = {}
        self.container_var["SMPL"] = {}
        self.container_var["LASER"] = tk.StringVar()
        self.container_var["charge"] = {}
        self.list_isotopes = []
        self.srm_actual = {}
        self.container_files = {}
        self.container_files["STD"] = {}
        self.container_files["SRM"] = {}
        self.container_files["SMPL"] = {}
        self.container_optionmenu = {}
        self.container_optionmenu["STD"] = {}
        self.container_optionmenu["SMPL"] = {}
        self.container_optionmenu["ISOTOPES"] = {}
        self.container_measurements = {}
        categories_01 = ["RAW", "SELECTED", "EDITED"]
        for category_01 in categories_01:
            self.container_measurements[category_01] = {}
        #
        self.mineral_chem = {}
        #
        self.container_helper = {}
        self.container_helper["STD"] = {}
        self.container_helper["SMPL"] = {}
        self.container_helper["positions"] = {}
        self.container_helper["positions"]["BG STD"] = {}
        self.container_helper["positions"]["SIG STD"] = {}
        self.container_helper["positions"]["MAT STD"] = {}
        self.container_helper["positions"]["INCL STD"] = {}
        self.container_helper["positions"]["SPK STD"] = {}
        self.container_helper["positions"]["BG SMPL"] = {}
        self.container_helper["positions"]["SIG SMPL"] = {}
        self.container_helper["positions"]["MAT SMPL"] = {}
        self.container_helper["positions"]["INCL SMPL"] = {}
        self.container_helper["positions"]["SPK SMPL"] = {}
        self.container_helper["positions"]["BG"] = {}
        self.container_helper["positions"]["SIG"] = {}
        self.container_helper["positions"]["SPK"] = {}
        self.container_helper["positions"]["MAT"] = {}
        self.container_helper["positions"]["INCL"] = {}
        self.container_helper["indices"] = {}
        self.container_helper["limits BG"] = {}
        self.container_helper["limits SIG"] = {}
        self.container_helper["limits MAT"] = {}
        self.container_helper["limits INCL"] = {}
        self.container_helper["limits SPK"] = {}
        self.container_helper["limits BG Ratio"] = {}
        self.container_helper["limits SIG Ratio"] = {}
        self.container_helper["limits MAT Ratio"] = {}
        self.container_helper["limits INCL Ratio"] = {}
        self.container_helper["limits SPK Ratio"] = {}
        #
        self.container_lists = {}
        self.container_lists["SRM"] = []
        self.container_lists["IS"] = []
        self.container_lists["ID"] = []
        self.container_lists["ID Files"] = {}
        self.container_lists["STD"] = {}
        self.container_lists["STD"]["Long"] = []
        self.container_lists["STD"]["Short"] = []
        self.container_lists["SMPL"] = {}
        self.container_lists["SMPL"]["Long"] = []
        self.container_lists["SMPL"]["Short"] = []
        self.container_lists["ISOTOPES"] = []
        self.container_lists["Plugins FI"] = {} # FI = Fluid Inclusion
        self.container_lists["Plugins FI"]["Names"] = []
        self.container_lists["Plugins FI"]["Files"] = []
        self.container_lists["Plugins MI"] = {} # MI = Melt Inclusion
        self.container_lists["Plugins MI"]["Names"] = []
        self.container_lists["Plugins MI"]["Files"] = []
        self.container_lists["Plugins SE"] = {} # SE = Spike Elimination
        self.container_lists["Plugins SE"]["Names"] = []
        self.container_lists["Plugins SE"]["Files"] = []
        self.container_lists["Oxides"] = [
            "SiO2", "TiO2", "Al2O3", "Fe2O3", "Fe3O4", "FeO", "MgO", "MnO", "CaO", "BaO", "Na2O", "K2O", "P2O5",
            "Cr2O3", "ZrO2"]
        self.container_lists["Sulfides"] = [
            "FeS2", "ZnS" "PbS", "Ag2S", "Na2S", "MoS2", "CdS", "SeS2", "BaS", "BeS", "CoS", "Cu2S", "CuS", "FeS",
            "Fe2S3", "Hg2S", "HgS", "MnS", "NiS", "Tl2S", "SnS", "SnS2"]
        self.container_lists["Halides"] = [
            "NaCl", "KCl", "KI", "LiCl", "CuCl2", "AgCl", "CaCl2", "ClF", "CH3Br", "CHI3", "HCl", "HBr"]
        self.container_results = {}
        self.container_results["STD"] = {}
        self.container_results["STD"]["RAW"] = {}
        self.container_results["STD"]["SMOOTHED"] = {}
        self.container_results["SMPL"] = {}
        self.container_results["SMPL"]["RAW"] = {}
        self.container_results["SMPL"]["SMOOTHED"] = {}
        self.xi_std_time = {}
        self.xi_regr = None
        #
        self.demo_view = False
        #
        self.fast_track_std = False
        self.fast_track_smpl = False
        #
        self.file_loaded = False
        #
        self.spikes_isotopes = {}
        #
        self.diagrams_setup = {}
        categories_01 = ["STD", "SMPL"]
        for category_01 in categories_01:
            self.diagrams_setup[category_01] = {}
        #
        self.container_diagrams = {}
        self.container_listboxes = {}
        categories_01 = ["STD", "SMPL"]
        for category_01 in categories_01:
            self.container_diagrams[category_01] = {}
            self.container_listboxes[category_01] = {}
            self.spikes_isotopes[category_01] = {}
        #
        # Calculation Report
        self.container_report = {}
        categories_01 = ["Total STD", "Total SMPL"]
        categories_02 = ["Intensity Ratio", "Sensitivity", "Concentration", "RSF", "LOD"]
        for category_01 in categories_01:
            self.container_report[category_01] = {}
            self.container_report[category_01]["Mean"] = {}
            self.container_report[category_01]["Error"] = {}
            for category_02 in categories_02:
                self.container_report[category_01]["Mean"][category_02] = {}
                self.container_report[category_01]["Error"][category_02] = {}
                self.container_report[category_01]["Mean"][category_02]["filename"] = category_01
                self.container_report[category_01]["Error"][category_02]["filename"] = category_01
        #
        self.list_srm = np.array([["NIST 606"], ["NIST 610"], ["NIST 610 (GeoReM)"], ["NIST 610 (Spandler)"],
                                  ["NIST 611"], ["NIST 611 (GeoReM)"], ["NIST 612"], ["NIST 612 (GeoReM)"],
                                  ["NIST 613"], ["NIST 613 (GeoReM)"], ["NIST 614"], ["NIST 614 (GeoReM)"],
                                  ["NIST 615"], ["NIST 615 (GeoReM)"], ["NIST 616"], ["NIST 616 (GeoReM)"],
                                  ["NIST 617"], ["NIST 617 (GeoReM)"], ["USGS BCR-2G (GeoReM)"],
                                  ["USGS GSD-1G (GeoReM)"], ["USGS GSE-1G (GeoReM)"], ["B6"], ["Durango Apatite"]])[:, 0]
        self.srm_window_checker = tk.IntVar()
        self.srm_window_checker.set(0)
        self.previous_std_list = []
        self.list_pse = PSE().get_element_names()
        self.ionization_energies = {}
        self.ionization_energies["First"] = {}
        self.ionization_energies["Second"] = {}
        for element in self.list_pse:
            data_element = PeriodicSystem(name=element).get_data()
            if len(data_element) == 13:
                self.ionization_energies["First"][element] = data_element[-2]
                self.ionization_energies["Second"][element] = data_element[-1]
            elif len(data_element) == 12:
                self.ionization_energies["First"][element] = data_element[-1]
                self.ionization_energies["Second"][element] = 0.0
        #
        self.container_settings = {}
        categories_01 = ["MA", "FI", "MI"] # MA=Mineral Analysis, FI=Fluid Inclusions, MI=Melt Inclusions
        categories_02 = ["Start BG", "End BG", "Start SIG", "End SIG", "Start MAT", "End MAT", "Start INCL", "End INCL"]
        categories_03 = ["Deviation", "Threshold", "Author", "Source ID"]
        for category_01 in categories_01:
            self.container_settings[category_01] = {}
            for category_02 in categories_02:
                if category_01 == "MA" and category_02 in ["Start MAT", "End MAT", "Start INCL", "End INCL"]:
                    pass
                elif category_01 in ["FI", "MI"] and category_02 in ["Start SIG", "End SIG"]:
                    pass
                else:
                    self.container_settings[category_01][category_02] = tk.StringVar()
            for category_03 in categories_03:
                self.container_settings[category_01][category_03] = tk.StringVar()
        #
        self.mineral_list = ["Quartz", "Calcite", "Fluorite", "Apatite-Cl", "Apatite-F", "Apatite-OH", "Forsterite",
                             "Fayalite", "Tephroite", "Albite", "Anorthite", "Orthoclase", "Microcline", "Zircon",
                             "Enargite", "Pyrite", "Chalcopyrite", "Bornite", "Arsenopyrite", "Sphalerite", "Galena",
                             "Molybdenite", "Hematite", "Magnetite", "Chromite", "Gahnite", "Meionite", "Marialite",
                             "Strontianite", "Titanite", "Aegirine", "Diopside", "Hedenbergite", "Ferrosilite",
                             "Enstatite", "Monazite-La", "Monazite-Ce", "Monazite-Pr", "Monazite-Nd", "Monazite-Sm",
                             "Monazite-Eu", "Monazite-Gd", "Monazite-Th"]
        self.mineral_list.sort()
        self.container_lists["Minerals"] = self.mineral_list
        #
        self.calculate_mineral_chemistry()
        #
        window_width = 1800
        window_heigth = 1000
        row_min = 25
        n_rows = int(window_heigth/row_min)
        column_min = 20
        n_columns = int(window_width/column_min)
        #
        for x in range(n_columns):
            tk.Grid.columnconfigure(self.parent, x, weight=1)
        for y in range(n_rows):
            tk.Grid.rowconfigure(self.parent, y, weight=1)
        #
        # Rows
        for i in range(0, n_rows):
            self.parent.grid_rowconfigure(i, minsize=row_min)
        # Columns
        for i in range(0, n_columns):
            self.parent.grid_columnconfigure(i, minsize=column_min)
        #
        frame_01 = tk.Frame(self.parent, bg=self.green_dark, borderwidth=0, highlightthickness=0)
        frame_01.grid(row=0, column=0, rowspan=42, columnspan=21, sticky="nesw")
        #
        ## Logo
        pysills_logo = tk.PhotoImage(file="../documentation/images/PySILLS_Logo.png")
        pysills_logo = pysills_logo.subsample(1, 1)
        img = tk.Label(self.parent, image=pysills_logo, bg=self.green_dark)
        img.image = pysills_logo
        img.grid(row=0, column=0, rowspan=2, columnspan=20, sticky="nesw")
        #
        ## Labels
        SE(
            parent=self.parent, row_id=2, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Standard Reference\n Material (SRM)", relief=tk.GROOVE, fontsize="sans 10 bold")
        SE(
            parent=self.parent, row_id=6, column_id=0, n_rows=2,  n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Mineral Analysis (MA)", relief=tk.GROOVE, fontsize="sans 10 bold")
        SE(
            parent=self.parent, row_id=14, column_id=0, n_rows=2,  n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Fluid Inclusions (FI)", relief=tk.GROOVE, fontsize="sans 10 bold")
        SE(
            parent=self.parent, row_id=22, column_id=0, n_rows=2,  n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Melt Inclusions (MI)", relief=tk.GROOVE, fontsize="sans 10 bold")
        #
        SE(
            parent=self.parent, row_id=2, column_id=10, n_rows=2, n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
        SE(
            parent=self.parent, row_id=18, column_id=10, n_rows=2, n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
        #
        ## Listboxes
        self.lb_std = SE(
            parent=self.parent, row_id=6, column_id=10, n_rows=12, n_columns=10, fg=self.green_dark,
            bg=self.green_light).create_simple_listbox()
        self.lb_smpl = SE(
            parent=self.parent, row_id=22, column_id=10, n_rows=12, n_columns=10, fg=self.green_dark,
            bg=self.green_light).create_simple_listbox()
        #
        ## Buttons
        # Standard Reference Material
        SE(parent=self.parent, row_id=4, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="SRM Data", bg_active=self.red_dark,
                                                      fg_active=self.green_dark, command=self.sub_srm)
        # Mineral Analysis
        SE(parent=self.parent, row_id=8, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="Settings", bg_active=self.red_dark,
                                                      fg_active=self.green_dark,
                                                      command=self.sub_mineralanalysis_settings)
        SE(parent=self.parent, row_id=10, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="Data Reduction", bg_active=self.red_dark,
                                                      fg_active=self.green_dark,
                                                      command=self.sub_mineralanalysis_reduction)
        SE(parent=self.parent, row_id=12, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="Data Exploration", bg_active=self.red_dark,
                                                      fg_active=self.green_dark,
                                                      command=self.sub_mineralanalysis_exploration)
        # Fluid Inclusions
        SE(
            parent=self.parent, row_id=16, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Settings", bg_active=self.red_dark, fg_active=self.green_dark,
            command=self.sub_fluidinclusions_settings)
        SE(
            parent=self.parent, row_id=18, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Data Reduction", bg_active=self.red_dark, fg_active=self.green_dark,
            command=lambda container_elements=self.container_elements, gui_elements=self.gui_elements,
                           list_srm=self.list_srm: FluidInclusions(
                parent=self.parent, list_isotopes=self.list_isotopes, srm_actual=self.srm_actual,
                container_var=self.container_var, container_lists=self.container_lists,
                container_measurements=self.container_measurements, container_files=self.container_files,
                xi_std_time=self.xi_std_time, container_results=self.container_results).create_datareduction_window(
                container_elements, gui_elements, list_srm))
        SE(
            parent=self.parent, row_id=20, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Data Exploration", bg_active=self.red_dark, fg_active=self.green_dark,
            command=lambda container_elements=self.container_elements: FluidInclusions(
                parent=self.parent, list_isotopes=self.list_isotopes, srm_actual=self.srm_actual,
                container_var=self.container_var, container_lists=self.container_lists,
                container_measurements=self.container_measurements, container_files=self.container_files,
                xi_std_time=self.xi_std_time, container_results=self.container_results).create_dataexploration_window(
                container_elements))
        # Melt Inclusions
        SE(parent=self.parent, row_id=24, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="Settings", bg_active=self.red_dark,
                                                      fg_active=self.green_dark)
        SE(parent=self.parent, row_id=26, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="Data Reduction", bg_active=self.red_dark,
                                                      fg_active=self.green_dark)
        SE(parent=self.parent, row_id=28, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
           bg=self.green_medium).create_simple_button(text="Data Exploration", bg_active=self.red_dark,
                                                      fg_active=self.green_dark)
        # Data Import
        SE(
            parent=self.parent, row_id=4, column_id=10, n_rows=2, n_columns=5, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Add", bg_active=self.red_dark, fg_active=self.green_dark,
            command=lambda datatype="STD": self.open_csv(datatype))
        SE(
            parent=self.parent, row_id=4, column_id=15, n_rows=2, n_columns=5, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Delete", bg_active=self.red_dark, fg_active=self.green_dark,
            command=lambda var_lb=self.lb_std, var_list=self.list_std: self.delete_csv(var_lb, var_list))
        SE(
            parent=self.parent, row_id=20, column_id=10, n_rows=2, n_columns=5, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Add", bg_active=self.red_dark, fg_active=self.green_dark,
            command=lambda datatype="SMPL": self.open_csv(datatype))
        SE(
            parent=self.parent, row_id=20, column_id=15, n_rows=2, n_columns=5, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Delete", bg_active=self.red_dark, fg_active=self.green_dark,
            command=lambda var_lb=self.lb_smpl, var_list=self.list_smpl: self.delete_csv(var_lb, var_list))
        #
        SE(
            parent=self.parent, row_id=36, column_id=10, n_rows=2, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Restart", bg_active=self.red_dark, fg_active=self.green_dark, command=self.restart_pysills)
        SE(
            parent=self.parent, row_id=36, column_id=0, n_rows=2, n_columns=5, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Load Project", bg_active=self.red_dark, fg_active=self.green_dark, command=self.load_settings)
        SE(
            parent=self.parent, row_id=36, column_id=5, n_rows=2, n_columns=5, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Save Project", bg_active=self.red_dark, fg_active=self.green_dark, command=self.save_settings)
        SE(
            parent=self.parent, row_id=38, column_id=0, n_rows=1, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Documentation", bg_active=self.red_dark, fg_active=self.green_dark)
        SE(
            parent=self.parent, row_id=39, column_id=0, n_rows=1, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="About PySILLS", bg_active=self.red_dark, fg_active=self.green_dark)
        SE(
            parent=self.parent, row_id=38, column_id=10, n_rows=2, n_columns=10, fg=self.green_dark,
            bg=self.green_medium).create_simple_button(
            text="Quit", bg_active=self.red_dark, fg_active=self.green_dark, command=self.parent.quit)
    #
    def sub_srm(self):
        #
        if self.previous_std_list != self.list_std and self.srm_window_checker.get() == 1:
            self.srm_window_checker.set(0)
            for element in self.list_pse:
                self.container_var["SRM"][element].set(0.0)
        if len(self.previous_std_list) > 0 and self.srm_window_checker.get() == 1 and self.previous_std_list != self.list_std:
            for element in self.list_pse:
                self.container_var["SRM"][element].set(0.0)
        #
        ## Cleaning
        categories = ["SRM", "ma_setting", "plotting", "PSE", "ma_datareduction", "ma_dataexploration", "fi_setting"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Radiobutton"]) > 0:
                for item in self.container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Checkbox"]) > 0:
                for item in self.container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Listbox"]) > 0:
                for item in self.container_elements[category]["Listbox"]:
                    item.grid_remove()
        #
        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().grid_remove()
            self.toolbarFrame.grid_remove()
        except AttributeError:
            pass
        try:
            if self.canvas:
                self.canvas.destroy()
            if self.toolbarFrame:
                self.toolbarFrame.destroy()
        except AttributeError:
            pass
        try:
            self.canvas_drift.get_tk_widget().grid_forget()
            self.toolbarFrame_drift.grid_forget()
        except AttributeError:
            pass
        #
        ## Reconstruction
        try:
            for lbl_item in self.container_elements["SRM"]["Label"]:
                lbl_item.grid()
            for btn_item in self.container_elements["SRM"]["Button"]:
                btn_item.grid()
            for optmen_item in self.container_elements["SRM"]["Option Menu"]:
                optmen_item.grid()
            for entr_item in self.container_elements["SRM"]["Entry"]:
                entr_item.grid()
        except:
            print("Error!")
        try:
            for lbl_item in self.container_elements["PSE"]["Label"]:
                lbl_item.grid()
            for entr_item in self.container_elements["PSE"]["Entry"]:
                entr_item.grid()
        except:
            print("Error!")
        #
        start_column = 38   # start column PSE
        #
        if self.srm_window_checker.get() == 0:
            if len(self.list_std) == 0:
                ## LABELS
                lbl_srm_01 = SE(
                    parent=self.parent, row_id=0, column_id=21, n_rows=1, n_columns=16, fg=self.green_light,
                    bg=self.green_dark).create_simple_label(
                    text="Show SRM Concentrations", relief=tk.GROOVE, fontsize="sans 10 bold")
                lbl_srm_02 = SE(
                    parent=self.parent, row_id=0, column_id=start_column, n_rows=1, n_columns=42, fg=self.green_light,
                    bg=self.green_dark).create_simple_label(
                    text="Element Concentrations (ppm)", relief=tk.GROOVE, fontsize="sans 10 bold")
                #
                self.container_elements["SRM"]["Label"].extend([lbl_srm_01, lbl_srm_02])
                #
                lbl_def_srm = SE(
                    parent=self.parent, row_id=1, column_id=21, n_rows=1, n_columns=8, fg=self.green_dark,
                    bg=self.red_dark).create_simple_label(
                    text="Default SRM", relief=tk.GROOVE, fontsize="sans 10 bold")
                lbl_def_min = SE(
                    parent=self.parent, row_id=3, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                    bg=self.green_medium).create_simple_label(
                    text="Check Mineral Data", relief=tk.GROOVE, fontsize="sans 10 bold")
                #
                self.container_elements["SRM"]["Label"].extend([lbl_def_srm, lbl_def_min])
                #
                ## OPTION MENUS
                opt_menu_srm = SE(
                    parent=self.parent, row_id=1, column_id=29, n_rows=1, n_columns=8, fg=self.font_dark,
                    bg=self.red_dark).create_option_srm(
                    var_srm=self.container_var["SRM"]["default"][0], text_set="Select SRM for all",
                    fg_active=self.font_dark, bg_active=self.green_light,
                    command=lambda var_srm=self.container_var["SRM"]["default"][0], header_col=start_column,
                                   default=True: self.place_srm_values(var_srm, header_col, default))
                opt_menu_min = SE(
                    parent=self.parent, row_id=3, column_id=29, n_rows=1, n_columns=8, fg=self.green_dark,
                    bg=self.green_medium).create_option_mineral(
                    var_min=self.container_var["mineral"], text_set="Select mineral", fg_active=self.font_dark,
                    bg_active=self.red_dark, option_list=self.mineral_list,
                    command=lambda var_min=self.container_var["mineral"],
                                   header_col=start_column: self.place_mineral_values(var_min, header_col))
                self.container_elements["SRM"]["Option Menu"].extend([opt_menu_srm, opt_menu_min])
            else:
                ## LABELS
                lbl_srm_01 = SE(
                    parent=self.parent, row_id=0, column_id=21, n_rows=1, n_columns=16, fg=self.green_light,
                    bg=self.green_dark).create_simple_label(
                    text="Assign SRM to Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
                lbl_srm_02 = SE(
                    parent=self.parent, row_id=0, column_id=start_column, n_rows=1, n_columns=42, fg=self.green_light,
                    bg=self.green_dark).create_simple_label(
                    text="Element Concentrations (ppm)", relief=tk.GROOVE, fontsize="sans 10 bold")
                #
                self.container_elements["SRM"]["Label"].extend([lbl_srm_01, lbl_srm_02])
                #
                lbl_def_srm = SE(
                    parent=self.parent, row_id=1+len(self.list_std), column_id=21, n_rows=1, n_columns=8,
                    fg=self.green_dark, bg=self.red_dark).create_simple_label(
                    text="Default SRM", relief=tk.GROOVE, fontsize="sans 10 bold")
                lbl_def_min = SE(
                    parent=self.parent, row_id=3+len(self.list_std), column_id=21, n_rows=1, n_columns=8,
                    fg=self.green_light, bg=self.green_medium).create_simple_label(
                    text="Check Mineral", relief=tk.GROOVE, fontsize="sans 10 bold")
                #
                self.container_elements["SRM"]["Label"].extend([lbl_def_srm, lbl_def_min])
                #
                var_opt = tk.StringVar()
                #self.container_var["SRM"]["default"] = [tk.StringVar(), tk.StringVar()]
                for index, file in enumerate(self.list_std):
                    parts = file.split("/")
                    if parts[-1] not in self.container_files["STD"]:
                        self.container_files["STD"][parts[-1]] = {}
                        self.container_files["STD"][parts[-1]]["SRM"] = tk.StringVar()
                        self.container_files["STD"][parts[-1]]["IS"] = tk.StringVar()
                    lbl_std = SE(parent=self.parent, row_id=1+index, column_id=21, n_rows=1, n_columns=8,
                                 fg=self.green_dark, bg=self.green_medium).create_simple_label(text=parts[-1],
                                                                                                relief=tk.GROOVE,
                                                                                                fontsize="sans 10 bold")
                    self.container_elements["SRM"]["Label"].append(lbl_std)
                    self.container_var["SRM"][file] = tk.StringVar()
                    opt_menu_srm = SE(parent=self.parent, row_id=1+index, column_id=29, n_rows=1, n_columns=8,
                                      fg=self.green_dark, bg=self.green_medium).create_option_srm(var_srm=self.container_var["SRM"][file],
                                                                                                   text_set="Select SRM",
                                                                                                   fg_active=self.green_dark,
                                                                                                   bg_active=self.red_dark,
                                                                                                   command=lambda var_srm=var_opt,
                                                                                                                  header_col=start_column: self.place_srm_values(var_srm, header_col))
                    self.container_elements["SRM"]["Option Menu"].append(opt_menu_srm)
                    opt_menu_srm = SE(
                        parent=self.parent, row_id=1+len(self.list_std), column_id=29, n_rows=1, n_columns=8,
                        fg=self.font_dark, bg=self.red_dark).create_option_srm(
                        var_srm=self.container_var["SRM"]["default"][0], text_set="Select SRM for all",
                        fg_active=self.font_dark, bg_active=self.green_light,
                        command=lambda var_srm=self.container_var["SRM"]["default"][0], header_col=start_column,
                                       default=True: self.place_srm_values(var_srm, header_col, default))
                    opt_menu_min = SE(
                        parent=self.parent, row_id=3+len(self.list_std), column_id=29, n_rows=1, n_columns=8,
                        fg=self.green_dark, bg=self.green_medium).create_option_mineral(
                        var_min=self.container_var["mineral"], text_set="Select mineral", fg_active=self.font_dark,
                        bg_active=self.red_dark, option_list=self.mineral_list,
                        command=lambda var_min=self.container_var["mineral"], header_col=start_column:
                        self.place_mineral_values(var_min, header_col))
                    self.container_elements["SRM"]["Option Menu"].extend([opt_menu_srm, opt_menu_min])
            self.previous_std_list.clear()
            self.previous_std_list.extend(self.list_std)
        else:
            if self.previous_std_list != self.list_std:
                if len(self.list_std) == 0:
                    ## LABELS
                    lbl_srm_01 = SE(parent=self.parent, row_id=0, column_id=21, n_rows=2, n_columns=8, fg=self.green_light,
                                    bg=self.green_dark).create_simple_label(text="Show SRM Concentrations",
                                                                            relief=tk.GROOVE, fontsize="sans 10 bold")
                    lbl_srm_02 = SE(parent=self.parent, row_id=0, column_id=29, n_rows=2, n_columns=24, fg=self.green_light,
                                    bg=self.green_dark).create_simple_label(text="Element Concentrations (ppm)", relief=tk.GROOVE,
                                                                            fontsize="sans 10 bold")
                    self.container_elements["SRM"]["Label"].extend([lbl_srm_01, lbl_srm_02])
                    lbl_def_srm = SE(parent=self.parent, row_id=2, column_id=21, n_rows=2, n_columns=8, fg=self.green_dark,
                                     bg=self.red_dark).create_simple_label(text="Default SRM", relief=tk.GROOVE,
                                                                           fontsize="sans 10 bold")
                    lbl_def_min = SE(parent=self.parent, row_id=6, column_id=21, n_rows=2, n_columns=8, fg=self.green_light,
                                     bg=self.green_medium).create_simple_label(text="Check Mineral Data", relief=tk.GROOVE,
                                                                               fontsize="sans 10 bold")
                    self.container_elements["SRM"]["Label"].extend([lbl_def_srm, lbl_def_min])
                    ## OPTION MENUS
                    #self.container_var["SRM"]["default"] = [tk.StringVar(), tk.StringVar()]
                    opt_menu_srm = SE(parent=self.parent, row_id=2, column_id=29, n_rows=2, n_columns=8,
                                      fg=self.font_dark, bg=self.red_dark).create_option_srm(var_srm=self.container_var["SRM"]["default"][0],
                                                                                             text_set="Select SRM for all",
                                                                                             fg_active=self.font_dark,
                                                                                             bg_active=self.green_light,
                                                                                             command=lambda var_srm=self.container_var["SRM"]["default"][0],
                                                                                                            header_col=start_column, default=True: self.place_srm_values(var_srm, header_col, default))
                    opt_menu_min = SE(parent=self.parent, row_id=6, column_id=29, n_rows=2, n_columns=8,
                                      fg=self.green_dark, bg=self.green_medium).create_option_mineral(var_min=self.container_var["mineral"],
                                                                                                       text_set="Select mineral",
                                                                                                       fg_active=self.font_dark,
                                                                                                       bg_active=self.red_dark,
                                                                                                       option_list=self.mineral_list,
                                                                                                       command=lambda
                                                                                                           var_min=self.container_var["mineral"],
                                                                                                           header_col=start_column: self.place_mineral_values(var_min, header_col))
                    self.container_elements["SRM"]["Option Menu"].extend([opt_menu_srm, opt_menu_min])
                else:
                    ## LABELS
                    lbl_srm_01 = SE(
                        parent=self.parent, row_id=0, column_id=21, n_rows=2, n_columns=16, fg=self.green_light,
                        bg=self.green_dark).create_simple_label(
                        text="Assign SRM to Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
                    lbl_srm_02 = SE(
                        parent=self.parent, row_id=0, column_id=start_column, n_rows=2, n_columns=42,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text="Element Concentrations (ppm)", relief=tk.GROOVE, fontsize="sans 10 bold")
                    #
                    self.container_elements["SRM"]["Label"].extend([lbl_srm_01, lbl_srm_02])
                    #
                    lbl_def_srm = SE(
                        parent=self.parent, row_id=2+len(self.list_std)*2, column_id=21, n_rows=2, n_columns=8,
                        fg=self.green_dark, bg=self.red_dark).create_simple_label(
                        text="Default SRM", relief=tk.GROOVE, fontsize="sans 10 bold")
                    lbl_def_min = SE(
                        parent=self.parent, row_id=6+len(self.list_std)*2, column_id=21, n_rows=2,n_columns=8,
                        fg=self.green_light, bg=self.green_medium).create_simple_label(
                        text="Check Mineral", relief=tk.GROOVE, fontsize="sans 10 bold")
                    #
                    self.container_elements["SRM"]["Label"].extend([lbl_def_srm, lbl_def_min])
                    #
                    var_opt = tk.StringVar()
                    for index, file in enumerate(self.list_std):
                        parts = file.split("/")
                        if parts[-1] not in self.container_files["STD"]:
                            self.container_files["STD"][parts[-1]] = {}
                            self.container_files["STD"][parts[-1]]["SRM"] = tk.StringVar()
                            self.container_files["STD"][parts[-1]]["IS"] = tk.StringVar()
                        lbl_std = SE(parent=self.parent, row_id=2+index*2, column_id=21, n_rows=2, n_columns=8,
                                     fg=self.green_light, bg=self.green_medium).create_simple_label(text=parts[-1],
                                                                                                    relief=tk.GROOVE,
                                                                                                    fontsize="sans 10 bold")
                        self.container_elements["SRM"]["Label"].append(lbl_std)
                        self.container_var["SRM"][file] = tk.StringVar()
                        opt_menu_srm = SE(parent=self.parent, row_id=2+index*2, column_id=29, n_rows=2, n_columns=8,
                                          fg=self.green_dark, bg=self.green_medium).create_option_srm(var_srm=self.container_var["SRM"][file],
                                                                                                       text_set="Select SRM",
                                                                                                       fg_active=self.green_dark,
                                                                                                       bg_active=self.red_dark,
                                                                                                       command=lambda var_srm=var_opt,
                                                                                                                      header_col=start_column: self.place_srm_values(var_srm, header_col))
                        self.container_elements["SRM"]["Option Menu"].append(opt_menu_srm)
                        opt_menu_srm = SE(
                            parent=self.parent, row_id=2+len(self.list_std)*2, column_id=29, n_rows=2, n_columns=8,
                            fg=self.font_dark, bg=self.red_dark).create_option_srm(
                            var_srm=self.container_var["SRM"]["default"][0],
                            text_set=self.container_var["SRM"]["default"][0].get(), fg_active=self.font_dark,
                            bg_active=self.green_light, command=lambda var_srm=self.container_var["SRM"]["default"][0],
                                                                       header_col=start_column, default=True:
                            self.place_srm_values(var_srm, header_col, default))
                        opt_menu_min = SE(
                            parent=self.parent, row_id=6+len(self.list_std)*2, column_id=29, n_rows=2, n_columns=8,
                            fg=self.green_dark, bg=self.green_medium).create_option_mineral(
                            var_min=self.container_var["mineral"], text_set="Select mineral", fg_active=self.font_dark,
                            bg_active=self.red_dark, command=lambda var_min=self.container_var["mineral"],
                                                                    header_col=start_column:
                            self.place_mineral_values(var_min, header_col))
                        #
                        self.container_elements["SRM"]["Option Menu"].extend([opt_menu_srm, opt_menu_min])
        #
        if self.srm_window_checker.get() == 0 and len(self.container_elements["PSE"]["Label"]) == 0:
            ## Labels Elements
            for index, element in enumerate(self.list_pse, start=0):
                if index < 16:
                    lbl_element = SE(
                        parent=self.parent, row_id=1+index, column_id=start_column, n_rows=1, n_columns=2,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text=element, relief=tk.GROOVE, fontsize="sans 10 bold")
                    var_entr, entr = SE(
                        parent=self.parent, row_id=1+index, column_id=start_column+2, n_rows=1, n_columns=5,
                        fg=self.green_light, bg=self.green_dark).create_simple_entries(command=None)
                    #
                    self.container_elements["PSE"]["Label"].append(lbl_element)
                    self.container_elements["PSE"]["Entry"].append(entr)
                    self.container_var["SRM"][element] = var_entr
                    #
                elif index >= 16 and index < 32:
                    lbl_element = SE(
                        parent=self.parent, row_id=1+(index-16), column_id=start_column+7, n_rows=1, n_columns=2,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text=element, relief=tk.GROOVE, fontsize="sans 10 bold")
                    var_entr, entr = SE(
                        parent=self.parent, row_id=1+(index-16), column_id=start_column+9, n_rows=1, n_columns=5,
                        fg=self.green_light, bg=self.green_dark).create_simple_entries(command=None)
                    #
                    self.container_elements["PSE"]["Label"].append(lbl_element)
                    self.container_elements["PSE"]["Entry"].append(entr)
                    self.container_var["SRM"][element] = var_entr
                    #
                elif index >= 32 and index < 48:
                    lbl_element = SE(
                        parent=self.parent, row_id=1+(index-32), column_id=start_column+14, n_rows=1, n_columns=2,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text=element, relief=tk.GROOVE, fontsize="sans 10 bold")
                    var_entr, entr = SE(
                        parent=self.parent, row_id=1+(index-32), column_id=start_column+16, n_rows=1, n_columns=5,
                        fg=self.green_light, bg=self.green_dark).create_simple_entries(command=None)
                    #
                    self.container_elements["PSE"]["Label"].append(lbl_element)
                    self.container_elements["PSE"]["Entry"].append(entr)
                    self.container_var["SRM"][element] = var_entr
                    #
                elif index >= 48 and index < 64:
                    lbl_element = SE(
                        parent=self.parent, row_id=1+(index-48), column_id=start_column+21, n_rows=1, n_columns=2,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text=element, relief=tk.GROOVE, fontsize="sans 10 bold")
                    var_entr, entr = SE(
                        parent=self.parent, row_id=1+(index-48), column_id=start_column+23, n_rows=1, n_columns=5,
                        fg=self.green_light, bg=self.green_dark).create_simple_entries(command=None)
                    #
                    self.container_elements["PSE"]["Label"].append(lbl_element)
                    self.container_elements["PSE"]["Entry"].append(entr)
                    self.container_var["SRM"][element] = var_entr
                elif index >= 64 and index < 80:
                    lbl_element = SE(
                        parent=self.parent, row_id=1+(index-64), column_id=start_column+28, n_rows=1, n_columns=2,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text=element, relief=tk.GROOVE, fontsize="sans 10 bold")
                    var_entr, entr = SE(
                        parent=self.parent, row_id=1+(index-64), column_id=start_column+30, n_rows=1, n_columns=5,
                        fg=self.green_light, bg=self.green_dark).create_simple_entries(command=None)
                    #
                    self.container_elements["PSE"]["Label"].append(lbl_element)
                    self.container_elements["PSE"]["Entry"].append(entr)
                    self.container_var["SRM"][element] = var_entr
                elif index >= 80:
                    lbl_element = SE(
                        parent=self.parent, row_id=1+(index-80), column_id=start_column+35, n_rows=1, n_columns=2,
                        fg=self.green_light, bg=self.green_dark).create_simple_label(
                        text=element, relief=tk.GROOVE, fontsize="sans 10 bold")
                    var_entr, entr = SE(
                        parent=self.parent, row_id=1+(index-80), column_id=start_column+37, n_rows=1, n_columns=5,
                        fg=self.green_light, bg=self.green_dark).create_simple_entries(command=None)
                    #
                    self.container_elements["PSE"]["Label"].append(lbl_element)
                    self.container_elements["PSE"]["Entry"].append(entr)
                    self.container_var["SRM"][element] = var_entr
        else:
            pass
        if self.srm_window_checker.get() == 0:
            self.srm_window_checker.set(1)
    #
    def sub_mineralanalysis_settings(self):
        #
        ## Cleaning
        if self.demo_view == False:
            categories = ["SRM", "plotting", "PSE", "ma_datareduction", "ma_dataexploration", "fi_datareduction",
                          "fi_setting"]
        else:
            categories = ["SRM", "plotting", "PSE", "ma_setting", "ma_datareduction", "ma_dataexploration",
                          "fi_setting"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Radiobutton"]) > 0:
                for item in self.container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Checkbox"]) > 0:
                for item in self.container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Listbox"]) > 0:
                for item in self.container_elements[category]["Listbox"]:
                    item.grid_remove()
        try:
            self.canvas.get_tk_widget().grid_forget()
            self.toolbarFrame.grid_forget()
        except AttributeError:
            pass
        try:
            self.canvas_ratio.get_tk_widget().grid_forget()
            self.toolbarFrame_ratio.grid_forget()
        except AttributeError:
            pass
        try:
            self.canvas_drift.get_tk_widget().grid_forget()
            self.toolbarFrame_drift.grid_forget()
        except AttributeError:
            pass
        #
        ## Reconstruction
        if self.demo_view == False:
            try:
                for lbl_item in self.container_elements["ma_setting"]["Label"]:
                    lbl_item.grid()
                #print("Label: check!")
                for btn_item in self.container_elements["ma_setting"]["Button"]:
                    btn_item.grid()
                #print("Button: check!")
                for optmen_item in self.container_elements["ma_setting"]["Option Menu"]:
                    optmen_item.grid()
                #print("Option Menu: check!")
                for entr_item in self.container_elements["ma_setting"]["Entry"]:
                    entr_item.grid()
                #print("Entry: check!")
                for entr_item in self.container_elements["ma_setting"]["Frame"]:
                    entr_item.grid()
                #print("Frame: check!")
            except:
                print("Error! Reconstruction failed!")
        else:
            for category in ["Label", "Button", "Option Menu", "Entry", "Frame"]:
                self.container_elements["ma_setting"][category].clear()
            self.list_isotopes.clear()
            del self.palette_complete
            del self.isotope_colors
            del self.times
            self.container_files["SRM"].clear()
            self.container_files["STD"].clear()
            self.container_files["SMPL"].clear()
            self.container_helper["STD"].clear()
            self.container_helper["SMPL"].clear()
            self.container_lists["STD"]["Long"].clear()
            self.container_lists["STD"]["Short"].clear()
            self.container_lists["SMPL"]["Long"].clear()
            self.container_lists["SMPL"]["Short"].clear()
            list_std = ["Default_STD_01.csv", "Default_STD_02.csv", "Default_STD_03.csv", "Default_STD_04.csv",
                        "Default_STD_05.csv", "Default_STD_06.csv"]
            for item in list_std:
                self.container_var["STD"].pop(item, None)
                self.container_helper["positions"]["SPK"].pop(item, None)
            list_smpl = ["Default_SMPL_01.csv", "Default_SMPL_02.csv", "Default_SMPL_03.csv", "Default_SMPL_04.csv",
                         "Default_SMPL_05.csv", "Default_SMPL_06.csv", "Default_SMPL_07.csv", "Default_SMPL_08.csv",
                         "Default_SMPL_09.csv", "Default_SMPL_10.csv"]
            for item in list_smpl:
                self.container_var["SMPL"].pop(item, None)
                self.container_helper["positions"]["SPK"].pop(item, None)
            self.window_created["ma_setting"] = False
            self.demo_view = False
        #
        try:
            dataset_exmpl = Data(filename=self.list_std[0])
            df_exmpl = dataset_exmpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            self.times = df_exmpl.iloc[:, 0]
            self.list_isotopes = list(df_exmpl.columns.values)
            self.list_isotopes.pop(0)
            self.palette_complete = sns.color_palette("nipy_spectral", n_colors=len(self.list_isotopes)).as_hex()
            if bool(self.container_files["SRM"]) == False:
                self.isotope_colors = {}
                for index, isotope in enumerate(self.list_isotopes):
                    self.container_files["SRM"][isotope] = tk.StringVar()
                    self.isotope_colors[isotope] = self.palette_complete[index]
        except:
            #
            path = os.getcwd()
            parent = os.path.dirname(path)
            ma_demo_files = {"ALL": [], "STD": [], "SMPL": []}
            demo_files = os.listdir(path=parent + str("/demo_files/"))
            for file in demo_files:
                if file.startswith("demo_ma"):
                    path_complete = os.path.join(parent + str("/demo_files/"), file)
                    path_raw = pathlib.PureWindowsPath(path_complete)
                    ma_demo_files["ALL"].append(str(path_raw.as_posix()))
            ma_demo_files["ALL"].sort()
            # ma_demo_files["STD"].extend(ma_demo_files["ALL"][:3])
            # ma_demo_files["STD"].extend(ma_demo_files["ALL"][-3:])
            # ma_demo_files["SMPL"].extend(ma_demo_files["ALL"][3:-3])
            ma_demo_files["STD"].extend(ma_demo_files["ALL"][:1])
            ma_demo_files["STD"].extend(ma_demo_files["ALL"][-1:])
            ma_demo_files["SMPL"].extend(ma_demo_files["ALL"][4:6])
            #
            self.list_std = ma_demo_files["STD"]
            self.list_smpl = ma_demo_files["SMPL"]
            #
            for file_std in self.list_std:
                file_parts = file_std.split("/")
                self.lb_std.insert(tk.END, file_parts[-1])
            for file_smpl in self.list_smpl:
                file_parts = file_smpl.split("/")
                self.lb_smpl.insert(tk.END, file_parts[-1])
            #
            dataset_exmpl = Data(filename=self.list_std[0])
            df_exmpl = dataset_exmpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            self.times = df_exmpl.iloc[:, 0]
            self.list_isotopes = list(df_exmpl.columns.values)
            self.list_isotopes.pop(0)
            self.container_lists["ISOTOPES"] = self.list_isotopes
            self.palette_complete = sns.color_palette("nipy_spectral", n_colors=len(self.list_isotopes)).as_hex()
            if bool(self.container_files["SRM"]) == False:
                self.isotope_colors = {}
                for index, isotope in enumerate(self.list_isotopes):
                    self.container_files["SRM"][isotope] = tk.StringVar()
                    self.isotope_colors[isotope] = self.palette_complete[index]
            #
            self.demo_view = False
        #
        ## Labels
        start_col_std = 21
        start_col_smpl = 51
        start_col_iso = 72
        start_row_settings_01 = 25
        #
        if len(self.container_elements["ma_setting"]["Label"]) == 0:
            lbl_ma_setting_01 = SE(
                parent=self.parent, row_id=0, column_id=start_col_std, n_rows=1, n_columns=29, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Standard Files)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_02 = SE(
                parent=self.parent, row_id=0, column_id=start_col_smpl, n_rows=1, n_columns=20, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Sample Files)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_03 = SE(
                parent=self.parent, row_id=0, column_id=start_col_iso, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Isotopes)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_18 = SE(
                parent=self.parent, row_id=start_row_settings_01, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Standard Reference Material (SRM)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_19 = SE(
                parent=self.parent, row_id=start_row_settings_01+1, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_20 = SE(
                parent=self.parent, row_id=start_row_settings_01+2, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Isotopes", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_21 = SE(
                parent=self.parent, row_id=start_row_settings_01+3, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Internal Standard (IS)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_04 = SE(
                parent=self.parent, row_id=start_row_settings_01+8, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Default Time Windows (Background)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_05 = SE(
                parent=self.parent, row_id=start_row_settings_01+9, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_06 = SE(
                parent=self.parent, row_id=start_row_settings_01+10, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_07 = SE(
                parent=self.parent, row_id=start_row_settings_01+11, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Default Time Windows (Signal)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_08 = SE(
                parent=self.parent, row_id=start_row_settings_01+12, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_09 = SE(
                parent=self.parent, row_id=start_row_settings_01+13, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_10 = SE(
                parent=self.parent, row_id=start_row_settings_01+6, column_id=38, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Spike Elimination)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_11 = SE(
                parent=self.parent, row_id=start_row_settings_01+7, column_id=38, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Deviation", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_12 = SE(
                parent=self.parent, row_id=start_row_settings_01+8, column_id=38, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Threshold", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_13 = SE(
                parent=self.parent, row_id=start_row_settings_01+9, column_id=38, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE,fontsize="sans 10 bold")
            lbl_ma_setting_14 = SE(
                parent=self.parent, row_id=start_row_settings_01+10, column_id=38, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_15 = SE(
                parent=self.parent, row_id=start_row_settings_01+11, column_id=38, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Additional Information)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_16 = SE(
                parent=self.parent, row_id=start_row_settings_01+12, column_id=38, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Author", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_17 = SE(
                parent=self.parent, row_id=start_row_settings_01+13, column_id=38, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Source ID", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_22 = SE(
                parent=self.parent, row_id=start_row_settings_01+5, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_23 = SE(
                parent=self.parent, row_id=start_row_settings_01+6, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_24 = SE(
                parent=self.parent, row_id=start_row_settings_01+7, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Concentration (ppm)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_25 = SE(
                parent=self.parent, row_id=0, column_id=start_col_iso+12, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Ionization", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_26 = SE(
                parent=self.parent, row_id=start_row_settings_01+3, column_id=38, n_rows=1, n_columns=12,
                fg=self.green_light, bg=self.green_dark).create_simple_label(
                text="Assemblage Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_27 = SE(
                parent=self.parent, row_id=start_row_settings_01+4, column_id=38, n_rows=1, n_columns=6,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_28 = SE(
                parent=self.parent, row_id=start_row_settings_01+5, column_id=38, n_rows=1, n_columns=6,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_29 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 1, column_id=38, n_rows=1, n_columns=12,
                fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Dwell Time Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_ma_setting_30 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 2, column_id=38, n_rows=1, n_columns=6,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Dwell Times", relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            self.container_elements["ma_setting"]["Label"].extend(
                [lbl_ma_setting_01, lbl_ma_setting_02, lbl_ma_setting_03, lbl_ma_setting_04, lbl_ma_setting_05,
                 lbl_ma_setting_06, lbl_ma_setting_07, lbl_ma_setting_08, lbl_ma_setting_09, lbl_ma_setting_10,
                 lbl_ma_setting_11, lbl_ma_setting_12, lbl_ma_setting_13, lbl_ma_setting_14, lbl_ma_setting_15,
                 lbl_ma_setting_16, lbl_ma_setting_17, lbl_ma_setting_18, lbl_ma_setting_19, lbl_ma_setting_20,
                 lbl_ma_setting_21, lbl_ma_setting_22, lbl_ma_setting_23, lbl_ma_setting_24, lbl_ma_setting_25,
                 lbl_ma_setting_26, lbl_ma_setting_27, lbl_ma_setting_28, lbl_ma_setting_29, lbl_ma_setting_30])
            #
            # Ionization Energy
            self.var_entr_10 = tk.StringVar()
            self.container_var["settings"]["Ionization Energy"] = self.var_entr_10
            entr_10 = SE(
                parent=self.parent, row_id=int(1+ len(self.list_isotopes)), column_id=start_col_iso+12, n_rows=1,
                n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_entry(var=self.var_entr_10, text_default="15.760")
            #
            gui_categories = ["Label", "Button", "Option Menu", "Entry", "Frame", "Radiobutton", "Checkbox", "Listbox",
                              "Canvas"]
            #
            if self.window_created["ma_setting"] == False:
                ##################
                # STANDARD FILES #
                ##################
                if len(self.list_std) > 0:
                    for index, file in enumerate(self.list_std):
                        #
                        parts = file.split("/")
                        filename_short = parts[-1]
                        #
                        self.container_gui[filename_short] = {}
                        for gui_category in gui_categories:
                            self.container_gui[filename_short][gui_category] = {}
                            self.container_gui[filename_short][gui_category]["General"] = []
                            self.container_gui[filename_short][gui_category]["Specific"] = []
                        #
                        self.container_helper["limits BG"][file] = {}
                        self.container_helper["limits BG"][file]["ID"] = []
                        self.container_helper["limits BG"][file]["type"] = []
                        self.container_helper["limits SIG"][file] = {}
                        self.container_helper["limits SIG"][file]["ID"] = []
                        self.container_helper["limits SIG"][file]["type"] = []
                        self.container_helper["limits SPK"][file] = {}
                        self.container_helper["limits SPK"][file]["ID"] = []
                        self.container_helper["limits SPK"][file]["type"] = []
                        self.container_helper["limits SPK"][file]["info"] = []
                        self.container_helper["limits BG Ratio"][file] = {}
                        self.container_helper["limits BG Ratio"][file]["ID"] = []
                        self.container_helper["limits BG Ratio"][file]["type"] = []
                        self.container_helper["limits SIG Ratio"][file] = {}
                        self.container_helper["limits SIG Ratio"][file]["ID"] = []
                        self.container_helper["limits SIG Ratio"][file]["type"] = []
                        self.container_helper["limits SPK Ratio"][file] = {}
                        self.container_helper["limits SPK Ratio"][file]["ID"] = []
                        self.container_helper["limits SPK Ratio"][file]["type"] = []
                        self.container_helper["limits SPK Ratio"][file]["info"] = []
                        self.container_helper["positions"]["SPK"][filename_short] = []
                        self.spikes_isotopes["STD"][filename_short] = {}
                        if self.file_loaded is False:
                            self.container_var["STD"][file] = {}
                            self.container_var["STD"][file]["IS"] = tk.StringVar()
                            self.container_var["STD"][file]["IS"].set("Select IS")
                            self.container_var["STD"][file]["ID"] = tk.StringVar()
                            self.container_var["STD"][file]["ID"].set("A")
                        #
                        categories = ["FIG", "AX", "CANVAS", "TOOLBARFRAME", "CANVAS_RATIO", "TOOLBARFRAME_RATIO"]
                        self.container_diagrams["STD"][filename_short] = {}
                        self.container_listboxes["STD"][filename_short] = {}
                        self.diagrams_setup["STD"][filename_short] = {}
                        for category in categories:
                            self.container_diagrams["STD"][filename_short][category] = None
                            self.diagrams_setup["STD"][filename_short][category] = None
                        categories = ["Time Signal Raw", "Time Signal Smoothed", "Histogram", "Scatter", "Time Ratio"]
                        for category in categories:
                            self.diagrams_setup["STD"][filename_short][category] = {}
                        categories = ["BG", "SIG", "SPK", "ISORAT"]
                        for category in categories:
                            self.container_listboxes["STD"][filename_short][category] = None
                        #
                        self.container_report[filename_short] = {}
                        self.container_report[filename_short]["Mean"] = {}
                        self.container_report[filename_short]["Error"] = {}
                        categories_02 = ["Intensity Ratio", "Sensitivity", "Concentration", "RSF", "LOD"]
                        for category_02 in categories_02:
                            self.container_report[filename_short]["Mean"][category_02] = {}
                            self.container_report[filename_short]["Error"][category_02] = {}
                            self.container_report[filename_short]["Mean"][category_02]["filename"] = filename_short
                            self.container_report[filename_short]["Error"][category_02]["filename"] = filename_short
                        #
                        if len(self.container_lists["STD"]["Long"]) < len(self.list_std):
                            self.container_lists["STD"]["Long"].append(file)
                            self.container_lists["STD"]["Short"].append(filename_short)
                            self.container_helper["STD"][filename_short] = {}
                            self.container_helper["STD"][filename_short]["BG"] = {}
                            self.container_helper["STD"][filename_short]["SIG"] = {}
                            self.container_helper["STD"][filename_short]["SPK"] = {}
                        if filename_short not in self.container_files["STD"]:
                            self.container_files["STD"][filename_short] = {}
                            self.container_files["STD"][filename_short]["SRM"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["IS"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["ID"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["ID"].set("A")
                            self.container_files["STD"][filename_short]["Plot"] = False
                            self.container_files["STD"][filename_short]["Time Signal Plot"] = None
                            self.container_files["STD"][filename_short]["Histogram Plot"] = None
                            self.container_files["STD"][filename_short]["Scatter Plot"] = None
                            self.container_files["STD"][filename_short]["Time Ratio Plot"] = None
                            self.container_files["STD"][filename_short]["BG"] = {}
                            self.container_files["STD"][filename_short]["SIG"] = {}
                            self.container_files["STD"][filename_short]["SPK"] = {}
                            #
                            self.container_var["plotting"][filename_short] = {}
                            self.container_var["plotting"][filename_short]["Entry"] = {}
                            self.container_var["plotting"][filename_short]["Entry"]["Start"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                            self.container_var["plotting"][filename_short]["Entry"]["End"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                            self.container_var["plotting"][filename_short]["Checkboxes"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "BG"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "SIG"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "SPK"] = tk.IntVar()
                            #
                            self.container_helper["positions"]["BG STD"][filename_short] = []
                            self.container_helper["positions"]["SIG STD"][filename_short] = []
                            self.container_helper["positions"]["SPK STD"][filename_short] = []
                            #
                        #
                        if file not in self.container_var["SRM"] and self.file_loaded is False:
                            self.container_var["SRM"][file] = tk.StringVar()
                            self.container_var["SRM"][file].set("Select SRM")
                        #
                        lbl_std = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std, n_rows=1, n_columns=8,
                            fg=self.green_light, bg=self.green_medium).create_simple_label(
                            text=filename_short, relief=tk.GROOVE, fontsize="sans 10 bold")
                        #
                        self.container_elements["ma_setting"]["Label"].append(lbl_std)
                        #
                        btn_ma_setting_std = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+25, n_rows=1, n_columns=3,
                            fg=self.green_dark, bg=self.green_medium).create_simple_button(
                            text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                            command=lambda filename=self.list_std[index]: self.sub_minerlanalysis_plotting(filename))
                        self.container_elements["ma_setting"]["Button"].append(btn_ma_setting_std)
                        #
                        frm_std = SE(parent=self.parent, row_id=1+index, column_id=start_col_std+28, n_rows=1,
                                     n_columns=1, fg=self.green_light, bg=self.sign_red).create_frame()
                        #
                        self.container_elements["ma_setting"]["Frame"].append(frm_std)
                        self.container_var["STD"][file]["Frame"] = frm_std
                        #
                        ## Option Menus
                        # Standard Reference Material
                        if self.container_var["SRM"][file].get() != "Select SRM":
                            var_text = self.container_var["SRM"][file].get()
                            self.container_files["STD"][filename_short]["SRM"].set(var_text)
                        else:
                            var_text = "Select SRM"
                        opt_menu_srm = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+8, n_rows=1, n_columns=9,
                            fg=self.green_dark, bg=self.green_medium).create_option_srm(
                            var_srm=self.container_var["SRM"][file],text_set=var_text, fg_active=self.green_dark,
                            bg_active=self.red_dark, command=lambda var_srm=self.container_var["SRM"][file], file=file:
                            self.change_srm_std(var_srm, file))
                        #
                        self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_srm)
                        #
                        # Internal Standard
                        if self.container_var["STD"][file]["IS"].get() != "Select IS":
                            var_text = self.container_var["STD"][file]["IS"].get()
                        else:
                            var_text = "Select IS"
                        opt_menu_std = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+17, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["STD"][file]["IS"], option_list=self.list_isotopes,
                            text_set=var_text, fg_active=self.green_dark, bg_active=self.red_dark,
                            command=lambda element=self.container_var["STD"][file]["IS"], file=file:
                            self.change_std_is(element, file))
                        #
                        self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_std)
                        self.container_optionmenu["STD"][file] = opt_menu_std
                        #
                        # Sample ID
                        if self.container_var["STD"][file]["ID"].get() != "A":
                            var_text = self.container_var["STD"][file]["ID"].get()
                        else:
                            var_text = "A"
                        opt_menu_std_id = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+21, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["STD"][file]["ID"], option_list=self.list_alphabet,
                            text_set=var_text, fg_active=self.green_dark, bg_active=self.red_dark,
                            command=lambda var_id=self.container_var["STD"][file]["ID"], filename=file,
                                           filetype="STD": self.change_id_file(var_id, filename, filetype))
                        #
                        self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_std_id)
                    #
                if len(self.list_smpl) > 0:
                    for index, file in enumerate(self.list_smpl):
                        #
                        parts = file.split("/")
                        filename_short = parts[-1]
                        #
                        self.container_gui[filename_short] = {}
                        for gui_category in gui_categories:
                            self.container_gui[filename_short][gui_category] = {}
                            self.container_gui[filename_short][gui_category]["General"] = []
                            self.container_gui[filename_short][gui_category]["Specific"] = []
                        #
                        self.container_helper["limits BG"][file] = {}
                        self.container_helper["limits BG"][file]["ID"] = []
                        self.container_helper["limits BG"][file]["type"] = []
                        self.container_helper["limits SIG"][file] = {}
                        self.container_helper["limits SIG"][file]["ID"] = []
                        self.container_helper["limits SIG"][file]["type"] = []
                        self.container_helper["limits SPK"][file] = {}
                        self.container_helper["limits SPK"][file]["ID"] = []
                        self.container_helper["limits SPK"][file]["type"] = []
                        self.container_helper["limits SPK"][file]["info"] = []
                        self.container_helper["limits BG Ratio"][file] = {}
                        self.container_helper["limits BG Ratio"][file]["ID"] = []
                        self.container_helper["limits BG Ratio"][file]["type"] = []
                        self.container_helper["limits SIG Ratio"][file] = {}
                        self.container_helper["limits SIG Ratio"][file]["ID"] = []
                        self.container_helper["limits SIG Ratio"][file]["type"] = []
                        self.container_helper["limits SPK Ratio"][file] = {}
                        self.container_helper["limits SPK Ratio"][file]["ID"] = []
                        self.container_helper["limits SPK Ratio"][file]["type"] = []
                        self.container_helper["limits SPK Ratio"][file]["info"] = []
                        self.container_helper["positions"]["SPK"][filename_short] = []
                        self.spikes_isotopes["SMPL"][filename_short] = {}
                        if self.file_loaded is False:
                            self.container_var["SMPL"][file] = {}
                            self.container_var["SMPL"][file]["IS"] = tk.StringVar()
                            self.container_var["SMPL"][file]["IS"].set("Select IS")
                            self.container_var["SMPL"][file]["ID"] = tk.StringVar()
                            self.container_var["SMPL"][file]["ID"].set("B")
                        #
                        categories = ["FIG", "AX", "CANVAS", "TOOLBARFRAME", "CANVAS_RATIO", "TOOLBARFRAME_RATIO"]
                        self.container_diagrams["SMPL"][filename_short] = {}
                        self.diagrams_setup["SMPL"][filename_short] = {}
                        self.container_listboxes["SMPL"][filename_short] = {}
                        for category in categories:
                            self.container_diagrams["SMPL"][filename_short][category] = None
                            self.diagrams_setup["SMPL"][filename_short][category] = None
                        categories = ["Time Signal Raw", "Time Signal Smoothed", "Histogram", "Scatter", "Time Ratio"]
                        for category in categories:
                            self.diagrams_setup["SMPL"][filename_short][category] = {}
                        categories = ["BG", "SIG", "SPK", "ISORAT"]
                        for category in categories:
                            self.container_listboxes["SMPL"][filename_short][category] = None
                        #
                        self.container_report[filename_short] = {}
                        self.container_report[filename_short]["Mean"] = {}
                        self.container_report[filename_short]["Error"] = {}
                        categories_02 = ["Intensity Ratio", "Sensitivity", "Concentration", "RSF", "LOD"]
                        for category_02 in categories_02:
                            self.container_report[filename_short]["Mean"][category_02] = {}
                            self.container_report[filename_short]["Error"][category_02] = {}
                            self.container_report[filename_short]["Mean"][category_02]["filename"] = filename_short
                            self.container_report[filename_short]["Error"][category_02]["filename"] = filename_short
                        #
                        if len(self.container_lists["SMPL"]["Long"]) < len(self.list_smpl):
                            self.container_lists["SMPL"]["Long"].append(file)
                            self.container_lists["SMPL"]["Short"].append(filename_short)
                            self.container_helper["SMPL"][filename_short] = {}
                            self.container_helper["SMPL"][filename_short]["BG"] = {}
                            self.container_helper["SMPL"][filename_short]["SIG"] = {}
                            self.container_helper["SMPL"][filename_short]["SPK"] = {}
                        if filename_short not in self.container_files["SMPL"]:
                            self.container_files["SMPL"][filename_short] = {}
                            self.container_files["SMPL"][filename_short]["SRM"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["IS"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["IS Concentration"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["ID"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["ID"].set("B")
                            self.container_files["SMPL"][filename_short]["Plot"] = False
                            self.container_files["SMPL"][filename_short]["Time Signal Plot"] = None
                            self.container_files["SMPL"][filename_short]["Histogram Plot"] = None
                            self.container_files["SMPL"][filename_short]["Scatter Plot"] = None
                            self.container_files["SMPL"][filename_short]["Time Ratio Plot"] = None
                            self.container_files["SMPL"][filename_short]["BG"] = {}
                            self.container_files["SMPL"][filename_short]["SIG"] = {}
                            self.container_files["SMPL"][filename_short]["SPK"] = {}
                            #
                            self.container_var["plotting"][filename_short] = {}
                            self.container_var["plotting"][filename_short]["Entry"] = {}
                            self.container_var["plotting"][filename_short]["Entry"]["Start"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                            self.container_var["plotting"][filename_short]["Entry"]["End"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                            self.container_var["plotting"][filename_short]["Checkboxes"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "BG"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "SIG"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "SPK"] = tk.IntVar()
                        #
                        lbl_smpl = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl, n_rows=1, n_columns=8,
                            fg=self.green_light, bg=self.green_medium).create_simple_label(
                            text=filename_short, relief=tk.GROOVE, fontsize="sans 10 bold")
                        #
                        self.container_elements["ma_setting"]["Label"].append(lbl_smpl)
                        #
                        btn_ma_setting_smpl = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl+16, n_rows=1, n_columns=3,
                            fg=self.green_dark, bg=self.green_medium).create_simple_button(
                            text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                            command=lambda filename=self.list_smpl[index]: self.sub_minerlanalysis_plotting(filename))
                        #
                        self.container_elements["ma_setting"]["Button"].append(btn_ma_setting_smpl)
                        #
                        frm_smpl = SE(parent=self.parent, row_id=1+index, column_id=start_col_smpl+19, n_rows=1,
                                      n_columns=1, fg=self.green_light, bg=self.sign_red).create_frame()
                        #
                        self.container_elements["ma_setting"]["Frame"].append(frm_smpl)
                        self.container_var["SMPL"][file]["Frame"] = frm_smpl
                        #
                        ## Option Menus
                        self.container_var["isotopes"][file] = tk.StringVar()
                        #self.container_var["SMPL"][file]["IS"] = tk.StringVar()
                        # Internal Standard
                        if self.container_var["SMPL"][file]["IS"].get() != "Select IS":
                            var_text = self.container_var["SMPL"][file]["IS"].get()
                        else:
                            var_text = "Select IS"
                        opt_menu_iso = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl+8, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["SMPL"][file]["IS"], option_list=self.list_isotopes,
                            text_set=var_text, fg_active=self.green_dark,  bg_active=self.red_dark,
                            command=lambda element=self.container_var["SMPL"][file]["IS"], file=file,
                                           mineral=self.container_var["mineral"].get():
                            self.change_smpl_is(element, file, mineral))
                        #
                        self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_iso)
                        self.container_optionmenu["SMPL"][file] = opt_menu_iso
                        #
                        # Sample ID
                        if self.container_var["SMPL"][file]["ID"].get() != "B":
                            var_text = self.container_var["SMPL"][file]["ID"].get()
                        else:
                            var_text = "B"
                        opt_menu_smpl_id = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl+12, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["SMPL"][file]["ID"], option_list=self.list_alphabet,
                            text_set=var_text, fg_active=self.green_dark, bg_active=self.red_dark,
                            command=lambda var_id=self.container_var["SMPL"][file]["ID"], filename=file,
                                           filetype="SMPL": self.change_id_file(var_id, filename, filetype))
                        #
                        self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_smpl_id)
                        #
                if len(self.list_std) > 0 or len(self.list_smpl) > 0:
                    if len(self.list_isotopes) < 20:
                        for index, isotope in enumerate(self.list_isotopes):
                            self.container_results["STD"]["RAW"][isotope] = {}
                            self.container_results["STD"]["SMOOTHED"][isotope] = {}
                            self.container_results["SMPL"]["RAW"][isotope] = {}
                            self.container_results["SMPL"]["SMOOTHED"][isotope] = {}
                            #
                            self.container_var["dwell_times"]["Entry"][isotope] = tk.StringVar()
                            self.container_var["dwell_times"]["Entry"][isotope].set("0.01")
                            #
                            ## Labels
                            rgb = mcolors.to_rgb(self.isotope_colors[isotope])
                            brightness = np.sqrt(0.299*(rgb[0] * 255)**2 + 0.587*(rgb[1]*255)**2 + 0.114*(rgb[2]*255)**2)
                            if brightness < 128:
                                color_fg = "white"
                            else:
                                color_fg = "black"
                            # LABELS
                            lbl_iso = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso, fg=color_fg, n_rows=1,
                                n_columns=3, bg=self.isotope_colors[isotope]).create_simple_label(
                                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
                            #
                            key_element = re.search("(\D+)(\d+)", isotope)
                            element = key_element.group(1)
                            self.container_var["charge"][isotope] = {"textvar": tk.StringVar()}
                            #
                            if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                                self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.red_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            else:
                                self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.blue_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            #
                            self.container_elements["ma_setting"]["Label"].extend([lbl_iso, lbl_charge])
                            #
                            ## Frame
                            # frm_iso = SE(
                            #     parent=self.parent, row_id=1+index, column_id=start_col_iso+16, n_rows=1, n_columns=6,
                            #     fg=self.blue_light, bg=self.isotope_colors[isotope]).create_frame(
                            #     relief=tk.GROOVE)
                            # self.container_elements["ma_setting"]["Frame"].append(frm_iso)
                            ## Option Menus
                            # Standard Reference Material
                            self.container_var["SRM"][isotope] = tk.StringVar()
                            if self.container_var["SRM"]["default"][0].get() != "Select SRM":
                                var_text = self.container_var["SRM"]["default"][0].get()
                                self.container_files["SRM"][isotope].set(var_text)
                            else:
                                var_text = "Select SRM"
                            opt_menu_srm = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso+3, n_rows=1, n_columns=9,
                                fg=self.green_dark, bg=self.green_medium).create_option_srm(
                                var_srm=self.container_var["SRM"][isotope], text_set=var_text, fg_active=self.green_dark,
                                bg_active=self.red_dark,
                                command=lambda var_srm=self.container_var["SRM"][isotope], isotope=isotope:
                                self.change_srm_iso(var_srm, isotope))
                            #
                            self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_srm)
                            #
                    else:
                        for index, isotope in enumerate(self.list_isotopes):
                            self.container_results["STD"]["RAW"][isotope] = {}
                            self.container_results["STD"]["SMOOTHED"][isotope] = {}
                            self.container_results["SMPL"]["RAW"][isotope] = {}
                            self.container_results["SMPL"]["SMOOTHED"][isotope] = {}
                            ## Labels
                            rgb = mcolors.to_rgb(self.isotope_colors[isotope])
                            brightness = np.sqrt(0.299*(rgb[0]*255)**2 + 0.587*(rgb[1]*255)**2 + 0.114*(rgb[2]*255)**2)
                            if brightness < 128:
                                color_fg = "white"
                            else:
                                color_fg = "black"
                            # LABELS
                            lbl_iso = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso, fg=color_fg, n_rows=1,
                                n_columns=3, bg=self.isotope_colors[isotope]).create_simple_label(
                                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
                            #
                            key_element = re.search("(\D+)(\d+)", isotope)
                            element = key_element.group(1)
                            self.container_var["charge"][isotope] = {"textvar": tk.StringVar()}
                            #
                            if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                                self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.red_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            else:
                                self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.blue_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            self.container_elements["ma_setting"]["Label"].extend([lbl_iso, lbl_charge])
                            ## Frame
                            # frm_iso = SE(
                            #     parent=self.parent, row_id=2+index, column_id=start_col_iso+12, n_rows=1, n_columns=4,
                            #     fg=self.blue_light, bg=self.isotope_colors[isotope]).create_frame(
                            #     relief=tk.GROOVE)
                            # self.container_elements["ma_setting"]["Frame"].append(frm_iso)
                            ## Option Menus
                            self.container_var["SRM"][isotope] = tk.StringVar()
                            if self.container_var["SRM"]["default"][0].get() != "Select SRM":
                                var_text = self.container_var["SRM"]["default"][0].get()
                                self.container_files["SRM"][isotope].set(var_text)
                            else:
                                var_text = "Select SRM"
                            opt_menu_srm = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso+3, n_rows=1, n_columns=9,
                                fg=self.green_dark, bg=self.green_medium).create_option_srm(
                                var_srm=self.container_var["SRM"][isotope], text_set=var_text, fg_active=self.green_dark,
                                bg_active=self.red_dark,
                                command=lambda var_srm=self.container_var["SRM"][isotope], isotope=isotope:
                                self.change_srm_iso(var_srm, isotope))
                            #
                            self.container_elements["ma_setting"]["Option Menu"].append(opt_menu_srm)
                #
                ## Buttons
                btn_std_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+9, column_id=44, n_rows=1, n_columns=6, fg=self.green_dark,
                    bg=self.green_medium).create_simple_button(
                    text="Apply to all", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=lambda filetype="STD": self.fast_track(filetype))
                btn_smpl_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+10, column_id=44, n_rows=1, n_columns=6, fg=self.green_dark,
                    bg=self.green_medium).create_simple_button(
                    text="Apply to all", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=lambda filetype="SMPL": self.fast_track(filetype))
                btn_is_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+4, column_id=21, n_rows=1, n_columns=8, fg=self.green_dark,
                    bg=self.green_medium).create_simple_button(
                    text="Load IS Data", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=self.import_concentration_data)
                btn_dwell = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 2, column_id=44, n_rows=1, n_columns=6,
                    fg=self.green_dark,
                    bg=self.green_medium).create_simple_button(
                    text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=self.create_dwell_time_window)
                #
                self.container_elements["ma_setting"]["Button"].extend([btn_std_01, btn_smpl_01, btn_is_01, btn_dwell])
                #
                ## Entries
                # Element concentration
                self.var_entr_09, self.entr_09 = SE(
                    parent=self.parent, row_id=start_row_settings_01+7, column_id=29, n_rows=1, n_columns=9, fg=self.green_light,
                    bg=self.green_dark).create_simple_entries(command=None)
                self.container_var["settings"]["IS Concentration"] = self.var_entr_09
                # Time Interval Background
                if self.container_var["settings"]["Time BG Start"].get() != "Set start time":
                    var_text = self.container_var["settings"]["Time BG Start"].get()
                else:
                    var_text = "Set start time"
                entr_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+9, column_id=29, n_rows=1, n_columns=9, fg=self.green_light,
                    bg=self.green_dark).create_simple_entry(
                    var=self.container_var["settings"]["Time BG Start"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["settings"]["Time BG Start"], times=self.times,
                                   category_01="MA", category_02="Start BG":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                if self.container_var["settings"]["Time BG End"].get() != "Set end time":
                    var_text = self.container_var["settings"]["Time BG End"].get()
                else:
                    var_text = "Set end time"
                entr_02 = SE(
                    parent=self.parent, row_id=start_row_settings_01+10, column_id=29, n_rows=1, n_columns=9, fg=self.green_light,
                    bg=self.green_dark).create_simple_entry(
                    var=self.container_var["settings"]["Time BG End"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["settings"]["Time BG End"], times=self.times,
                                   category_01="MA", category_02="End BG":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                # Time Interval Signal
                if self.container_var["settings"]["Time SIG Start"].get() != "Set start time":
                    var_text = self.container_var["settings"]["Time SIG Start"].get()
                else:
                    var_text = "Set end time"
                entr_03 = SE(
                    parent=self.parent, row_id=start_row_settings_01+12, column_id=29, n_rows=1, n_columns=9, fg=self.green_light,
                    bg=self.green_dark).create_simple_entry(
                    var=self.container_var["settings"]["Time SIG Start"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["settings"]["Time SIG Start"], times=self.times,
                                   category_01="MA",  category_02="Start SIG":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                if self.container_var["settings"]["Time SIG End"].get() != "Set end time":
                    var_text = self.container_var["settings"]["Time SIG End"].get()
                else:
                    var_text = "Set end time"
                entr_04 = SE(
                    parent=self.parent, row_id=start_row_settings_01+13, column_id=29, n_rows=1, n_columns=9, fg=self.green_light,
                    bg=self.green_dark).create_simple_entry(
                    var=self.container_var["settings"]["Time SIG End"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["settings"]["Time SIG End"], times=self.times,
                                   category_01="MA", category_02="End SIG":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                # Deviation and Threshold
                var_entr_05 = tk.StringVar()
                self.container_var["settings"]["SE Deviation"] = var_entr_05
                entr_05 = SE(parent=self.parent, row_id=start_row_settings_01+7, column_id=44, n_rows=1, n_columns=6,
                             fg=self.green_light, bg=self.green_dark).create_simple_entry(var=var_entr_05, text_default="10",
                                                                                          command=lambda event, var=var_entr_05, category_01="MA",
                                                                                                         category_02="Deviation": self.set_entry_value(var, category_01, category_02, event))
                var_entr_06 = tk.StringVar()
                self.container_var["settings"]["SE Threshold"] = var_entr_06
                entr_06 = SE(parent=self.parent, row_id=start_row_settings_01+8, column_id=44, n_rows=1, n_columns=6,
                             fg=self.green_light, bg=self.green_dark).create_simple_entry(var=var_entr_06,
                                                                                          text_default="1000",
                                                                                          command=lambda event, var=var_entr_06, category_01="MA",
                                                                                                         category_02="Threshold": self.set_entry_value(var, category_01, category_02, event))
                # Author and Source ID
                var_entr_07 = tk.StringVar()
                self.container_var["settings"]["Author"] = var_entr_07
                entr_07 = SE(parent=self.parent, row_id=start_row_settings_01+12, column_id=44, n_rows=1, n_columns=6,
                             fg=self.green_light, bg=self.green_dark).create_simple_entry(var=var_entr_07, text_default="J. Doe",
                                                                                          command=lambda event, var=var_entr_07, category_01="MA",
                                                                                                         category_02="Author": self.set_entry_value(var, category_01, category_02, event))
                var_entr_08 = tk.StringVar()
                self.container_var["settings"]["Source ID"] = var_entr_08
                entr_08 = SE(parent=self.parent, row_id=start_row_settings_01+13, column_id=44, n_rows=1, n_columns=6,
                             fg=self.green_light, bg=self.green_dark).create_simple_entry(var=var_entr_08, text_default="RUR01",
                                                                                          command=lambda event, var=var_entr_08, category_01="MA",
                                                                                                         category_02="Source ID": self.set_entry_value(var, category_01, category_02, event))
                #
                self.container_elements["ma_setting"]["Entry"].extend([
                    entr_01, entr_02, entr_03, entr_04, entr_05, entr_06, entr_07, entr_08, self.entr_09, entr_10])
                self.container_var["ma_setting"].extend([
                    self.container_var["settings"]["Time BG Start"], self.container_var["settings"]["Time BG End"],
                    self.container_var["settings"]["Time SIG Start"], self.container_var["settings"]["Time SIG End"],
                    var_entr_05, var_entr_06, var_entr_07, var_entr_08, self.var_entr_09, self.var_entr_10])
                #
                ## Option Menus
                if self.container_var["SRM"]["default"][0].get() != "Select SRM":
                    var_text = self.container_var["SRM"]["default"][0].get()
                else:
                    var_text = "Select SRM"
                #
                opt_menu_srm_default_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+1, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_srm(
                    var_srm=self.container_var["SRM"]["default"][0], text_set=var_text, fg_active=self.green_dark,
                    bg_active=self.red_dark, command=lambda var_srm=self.container_var["SRM"]["default"][0]:
                    self.change_srm_default(var_srm))
                opt_menu_srm_default_02 = SE(
                    parent=self.parent, row_id=start_row_settings_01+2, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_srm(
                    var_srm=self.container_var["SRM"]["default"][1], text_set=var_text, fg_active=self.green_dark,
                    bg_active=self.red_dark, command=lambda var_srm=self.container_var["SRM"]["default"][1]:
                    self.change_srm_default(var_srm, key="isotope"))
                if self.container_var["mineral"].get() != "Select Mineral":
                    var_text = self.container_var["mineral"].get()
                else:
                    var_text = "Select Mineral"
                opt_menu_mineral = SE(
                    parent=self.parent, row_id=start_row_settings_01+4, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_mineral(
                    var_min=self.container_var["mineral"], text_set=var_text, fg_active=self.green_dark,
                    bg_active=self.red_dark, option_list=self.mineral_list,
                    command=lambda var_min=self.container_var["mineral"]: self.select_mineral_is(var_min))
                if self.container_var["IS"]["Default STD"].get() != "Select IS":
                    var_text = self.container_var["IS"]["Default STD"].get()
                else:
                    var_text = "Select IS"
                self.opt_is_std_def = SE(
                    parent=self.parent, row_id=start_row_settings_01+5, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["IS"]["Default STD"], option_list=self.list_isotopes, text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda element=self.container_var["IS"]["Default STD"],
                                   mineral=self.container_var["mineral"].get(): self.change_std_is_default(element,
                                                                                                           mineral))
                if self.container_var["IS"]["Default SMPL"].get() != "Select IS":
                    var_text = self.container_var["IS"]["Default SMPL"].get()
                else:
                    var_text = "Select IS"
                self.opt_is_smpl_def = SE(
                    parent=self.parent, row_id=start_row_settings_01+6, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["IS"]["Default SMPL"], option_list=self.list_isotopes, text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda element=self.container_var["IS"]["Default SMPL"],
                                   mineral=self.container_var["mineral"].get(): self.change_smpl_is_default(element,
                                                                                                            mineral))
                #
                list_opt_gas = ["Helium", "Neon", "Argon", "Krypton", "Xenon", "Radon"]
                opt_laser = SE(
                    parent=self.parent, row_id=int(1 + len(self.list_isotopes)), column_id=start_col_iso, n_rows=1,
                    n_columns=12, fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["LASER"], option_list=list_opt_gas, text_set="Argon",
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda var_opt=self.container_var["LASER"]: self.change_carrier_gas(var_opt))
                #
                self.container_elements["ma_setting"]["Option Menu"].extend([opt_menu_srm_default_01, opt_menu_srm_default_02,
                                                                             opt_menu_mineral, self.opt_is_std_def,
                                                                             self.opt_is_smpl_def, opt_laser])
                #
                if self.container_var["ID"]["Default STD"].get() != "A":
                    var_text = self.container_var["ID"]["Default STD"].get()
                else:
                    var_text = "A"
                self.opt_id_std_def = SE(
                    parent=self.parent, row_id=start_row_settings_01+4, column_id=44, n_rows=1, n_columns=6,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["ID"]["Default STD"], option_list=self.list_alphabet, text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda var_id=self.container_var["ID"]["Default STD"],
                                   filetype="STD": self.change_id_default(var_id, filetype))
                #
                if self.container_var["ID"]["Default SMPL"].get() != "B":
                    var_text = self.container_var["ID"]["Default SMPL"].get()
                else:
                    var_text = "B"
                self.opt_id_smpl_def = SE(
                    parent=self.parent, row_id=start_row_settings_01+5, column_id=44, n_rows=1, n_columns=6,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["ID"]["Default SMPL"], option_list=self.list_alphabet, text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda var_id=self.container_var["ID"]["Default SMPL"],
                                   filetype="SMPL": self.change_id_default(var_id, filetype))
                #
                self.container_elements["ma_setting"]["Option Menu"].extend([self.opt_id_std_def, self.opt_id_smpl_def])
                #
                ## ADDITIONAL OPERATIONS DUE TO FILE LOADING
                if self.file_loaded is True:
                    self.select_mineral_is(var_min=self.container_var["mineral"].get())
                #
                self.window_created["ma_setting"] = True
        else:
            pass
    #
    def fast_track(self, filetype, mode="MA"):
        isotopes_spiked_list = [*self.list_isotopes]
        corrected_isotopes = []
        #
        if filetype == "STD":
            for file in self.list_std:
                parts = file.split("/")
                filename_short = parts[-1]
                #
                self.container_measurements["RAW"][filename_short] = {}
                self.container_measurements["EDITED"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short]["RAW"] = {}
                self.container_measurements["SELECTED"][filename_short]["SMOOTHED"] = {}
                #
                # self.container_diagrams["STD"][filename_short]["FIG"] = Figure(
                #     figsize=(10, 5), facecolor=self.green_light)
                # self.container_diagrams["STD"][filename_short]["AX"] = self.container_diagrams["STD"][filename_short][
                #     "FIG"].add_subplot()
                if self.diagrams_setup[filetype][filename_short]["FIG"] == None:
                    self.diagrams_setup[filetype][filename_short]["FIG"] = Figure(figsize=(10, 5),
                                                                                  facecolor=self.green_light)
                    self.diagrams_setup[filetype][filename_short]["AX"] = self.diagrams_setup[filetype][filename_short][
                        "FIG"].add_subplot()
                #
                df_data = self.load_and_assign_data(filename=file)
                times = df_data.iloc[:, 0]
                start_time = times.iloc[0]
                end_time = times.iloc[-1]
                start_index = times[times == start_time].index[0]
                end_index = times[times == end_time].index[0]
                spk_id = 1
                # box_spk = self.container_diagrams["STD"][filename_short]["AX"].axvspan(
                #     start_time, end_time, alpha=0.125, color=self.yellow_dark)
                box_spk = self.diagrams_setup[filetype][filename_short]["AX"].axvspan(
                    start_time, end_time, alpha=0.125, color=self.yellow_dark)
                isotope = "".join(self.list_isotopes)
                #
                self.container_measurements["RAW"][filename_short]["Time"] = times.tolist()
                self.container_measurements["EDITED"][filename_short]["Time"] = times.tolist()
                self.container_measurements["SELECTED"][filename_short]["Time"] = times.tolist()
                #
                self.container_helper["limits SPK"][file]["ID"].append(spk_id)
                self.container_helper["limits SPK"][file]["type"].append("custom")
                self.container_helper["limits SPK"][file]["info"].append([isotope, spk_id])
                self.container_helper["positions"]["SPK"][filename_short].append(
                    [round(start_time, 4), round(end_time, 4)])
                #
                for isotope in self.list_isotopes:
                    self.container_measurements["RAW"][filename_short][isotope] = df_data[isotope].tolist()
                    self.container_measurements["EDITED"][filename_short][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope] = {}
                    #
                    self.container_measurements["EDITED"][filename_short][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["BG"] = []
                    if mode == "MA":
                        self.container_measurements["EDITED"][filename_short][isotope]["SIG"] = []
                        self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["SIG"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["SIG"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["SIG"] = []
                        var_settings = "settings"
                    elif mode in ["FI", "MI"]:
                        self.container_measurements["EDITED"][filename_short][isotope]["MAT"] = []
                        self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["MAT"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["MAT"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["MAT"] = []
                        self.container_measurements["EDITED"][filename_short][isotope]["INCL"] = []
                        self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["INCL"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["INCL"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["INCL"] = []
                        if mode == "FI":
                            var_settings = "fi_setting"
                        elif mode == "MI":
                            var_settings = "mi_setting"
                    #
                    self.spikes_isotopes["STD"][filename_short][isotope] = []
                    self.spikes_isotopes["STD"][filename_short][isotope].append([start_index, end_index])
                    self.container_helper["STD"][filename_short]["SPK"][isotope] = {}
                    self.container_helper["STD"][filename_short]["SPK"][isotope][spk_id] = {
                        "Times": [round(start_time, 4), round(end_time, 4)],
                        "Positions": [start_index, end_index],
                        "Object": box_spk}
            #
            self.do_spike_elimination_all(file_type=filetype, settings=var_settings)
            self.fast_track_std = True
        #
        elif filetype == "SMPL":
            for file in self.list_smpl:
                parts = file.split("/")
                filename_short = parts[-1]
                #
                self.container_measurements["RAW"][filename_short] = {}
                self.container_measurements["EDITED"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short]["RAW"] = {}
                self.container_measurements["SELECTED"][filename_short]["SMOOTHED"] = {}
                #
                # self.container_diagrams["SMPL"][filename_short]["FIG"] = Figure(
                #     figsize=(10, 5), facecolor=self.green_light)
                # self.container_diagrams["SMPL"][filename_short]["AX"] = self.container_diagrams["SMPL"][filename_short][
                #     "FIG"].add_subplot()
                if self.diagrams_setup[filetype][filename_short]["FIG"] == None:
                    self.diagrams_setup["SMPL"][filename_short]["FIG"] = Figure(figsize=(10, 5), facecolor=self.green_light)
                    self.diagrams_setup["SMPL"][filename_short]["AX"] = self.diagrams_setup["SMPL"][filename_short][
                        "FIG"].add_subplot()
                #
                df_data = self.load_and_assign_data(filename=file)
                times = df_data.iloc[:, 0]
                start_time = times.iloc[0]
                end_time = times.iloc[-1]
                start_index = times[times == start_time].index[0]
                end_index = times[times == end_time].index[0]
                spk_id = 1
                # box_spk = self.container_diagrams["SMPL"][filename_short]["AX"].axvspan(
                #     start_time, end_time, alpha=0.125, color=self.yellow_dark)
                box_spk = self.diagrams_setup["SMPL"][filename_short]["AX"].axvspan(
                    start_time, end_time, alpha=0.125, color=self.yellow_dark)
                isotope = "".join(self.list_isotopes)
                #
                self.container_measurements["RAW"][filename_short]["Time"] = times.tolist()
                self.container_measurements["EDITED"][filename_short]["Time"] = times.tolist()
                self.container_measurements["SELECTED"][filename_short]["Time"] = times.tolist()
                #
                self.container_helper["limits SPK"][file]["ID"].append(spk_id)
                self.container_helper["limits SPK"][file]["type"].append("custom")
                self.container_helper["limits SPK"][file]["info"].append([isotope, spk_id])
                self.container_helper["positions"]["SPK"][filename_short].append(
                    [round(start_time, 4), round(end_time, 4)])
                #
                for isotope in self.list_isotopes:
                    self.container_measurements["RAW"][filename_short][isotope] = df_data[isotope].tolist()
                    self.container_measurements["EDITED"][filename_short][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope] = {}
                    #
                    self.container_measurements["EDITED"][filename_short][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["BG"] = []
                    if mode == "MA":
                        self.container_measurements["EDITED"][filename_short][isotope]["SIG"] = []
                        self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["SIG"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["SIG"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["SIG"] = []
                        var_settings="settings"
                    elif mode in ["FI", "MI"]:
                        self.container_measurements["EDITED"][filename_short][isotope]["MAT"] = []
                        self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["MAT"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["MAT"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["MAT"] = []
                        self.container_measurements["EDITED"][filename_short][isotope]["INCL"] = []
                        self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["INCL"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["INCL"] = []
                        self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["INCL"] = []
                        if mode == "FI":
                            var_settings = "fi_setting"
                        elif mode == "MI":
                            var_settings = "mi_setting"
                    #
                    self.spikes_isotopes["SMPL"][filename_short][isotope] = []
                    self.spikes_isotopes["SMPL"][filename_short][isotope].append([start_index, end_index])
                    self.container_helper["SMPL"][filename_short]["SPK"][isotope] = {}
                    self.container_helper["SMPL"][filename_short]["SPK"][isotope][spk_id] = {
                        "Times": [round(start_time, 4), round(end_time, 4)],
                        "Positions": [start_index, end_index],
                        "Object": box_spk}
            #
            self.do_spike_elimination_all(file_type=filetype, settings=var_settings)
            self.fast_track_smpl = True
    #
    def sub_minerlanalysis_plotting(self, filename):
        #
        if filename in self.list_std:
            self.file_type = "STD"
        elif filename in self.list_smpl:
            self.file_type = "SMPL"
        #
        ## Cleaning
        categories = ["SRM", "ma_setting"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
        #
        try:
            parts = filename.split("/")
            self.container_files[self.file_type][parts[-1]]["Time Signal Plot"].draw()
        except:
            pass
        #
        self.file = filename
        parts = filename.split("/")
        filename_short = parts[-1]
        self.filename_short = filename_short
        df_data = self.load_and_assign_data(filename=filename)
        self.times = df_data.iloc[:, 0]
        icp_measurements = np.array([[df_data[isotope] for isotope in self.list_isotopes]])
        x_max = np.amax(self.times)
        y_max = np.amax(icp_measurements)
        if self.container_files[self.file_type][filename_short]["Plot"] == False:
            self.bg_id = 0
            self.bg_idlist = []
            self.sig_id = 0
            self.sig_idlist = []
            self.spk_id = 0
            self.spk_idlist = []
            self.lines = {}
            self.lines["raw"] = {}
            self.lines["edited"] = {}
            self.lines["ratio"] = {}
            self.time_ratio_data = {}
            self.time_ratio_data[self.filename_short] = {}
            if filename_short not in self.container_helper["positions"]:
                self.container_helper["positions"]["BG"][filename_short] = []
                self.container_helper["positions"]["BG SMPL"] = {}
                self.container_helper["positions"]["BG SMPL"][filename_short] = []
                self.container_helper["positions"]["SIG"][filename_short] = []
                self.container_helper["positions"]["SIG SMPL"] = {}
                self.container_helper["positions"]["SIG SMPL"][filename_short] = []
                self.container_helper["positions"]["SPK"][filename_short] = []
                self.container_helper["positions"]["SPK SMPL"] = {}
                self.container_helper["positions"]["SPK SMPL"][filename_short] = []
                self.container_helper["positions"][filename_short] = []
                self.container_helper["indices"][filename_short] = []
            #
            if filename_short not in self.container_measurements["RAW"]:
                self.container_measurements["RAW"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short]["RAW"] = {}
                self.container_measurements["SELECTED"][filename_short]["SMOOTHED"] = {}
                self.container_measurements["EDITED"][filename_short] = {}
                self.container_measurements["RAW"]["Time"] = self.times.tolist()
                self.container_measurements["SELECTED"][filename_short]["Time"] = self.times.tolist()
                self.container_measurements["EDITED"]["Time"] = self.times.tolist()
                for isotope in self.list_isotopes:
                    self.container_measurements["RAW"][filename_short][isotope] = df_data[isotope].tolist()
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["SIG"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["SIG"] = []
                    self.container_measurements["EDITED"][filename_short][isotope] = {}
                    self.container_measurements["EDITED"][filename_short][isotope]["BG"] = []
                    self.container_measurements["EDITED"][filename_short][isotope]["SIG"] = []
            #
            ## FRAMES
            frm_bg = SE(parent=self.parent, row_id=29, column_id=21, n_rows=1, n_columns=12, fg=self.blue_light,
                        bg=self.blue_dark).create_frame(relief=tk.FLAT)
            frm_sig = SE(parent=self.parent, row_id=29, column_id=33, n_rows=1, n_columns=12, fg=self.brown_light,
                         bg=self.brown_dark).create_frame(relief=tk.FLAT)
            frm_spkelim = SE(parent=self.parent, row_id=29, column_id=45, n_rows=1, n_columns=12, fg=self.yellow_light,
                             bg=self.yellow_dark).create_frame(relief=tk.FLAT)
            frm_isorat = SE(parent=self.parent, row_id=29, column_id=57, n_rows=1, n_columns=12, fg=self.slate_grey_light,
                            bg=self.slate_grey_light).create_frame(relief=tk.FLAT)
            frm_spke_bg = SE(parent=self.parent, row_id=1, column_id=87, n_rows=1*len(self.list_isotopes), n_columns=2,
                             fg=self.yellow_medium, bg=self.yellow_medium).create_frame()
            self.container_elements["plotting"]["Frame"].extend([frm_bg, frm_sig, frm_spkelim, frm_isorat, frm_spke_bg])
            self.container_gui[filename_short]["Frame"]["General"].extend(
                [frm_bg, frm_sig, frm_spkelim, frm_isorat, frm_spke_bg])
            #
            ## LABELS
            # lbl_isorat = SE(parent=self.parent, row_id=30, column_id=51, n_rows=2, n_columns=6, fg=self.slate_grey_light,
            #                  bg=self.slate_grey_dark).create_simple_label(text="Isotope Ratios", relief=tk.GROOVE,
            #                                                          fontsize="sans 10 bold")
            lbl_file = SE(parent=self.parent, row_id=0, column_id=80, n_rows=1, n_columns=9, fg=self.green_light,
                          bg=self.green_dark).create_simple_label(text=filename_short, relief=tk.GROOVE,
                                                                  fontsize="sans 10 bold")
            lbl_spk = SE(
                parent=self.parent, row_id=33, column_id=66, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Spike Elimination", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_disply = SE(
                parent=self.parent, row_id=30, column_id=66, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Plot Selection", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_start = SE(
                parent=self.parent, row_id=36, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start (Time)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_end = SE(
                parent=self.parent, row_id=37, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End (Time)", relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            self.container_elements["plotting"]["Label"].extend(
                [lbl_file, lbl_spk, lbl_disply, lbl_start, lbl_end])
            self.container_gui[filename_short]["Label"]["General"].extend(
                [lbl_file, lbl_spk, lbl_disply, lbl_start, lbl_end])
            #
            ## ENTRY
            #
            entr_start = SE(
                parent=self.parent, row_id=36, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_entry(
                var=self.container_var["plotting"][filename_short]["Entry"]["Start"], text_default="0.0",
                command=lambda event, filename_short=filename_short, var_key="Start":
                self.set_integration_window(filename_short, var_key, event))
            entr_end = SE(
                parent=self.parent, row_id=37, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_entry(
                var=self.container_var["plotting"][filename_short]["Entry"]["End"], text_default="0.0",
                command=lambda event, filename_short=filename_short, var_key="End":
                self.set_integration_window(filename_short, var_key, event))
            #
            self.container_elements["plotting"]["Entry"].extend([entr_start, entr_end])
            self.container_gui[filename_short]["Entry"]["General"].extend([entr_start, entr_end])
            #
            for index, isotope in enumerate(self.list_isotopes):
                self.time_ratio_data[self.filename_short][isotope] = []
                rgb = mcolors.to_rgb(self.isotope_colors[isotope])
                brightness = np.sqrt(0.299*(rgb[0]*255)**2 + 0.587*(rgb[1]*255)**2 + 0.114*(rgb[2]*255)**2)
                if brightness < 128:
                    color_fg = "white"
                else:
                    color_fg = "black"
                # LABELS
                lbl_iso = SE(parent=self.parent, row_id=1+index, column_id=80, fg=color_fg, n_rows=1, n_columns=3,
                             bg=self.isotope_colors[isotope]).create_simple_label(text=isotope)
                #
                self.container_elements["plotting"]["Label"].append(lbl_iso)
                self.container_gui[filename_short]["Label"]["General"].append(lbl_iso)
                #
                # CHECKBOXES
                self.container_var["plotting"][isotope] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
                self.container_var["plotting"][isotope][0].set(1)
                self.container_var["plotting"][isotope][1].set(0)
                self.container_var["plotting"][isotope][2].set(0)
                self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope] = tk.IntVar()
                self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope] = tk.IntVar()
                self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"][isotope] = tk.IntVar()
                self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope].set(1)
                self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope].set(0)
                self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"][isotope].set(0)
                #
                frm_iso_bg = SE(parent=self.parent,  row_id=1+index, column_id=83, n_rows=1, n_columns=4,
                                fg=self.isotope_colors[isotope], bg=self.isotope_colors[isotope]).create_frame()
                self.container_elements["plotting"]["Frame"].append(frm_iso_bg)
                self.container_gui[filename_short]["Frame"]["General"].append(frm_iso_bg)
                cb_iso = SE(
                    parent=self.parent, row_id=1+index, column_id=83, fg=color_fg, n_rows=1, n_columns=2,
                    bg=self.isotope_colors[isotope]).create_simple_checkbox(
                    var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope], text="",
                    set_sticky="", command=lambda
                        var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope],
                        name=isotope: self.change_visibility(var_cb, name))
                cb_isosmoothed = SE(
                    parent=self.parent, row_id=1+index, column_id=85, fg=color_fg, n_rows=1, n_columns=2,
                    bg=self.isotope_colors[isotope]).create_simple_checkbox(
                    var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope], text="",
                    set_sticky="", command=lambda
                        var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope],
                        name=isotope: self.change_visibility(var_cb, name))
                cb_spk = SE(
                    parent=self.parent, row_id=1+index, column_id=87, fg=color_fg, n_rows=1, n_columns=2,
                    bg=self.yellow_medium).create_simple_checkbox(
                    var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"][isotope], text="",
                    set_sticky="")
                #
                self.container_elements["plotting"]["Checkbox"].extend([cb_iso, cb_spk, cb_isosmoothed])
                self.container_gui[filename_short]["Checkbox"][isotope] = []
                self.container_gui[filename_short]["Checkbox"][isotope].extend([cb_iso, cb_spk, cb_isosmoothed])
            #
            ## RADIOBUTTONS
            self.container_var["plotting"][filename_short]["RB"] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
            rb_bg = SE(
                parent=self.parent, row_id=29, column_id=21, n_rows=1, n_columns=9, fg=self.blue_light,
                bg=self.blue_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=1, color_bg=self.blue_dark,
                fg=self.blue_light, text="Background", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=1: self.change_radiobutton(var, value))
            rb_sig = SE(
                parent=self.parent, row_id=29, column_id=33, n_rows=1, n_columns=9, fg=self.brown_light,
                bg=self.brown_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=2, color_bg=self.brown_dark,
                fg=self.brown_light, text="Signal", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=2: self.change_radiobutton(var, value))
            rb_spk = SE(
                parent=self.parent, row_id=29, column_id=45, n_rows=1, n_columns=9, fg=self.yellow_light,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=3, color_bg=self.yellow_dark,
                fg=self.yellow_light, text="Spike Elimination", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=3: self.change_radiobutton(var, value))
            rb_nslctn = SE(
                parent=self.parent, row_id=28, column_id=21, n_rows=1, n_columns=36, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="No Selection", sticky="nesw", relief=tk.GROOVE)
            rb_01 = SE(
                parent=self.parent, row_id=28, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][1], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Raw Data", sticky="nesw", relief=tk.GROOVE,
                command=lambda var_rb=self.container_var["plotting"][filename_short]["RB"][1]: self.change_rb_value(var_rb))
            rb_02 = SE(
                parent=self.parent, row_id=29, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][1], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Smoothed Data", sticky="nesw", relief=tk.GROOVE,
                command=lambda var_rb=self.container_var["plotting"][filename_short]["RB"][1]: self.change_rb_value(var_rb))
            rb_03 = SE(
                parent=self.parent, row_id=31, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Time-Signal Plot", sticky="nesw", relief=tk.GROOVE,
                command=self.show_time_signal_diagram)
            rb_04 = SE(
                parent=self.parent, row_id=32, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Histogram", sticky="nesw", relief=tk.GROOVE)
            rb_05 = SE(
                parent=self.parent, row_id=32, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=2, color_bg=self.green_medium,
                fg=self.green_light, text="Scatter Plot", sticky="nesw", relief=tk.GROOVE)
            rb_06 = SE(
                parent=self.parent, row_id=31, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=3, color_bg=self.green_medium,
                fg=self.green_light, text="Time-Ratio Plot", sticky="nesw", relief=tk.GROOVE,
                command=self.show_time_ratio_diagram)
            #
            self.container_elements["plotting"]["Radiobutton"].extend(
                [rb_bg, rb_sig, rb_spk, rb_nslctn, rb_01, rb_02, rb_03, rb_04, rb_05, rb_06])
            self.container_gui[filename_short]["Radiobutton"]["General"].extend(
                [rb_bg, rb_sig, rb_spk, rb_nslctn, rb_01, rb_02, rb_03, rb_04, rb_05, rb_06])
            #
            ## CHECKBOXES
            self.container_var["plotting"]["Integration Window"] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"].set(1)
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SIG"].set(1)
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"].set(1)
            self.container_var["plotting"]["Integration Window"][0].set(1)
            self.container_var["plotting"]["Integration Window"][1].set(1)
            self.container_var["plotting"]["Integration Window"][2].set(1)
            cb_iw_bg = SE(
                parent=self.parent, row_id=29, column_id=30, fg=self.blue_light, n_rows=1, n_columns=3,
                bg=self.blue_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"]:
                self.change_visibility_iw(var_cb))
            cb_iw_sig = SE(
                parent=self.parent, row_id=29, column_id=42, fg=self.brown_light, n_rows=1, n_columns=3,
                bg=self.brown_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SIG"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SIG"]:
                self.change_visibility_iw(var_cb))
            cb_iw_spk = SE(
                parent=self.parent, row_id=29, column_id=54, fg=self.yellow_light, n_rows=1, n_columns=3,
                bg=self.yellow_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"]:
                self.change_visibility_iw(var_cb))
            #
            self.container_elements["plotting"]["Checkbox"].extend([cb_iw_bg, cb_iw_sig, cb_iw_spk])
            self.container_gui[filename_short]["Checkbox"]["General"].extend([cb_iw_bg, cb_iw_sig, cb_iw_spk])
            #
            ## BUTTONS
            btn_back = SE(
                parent=self.parent, row_id=38, column_id=66, n_rows=2, n_columns=12, fg=self.green_dark,
                bg=self.red_dark).create_simple_button(
                text="Back to Settings", bg_active=self.green_dark, fg_active=self.green_light,
                command=self.sub_mineralanalysis_settings)
            btn_rmv = SE(
                parent=self.parent, row_id=28, column_id=57, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.red_dark).create_simple_button(
                text="Remove Interval", bg_active=self.green_dark, fg_active=self.green_light,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0]: self.delete_interval(var))
            btn_all = SE(
                parent=self.parent, row_id=28, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Show All", bg_active=self.red_dark, fg_active=self.green_dark, command=self.show_all_lines)
            btn_none = SE(
                parent=self.parent, row_id=29, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Show None", bg_active=self.red_dark, fg_active=self.green_dark, command=self.hide_all_lines)
            btn_smthall = SE(
                parent=self.parent, row_id=34, column_id=66, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="All Isotopes", bg_active=self.red_dark, fg_active=self.green_dark,
                command=self.smooth_all_isotopes)
            btn_smoothit = SE(
                parent=self.parent, row_id=34, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Smooth it", bg_active=self.red_dark, fg_active=self.green_dark,
                command=self.do_spike_elimination)
            btn_cnfrm = SE(
                parent=self.parent, row_id=35, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Confirm Edits", bg_active=self.red_dark, fg_active=self.green_dark,
                command=lambda filename=self.file, filetype=self.file_type: self.confirm_edits(filename, filetype))
            btn_showspkelim = SE(
                parent=self.parent, row_id=35, column_id=66, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Update Data", bg_active=self.red_dark, fg_active=self.green_dark,
                command=self.update_edited_datasets)
            #
            self.container_elements["plotting"]["Button"].extend(
                [btn_back, btn_rmv, btn_all, btn_none, btn_smthall, btn_cnfrm, btn_showspkelim, btn_smoothit])
            self.container_gui[filename_short]["Button"]["General"].extend(
                [btn_back, btn_rmv, btn_all, btn_none, btn_smthall, btn_cnfrm, btn_showspkelim, btn_smoothit])
            #
            ## LISTBOXES and TREEVIEWS
            lb_bg, scrollbar_bg_x, scrollbar_bg_y = SE(
                parent=self.parent, row_id=30, column_id=21, n_rows=10, n_columns=12, fg=self.blue_dark,
                bg=self.blue_light).create_simple_listbox_grid()
            lb_sig, scrollbar_sig_x, scrollbar_sig_y = SE(
                parent=self.parent, row_id=30, column_id=33, n_rows=10, n_columns=12, fg=self.brown_dark,
                bg=self.brown_light).create_simple_listbox_grid()
            lb_spk, scrollbar_spk_x, scrollbar_spk_y = SE(
                parent=self.parent, row_id=30, column_id=45, n_rows=10, n_columns=12, fg=self.yellow_dark,
                bg=self.yellow_light).create_simple_listbox_grid()
            lb_isorat = SE(
                parent=self.parent, row_id=30, column_id=57, n_rows=10, n_columns=9, fg=self.slate_grey_dark,
                bg=self.slate_grey_light).create_treeview()
            #
            self.container_elements["plotting"]["Listbox"].extend([lb_bg, scrollbar_bg_x, scrollbar_bg_y,
                                                                   lb_sig, scrollbar_sig_x, scrollbar_sig_y,
                                                                   lb_spk, scrollbar_spk_x, scrollbar_spk_y,
                                                                   lb_isorat])
            self.container_listboxes[self.file_type][filename_short]["BG"] = [lb_bg, scrollbar_bg_x, scrollbar_bg_y]
            self.container_listboxes[self.file_type][filename_short]["SIG"] = [lb_sig, scrollbar_sig_x, scrollbar_sig_y]
            self.container_listboxes[self.file_type][filename_short]["SPK"] = [lb_spk, scrollbar_spk_x, scrollbar_spk_y]
            self.container_listboxes[self.file_type][filename_short]["ISORAT"] = lb_isorat
            #
            ## OPTION MENU
            if filename in self.container_var["STD"]:
                if self.container_var["STD"][filename]["IS"].get() != "Select IS":
                    var_text = self.container_var["STD"][filename]["IS"].get()
                    var_iso = self.container_var["STD"][filename]["IS"]
                    self.calculate_and_place_isotope_ratios(
                        var_is=self.container_var["STD"][filename]["IS"].get(), data=df_data, lb=lb_isorat)
                else:
                    var_iso = self.container_var["STD"][filename]
                    var_text = "Select IS"
            else:
                if self.container_var["SMPL"][filename]["IS"].get() != "Select IS":
                    var_text = self.container_var["SMPL"][filename]["IS"].get()
                    var_iso = self.container_var["SMPL"][filename]["IS"]
                    self.calculate_and_place_isotope_ratios(var_is=self.container_var["SMPL"][filename]["IS"].get(), data=df_data,
                                                            lb=lb_isorat)
                else:
                    var_iso = self.container_var["SMPL"][filename]["IS"]
                    var_text = "Select IS"
            opt_is = SE(
                parent=self.parent, row_id=29, column_id=57, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=var_iso, option_list=self.list_isotopes, text_set=var_text, fg_active=self.green_dark,
                bg_active=self.red_dark, command=lambda var_is=var_iso, data=df_data, lb=lb_isorat:
                self.calculate_and_place_isotope_ratios(var_is, data, lb))
            #
            self.container_elements["plotting"]["Option Menu"].append(opt_is)
            self.container_gui[filename_short]["Option Menu"]["General"].append(opt_is)
            #
            ## DIAGRAM
            if self.container_var["plotting"][filename_short]["RB"][1].get() == 0:
                if self.file_type == "STD":
                    if self.fast_track_std == True:
                        self.fig = self.diagrams_setup[self.file_type][filename_short]["FIG"]
                        self.ax = self.diagrams_setup[self.file_type][filename_short]["AX"]
                        #
                        self.fig_ratio = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax_ratio = self.fig_ratio.add_subplot()
                    else:
                        self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax = self.fig.add_subplot()
                        self.diagrams_setup[self.file_type][filename_short]["FIG"] = self.fig
                        self.diagrams_setup[self.file_type][filename_short]["AX"] = self.ax
                        #
                        self.fig_ratio = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax_ratio = self.fig_ratio.add_subplot()
                elif self.file_type == "SMPL":
                    if self.fast_track_smpl == True:
                        self.fig = self.container_diagrams[self.file_type][filename_short]["FIG"]
                        self.ax = self.container_diagrams[self.file_type][filename_short]["AX"]
                        self.fig = self.diagrams_setup[self.file_type][filename_short]["FIG"]
                        self.ax = self.diagrams_setup[self.file_type][filename_short]["AX"]
                        #
                        self.fig_ratio = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax_ratio = self.fig_ratio.add_subplot()
                    else:
                        self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax = self.fig.add_subplot()
                        self.container_diagrams[self.file_type][filename_short]["FIG"] = self.fig
                        self.container_diagrams[self.file_type][filename_short]["AX"] = self.ax
                        self.diagrams_setup[self.file_type][filename_short]["FIG"] = self.fig
                        self.diagrams_setup[self.file_type][filename_short]["AX"] = self.ax
                        #
                        self.fig_ratio = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax_ratio = self.fig_ratio.add_subplot()
                #
                for isotope in self.list_isotopes:
                    ln = self.ax.plot(
                        self.times, df_data[isotope], label=isotope, color=self.isotope_colors[isotope], visible=True)
                    self.lines["raw"][isotope] = ln
                    self.diagrams_setup[self.file_type][filename_short]["Time Signal Raw"][isotope] = ln
                self.ax.grid(True)
                self.ax.set_yscale("log")
                self.ax.set_xlim(left=0, right=x_max)
                self.ax.set_xticks(np.arange(0, x_max, 10))
                self.ax.set_ylim(top=1.5*y_max)
                self.ax.set_axisbelow(True)
                self.ax.set_xlabel("Time (s)", labelpad=0.5)
                self.ax.set_ylabel("Signal (cps)", labelpad=0.5)

                self.fig.subplots_adjust(bottom=0.125, top=0.975, left=0.075, right=0.975)

                legend = self.ax.legend(fontsize="x-small", framealpha=1.0, edgecolor="white",
                                        bbox_to_anchor=(0.10, 0.010), loc=3, borderaxespad=0,
                                        bbox_transform=plt.gcf().transFigure, ncol=int(len(self.list_isotopes)/2 + 1),
                                        facecolor="white")
                plt.rcParams["savefig.facecolor"] = "white"
                plt.rcParams["savefig.dpi"] = 300

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
                self.canvas.get_tk_widget().grid(
                    row=0, column=21, rowspan=26, columnspan=59, sticky="nesw")
                self.toolbarFrame = tk.Frame(master=self.parent)
                self.toolbarFrame.grid(
                    row=26, column=21, rowspan=2, columnspan=59, sticky="w")
                self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
                self.toolbar.config(background=self.green_light)
                self.toolbar._message_label.config(background=self.green_light)
                self.toolbar.winfo_children()[-2].config(background=self.green_light)

                self.container_files[self.file_type][filename_short]["Time Signal Plot"] = [self.canvas,
                                                                                            self.toolbarFrame]
                self.container_files[self.file_type][filename_short]["Plot"] = True
                self.diagrams_setup[self.file_type][filename_short]["CANVAS"] = self.canvas
                self.diagrams_setup[self.file_type][filename_short]["TOOLBARFRAME"] = self.toolbarFrame

                if self.container_settings["MA"]["Start BG"].get() != "":
                    filename = self.file.split("/")[-1]
                    x_nearest_start = min(self.times, key=lambda x: abs(x-float(self.container_settings["MA"]["Start BG"].get())))
                    x_nearest_end = min(self.times, key=lambda x: abs(x-float(self.container_settings["MA"]["End BG"].get())))
                    index_start = self.times[self.times == x_nearest_start].index[0]
                    index_end = self.times[self.times == x_nearest_end].index[0]
                    #
                    self.bg_id += 1
                    self.container_listboxes[self.file_type][filename]["BG"][0].insert(
                        tk.END, "BG"+str(self.bg_id)+" ["+str(x_nearest_start)+"-"+str(x_nearest_end)+"]")
                    box_bg = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                    box_bg_ratio = self.ax_ratio.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                    self.container_helper["limits BG"][self.file]["ID"].append(self.bg_id)
                    self.container_helper["limits BG"][self.file]["type"].append("custom")
                    self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                    self.container_helper["limits BG Ratio"][self.file][str(self.bg_id)] = box_bg_ratio
                    #
                    self.canvas.draw()
                    #
                    if self.file_type == "STD":
                        self.container_helper["STD"][filename]["BG"][self.bg_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": [box_bg, box_bg_ratio]}
                        self.container_helper["positions"]["BG STD"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
                    elif self.file_type == "SMPL":
                        self.container_helper["SMPL"][filename]["BG"][self.bg_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": [box_bg, box_bg_ratio]}
                        self.container_helper["positions"]["BG SMPL"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
                if self.container_settings["MA"]["Start SIG"].get() != "":
                    filename = self.file.split("/")[-1]
                    x_nearest_start = min(self.times,
                                          key=lambda x: abs(x-float(self.container_settings["MA"]["Start SIG"].get())))
                    x_nearest_end = min(self.times,
                                        key=lambda x: abs(x-float(self.container_settings["MA"]["End SIG"].get())))
                    index_start = self.times[self.times == x_nearest_start].index[0]
                    index_end = self.times[self.times == x_nearest_end].index[0]
                    #
                    self.sig_id += 1
                    self.container_listboxes[self.file_type][filename]["SIG"][0].insert(
                        tk.END, "SIG"+str(self.sig_id)+" ["+str(x_nearest_start)+"-"+str(x_nearest_end)+"]")
                    #
                    box_sig = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                    box_sig_ratio = self.ax_ratio.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                    #
                    self.container_helper["limits SIG"][self.file]["ID"].append(self.sig_id)
                    self.container_helper["limits SIG"][self.file]["type"].append("custom")
                    self.container_helper["limits SIG"][self.file][str(self.sig_id)] = box_sig
                    self.container_helper["limits SIG Ratio"][self.file][str(self.sig_id)] = box_sig_ratio
                    self.canvas.draw()
                    #
                    if self.file_type == "STD":
                        self.container_helper["STD"][filename]["SIG"][self.sig_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": [box_sig, box_sig_ratio]}
                        self.container_helper["positions"]["SIG STD"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.sig_id])
                    elif self.file_type == "SMPL":
                        self.container_helper["SMPL"][filename]["SIG"][self.sig_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": [box_sig, box_sig_ratio]}
                        self.container_helper["positions"]["SIG SMPL"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.sig_id])
                if self.file_type == "STD" and self.fast_track_std == True:
                    self.container_listboxes[self.file_type][filename_short]["SPK"][0].insert(
                        tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                            self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                                + "-" + str(self.container_helper["STD"][filename_short]["SPK"][
                                                self.list_isotopes[0]][1]["Times"][1]) + "]")
                    box_spk = self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Object"]
                    self.diagrams_setup[self.file_type][filename_short]["CANVAS"].draw()
                    self.show_smoothed_data()
                elif self.file_type == "SMPL" and self.fast_track_smpl == True:
                    self.container_listboxes[self.file_type][filename_short]["SPK"][0].insert(
                        tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                            self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                                + "-" + str(self.container_helper["SMPL"][filename_short]["SPK"][
                                                self.list_isotopes[0]][1]["Times"][1]) + "]")
                    box_spk = self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Object"]
                    self.diagrams_setup[self.file_type][filename_short]["CANVAS"].draw()
                    self.show_smoothed_data()
            #
            self.canvas.mpl_connect(
                "button_press_event", lambda event, var=self.container_var["plotting"][filename_short]["RB"][0],
                                             filename=filename_short, ratio_mode=False:
                self.onclick(var, filename, ratio_mode, event))
        else:
            ## Reconstruction
            try:
                # FRAMES
                for frm_item in self.container_gui[filename_short]["Frame"]["General"]:
                    frm_item.grid()
                # LABELS
                for lbl_item in self.container_gui[filename_short]["Label"]["General"]:
                    lbl_item.grid()
                # CHECKBOXES
                for cb_item in self.container_gui[filename_short]["Checkbox"]["General"]:
                    cb_item.grid()
                for isotope in self.list_isotopes:
                    for cb_iso_item in self.container_gui[filename_short]["Checkbox"][isotope]:
                        cb_iso_item.grid()
                # RADIOBUTTONS
                for rbtn_item in self.container_gui[filename_short]["Radiobutton"]["General"]:
                    rbtn_item.grid()
                # ENTRY
                for entr_item in self.container_gui[filename_short]["Entry"]["General"]:
                    entr_item.grid()
                # BUTTONS
                for btn_item in self.container_gui[filename_short]["Button"]["General"]:
                    btn_item.grid()
                # OPTION MENUS
                for optmn_item in self.container_gui[filename_short]["Option Menu"]["General"]:
                    optmn_item.grid()
                #
                for lb_item in self.container_listboxes[self.file_type][filename_short]["BG"]:
                    lb_item.grid()
                for lb_item in self.container_listboxes[self.file_type][filename_short]["SIG"]:
                    lb_item.grid()
                for lb_item in self.container_listboxes[self.file_type][filename_short]["SPK"]:
                    lb_item.grid()
                self.container_listboxes[self.file_type][filename_short]["ISORAT"].grid()
                #
                self.fig = self.diagrams_setup[self.file_type][filename_short]["FIG"]
                self.ax = self.diagrams_setup[self.file_type][filename_short]["AX"]
                self.canvas = self.diagrams_setup[self.file_type][filename_short]["CANVAS"]
                self.toolbarFrame = self.diagrams_setup[self.file_type][filename_short]["TOOLBARFRAME"]
                self.canvas.get_tk_widget().grid(row=0, column=21, rowspan=26, columnspan=59, sticky="nesw")
                self.toolbarFrame.grid(row=26, column=21, rowspan=2, columnspan=59, sticky="w")
                #
            except:
                print("Error! Fehler mit Plotting Recreation")
            #
            if self.container_settings["MA"]["Start BG"].get() != "" \
                    and len(self.container_helper[self.file_type][filename_short]["BG"]) == 0:
                filename = self.file.split("/")[-1]
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(x - float(self.container_settings["MA"]["Start BG"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(x - float(self.container_settings["MA"]["End BG"].get())))
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.bg_id += 1
                self.container_listboxes[self.file_type][filename]["BG"][0].insert(
                    tk.END, "BG" + str(self.bg_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                #
                box_bg = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                box_bg_ratio = self.ax_ratio.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                #
                self.container_helper["limits BG"][self.file]["ID"].append(self.bg_id)
                self.container_helper["limits BG"][self.file]["type"].append("custom")
                self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                self.container_helper["limits BG Ratio"][self.file][str(self.bg_id)] = box_bg_ratio
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename]["BG"][self.bg_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": [box_bg, box_bg_ratio]}
                    self.container_helper["positions"]["BG STD"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename]["BG"][self.bg_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": [box_bg, box_bg_ratio]}
                    self.container_helper["positions"]["BG SMPL"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
            #
            if self.container_settings["MA"]["Start SIG"].get() != "" \
                    and len(self.container_helper[self.file_type][filename_short]["SIG"]) == 0:
                filename = self.file.split("/")[-1]
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(x - float(self.container_settings["MA"]["Start SIG"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(x - float(self.container_settings["MA"]["End SIG"].get())))
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.sig_id += 1
                self.container_listboxes[self.file_type][filename]["SIG"][0].insert(
                    tk.END, "SIG" + str(self.sig_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                #
                box_sig = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                box_sig_ratio = self.ax_ratio.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                #
                self.container_helper["limits SIG"][self.file]["ID"].append(self.sig_id)
                self.container_helper["limits SIG"][self.file]["type"].append("custom")
                self.container_helper["limits SIG"][self.file][str(self.sig_id)] = box_sig
                self.container_helper["limits SIG Ratio"][self.file][str(self.sig_id)] = box_sig_ratio
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename]["SIG"][self.sig_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": [box_sig, box_sig_ratio]}
                    self.container_helper["positions"]["SIG STD"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.sig_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename]["SIG"][self.sig_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": [box_sig, box_sig_ratio]}
                    self.container_helper["positions"]["SIG SMPL"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.sig_id])
            #
            if self.file_type == "STD" and self.fast_track_std == True \
                    and self.container_listboxes[self.file_type][filename_short]["SPK"][0].size() == 0:
                x_nearest_start = float(
                    self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                x_nearest_end = float(
                    self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][1])
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.container_listboxes[self.file_type][filename_short]["SPK"][0].insert(
                    tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                        self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                            + "-" + str(self.container_helper["STD"][filename_short]["SPK"][
                                            self.list_isotopes[0]][1]["Times"][1]) + "]")
                #box_spk = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.125, color=self.yellow_dark)
                box_spk = self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Object"]
            elif self.file_type == "SMPL" and self.fast_track_smpl == True \
                    and self.container_listboxes[self.file_type][filename_short]["SPK"][0].size() == 0:
                self.container_listboxes["SMPL"][filename_short]["SPK"][0].insert(
                    tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                        self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                            + "-" + str(self.container_helper["SMPL"][filename_short]["SPK"][
                                            self.list_isotopes[0]][1]["Times"][1]) + "]")
                box_spk = self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Object"]
            #
            self.diagrams_setup[self.file_type][filename_short]["CANVAS"].draw()
            #
            if self.fast_track_std == True:
                self.show_smoothed_data()
            if self.fast_track_smpl == True:
                self.show_smoothed_data()
    #
    def show_time_signal_diagram(self):
        try:
            self.canvas_ratio.get_tk_widget().grid_remove()
            self.toolbarFrame_ratio.grid_remove()
        except AttributeError:
            pass
        #
        try:
            self.canvas.get_tk_widget().grid()
            self.toolbarFrame.grid()
        except AttributeError:
            pass
    #
    def show_time_ratio_diagram(self):
        try:
            self.canvas.get_tk_widget().grid_remove()
            self.toolbarFrame.grid_remove()
        except AttributeError:
            pass
        #
        internal_standard = self.container_var[self.file_type][self.file]["IS"].get()
        intensity_raw_is = np.array(self.container_measurements["RAW"][self.filename_short][internal_standard])
        #
        if len(self.time_ratio_data[self.filename_short][internal_standard]) == 0:
            for isotope in self.container_lists["ISOTOPES"]:
                intensity_raw_i = np.array(self.container_measurements["RAW"][self.filename_short][isotope])
                value = intensity_raw_i/intensity_raw_is
                #
                self.time_ratio_data[self.filename_short][isotope].extend(value)
            #
            ratio_measurements = np.array(
                [[self.time_ratio_data[self.filename_short][isotope] for isotope in self.list_isotopes]])
            x_max = np.amax(self.times)
            y_max = np.amax(ratio_measurements)
            #
            for isotope in self.list_isotopes:
                ln = self.ax_ratio.plot(
                    self.times, self.time_ratio_data[self.filename_short][isotope], label=isotope,
                    color=self.isotope_colors[isotope], visible=True)
                self.lines["ratio"][isotope] = ln
                self.diagrams_setup[self.file_type][self.filename_short]["Time Ratio"][isotope] = ln
            self.ax_ratio.grid(True)
            self.ax_ratio.set_yscale("log")
            self.ax_ratio.set_xlim(left=0, right=x_max)
            self.ax_ratio.set_xticks(np.arange(0, x_max, 10))
            self.ax_ratio.set_ylim(top=1.1*y_max)
            self.ax_ratio.set_axisbelow(True)
            self.ax_ratio.set_xlabel("Time (s)", labelpad=0.5)
            self.ax_ratio.set_ylabel("Ratio I(i)/I(IS) (cps(i)/cps(IS))", labelpad=0.5)

            self.fig_ratio.subplots_adjust(bottom=0.125, top=0.975, left=0.075, right=0.975)

            plt.rcParams["savefig.facecolor"] = "white"
            plt.rcParams["savefig.dpi"] = 300

            self.canvas_ratio = FigureCanvasTkAgg(self.fig_ratio, master=self.parent)
            self.canvas_ratio.get_tk_widget().grid(
                row=0, column=21, rowspan=26, columnspan=59, sticky="nesw")
            self.toolbarFrame_ratio = tk.Frame(master=self.parent)
            self.toolbarFrame_ratio.grid(
                row=26, column=21, rowspan=2, columnspan=59, sticky="w")
            self.toolbar_ratio = NavigationToolbar2Tk(self.canvas_ratio, self.toolbarFrame_ratio)
            self.toolbar_ratio.config(background=self.green_light)
            self.toolbar_ratio._message_label.config(background=self.green_light)
            self.toolbar_ratio.winfo_children()[-2].config(background=self.green_light)
            #
            self.container_files[self.file_type][self.filename_short]["Time Ratio Plot"] = [
                self.canvas_ratio, self.toolbarFrame_ratio]
            self.diagrams_setup[self.file_type][self.filename_short]["CANVAS_RATIO"] = self.canvas_ratio
            self.diagrams_setup[self.file_type][self.filename_short]["TOOLBARFRAME_RATIO"] = self.toolbarFrame_ratio
            #
            if self.container_settings["MA"]["Start BG"].get() != "" \
                    and len(self.container_helper[self.file_type][self.filename_short]["BG"]) == 1:
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(x - float(self.container_settings["MA"]["Start BG"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(x - float(self.container_settings["MA"]["End BG"].get())))
                # box_bg_ratio = self.ax_ratio.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                # #
                # bg_id = self.container_helper["limits BG"][self.file]["ID"][-1]
                # self.container_helper["limits BG Ratio"][self.file][str(bg_id)] = box_bg_ratio
            #
            if self.container_settings["MA"]["Start SIG"].get() != "" \
                    and len(self.container_helper[self.file_type][self.filename_short]["SIG"]) == 1:
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(x - float(self.container_settings["MA"]["Start SIG"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(x - float(self.container_settings["MA"]["End SIG"].get())))
                # box_sig_ratio = self.ax_ratio.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                # #
                # sig_id = self.container_helper["limits SIG"][self.file]["ID"][-1]
                # self.container_helper["limits SIG Ratio"][self.file][str(sig_id)] = box_sig_ratio
            #
            if self.file_type == "STD" and self.fast_track_std == True \
                    and self.container_listboxes[self.file_type][self.filename_short]["SPK"][0].size() == 1:
                x_nearest_start = float(
                    self.container_helper[self.file_type][self.filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                x_nearest_end = float(
                    self.container_helper[self.file_type][self.filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][1])
                box_spk_ratio = self.ax_ratio.axvspan(
                    x_nearest_start, x_nearest_end, alpha=0.125, color=self.yellow_dark)
                #
                spk_id = self.container_helper["limits SPK"][self.file]["ID"][-1]
                self.container_helper["limits SPK Ratio"][self.file][str(spk_id)] = box_spk_ratio
            #
        else:
            #
            try:
                self.canvas_ratio.get_tk_widget().grid()
                self.toolbarFrame_ratio.grid()
            except AttributeError:
                pass
        #
        self.canvas_ratio.draw()
        self.canvas_ratio.mpl_connect(
            "button_press_event", lambda event, var=self.container_var["plotting"][self.filename_short]["RB"][0],
                                         filename=self.filename_short, ratio_mode=True:
            self.onclick(var, filename, ratio_mode, event))

    #
    def sub_mineralanalysis_reduction(self):
        ## Cleaning
        categories = ["SRM", "ma_setting", "plotting", "PSE"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Radiobutton"]) > 0:
                for item in self.container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Checkbox"]) > 0:
                for item in self.container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Listbox"]) > 0:
                for item in self.container_elements[category]["Listbox"]:
                    item.grid_remove()
        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().grid_remove()
            self.toolbarFrame.grid_remove()
        except AttributeError:
            pass
        try:
            if self.canvas:
                self.canvas.destroy()
            if self.toolbarFrame:
                self.toolbarFrame.destroy()
        except AttributeError:
            pass
        #
        ## Reconstruction
        try:
            for lbl_item in self.container_elements["ma_datareduction"]["Label"]:
                lbl_item.grid()
            for btn_item in self.container_elements["ma_datareduction"]["Button"]:
                btn_item.grid()
            for optmen_item in self.container_elements["ma_datareduction"]["Option Menu"]:
                optmen_item.grid()
            for entr_item in self.container_elements["ma_datareduction"]["Entry"]:
                entr_item.grid()
            for entr_item in self.container_elements["ma_datareduction"]["Frame"]:
                entr_item.grid()
            for rb_item in self.container_elements["ma_datareduction"]["Radiobutton"]:
                rb_item.grid()
        except:
            print("Error! Reconstruction 'Data Reduction' failed!")
        #
        self.container_lists["SRM"].clear()
        self.container_lists["IS"].clear()
        self.container_lists["ID"].clear()
        self.container_lists["ID Files"].clear()
        list_files = ["All Standard Files", "All Sample Files"]
        #
        for key, value in self.container_files["SRM"].items():
            if value.get() not in self.container_lists["SRM"] and value.get() in self.list_srm:
                self.container_lists["SRM"].append(value.get())
                self.fill_srm_values(var_srm=value.get())
        #
        for key_01, value_01 in self.container_files["STD"].items():
            for key_02, value_02 in value_01.items():
                if key_02 not in ["Plot", "Time Signal Plot", "Histogram Plot", "Scatter Plot", "BG limits",
                                  "SIG limits", "BG", "SIG", "SPK", "Time Ratio Plot"]:
                    if value_02.get() not in self.container_lists["IS"] and value_02.get() in self.list_isotopes:
                        self.container_lists["IS"].append(value_02.get())
        for key_01, value_01 in self.container_files["SMPL"].items():
            for key_02, value_02 in value_01.items():
                if key_02 not in ["Plot", "Time Signal Plot", "Histogram Plot", "Scatter Plot", "BG limits",
                                  "SIG limits", "BG", "SIG", "SPK", "Time Ratio Plot"]:
                    if value_02.get() not in self.container_lists["IS"] and value_02.get() in self.list_isotopes:
                        self.container_lists["IS"].append(value_02.get())
        #
        for filename, item in self.container_files["STD"].items():
            if item["ID"].get() not in self.container_lists["ID"]:
                self.container_lists["ID"].append(item["ID"].get())
                self.container_lists["ID Files"][item["ID"].get()] = [filename]
                list_files.append(str(item["ID"].get())+" Files")
            elif item["ID"].get() in self.container_lists["ID"] and item["ID"].get() in self.container_lists["ID Files"]:
                self.container_lists["ID Files"][item["ID"].get()].append(filename)
        for filename, item in self.container_files["SMPL"].items():
            if item["ID"].get() not in self.container_lists["ID"]:
                self.container_lists["ID"].append(item["ID"].get())
                self.container_lists["ID Files"][item["ID"].get()] = [filename]
                list_files.append(str(item["ID"].get()) + " Files")
            elif item["ID"].get() in self.container_lists["ID"] and item["ID"].get() in self.container_lists["ID Files"]:
                self.container_lists["ID Files"][item["ID"].get()].append(filename)
        #
        ## LABELS
        if len(self.container_elements["ma_datareduction"]["Label"]) == 0:
            lbl_01 = SE(
                parent=self.parent, row_id=0, column_id=21, n_rows=2, n_columns=9, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="General Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            self.gui_elements["ma_datareduction"]["Label"]["General"].append(lbl_01)
            lbl_02 = SE(
                parent=self.parent, row_id=0, column_id=31, n_rows=2, n_columns=3, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Isotope", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_03 = SE(
                parent=self.parent, row_id=0, column_id=34, n_rows=1, n_columns=11, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Intensity Ratios I/I(IS)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_03a = SE(
                parent=self.parent, row_id=1, column_id=34, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Mean \u03BC", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_03b = SE(
                parent=self.parent, row_id=1, column_id=40, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Error \u03C3", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_04 = SE(
                parent=self.parent, row_id=0, column_id=45, n_rows=1, n_columns=11, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Sensitivity \u03BE", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_04a = SE(
                parent=self.parent, row_id=1, column_id=45, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Mean \u03BC", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_04b = SE(
                parent=self.parent, row_id=1, column_id=51, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Error \u03C3", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_05 = SE(
                parent=self.parent, row_id=0, column_id=56, n_rows=1, n_columns=11, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Concentration C", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_05a = SE(
                parent=self.parent, row_id=1, column_id=56, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Mean \u03BC", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_05b = SE(
                parent=self.parent, row_id=1, column_id=62, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Error \u03C3", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_06 = SE(
                parent=self.parent, row_id=0, column_id=67, n_rows=1, n_columns=11, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Relative Sensitivity Factor RSF", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_06a = SE(
                parent=self.parent, row_id=1, column_id=67, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Mean \u03BC", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_06b = SE(
                parent=self.parent, row_id=1, column_id=73, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Error \u03C3", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_07 = SE(
                parent=self.parent, row_id=0, column_id=78, n_rows=1, n_columns=11, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Limit of Detection LOD", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_07a = SE(
                parent=self.parent, row_id=1, column_id=78, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Mean \u03BC", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_07b = SE(
                parent=self.parent, row_id=1, column_id=84, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Error \u03C3", relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            self.container_elements["ma_datareduction"]["Label"].extend(
                [lbl_01, lbl_02, lbl_03, lbl_03a, lbl_03b, lbl_04, lbl_04a, lbl_04b, lbl_05, lbl_05a, lbl_05b, lbl_06,
                 lbl_06a, lbl_06b, lbl_07, lbl_07a, lbl_07b])
            self.gui_elements["ma_datareduction"]["Label"]["Specific"].extend(
                [lbl_02, lbl_03, lbl_03a, lbl_03b, lbl_04, lbl_04a, lbl_04b, lbl_05, lbl_05a, lbl_05b, lbl_06,
                 lbl_06a, lbl_06b, lbl_07, lbl_07a, lbl_07b])
            #
            for index, isotope in enumerate(self.list_isotopes):
                ## LABELS
                lbl_isotope = SE(
                    parent=self.parent, row_id=2+index, column_id=31, n_rows=1, n_columns=3, fg=self.green_light,
                    bg=self.green_medium).create_simple_label(
                    text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
                #
                self.container_elements["ma_datareduction"]["Label"].append(lbl_isotope)
                self.gui_elements["ma_datareduction"]["Label"]["Specific"].append(lbl_isotope)
                #
                ## ENTRIES
                #self.container_var["ma_datareduction"] = {}
                self.container_var["ma_datareduction"][isotope] = [tk.StringVar(), tk.StringVar(), tk.StringVar(),
                                                                   tk.StringVar(), tk.StringVar(), tk.StringVar(),
                                                                   tk.StringVar(), tk.StringVar(), tk.StringVar(),
                                                                   tk.StringVar()]
                width_sum = 29
                for index_02, var_entr in enumerate(self.container_var["ma_datareduction"][isotope]):
                    if (index_02 % 2) == 0:
                        width = 5
                        width_col = 6
                    else:
                        width = 6
                        width_col = 5
                    width_sum += width
                    entr_iso = SE(
                        parent=self.parent, row_id=2+index, column_id=width_sum, n_rows=1, n_columns=width_col,
                        fg=self.green_light, bg=self.green_dark).create_simple_entry(
                        var=var_entr, text_default="0.0")
                    #
                    self.container_elements["ma_datareduction"]["Entry"].append(entr_iso)
                    self.gui_elements["ma_datareduction"]["Entry"]["Specific"].append(entr_iso)
            #
            ## OPTION MENUS
            self.container_var["ma_datareduction"]["Option SRM"] = tk.StringVar()
            self.container_var["ma_datareduction"]["Option IS"] = tk.StringVar()
            self.container_var["ma_datareduction"]["Option File"] = tk.StringVar()
            self.container_var["ma_datareduction"]["Option ID"] = tk.StringVar()
            opt_menu_srm = SE(
                parent=self.parent, row_id=2, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_srm(
                var_srm=self.container_var["ma_datareduction"]["Option SRM"], text_set=self.container_lists["SRM"][0],
                fg_active=self.green_dark, bg_active=self.red_dark, option_list=self.container_lists["SRM"])
            opt_menu_is = SE(
                parent=self.parent, row_id=3, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["ma_datareduction"]["Option IS"], option_list=self.container_lists["IS"],
                text_set=self.container_lists["IS"][0], fg_active=self.green_dark, bg_active=self.red_dark)
            opt_menu_file = SE(
                parent=self.parent, row_id=4, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["ma_datareduction"]["Option File"],
                option_list=list_files, text_set="Select File Type", fg_active=self.green_dark,
                bg_active=self.red_dark, command=lambda filetype=self.container_var["ma_datareduction"]["Option File"]:
                self.datareduction(filetype, fill_entry=True))
            opt_menu_id = SE(
                parent=self.parent, row_id=5, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["ma_datareduction"]["Option ID"],
                option_list=self.container_lists["ID"], text_set="Select Assemblage ID", fg_active=self.green_dark,
                bg_active=self.red_dark, command=lambda var_id=self.container_var["ma_datareduction"]["Option ID"]:
                self.change_id_option_results(var_id))
            #
            self.container_elements["ma_datareduction"]["Option Menu"].extend(
                [opt_menu_srm, opt_menu_is, opt_menu_file, opt_menu_id])
            #
            ## RADIOBUTTONS
            self.container_var["ma_datareduction"]["Radiobutton"] = [tk.IntVar(), tk.IntVar()]
            rb_01 = SE(
                parent=self.parent, row_id=6, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["ma_datareduction"]["Radiobutton"][0], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Raw Data", sticky="nesw", relief=tk.GROOVE)
            rb_02 = SE(
                parent=self.parent, row_id=7, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["ma_datareduction"]["Radiobutton"][0], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Smoothed Data", sticky="nesw", relief=tk.GROOVE)
            rb_03 = SE(
                parent=self.parent, row_id=8, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["ma_datareduction"]["Radiobutton"][1], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Show Results", sticky="nesw", relief=tk.GROOVE,
                command=self.show_results_table)
            rb_04 = SE(
                parent=self.parent, row_id=9, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["ma_datareduction"]["Radiobutton"][1], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Show Drift Correction", sticky="nesw", relief=tk.GROOVE,
                command=self.show_drift_correction)
            #
            self.container_elements["ma_datareduction"]["Radiobutton"].extend([rb_01, rb_02, rb_03, rb_04])
            #
            ## BUTTONS
            btn_01 = SE(
                parent=self.parent, row_id=10, column_id=21, n_rows=2, n_columns=9, fg=self.green_dark,
                bg=self.red_dark).create_simple_button(
                text="Export Calculation Report", bg_active=self.green_dark, fg_active=self.green_light,
                command=lambda file_type=self.container_var["ma_datareduction"]["Option File"],
                               data_type=self.container_var["ma_datareduction"]["Radiobutton"][0]:
                self.export_calculation_report(file_type, data_type))
            #
            self.container_elements["ma_datareduction"]["Button"].extend([btn_01])
            #
            for filetype in list_files:
                for datatype in [0, 1]:
                    self.calculcate_sensitivity_drift(var_datatype=datatype)
                    self.datareduction(filetype=filetype, datatype=datatype)
    #
    def show_drift_correction(self):
        ## Cleaning
        gui_categories = ["Label", "Entry"]
        for gui_category in gui_categories:
            if len(self.gui_elements["ma_datareduction"][gui_category]["Specific"]) > 0:
                for item in self.gui_elements["ma_datareduction"][gui_category]["Specific"]:
                    item.grid_remove()
        #
        ## OPTION MENU
        self.container_var["ma_datareduction"]["Option Drift"] = tk.StringVar()
        self.container_var["ma_datareduction"]["Option Drift Relativity"] = tk.StringVar()
        opt_menu_iso = SE(
            parent=self.parent, row_id=13, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
            bg=self.green_medium).create_option_isotope(
            var_iso=self.container_var["ma_datareduction"]["Option Drift"], option_list=self.list_isotopes,
            text_set="Select Isotope", fg_active=self.green_dark, bg_active=self.red_dark,
            command=lambda var_opt=self.container_var["ma_datareduction"]["Option Drift"]:
            self.create_drift_correction_diagram(var_opt))
        opt_menu_driftrelativity = SE(
            parent=self.parent, row_id=14, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
            bg=self.green_medium).create_option_isotope(
            var_iso=self.container_var["ma_datareduction"]["Option Drift Relativity"], option_list=self.list_isotopes,
            text_set=self.container_lists["IS"][0], fg_active=self.green_dark, bg_active=self.red_dark,
            command=lambda var_opt=self.container_var["ma_datareduction"]["Option Drift"]:
            self.create_drift_correction_diagram(var_opt))
        self.container_elements["ma_datareduction"]["Option Menu"].extend([opt_menu_iso, opt_menu_driftrelativity])
        self.gui_elements["ma_datareduction"]["Option Menu"]["Specific"].extend([opt_menu_iso, opt_menu_driftrelativity])
    #
    def show_results_table(self):
        ## Cleaning
        gui_categories = ["Option Menu"]
        for gui_category in gui_categories:
            if len(self.gui_elements["ma_datareduction"][gui_category]["Specific"]) > 0:
                for item in self.gui_elements["ma_datareduction"][gui_category]["Specific"]:
                    item.grid_remove()
        #
        try:
            self.fig_drift.clf()
            self.ax_drift.cla()
            self.ax_drift_02.cla()
            self.canvas_drift.get_tk_widget().grid_remove()
            self.toolbarFrame_drift.grid_remove()
        except AttributeError:
            pass
        ## Reconstruction
        try:
            for entr_item in self.gui_elements["ma_datareduction"]["Label"]["Specific"]:
                entr_item.grid()
            for entr_item in self.gui_elements["ma_datareduction"]["Entry"]["Specific"]:
                entr_item.grid()
        except:
            print("Error!")
    #
    def create_drift_correction_diagram(self, var_opt):
        #
        try:
            self.fig_drift.clf()
            self.ax_drift.cla()
            self.ax_drift_02.cla()
            self.canvas_drift.get_tk_widget().grid_remove()
            self.toolbarFrame_drift.grid_remove()
        except AttributeError:
            pass
        try:
            if self.canvas_drift:
                self.canvas_drift.destroy()
            if self.toolbarFrame_drift:
                self.toolbarFrame_drift.destroy()
        except AttributeError:
            pass
        self.gui_elements["ma_datareduction"]["Frame"]["Specific"].clear()
        self.gui_elements["ma_datareduction"]["Canvas"]["Specific"].clear()
        #
        var_is = self.container_var["ma_datareduction"]["Option IS"].get()
        var_i = self.container_var["ma_datareduction"]["Option Drift Relativity"].get()
        ## DIAGRAM
        self.fig_drift = Figure(figsize=(10, 5), facecolor=self.green_light)
        self.ax_drift = self.fig_drift.add_subplot(211)
        self.ax_drift_02 = self.fig_drift.add_subplot(212)

        if var_opt == self.container_var["ma_datareduction"]["Option Drift"]:
            isotope = var_opt
        else:
            isotope = self.container_var["ma_datareduction"]["Option Drift"].get()
        x_times = []
        x_smpl = []
        for key, item in self.std_times.items():
            x_times.append(item["Delta"])
        for key, item in self.smpl_times.items():
            x_times.append(item["Delta"])
            x_smpl.append(item["Delta"])
        x_times.sort()
        x_data = np.array(x_times)
        y_data = self.xi_opt[isotope][0]*x_data + self.xi_opt[isotope][1]
        x_max = max(x_data)
        if max(x_data) < 100:
            x_max = round(max(x_data)+10, -1)
        elif 100 <= max(x_data) < 1000:
            x_max = round(max(x_data)+50, -2)
        elif max(x_data) >= 1000:
            x_max = round(max(x_data)+100, -2)
        y_max = max(y_data)
        x_std = []
        y_std = []
        for file in self.container_lists["STD"]["Short"]:
            x_std.append(self.xi_std_time[file][isotope][0])
            y_std.append(self.xi_std_time[file][isotope][1])
        y_smpl = []
        key_id = re.search("(\D+)( Files)", self.container_var["ma_datareduction"]["Option File"].get())
        var_id = key_id.group(1)
        for index, file in enumerate(self.container_lists["SMPL"]["Short"]):
            if var_id not in ["All Standard", "All Sample"]:
                if file in self.container_lists["ID Files"][var_id]:
                    y_smpl.append(self.container_results["SMPL"]["SMOOTHED"][isotope]["Sensitivity"][index])
            else:
                y_smpl.append(self.container_results["SMPL"]["SMOOTHED"][isotope]["Sensitivity"][index])

        sct = self.ax_drift.scatter(
            x_std, y_std, label="Standard", color=self.isotope_colors[isotope], edgecolor="black", visible=True,
            marker="o", s=100)
        sct = self.ax_drift.scatter(
            x_smpl, y_smpl, label="Sample", color=self.isotope_colors[isotope], edgecolor="black", visible=True,
            marker="s", s=100)
        ln = self.ax_drift.plot(
            x_data, y_data, label="Sensitivity Fit", color=self.isotope_colors[isotope], visible=True, linewidth=3)
        #self.lines["raw"][isotope] = ln
        self.ax_drift.grid(True)
        self.ax_drift.set_xlim(left=0, right=x_max)
        self.ax_drift.set_xticks(np.linspace(0, x_max, 11))
        #self.ax_drift.set_ylim(top=1.5*y_max)
        self.ax_drift.set_axisbelow(True)
        self.ax_drift.set_xlabel("Time (s)", labelpad=0.5)
        self.ax_drift.set_ylabel("Sensitivity", labelpad=0.5)

        self.fig_drift.subplots_adjust(bottom=0.125, top=0.975, left=0.075, right=0.975)

        legend = self.ax_drift.legend(fontsize="x-small", framealpha=1.0, loc="best", prop={'size': 10})

        x_data_02 = self.container_results["SMPL"]["SMOOTHED"][var_i]["Concentration"]
        y_data_02 = self.container_results["SMPL"]["SMOOTHED"][isotope]["Concentration"]
        sct = self.ax_drift_02.scatter(
            x_data_02, y_data_02, label=isotope, color=self.isotope_colors[isotope], edgecolor="black", visible=True,
            marker="s", s=100)
        self.ax_drift_02.set_xlim(left=0, right=1.05*max(x_data_02))
        self.ax_drift_02.set_ylim(bottom=0, top=1.05*max(y_data_02))
        self.ax_drift_02.grid(True)
        self.ax_drift_02.set_axisbelow(True)
        self.ax_drift_02.set_xlabel("Concentration "+str(var_i)+" (ppm)", labelpad=0.5)
        self.ax_drift_02.set_ylabel("Concentration "+str(isotope)+" (ppm)", labelpad=0.5)

        plt.rcParams["savefig.facecolor"] = "white"
        plt.rcParams["savefig.dpi"] = 300

        self.canvas_drift = FigureCanvasTkAgg(self.fig_drift, master=self.parent)
        self.canvas_drift.get_tk_widget().grid(row=0, column=34, rowspan=38, columnspan=52, sticky="nesw")
        self.toolbarFrame_drift = tk.Frame(master=self.parent)
        self.toolbarFrame_drift.grid(row=38, column=34, rowspan=2, columnspan=52, sticky="w")
        self.toolbar_drift = NavigationToolbar2Tk(self.canvas_drift, self.toolbarFrame_drift)
        self.toolbar_drift.config(background=self.green_light)
        self.toolbar_drift._message_label.config(background=self.green_light)
        self.toolbar_drift.winfo_children()[-2].config(background=self.green_light)
        #
        self.gui_elements["ma_datareduction"]["Frame"]["Specific"].extend([self.toolbarFrame_drift])
        self.gui_elements["ma_datareduction"]["Canvas"]["Specific"].extend([self.canvas_drift])
    #
    def extract_data_times(self):
        self.std_times = {}
        dates_0, times_0 = Data(filename=self.list_std[0]).import_as_list()
        t_start_0 = datetime.timedelta(hours=int(times_0[0][0]), minutes=int(times_0[0][1]), seconds=int(times_0[0][2]))
        for file in self.list_std:
            parts = file.split("/")
            self.std_times[parts[-1]] = {}
            dates, times = Data(filename=file).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            t_delta_0 = (t_start - t_start_0).total_seconds()
            self.std_times[parts[-1]]["Start"] = t_start
            self.std_times[parts[-1]]["Delta"] = t_delta_0
        #
        self.smpl_times = {}
        #dates_0, times_0 = Data(filename=self.list_smpl[0]).import_as_list()
        #t_start_0 = datetime.timedelta(hours=int(times_0[0][0]), minutes=int(times_0[0][1]), seconds=int(times_0[0][2]))
        for file in self.list_smpl:
            parts = file.split("/")
            self.smpl_times[parts[-1]] = {}
            dates, times = Data(filename=file).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            t_delta_0 = (t_start - t_start_0).total_seconds()
            self.smpl_times[parts[-1]]["Start"] = t_start
            self.smpl_times[parts[-1]]["Delta"] = t_delta_0
    #
    def calculcate_sensitivity_drift(self, var_datatype):
        #
        self.xi_opt = {}
        var_is = self.container_var["ma_datareduction"]["Option IS"].get()
        key_element = re.search("(\D+)(\d+)", var_is)
        var_is_element = key_element.group(1)
        helper_data = {}
        for file in self.container_lists["STD"]["Short"]:
            if file not in self.xi_std_time:
                self.xi_std_time[file] = {}
        self.extract_data_times()
        #
        for isotope in self.list_isotopes:
            #
            key_element = re.search("(\D+)(\d+)", isotope)
            element = key_element.group(1)
            var_srm = self.container_files["SRM"][isotope].get()
            self.xi_opt[isotope] = []
            helper_data[isotope] = []
            #
            for file in self.container_lists["STD"]["Short"]:
                #
                if file not in self.xi_std_time:
                    self.xi_std_time[file] = {}
                var_srm_std = self.container_files["STD"][file]["SRM"].get()
                #
                if var_srm_std == var_srm:
                    #
                    var_is_bg_raw = np.mean(
                        self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                    var_is_bg_smoothed = np.mean(
                        self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                    var_i_bg_raw = np.mean(
                        self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"])
                    var_i_bg_smoothed = np.mean(
                        self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"])
                    #
                    var_is_sig_raw = np.mean(
                        self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                    var_is_sig_smoothed = np.mean(
                        self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                    var_i_sig_raw = np.mean(
                        self.container_measurements["SELECTED"][file]["RAW"][isotope]["SIG"])
                    var_i_sig_smoothed = np.mean(
                        self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["SIG"])
                    #
                    var_is_corrected_raw = var_is_sig_raw - var_is_bg_raw
                    var_i_corrected_raw = var_i_sig_raw - var_i_bg_raw
                    var_is_corrected_smoothed = var_is_sig_smoothed - var_is_bg_smoothed
                    var_i_corrected_smoothed = var_i_sig_smoothed - var_i_bg_smoothed
                    #
                    if var_datatype == 0:  # RAW
                        var_concentration_is = self.srm_actual[var_srm][var_is_element]  # Concentration IS
                        intensity_ratio = var_i_corrected_raw / var_is_corrected_raw
                        if element in self.srm_actual[var_srm]:
                            var_concentration_i = self.srm_actual[var_srm][element]  # Concentration Isotope
                            concentration_ratio = var_concentration_is / var_concentration_i
                            value_02 = round(intensity_ratio * concentration_ratio, 6)
                        else:
                            value_02 = round(0.0, 6)
                        if var_srm_std == self.container_var["ma_datareduction"]["Option SRM"].get() \
                                and var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                            helper_data[isotope].append(value_02)
                    #
                    elif var_datatype == 1:  # SMOOTHED
                        var_concentration_is = self.srm_actual[var_srm][var_is_element]  # Concentration IS
                        intensity_ratio = var_i_corrected_smoothed / var_is_corrected_smoothed
                        if element in self.srm_actual[var_srm]:
                            var_concentration_i = self.srm_actual[var_srm][element]  # Concentration Isotope
                            concentration_ratio = var_concentration_is / var_concentration_i
                            value_02 = round(intensity_ratio * concentration_ratio, 6)
                        else:
                            value_02 = round(0.0, 6)
                        if var_srm_std == self.container_var["ma_datareduction"]["Option SRM"].get() \
                                and var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                            helper_data[isotope].append(value_02)
                #
                if isotope not in self.xi_std_time[file]:
                    self.xi_std_time[file][isotope] = [self.std_times[file]["Delta"],
                                                       round(np.mean(helper_data[isotope]), 6)]
                #
            self.xi_regr = self.calculate_regression(data=self.xi_std_time, isotope=isotope,
                                                     file_data=self.container_lists["STD"]["Short"])
            self.xi_opt[isotope].extend(self.xi_regr)
    #
    def change_id_option_results(self, var_id):
        print("Selected ID:", var_id)
        print("Related Files:", self.container_lists["ID Files"][var_id])
    #
    def datareduction(self, filetype, datatype=None, fill_entry=False):
        #
        if datatype == None:
            var_datatype = self.container_var["ma_datareduction"]["Radiobutton"][0].get()
        else:
            var_datatype = datatype
        #
        var_is = self.container_var["ma_datareduction"]["Option IS"].get()
        key_element = re.search("(\D+)(\d+)", var_is)
        var_is_element = key_element.group(1)
        var_filetype = {"STD": 0, "SMPL": 0}
        if len(filetype) == 7:
            key_id = re.search("(\D+)( Files)", filetype)
            var_id = key_id.group(1)
            for file in self.container_lists["ID Files"][var_id]:
                if file in self.container_lists["STD"]["Short"]:
                    var_filetype["STD"] += 1
                elif file in self.container_lists["SMPL"]["Short"]:
                    var_filetype["SMPL"] += 1
            if var_filetype["STD"] > 0:
                var_filetype["Result"] = "STD"
            elif var_filetype["SMPL"] > 0:
                var_filetype["Result"] = "SMPL"
        #
        ## Intensity Ratios
        helper_data = {}        # Intensity Ratio Container
        helper_data_02 = {}     # Sensitivity Container
        helper_data_03 = {}     # Concentration Container
        helper_data_04 = {}     # Relative Sensitivity Factor Container
        helper_data_05 = {}     # Limit of Detection Container
        for isotope in self.list_isotopes:
            helper_data[isotope] = []
            helper_data_02[isotope] = []
            helper_data_03[isotope] = []
            helper_data_04[isotope] = []
            helper_data_05[isotope] = []
            #
            key_element = re.search("(\D+)(\d+)", isotope)
            element = key_element.group(1)
            #
            if filetype == "All Standard Files":
                for file in self.container_lists["STD"]["Short"]:
                    var_srm = self.container_files["STD"][file]["SRM"].get()
                    #
                    var_is_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                    var_is_bg_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                    var_i_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"])
                    var_i_bg_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"])
                    var_i_bg_raw_std = np.std(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"], ddof=1)
                    var_i_bg_smoothed_std = np.std(self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"], ddof=1)
                    var_n_bg_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                    var_n_bg_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                    #
                    var_is_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                    var_is_sig_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                    var_i_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["SIG"])
                    var_i_sig_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["SIG"])
                    var_n_sig_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                    var_n_sig_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                    #
                    var_dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                    #
                    var_is_corrected_raw_2 = var_is_sig_raw - var_is_bg_raw
                    if var_is_corrected_raw_2 >= 0:
                        var_is_corrected_raw = var_is_corrected_raw_2
                    else:
                        var_is_corrected_raw = 0.0
                    var_i_corrected_raw_2 = var_i_sig_raw - var_i_bg_raw
                    if var_i_corrected_raw_2 >= 0:
                        var_i_corrected_raw = var_i_corrected_raw_2
                    else:
                        var_i_corrected_raw = 0.0
                    var_is_corrected_smoothed_2 = var_is_sig_smoothed - var_is_bg_smoothed
                    if var_is_corrected_smoothed_2 >= 0:
                        var_is_corrected_smoothed = var_is_corrected_smoothed_2
                    else:
                        var_is_corrected_smoothed = 0.0
                    var_i_corrected_smoothed_2 = var_i_sig_smoothed - var_i_bg_smoothed
                    if var_i_corrected_smoothed_2 >= 0:
                        var_i_corrected_smoothed = var_i_corrected_smoothed_2
                    else:
                        var_i_corrected_smoothed = 0.0
                    #
                    if var_datatype == 0:                                                       # RAW
                        var_concentration_is = self.srm_actual[var_srm][var_is_element]         # Concentration IS
                        intensity_ratio = var_i_corrected_raw/var_is_corrected_raw
                        if element in self.srm_actual[var_srm]:
                            var_concentration_i = self.srm_actual[var_srm][element]             # Concentration Isotope
                            concentration_ratio = var_concentration_is/var_concentration_i
                            value_02 = intensity_ratio*concentration_ratio
                            value_03 = var_concentration_i
                            value_05 = (3.29*(var_i_bg_raw*var_dwell_time_i*var_n_sig_raw*(1 + var_n_sig_raw/var_n_bg_raw))**(0.5) + 2.71)/(var_n_sig_raw*var_dwell_time_i*value_02)
                            #value_05 = 3*var_i_bg_raw_std*np.sqrt(1/(var_n_bg_raw) + 1/(var_n_sig_raw))*1/(value_02)*(var_concentration_is)/(var_is_corrected_raw)
                        else:
                            value_02 = 0.0
                            value_03 = 0.0
                            value_05 = 0.0
                        value = intensity_ratio
                        value_04 = 1.0
                        if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                            helper_data[isotope].append(value)
                            helper_data_02[isotope].append(value_02)
                            helper_data_03[isotope].append(value_03)
                            helper_data_04[isotope].append(value_04)
                            helper_data_05[isotope].append(value_05)
                    #
                    elif var_datatype == 1:   # SMOOTHED
                        var_concentration_is = self.srm_actual[var_srm][var_is_element]     # Concentration IS
                        intensity_ratio = var_i_corrected_smoothed/var_is_corrected_smoothed
                        if element in self.srm_actual[var_srm]:
                            var_concentration_i = self.srm_actual[var_srm][element]             # Concentration Isotope
                            concentration_ratio = var_concentration_is/var_concentration_i
                            value_02 = intensity_ratio*concentration_ratio
                            value_03 = var_concentration_i
                            value_05 = (3.29 * (var_i_bg_smoothed * var_dwell_time_i * var_n_sig_smoothed * (
                                        1 + var_n_sig_smoothed / var_n_bg_smoothed)) ** (0.5) + 2.71) / (
                                                   var_n_sig_smoothed * var_dwell_time_i * value_02)
                            #value_05 = 3*var_i_bg_smoothed_std*np.sqrt(1/(var_n_bg_smoothed) + 1/(var_n_sig_smoothed))*1/(value_02)*(var_concentration_is)/(var_is_corrected_smoothed)
                        else:
                            value_02 = 0.0
                            value_03 = 0.0
                            value_05 = 0.0
                        value = intensity_ratio
                        value_04 = 1.0
                        if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                            helper_data[isotope].append(value)
                            helper_data_02[isotope].append(value_02)
                            helper_data_03[isotope].append(value_03)
                            helper_data_04[isotope].append(value_04)
                            helper_data_05[isotope].append(value_05)
            #
            elif filetype == "All Sample Files":
                var_srm = self.container_files["SRM"][isotope].get()
                var_dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                for file in self.container_lists["STD"]["Short"]:
                    var_srm_std = self.container_files["STD"][file]["SRM"].get()
                    if var_srm_std == var_srm:
                        #
                        var_is_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                        var_is_bg_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                        #
                        var_is_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                        var_is_sig_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                        #
                        var_is_corrected_raw_2 = var_is_sig_raw - var_is_bg_raw
                        if var_is_corrected_raw_2 >= 0:
                            var_is_corrected_raw = var_is_corrected_raw_2
                        else:
                            var_is_corrected_raw = 0.0
                        var_is_corrected_smoothed_2 = var_is_sig_smoothed - var_is_bg_smoothed
                        if var_is_corrected_smoothed_2 >= 0:
                            var_is_corrected_smoothed = var_is_corrected_smoothed_2
                        else:
                            var_is_corrected_smoothed = 0.0
                        #
                        var_is_corrected_raw_std = var_is_corrected_raw
                        var_is_corrected_smoothed_std = var_is_corrected_smoothed
                        #
                for file in self.container_lists["SMPL"]["Short"]:
                    var_is_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                    var_is_bg_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                    var_i_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"])
                    var_i_bg_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"])
                    var_i_bg_raw_std = np.std(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"], ddof=1)
                    var_i_bg_smoothed_std = np.std(self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"], ddof=1)
                    var_n_bg_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                    var_n_bg_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                    #
                    var_is_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                    var_is_sig_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                    var_i_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["SIG"])
                    var_i_sig_smoothed = np.mean(self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["SIG"])
                    var_n_sig_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                    var_n_sig_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                    #
                    var_is_corrected_raw_2 = var_is_sig_raw - var_is_bg_raw
                    if var_is_corrected_raw_2 >= 0:
                        var_is_corrected_raw = var_is_corrected_raw_2
                    else:
                        var_is_corrected_raw = 0.0
                    var_i_corrected_raw_2 = var_i_sig_raw - var_i_bg_raw
                    if var_i_corrected_raw_2 >= 0:
                        var_i_corrected_raw = var_i_corrected_raw_2
                    else:
                        var_i_corrected_raw = 0.0
                    var_is_corrected_smoothed_2 = var_is_sig_smoothed - var_is_bg_smoothed
                    if var_is_corrected_smoothed_2 >= 0:
                        var_is_corrected_smoothed = var_is_corrected_smoothed_2
                    else:
                        var_is_corrected_smoothed = 0.0
                    var_i_corrected_smoothed_2 = var_i_sig_smoothed - var_i_bg_smoothed
                    if var_i_corrected_smoothed_2 >= 0:
                        var_i_corrected_smoothed = var_i_corrected_smoothed_2
                    else:
                        var_i_corrected_smoothed = 0.0
                    #
                    if var_datatype == 0:     # RAW
                        var_concentration_is = float(self.container_files["SMPL"][file]["IS Concentration"].get()) # Concentration IS
                        var_concentration_is_std = self.srm_actual[var_srm][var_is_element]     # Concentration IS STD
                        intensity_ratio = var_i_corrected_raw/var_is_corrected_raw
                        if element in self.srm_actual[var_srm]:
                            value_02 = self.xi_opt[isotope][0]*self.smpl_times[file]["Delta"] + self.xi_opt[isotope][1]
                            value_03 = intensity_ratio*(var_concentration_is)/(value_02)
                            value_05 = (3.29 * (var_i_bg_raw * var_dwell_time_i * var_n_sig_raw * (
                                    1 + var_n_sig_raw / var_n_bg_raw)) ** (0.5) + 2.71) / (
                                               var_n_sig_raw * var_dwell_time_i * value_02)
                            #value_05 = 3*var_i_bg_raw_std*np.sqrt(1/(var_n_bg_raw) + 1/(var_n_sig_raw))*1/(value_02)*(var_concentration_is)/(var_is_corrected_raw)
                        else:
                            value_02 = 0.0
                            value_03 = 0.0
                            value_05 = 0.0
                        value = intensity_ratio
                        value_04 = (var_concentration_is_std)/(var_is_corrected_raw_std)*(var_is_corrected_raw)/(var_concentration_is)
                        if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                            helper_data[isotope].append(value)
                            helper_data_02[isotope].append(value_02)
                            helper_data_03[isotope].append(value_03)
                            helper_data_04[isotope].append(value_04)
                            helper_data_05[isotope].append(value_05)
                    #
                    elif var_datatype == 1:   # SMOOTHED
                        var_concentration_is = float(self.container_files["SMPL"][file]["IS Concentration"].get()) # Concentration IS
                        var_concentration_is_std = self.srm_actual[var_srm][var_is_element]     # Concentration IS STD
                        intensity_ratio = var_i_corrected_smoothed/var_is_corrected_smoothed
                        if element in self.srm_actual[var_srm]:
                            value_02 = self.xi_opt[isotope][0]*self.smpl_times[file]["Delta"] + self.xi_opt[isotope][1]
                            value_03 = intensity_ratio*(var_concentration_is)/(value_02)
                            value_05 = (3.29 * (var_i_bg_smoothed * var_dwell_time_i * var_n_sig_smoothed * (
                                    1 + var_n_sig_smoothed / var_n_bg_smoothed)) ** (0.5) + 2.71) / (
                                               var_n_sig_smoothed * var_dwell_time_i * value_02)
                            #value_05 = 3*var_i_bg_smoothed_std*np.sqrt(1/(var_n_bg_smoothed) + 1/(var_n_sig_smoothed))*1/(value_02)*(var_concentration_is)/(var_is_corrected_smoothed)
                        else:
                            value_02 = 0.0
                            value_03 = 0.0
                            value_05 = 0.0
                        value = intensity_ratio
                        value_04 = (var_concentration_is_std)/(var_is_corrected_smoothed_std)*(var_is_corrected_smoothed)/(var_concentration_is)
                        if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                            helper_data[isotope].append(value)
                            helper_data_02[isotope].append(value_02)
                            helper_data_03[isotope].append(value_03)
                            helper_data_04[isotope].append(value_04)
                            helper_data_05[isotope].append(value_05)
            #
            elif len(filetype) == 7:
                if var_filetype["Result"] == "STD":
                    for file in self.container_lists["ID Files"][var_id]:
                        var_srm = self.container_files["STD"][file]["SRM"].get()
                        var_dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                        #
                        var_is_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                        var_is_bg_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                        var_i_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"])
                        var_i_bg_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"])
                        var_i_bg_raw_std = np.std(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"],
                                                  ddof=1)
                        var_i_bg_smoothed_std = np.std(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"], ddof=1)
                        var_n_bg_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                        var_n_bg_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                        #
                        var_is_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                        var_is_sig_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                        var_i_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["SIG"])
                        var_i_sig_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["SIG"])
                        var_n_sig_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                        var_n_sig_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                        #
                        var_is_corrected_raw_2 = var_is_sig_raw - var_is_bg_raw
                        if var_is_corrected_raw_2 >= 0:
                            var_is_corrected_raw = var_is_corrected_raw_2
                        else:
                            var_is_corrected_raw = 0.0
                        var_i_corrected_raw_2 = var_i_sig_raw - var_i_bg_raw
                        if var_i_corrected_raw_2 >= 0:
                            var_i_corrected_raw = var_i_corrected_raw_2
                        else:
                            var_i_corrected_raw = 0.0
                        var_is_corrected_smoothed_2 = var_is_sig_smoothed - var_is_bg_smoothed
                        if var_is_corrected_smoothed_2 >= 0:
                            var_is_corrected_smoothed = var_is_corrected_smoothed_2
                        else:
                            var_is_corrected_smoothed = 0.0
                        var_i_corrected_smoothed_2 = var_i_sig_smoothed - var_i_bg_smoothed
                        if var_i_corrected_smoothed_2 >= 0:
                            var_i_corrected_smoothed = var_i_corrected_smoothed_2
                        else:
                            var_i_corrected_smoothed = 0.0
                        #
                        if var_datatype == 0:  # RAW
                            var_concentration_is = self.srm_actual[var_srm][var_is_element]  # Concentration IS
                            intensity_ratio = var_i_corrected_raw / var_is_corrected_raw
                            if element in self.srm_actual[var_srm]:
                                var_concentration_i = self.srm_actual[var_srm][element]  # Concentration Isotope
                                concentration_ratio = var_concentration_is / var_concentration_i
                                value_02 = intensity_ratio * concentration_ratio
                                value_03 = var_concentration_i
                                value_05 = (3.29 * (var_i_bg_raw * var_dwell_time_i * var_n_sig_raw * (
                                        1 + var_n_sig_raw / var_n_bg_raw)) ** (0.5) + 2.71) / (
                                                   var_n_sig_raw * var_dwell_time_i * value_02)
                                #value_05 = 3 * var_i_bg_raw_std * np.sqrt(1 / (var_n_bg_raw) + 1 / (var_n_sig_raw)) * 1 / (value_02) * (var_concentration_is) / (var_is_corrected_raw)
                            else:
                                value_02 = 0.0
                                value_03 = 0.0
                                value_05 = 0.0
                            value = intensity_ratio
                            value_04 = 1.0
                            if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                                helper_data[isotope].append(value)
                                helper_data_02[isotope].append(value_02)
                                helper_data_03[isotope].append(value_03)
                                helper_data_04[isotope].append(value_04)
                                helper_data_05[isotope].append(value_05)
                        #
                        elif var_datatype == 1:  # SMOOTHED
                            var_concentration_is = self.srm_actual[var_srm][var_is_element]  # Concentration IS
                            intensity_ratio = var_i_corrected_smoothed / var_is_corrected_smoothed
                            if element in self.srm_actual[var_srm]:
                                var_concentration_i = self.srm_actual[var_srm][element]  # Concentration Isotope
                                concentration_ratio = var_concentration_is / var_concentration_i
                                value_02 = intensity_ratio * concentration_ratio
                                value_03 = var_concentration_i
                                value_05 = (3.29 * (var_i_bg_smoothed * var_dwell_time_i * var_n_sig_smoothed * (
                                        1 + var_n_sig_smoothed / var_n_bg_smoothed)) ** (0.5) + 2.71) / (
                                                   var_n_sig_smoothed * var_dwell_time_i * value_02)
                                # value_05 = 3 * var_i_bg_smoothed_std * np.sqrt(
                                #     1 / (var_n_bg_smoothed) + 1 / (var_n_sig_smoothed)) * 1 / (value_02) * (
                                #                var_concentration_is) / (var_is_corrected_smoothed)
                            else:
                                value_02 = 0.0
                                value_03 = 0.0
                                value_05 = 0.0
                            value = intensity_ratio
                            value_04 = 1.0
                            if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                                helper_data[isotope].append(value)
                                helper_data_02[isotope].append(value_02)
                                helper_data_03[isotope].append(value_03)
                                helper_data_04[isotope].append(value_04)
                                helper_data_05[isotope].append(value_05)
                #
                elif var_filetype["Result"] == "SMPL":
                    var_srm = self.container_files["SRM"][isotope].get()
                    var_dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                    for file in self.container_lists["STD"]["Short"]:
                        var_srm_std = self.container_files["STD"][file]["SRM"].get()
                        if var_srm_std == var_srm:
                            #
                            var_is_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                            var_is_bg_smoothed = np.mean(
                                self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                            #
                            var_is_sig_raw = np.mean(
                                self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                            var_is_sig_smoothed = np.mean(
                                self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                            #
                            var_is_corrected_raw_2 = var_is_sig_raw - var_is_bg_raw
                            if var_is_corrected_raw_2 >= 0:
                                var_is_corrected_raw = var_is_corrected_raw_2
                            else:
                                var_is_corrected_raw = 0.0
                            var_is_corrected_smoothed_2 = var_is_sig_smoothed - var_is_bg_smoothed
                            if var_is_corrected_smoothed_2 >= 0:
                                var_is_corrected_smoothed = var_is_corrected_smoothed_2
                            else:
                                var_is_corrected_smoothed = 0.0
                            #
                            var_is_corrected_raw_std = var_is_corrected_raw
                            var_is_corrected_smoothed_std = var_is_corrected_smoothed
                            #
                    for file in self.container_lists["ID Files"][var_id]:
                        var_is_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                        var_is_bg_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                        var_i_bg_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"])
                        var_i_bg_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"])
                        var_i_bg_raw_std = np.std(self.container_measurements["SELECTED"][file]["RAW"][isotope]["BG"],
                                                  ddof=1)
                        var_i_bg_smoothed_std = np.std(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["BG"], ddof=1)
                        var_n_bg_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["BG"])
                        var_n_bg_smoothed = len(self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["BG"])
                        #
                        var_is_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                        var_is_sig_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                        var_i_sig_raw = np.mean(self.container_measurements["SELECTED"][file]["RAW"][isotope]["SIG"])
                        var_i_sig_smoothed = np.mean(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["SIG"])
                        var_n_sig_raw = len(self.container_measurements["SELECTED"][file]["RAW"][var_is]["SIG"])
                        var_n_sig_smoothed = len(
                            self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["SIG"])
                        #
                        var_is_corrected_raw_2 = var_is_sig_raw - var_is_bg_raw
                        if var_is_corrected_raw_2 >= 0:
                            var_is_corrected_raw = var_is_corrected_raw_2
                        else:
                            var_is_corrected_raw = 0.0
                        var_i_corrected_raw_2 = var_i_sig_raw - var_i_bg_raw
                        if var_i_corrected_raw_2 >= 0:
                            var_i_corrected_raw = var_i_corrected_raw_2
                        else:
                            var_i_corrected_raw = 0.0
                        var_is_corrected_smoothed_2 = var_is_sig_smoothed - var_is_bg_smoothed
                        if var_is_corrected_smoothed_2 >= 0:
                            var_is_corrected_smoothed = var_is_corrected_smoothed_2
                        else:
                            var_is_corrected_smoothed = 0.0
                        var_i_corrected_smoothed_2 = var_i_sig_smoothed - var_i_bg_smoothed
                        if var_i_corrected_smoothed_2 >= 0:
                            var_i_corrected_smoothed = var_i_corrected_smoothed_2
                        else:
                            var_i_corrected_smoothed = 0.0
                        #
                        if var_datatype == 0:  # RAW
                            var_concentration_is = float(
                                self.container_files["SMPL"][file]["IS Concentration"].get())  # Concentration IS
                            var_concentration_is_std = self.srm_actual[var_srm][var_is_element]  # Concentration IS STD
                            intensity_ratio = var_i_corrected_raw / var_is_corrected_raw
                            if element in self.srm_actual[var_srm]:
                                value_02 = self.xi_opt[isotope][0] * self.smpl_times[file]["Delta"] + \
                                           self.xi_opt[isotope][1]
                                value_03 = intensity_ratio * (var_concentration_is) / (value_02)
                                value_05 = (3.29 * (var_i_bg_raw * var_dwell_time_i * var_n_sig_raw * (
                                        1 + var_n_sig_raw / var_n_bg_raw)) ** (0.5) + 2.71) / (
                                                   var_n_sig_raw * var_dwell_time_i * value_02)
                                # value_05 = 3 * var_i_bg_raw_std * np.sqrt(
                                #     1 / (var_n_bg_raw) + 1 / (var_n_sig_raw)) * 1 / (value_02) * (
                                #                var_concentration_is) / (var_is_corrected_raw)
                            else:
                                value_02 = 0.0
                                value_03 = 0.0
                                value_05 = 0.0
                            value = intensity_ratio
                            value_04 = (var_concentration_is_std) / (var_is_corrected_raw_std) * (
                                var_is_corrected_raw) / (var_concentration_is)
                            if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                                helper_data[isotope].append(value)
                                helper_data_02[isotope].append(value_02)
                                helper_data_03[isotope].append(value_03)
                                helper_data_04[isotope].append(value_04)
                                helper_data_05[isotope].append(value_05)
                        #
                        elif var_datatype == 1:  # SMOOTHED
                            var_concentration_is = float(
                                self.container_files["SMPL"][file]["IS Concentration"].get())  # Concentration IS
                            var_concentration_is_std = self.srm_actual[var_srm][var_is_element]  # Concentration IS STD
                            intensity_ratio = var_i_corrected_smoothed / var_is_corrected_smoothed
                            if element in self.srm_actual[var_srm]:
                                value_02 = self.xi_opt[isotope][0] * self.smpl_times[file]["Delta"] + \
                                           self.xi_opt[isotope][1]
                                value_03 = intensity_ratio * (var_concentration_is) / (value_02)
                                value_05 = (3.29 * (var_i_bg_smoothed * var_dwell_time_i * var_n_sig_smoothed * (
                                        1 + var_n_sig_smoothed / var_n_bg_smoothed)) ** (0.5) + 2.71) / (
                                                   var_n_sig_smoothed * var_dwell_time_i * value_02)
                                # value_05 = 3 * var_i_bg_smoothed_std * np.sqrt(
                                #     1 / (var_n_bg_smoothed) + 1 / (var_n_sig_smoothed)) * 1 / (value_02) * (
                                #                var_concentration_is) / (var_is_corrected_smoothed)
                            else:
                                value_02 = 0.0
                                value_03 = 0.0
                                value_05 = 0.0
                            value = intensity_ratio
                            value_04 = (var_concentration_is_std) / (var_is_corrected_smoothed_std) * (
                                var_is_corrected_smoothed) / (var_concentration_is)
                            if var_srm == self.container_var["ma_datareduction"]["Option SRM"].get():
                                helper_data[isotope].append(value)
                                helper_data_02[isotope].append(value_02)
                                helper_data_03[isotope].append(value_03)
                                helper_data_04[isotope].append(value_04)
                                helper_data_05[isotope].append(value_05)
            #
            ## Intensity Ratio
            if fill_entry == True:
                self.container_var["ma_datareduction"][isotope][0].set(round(np.mean(helper_data[isotope]), 8))
                self.container_var["ma_datareduction"][isotope][1].set(round(np.std(helper_data[isotope], ddof=1), 8))
            if var_datatype == 0:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["RAW"][isotope]["Intensity Ratio"] = helper_data[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["RAW"][isotope]["Intensity Ratio"] = helper_data[isotope]
            elif var_datatype == 1:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["SMOOTHED"][isotope]["Intensity Ratio"] = helper_data[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["SMOOTHED"][isotope]["Intensity Ratio"] = helper_data[isotope]
            #
            ## Sensitivity
            if fill_entry == True:
                self.container_var["ma_datareduction"][isotope][2].set(round(np.mean(helper_data_02[isotope]), 8))
                self.container_var["ma_datareduction"][isotope][3].set(round(np.std(helper_data_02[isotope], ddof=1), 8))
            if var_datatype == 0:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["RAW"][isotope]["Sensitivity"] = helper_data_02[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["RAW"][isotope]["Sensitivity"] = helper_data_02[isotope]
            elif var_datatype == 1:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["SMOOTHED"][isotope]["Sensitivity"] = helper_data_02[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["SMOOTHED"][isotope]["Sensitivity"] = helper_data_02[isotope]
            #
            ## Concentration
            if fill_entry == True:
                self.container_var["ma_datareduction"][isotope][4].set(round(np.mean(helper_data_03[isotope]), 8))
                self.container_var["ma_datareduction"][isotope][5].set(round(np.std(helper_data_03[isotope], ddof=1), 8))
            if var_datatype == 0:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["RAW"][isotope]["Concentration"] = helper_data_03[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["RAW"][isotope]["Concentration"] = helper_data_03[isotope]
            elif var_datatype == 1:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["SMOOTHED"][isotope]["Concentration"] = helper_data_03[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["SMOOTHED"][isotope]["Concentration"] = helper_data_03[isotope]
            #
            ## Relative Sensitivity Factor
            if fill_entry == True:
                self.container_var["ma_datareduction"][isotope][6].set(round(np.mean(helper_data_04[isotope]), 8))
                self.container_var["ma_datareduction"][isotope][7].set(round(np.std(helper_data_04[isotope], ddof=1), 8))
            if var_datatype == 0:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["RAW"][isotope]["RSF"] = helper_data_04[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["RAW"][isotope]["RSF"] = helper_data_04[isotope]
            elif var_datatype == 1:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["SMOOTHED"][isotope]["RSF"] = helper_data_04[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["SMOOTHED"][isotope]["RSF"] = helper_data_04[isotope]
            #
            ## Limit of Detection
            if fill_entry == True:
                self.container_var["ma_datareduction"][isotope][8].set(round(np.mean(helper_data_05[isotope]), 8))
                self.container_var["ma_datareduction"][isotope][9].set(round(np.std(helper_data_05[isotope], ddof=1), 8))
            if var_datatype == 0:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["RAW"][isotope]["LOD"] = helper_data_05[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["RAW"][isotope]["LOD"] = helper_data_05[isotope]
            elif var_datatype == 1:
                if filetype == "All Standard Files":
                    self.container_results["STD"]["SMOOTHED"][isotope]["LOD"] = helper_data_05[isotope]
                elif filetype == "All Sample Files":
                    self.container_results["SMPL"]["SMOOTHED"][isotope]["LOD"] = helper_data_05[isotope]
    #
    def calculate_regression(self, data, isotope, file_data):
        x_data = []
        y_data = []
        for file in file_data:
            x_data.append(data[file][isotope][0])
            y_data.append(data[file][isotope][1])
        #
        A = np.vstack([x_data, np.ones(len(x_data))]).T
        m, c = np.linalg.lstsq(A, y_data, rcond=None)[0]  # m*x + c
        results = [m, c]
        #
        return results
    #
    def confirm_edits(self, filename, filetype):
        self.container_var[filetype][filename]["Frame"].config(bg=self.sign_green)
    #
    def change_radiobutton(self, var, value):
        var.set(value)
    #
    def change_carrier_gas(self, var_opt):
        if var_opt == "Helium":
            self.var_entr_10.set("24.587")
            for isotope in self.list_isotopes:
                key_element = re.search("(\D+)(\d+)", isotope)
                element = key_element.group(1)
                if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) \
                        and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                    self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.red_medium)
                else:
                    self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.blue_medium)
        elif var_opt == "Neon":
            self.var_entr_10.set("21.565")
            for isotope in self.list_isotopes:
                key_element = re.search("(\D+)(\d+)", isotope)
                element = key_element.group(1)
                if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) \
                        and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                    self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.red_medium)
                else:
                    self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.blue_medium)
        elif var_opt == "Argon":
            self.var_entr_10.set("15.760")
            for isotope in self.list_isotopes:
                key_element = re.search("(\D+)(\d+)", isotope)
                element = key_element.group(1)
                if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) \
                        and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                    self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.red_medium)
                else:
                    self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.blue_medium)
        elif var_opt == "Krypton":
            self.var_entr_10.set("14.000")
            for isotope in self.list_isotopes:
                key_element = re.search("(\D+)(\d+)", isotope)
                element = key_element.group(1)
                if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) \
                        and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                    self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.red_medium)
                else:
                    self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.blue_medium)
        elif var_opt == "Xenon":
            self.var_entr_10.set("12.130")
            for isotope in self.list_isotopes:
                key_element = re.search("(\D+)(\d+)", isotope)
                element = key_element.group(1)
                if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) \
                        and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                    self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.red_medium)
                else:
                    self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.blue_medium)
        elif var_opt == "Radon":
            self.var_entr_10.set("10.749")
            for isotope in self.list_isotopes:
                key_element = re.search("(\D+)(\d+)", isotope)
                element = key_element.group(1)
                if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) \
                        and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                    self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.red_medium)
                else:
                    self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                    self.container_var["charge"][isotope]["labelvar"].config(bg=self.blue_medium)
    #
    def change_visibility_iw(self, var_cb):
        if var_cb == self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"]:
            if var_cb.get() == 0:
                if self.file_type == "STD":
                    for key_01, value_01 in self.container_helper["STD"].items():
                        for key_02, value_02 in value_01["BG"].items():
                            for object in value_02["Object"]:
                                object.set_visible(False)
                    for key, item in self.container_files[self.file_type][self.filename_short]["BG"].items():
                        item["Box"].set_visible(False)
                elif self.file_type == "SMPL":
                    for key_01, value_01 in self.container_helper["SMPL"].items():
                        for key_02, value_02 in value_01["BG"].items():
                            for object in value_02["Object"]:
                                object.set_visible(False)
            else:
                if self.file_type == "STD":
                    for key_01, value_01 in self.container_helper["STD"].items():
                        for key_02, value_02 in value_01["BG"].items():
                            for object in value_02["Object"]:
                                object.set_visible(True)
                elif self.file_type == "SMPL":
                    for key_01, value_01 in self.container_helper["SMPL"].items():
                        for key_02, value_02 in value_01["BG"].items():
                            for object in value_02["Object"]:
                                object.set_visible(True)
        #
        elif var_cb == self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"]:
            if var_cb.get() == 0:
                if self.file_type == "STD":
                    for key_01, value_01 in self.container_helper["STD"].items():
                        for key_02, value_02 in value_01["SPK"].items():
                            for key_03, value_03 in value_02.items():
                                value_03["Object"].set_visible(False)
                elif self.file_type == "SMPL":
                    for key_01, value_01 in self.container_helper["SMPL"].items():
                        for key_02, value_02 in value_01["SPK"].items():
                            for key_03, value_03 in value_02.items():
                                value_03["Object"].set_visible(False)
            else:
                if self.file_type == "STD":
                    for key_01, value_01 in self.container_helper["STD"].items():
                        for key_02, value_02 in value_01["SPK"].items():
                            for key_03, value_03 in value_02.items():
                                value_03["Object"].set_visible(True)
                elif self.file_type == "SMPL":
                    for key_01, value_01 in self.container_helper["SMPL"].items():
                        for key_02, value_02 in value_01["SPK"].items():
                            for key_03, value_03 in value_02.items():
                                value_03["Object"].set_visible(True)
        #
        try:
            if var_cb == self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SIG"]:
                if var_cb.get() == 0:
                    if self.file_type == "STD":
                        for key_01, value_01 in self.container_helper["STD"].items():
                            for key_02, value_02 in value_01["SIG"].items():
                                for object in value_02["Object"]:
                                    object.set_visible(False)
                                #value_02["Object"].set_visible(False)
                    elif self.file_type == "SMPL":
                        for key_01, value_01 in self.container_helper["SMPL"].items():
                            for key_02, value_02 in value_01["SIG"].items():
                                for object in value_02["Object"]:
                                    object.set_visible(False)
                                #value_02["Object"].set_visible(False)
                else:
                    if self.file_type == "STD":
                        for key_01, value_01 in self.container_helper["STD"].items():
                            for key_02, value_02 in value_01["SIG"].items():
                                for object in value_02["Object"]:
                                    object.set_visible(True)
                                #value_02["Object"].set_visible(True)
                    elif self.file_type == "SMPL":
                        for key_01, value_01 in self.container_helper["SMPL"].items():
                            for key_02, value_02 in value_01["SIG"].items():
                                for object in value_02["Object"]:
                                    object.set_visible(True)
                                #value_02["Object"].set_visible(True)
        except:
            pass
        #
        try:
            if var_cb == self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["MAT"]:
                if var_cb.get() == 0:
                    if self.file_type == "STD":
                        for key_01, value_01 in self.container_helper["STD"].items():
                            for key_02, value_02 in value_01["MAT"].items():
                                value_02["Object"].set_visible(False)
                    elif self.file_type == "SMPL":
                        for key_01, value_01 in self.container_helper["SMPL"].items():
                            for key_02, value_02 in value_01["MAT"].items():
                                value_02["Object"].set_visible(False)
                else:
                    if self.file_type == "STD":
                        for key_01, value_01 in self.container_helper["STD"].items():
                            for key_02, value_02 in value_01["MAT"].items():
                                value_02["Object"].set_visible(True)
                    elif self.file_type == "SMPL":
                        for key_01, value_01 in self.container_helper["SMPL"].items():
                            for key_02, value_02 in value_01["MAT"].items():
                                value_02["Object"].set_visible(True)
        except:
            pass
        #
        try:
            if var_cb == self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["INCL"]:
                if var_cb.get() == 0:
                    if self.file_type == "STD":
                        for key_01, value_01 in self.container_helper["STD"].items():
                            for key_02, value_02 in value_01["INCL"].items():
                                value_02["Object"].set_visible(False)
                    elif self.file_type == "SMPL":
                        for key_01, value_01 in self.container_helper["SMPL"].items():
                            for key_02, value_02 in value_01["INCL"].items():
                                value_02["Object"].set_visible(False)
                else:
                    if self.file_type == "STD":
                        for key_01, value_01 in self.container_helper["STD"].items():
                            for key_02, value_02 in value_01["INCL"].items():
                                value_02["Object"].set_visible(True)
                    elif self.file_type == "SMPL":
                        for key_01, value_01 in self.container_helper["SMPL"].items():
                            for key_02, value_02 in value_01["INCL"].items():
                                value_02["Object"].set_visible(True)
        except:
            pass
        #
        self.diagrams_setup[self.file_type][self.filename_short]["CANVAS"].draw()
        try:
            self.diagrams_setup[self.file_type][self.filename_short]["CANVAS_RATIO"].draw()
        except:
            pass
    #
    def change_rb_value(self, var_rb):
        print(var_rb.get())
    #
    def show_all_lines(self):
        for isotope in self.list_isotopes:
            if self.container_var["plotting"][self.filename_short]["RB"][1].get() == 0:
                self.container_var["plotting"][self.filename_short]["Checkboxes"]["RAW"][isotope].set(1)
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Raw"][isotope][0].set_visible(True)
            elif self.container_var["plotting"][self.filename_short]["RB"][1].get() == 1:
                self.container_var["plotting"][self.filename_short]["Checkboxes"]["SMOOTHED"][isotope].set(1)
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Smoothed"][isotope][0].set_visible(True)
        #
        self.diagrams_setup[self.file_type][self.filename_short]["CANVAS"].draw()
    #
    def hide_all_lines(self):
        for isotope in self.list_isotopes:
            if self.container_var["plotting"][self.filename_short]["RB"][1].get() == 0:
                self.container_var["plotting"][self.filename_short]["Checkboxes"]["RAW"][isotope].set(0)
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Raw"][isotope][0].set_visible(False)
            elif self.container_var["plotting"][self.filename_short]["RB"][1].get() == 1:
                self.container_var["plotting"][self.filename_short]["Checkboxes"]["SMOOTHED"][isotope].set(0)
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Smoothed"][isotope][0].set_visible(False)
        #
        self.diagrams_setup[self.file_type][self.filename_short]["CANVAS"].draw()
    #
    def change_visibility(self, var_cb, name):
        if var_cb is self.container_var["plotting"][self.filename_short]["Checkboxes"]["RAW"][name]:
            if var_cb.get() == 0:
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Raw"][name][0].set_visible(False)
            elif var_cb.get() == 1:
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Raw"][name][0].set_visible(True)
        elif var_cb is self.container_var["plotting"][self.filename_short]["Checkboxes"]["SMOOTHED"][name]:
            if var_cb.get() == 0:
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Smoothed"][name][0].set_visible(False)
            elif var_cb.get() == 1:
                self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Smoothed"][name][0].set_visible(True)
        #
        self.diagrams_setup[self.file_type][self.filename_short]["CANVAS"].draw()
    #
    def calculate_and_place_isotope_ratios(self, var_is, data, lb, mode="MA"):
        #
        index_start = int(0.4 * len(self.times))
        index_end = int(0.6 * len(self.times))
        #
        if var_is != "Select IS":
            try:
                for row in lb.get_children():
                    lb.delete(row)
            except:
                pass
            #
            if mode == "MA":
                try:
                    if self.container_var["settings"]["Time SIG Start"].get() != "Set start time":
                        sig_start = float(self.container_var["settings"]["Time SIG Start"].get())
                        time_start = min(self.times, key=lambda x: abs(x - sig_start))
                        index_start = self.times[self.times == time_start].index[0]
                    if self.container_var["settings"]["Time SIG End"].get() != "Set end time":
                        sig_end = float(self.container_var["settings"]["Time SIG End"].get())
                        time_end = min(self.times, key=lambda x: abs(x - sig_end))
                        index_end = self.times[self.times == time_end].index[0]
                except:
                    index_start = int(0.4*len(self.times))
                    index_end = int(0.6*len(self.times))
            elif mode == "FI":
                try:
                    if self.container_var["settings"]["Time MAT Start"].get() != "Set start time":
                        mat_start = float(self.container_var["settings"]["Time MAT Start"].get())
                        time_start = min(self.times, key=lambda x: abs(x - mat_start))
                        index_start = self.times[self.times == time_start].index[0]
                    if self.container_var["settings"]["Time MAT End"].get() != "Set end time":
                        mat_end = float(self.container_var["settings"]["Time MAT End"].get())
                        time_end = min(self.times, key=lambda x: abs(x - mat_end))
                        index_end = self.times[self.times == time_end].index[0]
                except:
                    index_start = int(0.4*len(self.times))
                    index_end = int(0.6*len(self.times))
            #
            results = {}
            intensities_is = data[var_is][index_start:index_end+1]
            intensities_is = intensities_is.replace(0, np.NaN)
            for isotope in self.list_isotopes:
                intensities_i = data[isotope][index_start:index_end+1]
                intensities_i = intensities_i.replace(0, np.NaN)
                ir = intensities_i/intensities_is
                results[isotope] = round(ir.mean(), 4)
                lb.insert("", tk.END, values=[str(isotope)+"/"+str(var_is), results[isotope]])
    #
    def load_and_assign_data(self, filename):
        dataset_exmpl = Data(filename=filename)
        df_exmpl = dataset_exmpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        return df_exmpl
    #
    def change_srm_std(self, var_srm, file):
        parts = file.split("/")
        self.container_files["STD"][parts[-1]]["SRM"].set(var_srm)
        self.fill_srm_values(var_srm=var_srm)
    #
    def change_srm_iso(self, var_srm, isotope):
        self.container_files["SRM"][isotope].set(var_srm)
        self.fill_srm_values(var_srm=var_srm)
    #
    def change_std_is(self, element, file):
        self.container_var["STD"][file]["IS"].set(element)
        parts = file.split("/")
        self.container_files["STD"][parts[-1]]["IS"].set(element)
    #
    def change_std_is_default(self, element, mineral=None):
        self.container_var["IS"]["Default STD"].set(element)
        for file in self.list_std:
            self.container_var["STD"][file]["IS"].set(element)
            parts = file.split("/")
            self.container_files["STD"][parts[-1]]["IS"].set(element)
        #
        if element in self.list_isotopes:
            key_is = re.search("(\D+)(\d+)", element)
            element_is = key_is.group(1)
        if mineral != None:
            if element in self.mineral_chem[mineral]:
                self.var_entr_09.set(self.mineral_chem[mineral][element])
            elif element_is in self.mineral_chem[mineral]:
                self.var_entr_09.set(self.mineral_chem[mineral][element_is])
            else:
                self.var_entr_09.set(0.0)
            # try:
            #     if element in self.mineral_chem[mineral]:
            #         self.var_entr_09.set(self.mineral_chem[mineral][element])
            #     else:
            #         self.var_entr_09.set(0.0)
            # except:
            #     if element_is in self.mineral_chem[mineral]:
            #         self.var_entr_09.set(self.mineral_chem[mineral][element_is])
            #     else:
            #         self.var_entr_09.set(0.0)
        #
        if self.container_var["IS"]["Default SMPL"].get() == "Select IS":
            self.change_smpl_is_default(element=element, mineral=mineral)
    #
    def change_smpl_is(self, element, file, mineral=None):
        self.container_var["SMPL"][file]["IS"].set(element)
        if mineral != None:
            parts = file.split("/")
            self.container_files["SMPL"][parts[-1]]["IS Concentration"].set(self.mineral_chem[mineral][element])
    #
    def change_smpl_is_default(self, element, mineral=None):
        self.container_var["IS"]["Default SMPL"].set(element)
        for file in self.list_smpl:
            self.container_var["SMPL"][file]["IS"].set(element)
        #
        if element in self.list_isotopes:
            key_is = re.search("(\D+)(\d+)", element)
            element_is = key_is.group(1)
        if mineral != None:
            if element in self.mineral_chem[mineral]:
                self.var_entr_09.set(self.mineral_chem[mineral][element])
                for file in self.list_smpl:
                    parts = file.split("/")
                    self.container_files["SMPL"][parts[-1]]["IS"].set(element)
                    self.container_files["SMPL"][parts[-1]]["IS Concentration"].set(self.mineral_chem[mineral][element])
            elif element_is in self.mineral_chem[mineral]:
                self.var_entr_09.set(self.mineral_chem[mineral][element_is])
                for file in self.list_smpl:
                    parts = file.split("/")
                    self.container_files["SMPL"][parts[-1]]["IS"].set(element)
                    self.container_files["SMPL"][parts[-1]]["IS Concentration"].set(
                        self.mineral_chem[mineral][element_is])
            # try:
            #     if element in self.mineral_chem[mineral]:
            #         self.var_entr_09.set(self.mineral_chem[mineral][element])
            #         for file in self.list_smpl:
            #             parts = file.split("/")
            #             self.container_files["SMPL"][parts[-1]]["IS"].set(element)
            #             self.container_files["SMPL"][parts[-1]]["IS Concentration"].set(self.mineral_chem[mineral][element])
            # except:
            #     if element_is in self.mineral_chem[mineral]:
            #         self.var_entr_09.set(self.mineral_chem[mineral][element_is])
            #         for file in self.list_smpl:
            #             parts = file.split("/")
            #             self.container_files["SMPL"][parts[-1]]["IS"].set(element)
            #             self.container_files["SMPL"][parts[-1]]["IS Concentration"].set(
            #                 self.mineral_chem[mineral][element_is])
        #
        if self.container_var["IS"]["Default STD"].get() == "Select IS":
            self.change_std_is_default(element=element, mineral=mineral)
    #
    def change_is_default(self, mineral, element, category="SMPL"):
        if element in self.list_isotopes:
            key_is = re.search("(\D+)(\d+)", element)
            element_is = key_is.group(1)
        if self.container_var["isotopes"]["default"].get() == "Select IS":
            self.container_var["isotopes"]["default"].set(element)
        else:
            if self.container_var["isotopes"]["default"].get() in list(self.mineral_chem[mineral.get()].keys()):
                self.container_var["isotopes"]["default"].set(element)
            else:
                self.container_var["isotopes"]["default"].set("Select IS")
        try:
            self.var_entr_09.set(self.mineral_chem[mineral.get()][element])
        except:
            self.var_entr_09.set(self.mineral_chem[mineral.get()][element_is])
        for file in self.list_smpl:
            parts = file.split("/")
            self.container_var["isotopes"][file].set(element)
            #self.container_files["SMPL"][parts[-1]].set(element)
            self.container_files["SMPL"][parts[-1]]["IS"].set(element)
        if category == "STD":
            try:
                self.container_var["IS"]["Default STD"].set(element)
            except:
                self.container_var["IS"]["Default STD"].set(element_is)
        elif category == "SMPL":
            try:
                self.container_var["IS"]["Default SMPL"].set(element)
            except:
                self.container_var["IS"]["Default SMPL"].set(element_is)
    #
    def find_suitable_isotopes(self, var_is):
        possible_is = []
        key_is = re.search("(\D+)(\d+)", var_is)
        element_is = key_is.group(1)
        for isotope in self.list_isotopes:
            key = re.search("(\D+)(\d+)", isotope)
            if element_is == key.group(1):
                possible_is.append(isotope)

    #
    def change_srm_default(self, var_srm, key="STD"):
        if key == "STD":
            for file in self.list_std:
                parts = file.split("/")
                self.container_files["STD"][parts[-1]]["SRM"].set(var_srm)
                try:
                    self.container_var["SRM"][file].set(var_srm)
                except:
                    print(file, self.container_var["SRM"][file])
            if self.container_var["SRM"]["default"][1].get() == "Select SRM":
                self.container_var["SRM"]["default"][1].set(var_srm)
                for isotope in self.list_isotopes:
                    self.container_files["SRM"][isotope].set(var_srm)
                    try:
                        self.container_var["SRM"][isotope].set(var_srm)
                    except:
                        print(isotope, self.container_var["SRM"][isotope])
        elif key == "isotope":
            for isotope in self.list_isotopes:
                self.container_files["SRM"][isotope].set(var_srm)
                try:
                    self.container_var["SRM"][isotope].set(var_srm)
                except:
                    print(isotope, self.container_var["SRM"][isotope])
            if self.container_var["SRM"]["default"][0].get() == "Select SRM":
                self.container_var["SRM"]["default"][0].set(var_srm)
                for file in self.list_std:
                    parts = file.split("/")
                    self.container_files["STD"][parts[-1]]["SRM"].set(var_srm)
                    try:
                        self.container_var["SRM"][file].set(var_srm)
                    except:
                        print(file, self.container_var["SRM"][file])
        #
        self.fill_srm_values(var_srm=var_srm)
    #
    def sub_mineralanalysis_exploration(self):
        #
        ## Cleaning
        categories = ["SRM", "plotting", "PSE", "ma_setting", "ma_datareduction"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Radiobutton"]) > 0:
                for item in self.container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Checkbox"]) > 0:
                for item in self.container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Listbox"]) > 0:
                for item in self.container_elements[category]["Listbox"]:
                    item.grid_remove()
        try:
            self.canvas.get_tk_widget().grid_forget()
            self.toolbarFrame.grid_forget()
        except AttributeError:
            pass
        try:
            self.canvas_drift.get_tk_widget().grid_forget()
            self.toolbarFrame_drift.grid_forget()
        except AttributeError:
            pass
        #
        self.container_lists["SRM"].clear()
        self.container_lists["IS"].clear()
        for key, value in self.container_files["SRM"].items():
            if value.get() not in self.container_lists["SRM"] and value.get() in self.list_srm:
                self.container_lists["SRM"].append(value.get())
                self.fill_srm_values(var_srm=value.get())
        #
        for key_01, value_01 in self.container_files["STD"].items():
            for key_02, value_02 in value_01.items():
                if key_02 not in ["Plot", "Time Signal Plot", "Histogram Plot", "Scatter Plot", "BG limits",
                                  "SIG limits", "BG", "SIG", "SPK", "Time Ratio Plot"]:
                    if value_02.get() not in self.container_lists["IS"] and value_02.get() in self.list_isotopes:
                        self.container_lists["IS"].append(value_02.get())
        for key_01, value_01 in self.container_files["SMPL"].items():
            for key_02, value_02 in value_01.items():
                if key_02 not in ["Plot", "Time Signal Plot", "Histogram Plot", "Scatter Plot", "BG limits",
                                  "SIG limits", "BG", "SIG", "SPK", "Time Ratio Plot"]:
                    if value_02.get() not in self.container_lists["IS"] and value_02.get() in self.list_isotopes:
                        self.container_lists["IS"].append(value_02.get())
        #
        ## LABELS
        lbl_01 = SE(
                parent=self.parent, row_id=0, column_id=21, n_rows=2, n_columns=20, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="General Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_02 = SE(
                parent=self.parent, row_id=2, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Select File", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_03 = SE(
                parent=self.parent, row_id=3, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Select SRM", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_04 = SE(
                parent=self.parent, row_id=4, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Select IS", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_05 = SE(
                parent=self.parent, row_id=5, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Display Options", relief=tk.GROOVE, fontsize="sans 10 bold")
        #
        self.gui_elements["ma_dataexploration"]["Label"]["General"].extend([lbl_01, lbl_02, lbl_03, lbl_04, lbl_05])
        self.container_elements["ma_dataexploration"]["Label"].extend([lbl_01, lbl_02, lbl_03, lbl_04, lbl_05])
        #
        self.container_var["ma_dataexploration"]["RB"] = tk.IntVar()
        self.container_var["ma_dataexploration"]["RB"].set(0)
        for index, isotope in enumerate(self.list_isotopes):
            ## LABELS
            lbl_iso = SE(
                parent=self.parent, row_id=6 + 1*index, column_id=21, n_rows=1, n_columns=4, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text=str(isotope), relief=tk.GROOVE, fontsize="sans 10 bold")
            ## FRAMES
            frm_iso = SE(
                parent=self.parent, row_id=6 + 1*index, column_id=25, n_rows=1, n_columns=4, fg=self.blue_light,
                bg=self.isotope_colors[isotope]).create_frame(relief=tk.GROOVE)
            ## CHECKBOXES
            self.container_var["ma_dataexploration"][isotope] = tk.IntVar()
            rb_iso = SE(
                parent=self.parent, row_id=6 + 1*index, column_id=25, n_rows=1, n_columns=4, fg=self.blue_light,
                bg=self.isotope_colors[isotope]).create_radiobutton(
                var_rb=self.container_var["ma_dataexploration"]["RB"], value_rb=index, color_bg=self.isotope_colors[isotope],
                fg=self.blue_light, text="", sticky="", relief=tk.GROOVE)
            # cb_iso = SE(
            #     parent=self.parent, row_id=10 + 2*index, column_id=31, fg=self.blue_light, n_rows=2, n_columns=5,
            #     bg=self.isotope_colors[isotope]).create_simple_checkbox(
            #     var_cb=self.container_var["ma_dataexploration"][isotope], text="", set_sticky="", own_color=True)
            #
            self.gui_elements["ma_dataexploration"]["Label"]["General"].append(lbl_iso)
            self.gui_elements["ma_dataexploration"]["Frame"]["General"].append(frm_iso)
            #self.gui_elements["ma_dataexploration"]["Checkbox"]["General"].append(cb_iso)
            self.container_elements["ma_dataexploration"]["Label"].append(lbl_iso)
            self.container_elements["ma_dataexploration"]["Frame"].append(frm_iso)
            #self.container_elements["ma_dataexploration"]["Checkbox"].append(cb_iso)

        #
        ## OPTION MENUS
        self.container_var["ma_dataexploration"]["Option File"] = tk.StringVar()
        list_files = self.container_lists["STD"]["Short"] + self.container_lists["SMPL"]["Short"]
        self.container_var["ma_dataexploration"]["Option SRM"] = tk.StringVar()
        self.container_var["ma_dataexploration"]["Option IS"] = tk.StringVar()
        opt_menu_file = SE(
            parent=self.parent, row_id=2, column_id=29, n_rows=1, n_columns=12, fg=self.green_dark,
            bg=self.green_medium).create_option_isotope(
            var_iso=self.container_var["ma_dataexploration"]["Option File"], option_list=list_files,
            text_set="Select File", fg_active=self.green_dark, bg_active=self.red_dark,
            command=lambda filename=self.container_var["ma_dataexploration"]["Option File"].get():
            self.show_diagrams(filename))
        opt_menu_srm = SE(
            parent=self.parent, row_id=3, column_id=29, n_rows=1, n_columns=12, fg=self.green_dark,
            bg=self.green_medium).create_option_srm(
            var_srm=self.container_var["ma_dataexploration"]["Option SRM"], text_set=self.container_lists["SRM"][0],
            fg_active=self.green_dark, bg_active=self.red_dark, option_list=self.container_lists["SRM"])
        opt_menu_is = SE(
            parent=self.parent, row_id=4, column_id=29, n_rows=1, n_columns=12, fg=self.green_dark,
            bg=self.green_medium).create_option_isotope(
            var_iso=self.container_var["ma_dataexploration"]["Option IS"], option_list=self.container_lists["IS"],
            text_set=self.container_lists["IS"][0], fg_active=self.green_dark, bg_active=self.red_dark)
        #
        self.gui_elements["ma_dataexploration"]["Option Menu"]["General"].extend(
            [opt_menu_file, opt_menu_srm, opt_menu_is])
        self.container_elements["ma_dataexploration"]["Option Menu"].extend(
            [opt_menu_file, opt_menu_srm, opt_menu_is])
    #
    def check_functionality(self, functions):
        for key, value in functions.items():
            print(key)
            try:
                for key2, value2 in value.items():
                    print(key2, value2.get())
            except:
                print(key, value)
        for key, value in self.container_settings.items():
            print(key)
            try:
                for key2, value2 in value.items():
                    print(key2, value2.get())
            except:
                print(key, value)
    #
    def place_srm_values(self, var_srm, header_col, default=False):
        #
        lbl_srm_03 = SE(parent=self.parent, row_id=0, column_id=header_col, n_rows=1, n_columns=42, fg=self.green_light,
                            bg=self.green_dark).create_simple_label(text=str(var_srm)+" - Element Concentrations (ppm)",
                                                                    relief=tk.GROOVE, fontsize="sans 10 bold")
        self.container_elements["SRM"]["Label"].append(lbl_srm_03)
        #
        if default == True:
            for file in self.list_std:
                parts = file.split("/")
                self.container_var["SRM"][file].set(var_srm)
                self.container_files["STD"][parts[-1]]["SRM"].set(var_srm)
        #
        try:
            ESRM().place_srm_values(srm_name=var_srm, srm_dict=self.srm_actual)
        except:
            self.srm_actual[var_srm] = {}
            ESRM().place_srm_values(srm_name=var_srm, srm_dict=self.srm_actual)
        #
        for element in self.list_pse:
            if element in self.srm_actual[var_srm]:
                self.container_var["SRM"][element].set(self.srm_actual[var_srm][element])
            else:
                self.container_var["SRM"][element].set(0.0)
    #
    def fill_srm_values(self, var_srm):
        if var_srm not in self.srm_actual:
            self.srm_actual[var_srm] = {}
            ESRM().place_srm_values(srm_name=var_srm, srm_dict=self.srm_actual)
    #
    def calculate_mineral_chemistry(self):
        #
        M_H = 1.008
        M_C = 12.011
        M_O = 15.999
        M_F = 18.998
        M_Na = 22.990
        M_Mg = 24.305
        M_Al = 26.982
        M_Si = 28.085
        M_P = 30.974
        M_S = 32.059
        M_Cl = 35.450
        M_K = 39.098
        M_Ca = 40.078
        M_Ti = 47.867
        M_Cr = 51.996
        M_Mn = 54.938
        M_Fe = 55.845
        M_Cu = 63.546
        M_Zn = 65.382
        M_As = 74.922
        M_Sr = 87.620
        M_Zr = 91.224
        M_Mo = 95.950
        M_La = 138.91
        M_Ce = 140.12
        M_Pr = 140.91
        M_Nd = 144.24
        M_Sm = 150.360
        M_Eu = 151.960
        M_Gd = 157.25
        M_Pb = 207.200
        M_Th = 232.04
        #
        #self.mineral_chem = {}
        for mineral in self.mineral_list:
            self.mineral_chem[mineral] = {}
            if mineral == "Quartz":  # SiO2
                M_Qz = M_Si + 2 * M_O
                w_Si = (M_Si) / (M_Qz) * 1000000
                self.mineral_chem[mineral]["Si"] = w_Si
            elif mineral == "Arsenopyrite":  # FeAsS
                M_Apy = M_Fe + M_As + M_S
                w_S = (M_S)/(M_Apy)*1000000
                w_Fe = (M_Fe)/(M_Apy)*1000000
                w_As = (M_As)/(M_Apy)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Fe"] = w_Fe
                self.mineral_chem[mineral]["As"] = w_As
            elif mineral == "Bornite":  # Cu5FeS4
                M_Bn = 5*M_Cu + M_Fe + 4*M_S
                w_S = (4*M_S)/(M_Bn)*1000000
                w_Fe = (M_Fe)/(M_Bn)*1000000
                w_Cu = (5*M_Cu)/(M_Bn)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Fe"] = w_Fe
                self.mineral_chem[mineral]["Cu"] = w_Cu
            elif mineral == "Calcite":  # CaCO3
                M_Cal = M_Ca + M_C + 3 * M_O
                w_C = (M_C) / (M_Cal) * 1000000
                w_Ca = (M_Ca) / (M_Cal) * 1000000
                self.mineral_chem[mineral]["C"] = w_C
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Chalcopyrite":  # CuFeS2
                M_Ccp = M_Cu + M_Fe + 2*M_S
                w_S = (2*M_S)/(M_Ccp)*1000000
                w_Fe = (M_Fe)/(M_Ccp)*1000000
                w_Cu = (M_Cu)/(M_Ccp)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Fe"] = w_Fe
                self.mineral_chem[mineral]["Cu"] = w_Cu
            elif mineral == "Chromite":  # FeCr2O4
                M = M_Fe + 2*M_Cr + 4*M_O
                w_O = (4*M_O)/(M)*1000000
                w_Cr = (2*M_Cr)/(M)*1000000
                w_Fe = (M_Fe)/(M)*1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Cr"] = w_Cr
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Enargite":  # Cu3AsS4
                M_En = 3*M_Cu + M_As + 4*M_S
                w_S = (4*M_S)/(M_En)*1000000
                w_Cu = (3*M_Cu)/(M_En)*1000000
                w_As = (M_As)/(M_En)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Cu"] = w_Cu
                self.mineral_chem[mineral]["As"] = w_As
            elif mineral == "Fluorite":  # CaF2
                M_Fl = M_Ca + 2 * M_F
                w_F = (2 * M_F) / (M_Fl) * 1000000
                w_Ca = (M_Ca) / (M_Fl) * 1000000
                self.mineral_chem[mineral]["F"] = w_F
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Apatite-Cl":  # Ca5(PO4)3Cl
                M_Ap = 5 * M_Ca + 3 * (M_P + 4 * M_O) + M_Cl
                w_P = (3 * M_P) / (M_Ap) * 1000000
                w_Cl = (M_Cl) / (M_Ap) * 1000000
                w_Ca = (5 * M_Ca) / (M_Ap) * 1000000
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Cl"] = w_Cl
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Apatite-F":  # Ca5(PO4)3F
                M_Ap = 5 * M_Ca + 3 * (M_P + 4 * M_O) + M_F
                w_F = (M_F) / (M_Ap) * 1000000
                w_P = (3 * M_P) / (M_Ap) * 1000000
                w_Ca = (5 * M_Ca) / (M_Ap) * 1000000
                self.mineral_chem[mineral]["F"] = w_F
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Apatite-OH":  # Ca5(PO4)3OH
                M_Ap = 5 * M_Ca + 3 * (M_P + 4 * M_O) + (M_O + M_H)
                w_H = (M_H) / (M_Ap) * 1000000
                w_P = (3 * M_P) / (M_Ap) * 1000000
                w_Ca = (5 * M_Ca) / (M_Ap) * 1000000
                self.mineral_chem[mineral]["H"] = w_H
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Forsterite":  # Mg2SiO4
                M_Ol = 2 * M_Mg + M_Si + 4 * M_O
                w_Mg = (2 * M_Mg) / (M_Ol) * 1000000
                w_Si = (M_Si) / (M_Ol) * 1000000
                self.mineral_chem[mineral]["Mg"] = w_Mg
                self.mineral_chem[mineral]["Si"] = w_Si
            elif mineral == "Fayalite":  # Fe2SiO4
                M_Ol = 2 * M_Fe + M_Si + 4 * M_O
                w_Si = (M_Si) / (M_Ol) * 1000000
                w_Fe = (2 * M_Fe) / (M_Ol) * 1000000
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Gahnite":  # ZnAl2O4
                M = M_Zn + 2*M_Al + 4*M_O
                w_O = (4*M_O)/(M)*1000000
                w_Al = (2*M_Al)/(M)*1000000
                w_Zn = (M_Zn)/(M)*1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Al"] = w_Al
                self.mineral_chem[mineral]["Zn"] = w_Zn
            elif mineral == "Galena":  # PbS
                M_Gn = M_Pb + M_S
                w_S = (M_S)/(M_Gn)*1000000
                w_Pb = (M_Pb)/(M_Gn)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Pb"] = w_Pb
            elif mineral == "Hematite":  # Fe2O3
                M = 2*M_Fe + 3*M_O
                w_O = (3*M_O)/(M)*1000000
                w_Fe = (2*M_Fe)/(M)*1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Tephroite":  # Mn2SiO4
                M_Ol = 2 * M_Mn + M_Si + 4 * M_O
                w_Si = (M_Si) / (M_Ol) * 1000000
                w_Mn = (2 * M_Mn) / (M_Ol) * 1000000
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Mn"] = w_Mn
            elif mineral == "Albite":  # NaAlSi3O8
                M_Ab = M_Na + M_Al + 3 * M_Si + 8 * M_O
                w_Na = (M_Na) / (M_Ab) * 1000000
                w_Al = (M_Al) / (M_Ab) * 1000000
                w_Si = (3 * M_Si) / (M_Ab) * 1000000
                self.mineral_chem[mineral]["Na"] = w_Na
                self.mineral_chem[mineral]["Al"] = w_Al
                self.mineral_chem[mineral]["Si"] = w_Si
            elif mineral == "Anorthite":  # CaAl2Si2O8
                M_An = M_Ca + 2 * (M_Al + M_Si) + 8 * M_O
                w_Al = (2 * M_Al) / (M_An) * 1000000
                w_Si = (2 * M_Si) / (M_An) * 1000000
                w_Ca = (M_Ca) / (M_An) * 1000000
                self.mineral_chem[mineral]["Al"] = w_Al
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Magnetite":  # Fe3O4
                M = 3*M_Fe + 4*M_O
                w_O = (4*M_O)/(M)*1000000
                w_Fe = (3*M_Fe)/(M)*1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Molybdenite":  # MoS2
                M = M_Mo + 2*M_S
                w_S = (2*M_S)/(M)*1000000
                w_Mo = (M_Mo)/(M)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Mo"] = w_Mo
            elif mineral == "Pyrite":  # FeS2
                M_Py = M_Fe + 2*M_S
                w_S = (2*M_S)/(M_Py)*1000000
                w_Fe = (M_Fe)/(M_Py)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral in ["Orthoclase", "Microcline"]:  # KAlSi3O8
                M_OrMc = M_K + M_Al + 3 * M_Si + 8 * M_O
                w_Al = (M_Al) / (M_OrMc) * 1000000
                w_Si = (3 * M_Si) / (M_OrMc) * 1000000
                w_K = (M_K) / (M_OrMc) * 1000000
                self.mineral_chem[mineral]["Al"] = w_Al
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["K"] = w_K
            elif mineral == "Sphalerite":  # ZnS
                M_Sp = M_Zn + M_S
                w_S = (M_S)/(M_Sp)*1000000
                w_Zn = (M_Zn)/(M_Sp)*1000000
                self.mineral_chem[mineral]["S"] = w_S
                self.mineral_chem[mineral]["Zn"] = w_Zn
            elif mineral == "Zircon":  # ZrSiO4
                M_Zrn = M_Zr + (M_Si + 4*M_O)
                w_Si = (M_Si)/(M_Zrn)*1000000
                w_Zr = (M_Zr)/(M_Zrn)*1000000
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Zr"] = w_Zr
            elif mineral == "Meionite":  # Ca4 Al6 Si6 O24 CO3
                M = 4*M_Ca + 6*M_Al + 6*M_Si + 24*M_O + M_C + 3*M_O
                w_C = (M_C)/(M) * 1000000
                w_Al = (6*M_Al)/(M) * 1000000
                w_Si = (6*M_Si) / (M) * 1000000
                w_Ca = (4*M_Ca) / (M) * 1000000
                self.mineral_chem[mineral]["C"] = w_C
                self.mineral_chem[mineral]["Al"] = w_Al
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Marialite":  # Na4 Al3 Si9 O24 Cl
                M = 4*M_Na + 3*M_Al + 9*M_Si + 24*M_O + M_Cl
                w_Na = (4*M_Na)/(M) * 1000000
                w_Al = (3*M_Al)/(M) * 1000000
                w_Si = (9*M_Si) / (M) * 1000000
                w_Cl = (M_Cl) / (M) * 1000000
                self.mineral_chem[mineral]["Na"] = w_Na
                self.mineral_chem[mineral]["Al"] = w_Al
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Cl"] = w_Cl
            elif mineral == "Strontianite":  # Sr C O3
                M = M_Sr + M_C + 3*M_O
                w_C = (M_C)/(M) * 1000000
                w_O = (3*M_O)/(M) * 1000000
                w_Sr = (M_Sr)/(M) * 1000000
                self.mineral_chem[mineral]["C"] = w_C
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Sr"] = w_Sr
            elif mineral == "Titanite":  # Ca Ti Si O5
                M = M_Ca + M_Ti + M_Si + 5*M_O
                w_O = (5*M_O)/(M) * 1000000
                w_Si = (M_Si)/(M) * 1000000
                w_Ca = (M_Ca)/(M) * 1000000
                w_Ti = (M_Ti)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Ca"] = w_Ca
                self.mineral_chem[mineral]["Ti"] = w_Ti
            elif mineral == "Aegirine":  # Na Fe Si2 O6
                M = M_Na + M_Fe + 2*M_Si + 6*M_O
                w_O = (6*M_O)/(M) * 1000000
                w_Na = (M_Na)/(M) * 1000000
                w_Si = (2*M_Si)/(M) * 1000000
                w_Fe = (M_Fe)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Na"] = w_Na
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Diopside":  # Mg Ca Si2 O6
                M = M_Mg + M_Ca + 2*M_Si + 6*M_O
                w_O = (6*M_O)/(M) * 1000000
                w_Mg = (M_Mg)/(M) * 1000000
                w_Si = (2*M_Si)/(M) * 1000000
                w_Ca = (M_Ca)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Mg"] = w_Mg
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Ca"] = w_Ca
            elif mineral == "Hedenbergite":  # Fe Ca Si2 O6
                M = M_Fe + M_Ca + 2*M_Si + 6*M_O
                w_O = (6*M_O)/(M) * 1000000
                w_Si = (2*M_Si)/(M) * 1000000
                w_Ca = (M_Ca)/(M) * 1000000
                w_Fe = (M_Fe)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Ca"] = w_Ca
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Ferrosilite":  # Fe2 Si2 O6
                M = 2*M_Fe + 2*M_Si + 6*M_O
                w_O = (6*M_O)/(M) * 1000000
                w_Si = (2*M_Si)/(M) * 1000000
                w_Fe = (2*M_Fe)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Si"] = w_Si
                self.mineral_chem[mineral]["Fe"] = w_Fe
            elif mineral == "Enstatite":  # Mg2 Si2 O6
                M = 2*M_Mg + 2*M_Si + 6*M_O
                w_O = (6*M_O)/(M) * 1000000
                w_Mg = (2*M_Mg)/(M) * 1000000
                w_Si = (2*M_Si)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["Mg"] = w_Mg
                self.mineral_chem[mineral]["Si"] = w_Si
            elif mineral == "Monazite-La":  # La P O4
                M = M_La + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_La = (M_La)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["La"] = w_La
            elif mineral == "Monazite-Ce":  # Ce P O4
                M = M_Ce + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Ce = (M_Ce)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Ce"] = w_Ce
            elif mineral == "Monazite-Pr":  # Pr P O4
                M = M_Pr + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Pr = (M_Pr)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Pr"] = w_Pr
            elif mineral == "Monazite-Nd":  # Nd P O4
                M = M_Nd + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Nd = (M_Nd)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Nd"] = w_Nd
            elif mineral == "Monazite-Sm":  # Sm P O4
                M = M_Sm + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Sm = (M_Sm)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Sm"] = w_Sm
            elif mineral == "Monazite-Eu":  # Eu P O4
                M = M_Eu + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Eu = (M_Eu)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Eu"] = w_Eu
            elif mineral == "Monazite-Gd":  # Gd P O4
                M = M_Gd + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Gd = (M_Gd)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Gd"] = w_Gd
            elif mineral == "Monazite-Th":  # Th P O4
                M = M_Th + M_P + 4*M_O
                w_O = (4*M_O)/(M) * 1000000
                w_P = (M_P)/(M) * 1000000
                w_Th = (M_Th)/(M) * 1000000
                self.mineral_chem[mineral]["O"] = w_O
                self.mineral_chem[mineral]["P"] = w_P
                self.mineral_chem[mineral]["Th"] = w_Th
    #
    def place_mineral_values(self, var_min, header_col):
        #
        lbl_srm_03 = SE(parent=self.parent, row_id=0, column_id=header_col, n_rows=1, n_columns=42, fg=self.green_light,
                        bg=self.green_dark).create_simple_label(text=str(var_min)+" - Element Concentrations (ppm)",
                                                                relief=tk.GROOVE, fontsize="sans 10 bold")
        self.container_elements["SRM"]["Label"].append(lbl_srm_03)
        #
        self.srm_actual[var_min] = {}
        M_H = 1.008
        M_C = 12.011
        M_O = 15.999
        M_F = 18.998
        M_Na = 22.990
        M_Mg = 24.305
        M_Al = 26.982
        M_Si = 28.085
        M_P = 30.974
        M_Cl = 35.450
        M_K = 39.098
        M_Ca = 40.078
        M_Mn = 54.938
        M_Fe = 55.845
        M_Zr = 91.224
        #
        if var_min == "Quartz": # SiO2
            M_Qz = M_Si + 2*M_O
            w_Si = (M_Si)/(M_Qz) * 1000000
            self.srm_actual[var_min]["Si"] = w_Si
        elif var_min == "Arsenopyrite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
            self.srm_actual[var_min]["As"] = self.mineral_chem[var_min]["As"]
        elif var_min == "Bornite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
            self.srm_actual[var_min]["Cu"] = self.mineral_chem[var_min]["Cu"]
        elif var_min == "Calcite":  # CaCO3
            M_Cal = M_Ca + M_C + 3*M_O
            w_C = (M_C)/(M_Cal) * 1000000
            w_Ca = (M_Ca)/(M_Cal) * 1000000
            self.srm_actual[var_min]["C"] = w_C
            self.srm_actual[var_min]["Ca"] = w_Ca
        elif var_min == "Chalcopyrite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
            self.srm_actual[var_min]["Cu"] = self.mineral_chem[var_min]["Cu"]
        elif var_min == "Chromite":
            self.srm_actual[var_min]["Cr"] = self.mineral_chem[var_min]["Cr"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Sphalerite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Zn"] = self.mineral_chem[var_min]["Zn"]
        elif var_min == "Enargite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Cu"] = self.mineral_chem[var_min]["Cu"]
            self.srm_actual[var_min]["As"] = self.mineral_chem[var_min]["As"]
        elif var_min == "Fluorite": # CaF2
            M_Fl = M_Ca + 2*M_F
            w_F = (2*M_F)/(M_Fl) * 1000000
            w_Ca = (M_Ca)/(M_Fl) * 1000000
            self.srm_actual[var_min]["F"] = w_F
            self.srm_actual[var_min]["Ca"] = w_Ca
        elif var_min == "Hematite":
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Galena":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Pb"] = self.mineral_chem[var_min]["Pb"]
        elif var_min == "Gahnite":
            self.srm_actual[var_min]["Al"] = self.mineral_chem[var_min]["Al"]
            self.srm_actual[var_min]["Zn"] = self.mineral_chem[var_min]["Zn"]
        elif var_min == "Magnetite":
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Molybdenite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Mo"] = self.mineral_chem[var_min]["Mo"]
        elif var_min == "Pyrite":
            self.srm_actual[var_min]["S"] = self.mineral_chem[var_min]["S"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Apatite-Cl": # Ca5(PO4)3Cl
            M_Ap = 5*M_Ca + 3*(M_P + 4*M_O) + M_Cl
            w_P = (3*M_P)/(M_Ap) * 1000000
            w_Cl = (M_Cl)/(M_Ap) * 1000000
            w_Ca = (5*M_Ca)/(M_Ap) * 1000000
            self.srm_actual[var_min]["P"] = w_P
            self.srm_actual[var_min]["Cl"] = w_Cl
            self.srm_actual[var_min]["Ca"] = w_Ca
        elif var_min == "Apatite-F": # Ca5(PO4)3F
            M_Ap = 5*M_Ca + 3*(M_P + 4*M_O) + M_F
            w_F = (M_F)/(M_Ap) * 1000000
            w_P = (3*M_P)/(M_Ap) * 1000000
            w_Ca = (5*M_Ca)/(M_Ap) * 1000000
            self.srm_actual[var_min]["F"] = w_F
            self.srm_actual[var_min]["P"] = w_P
            self.srm_actual[var_min]["Ca"] = w_Ca
        elif var_min == "Apatite-OH": # Ca5(PO4)3OH
            M_Ap = 5*M_Ca + 3*(M_P + 4*M_O) + (M_O + M_H)
            w_H = (M_H)/(M_Ap) * 1000000
            w_P = (3*M_P)/(M_Ap) * 1000000
            w_Ca = (5*M_Ca)/(M_Ap) * 1000000
            self.srm_actual[var_min]["H"] = w_H
            self.srm_actual[var_min]["P"] = w_P
            self.srm_actual[var_min]["Ca"] = w_Ca
        elif var_min == "Forsterite": # Mg2SiO4
            M_Ol = 2*M_Mg + M_Si + 4*M_O
            w_Mg = (2*M_Mg)/(M_Ol) * 1000000
            w_Si = (M_Si)/(M_Ol) * 1000000
            self.srm_actual[var_min]["Mg"] = w_Mg
            self.srm_actual[var_min]["Si"] = w_Si
        elif var_min == "Fayalite": # Fe2SiO4
            M_Ol = 2*M_Fe + M_Si + 4*M_O
            w_Si = (M_Si)/(M_Ol) * 1000000
            w_Fe = (2*M_Fe)/(M_Ol) * 1000000
            self.srm_actual[var_min]["Si"] = w_Si
            self.srm_actual[var_min]["Fe"] = w_Fe
        elif var_min == "Tephroite": # Mn2SiO4
            M_Ol = 2*M_Mn + M_Si + 4*M_O
            w_Si = (M_Si)/(M_Ol) * 1000000
            w_Mn = (2*M_Mn)/(M_Ol) * 1000000
            self.srm_actual[var_min]["Si"] = w_Si
            self.srm_actual[var_min]["Mn"] = w_Mn
        elif var_min == "Albite": # NaAlSi3O8
            M_Ab = M_Na + M_Al + 3*M_Si + 8*M_O
            w_Na = (M_Na)/(M_Ab) * 1000000
            w_Al = (M_Al)/(M_Ab) * 1000000
            w_Si = (3*M_Si)/(M_Ab) * 1000000
            self.srm_actual[var_min]["Na"] = w_Na
            self.srm_actual[var_min]["Al"] = w_Al
            self.srm_actual[var_min]["Si"] = w_Si
        elif var_min == "Anorthite": # CaAl2Si2O8
            M_An = M_Ca + 2*(M_Al + M_Si) + 8*M_O
            w_Al = (2*M_Al)/(M_An) * 1000000
            w_Si = (2*M_Si)/(M_An) * 1000000
            w_Ca = (M_Ca)/(M_An) * 1000000
            self.srm_actual[var_min]["Al"] = w_Al
            self.srm_actual[var_min]["Si"] = w_Si
            self.srm_actual[var_min]["Ca"] = w_Ca
        elif var_min in ["Orthoclase", "Microcline"]: # KAlSi3O8
            M_OrMc = M_K + M_Al + 3*M_Si + 8*M_O
            w_Al = (M_Al)/(M_OrMc) * 1000000
            w_Si = (3*M_Si)/(M_OrMc) * 1000000
            w_K = (M_K)/(M_OrMc) * 1000000
            self.srm_actual[var_min]["Al"] = w_Al
            self.srm_actual[var_min]["Si"] = w_Si
            self.srm_actual[var_min]["K"] = w_K
        elif var_min == "Zircon": # ZrSiO4
            M_Zrn = M_Zr + (M_Si + 4*M_O)
            w_Si = (M_Si)/(M_Zrn)*1000000
            w_Zr = (M_Zr)/(M_Zrn)*1000000
            self.srm_actual[var_min]["Si"] = w_Si
            self.srm_actual[var_min]["Zr"] = w_Zr
        elif var_min == "Meionite":
            self.srm_actual[var_min]["C"] = self.mineral_chem[var_min]["C"]
            self.srm_actual[var_min]["Al"] = self.mineral_chem[var_min]["Al"]
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Ca"] = self.mineral_chem[var_min]["Ca"]
        elif var_min == "Marialite":
            self.srm_actual[var_min]["Na"] = self.mineral_chem[var_min]["Na"]
            self.srm_actual[var_min]["Al"] = self.mineral_chem[var_min]["Al"]
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Cl"] = self.mineral_chem[var_min]["Cl"]
        elif var_min == "Strontianite":
            self.srm_actual[var_min]["C"] = self.mineral_chem[var_min]["C"]
            self.srm_actual[var_min]["Sr"] = self.mineral_chem[var_min]["Sr"]
        elif var_min == "Titanite":
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Ca"] = self.mineral_chem[var_min]["Ca"]
            self.srm_actual[var_min]["Ti"] = self.mineral_chem[var_min]["Ti"]
        elif var_min == "Aegirine":
            self.srm_actual[var_min]["Na"] = self.mineral_chem[var_min]["Na"]
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Diopside":
            self.srm_actual[var_min]["Mg"] = self.mineral_chem[var_min]["Mg"]
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Ca"] = self.mineral_chem[var_min]["Ca"]
        elif var_min == "Hedenbergite":
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Ca"] = self.mineral_chem[var_min]["Ca"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Ferrosilite":
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
            self.srm_actual[var_min]["Fe"] = self.mineral_chem[var_min]["Fe"]
        elif var_min == "Enstatite":
            self.srm_actual[var_min]["Mg"] = self.mineral_chem[var_min]["Mg"]
            self.srm_actual[var_min]["Si"] = self.mineral_chem[var_min]["Si"]
        elif var_min == "Monazite-La":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["La"] = self.mineral_chem[var_min]["La"]
        elif var_min == "Monazite-Ce":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Ce"] = self.mineral_chem[var_min]["Ce"]
        elif var_min == "Monazite-Pr":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Pr"] = self.mineral_chem[var_min]["Pr"]
        elif var_min == "Monazite-Nd":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Nd"] = self.mineral_chem[var_min]["Nd"]
        elif var_min == "Monazite-Sm":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Sm"] = self.mineral_chem[var_min]["Sm"]
        elif var_min == "Monazite-Eu":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Eu"] = self.mineral_chem[var_min]["Eu"]
        elif var_min == "Monazite-Gd":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Gd"] = self.mineral_chem[var_min]["Gd"]
        elif var_min == "Monazite-Th":
            self.srm_actual[var_min]["P"] = self.mineral_chem[var_min]["P"]
            self.srm_actual[var_min]["Th"] = self.mineral_chem[var_min]["Th"]
        #
        for element in self.list_pse:
            if element in self.srm_actual[var_min]:
                self.container_var["SRM"][element].set(self.srm_actual[var_min][element])
            else:
                self.container_var["SRM"][element].set(0.0)
    #
    def select_mineral_is(self, var_min, fluidinclusion=False):
        if fluidinclusion == False:
            self.container_var["isotopes"]["default"].set("Select IS")
            self.var_entr_09.set(0.0)
        if len(self.container_var["mineralchemistry"]) > 0:
            self.container_var["mineralchemistry"].clear()
        self.container_var["mineralchemistry"].extend(list(self.mineral_chem[var_min].keys()))
        self.container_var["mineralchemistry"].sort()
        #
        possible_is = []
        for element in self.container_var["mineralchemistry"]:
            for isotope in self.list_isotopes:
                key = re.search("(\D+)(\d+)", isotope)
                if element == key.group(1):
                    possible_is.append(isotope)
        if fluidinclusion == True:
            list_fluidchemistry = ["H", "Na", "Mg", "Ca", "K", "Cl", "F", "Br", "I", "At"]
            for element in list_fluidchemistry:
                for isotope in self.list_isotopes:
                    key = re.search("(\D+)(\d+)", isotope)
                    if element == key.group(1):
                        possible_is.append(isotope)
        #
        if fluidinclusion == False:
            self.opt_is_std_def["menu"].delete(0, "end")
            self.opt_is_smpl_def["menu"].delete(0, "end")
            #
            for index, isotope in enumerate(possible_is):
                for file in self.list_std:
                    if index == 0:
                        self.container_optionmenu["STD"][file]["menu"].delete(0, "end")
                    self.container_optionmenu["STD"][file]["menu"].add_command(
                        label=isotope, command=lambda element=isotope, file=file: self.change_std_is(element, file))
                    if self.file_loaded is False:
                        self.container_var["STD"][file]["IS"].set("Select IS")
                for file in self.list_smpl:
                    if index == 0:
                        self.container_optionmenu["SMPL"][file]["menu"].delete(0, "end")
                    self.container_optionmenu["SMPL"][file]["menu"].add_command(
                        label=isotope, command=lambda element=isotope, file=file,
                                                      mineral=self.container_var["mineral"].get():
                        self.change_smpl_is(element, file, mineral))
                    if self.file_loaded is False:
                        self.container_var["SMPL"][file]["IS"].set("Select IS")
                #
                self.opt_is_std_def["menu"].add_command(
                    label=isotope, command=lambda element=isotope, mineral=var_min:
                    self.change_std_is_default(element, mineral))
                self.opt_is_smpl_def["menu"].add_command(
                    label=isotope, command=lambda element=isotope, mineral=var_min:
                    self.change_smpl_is_default(element, mineral))
    #
    def print_something(self, var):
        if isinstance(var, list):
            for item in var:
                print(item)
    #
    def find_nearest_time(self, var_t, times, category_01, category_02, event):
        try:
            time = var_t.get()
            time = time.replace(',', '.')

            x_nearest_start = round(min(times, key=lambda x: abs(x-float(time))), 8)
            var_t.set(x_nearest_start)
            self.container_settings[category_01][category_02].set(x_nearest_start)
        except:
            pass
    #
    def set_entry_value(self, var, category_01, category_02, event):
        var.set(var.get())
        self.container_settings[category_01][category_02].set(var.get())
    #
    def onclick(self, var, filename, ratio_mode, event, spikes=False):
        if spikes == False:
            if var.get() in [1, 2, 3, 4, 5]:
                if len(self.container_helper["positions"][filename]) == 2 and len(
                        self.container_helper["indices"][filename]) == 2:
                    self.container_helper["positions"][filename].clear()
                    self.container_helper["indices"][filename].clear()
                #
                x_nearest = min(self.times, key=lambda x: abs(x - event.xdata))
                self.container_helper["positions"][filename].append(x_nearest)
                self.container_helper["indices"][filename].append(self.times[self.times == x_nearest].index[0])
                #
                if len(self.container_helper["positions"][filename])+len(
                        self.container_helper["indices"][filename]) == 4:
                    if var.get() == 1:  # BG
                        if self.file_type == "STD":
                            if len(self.container_helper["positions"]["BG STD"][filename]) > 0:
                                self.bg_id = self.container_helper["positions"]["BG STD"][filename][-1][4]
                        elif self.file_type == "SMPL":
                            if len(self.container_helper["positions"]["BG SMPL"][filename]) > 0:
                                self.bg_id = self.container_helper["positions"]["BG SMPL"][filename][-1][4]
                        #
                        self.bg_id += 1
                        self.bg_idlist.append(self.bg_id)
                        self.container_helper["limits BG"][self.file]["ID"].append(self.bg_id)
                        self.container_helper["limits BG"][self.file]["type"].append("custom")
                        self.container_helper["positions"]["BG"][filename].append(
                            [round(self.container_helper["positions"][filename][0], 4),
                             round(self.container_helper["positions"][filename][1], 4)])
                        self.container_listboxes[self.file_type][filename]["BG"][0].insert(
                            tk.END, "BG" + str(self.bg_id) + " [" + str(
                                self.container_helper["positions"][filename][0]) + "-" +
                                    str(self.container_helper["positions"][filename][1]) + "]")
                        #
                        if ratio_mode == False:
                            box_bg = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.blue_dark)
                            box_bg_ratio = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.blue_dark)
                            #
                            self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                            self.container_helper["limits BG Ratio"][self.file][str(self.bg_id)] = box_bg_ratio
                            #
                            self.canvas.draw()
                            try:
                                self.canvas_ratio.draw()
                            except:
                                pass
                        else:
                            box_bg_ratio = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.blue_dark)
                            box_bg = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.blue_dark)
                            #
                            self.container_helper["limits BG Ratio"][self.file][str(self.bg_id)] = box_bg_ratio
                            self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                            #
                            self.canvas_ratio.draw()
                            self.canvas.draw()
                        #
                        self.indices_bg = self.container_helper["indices"][filename]
                        #
                        self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id] = {}
                        self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id]["Times"] = [
                            self.container_helper["positions"][filename][0],
                            self.container_helper["positions"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id]["Positions"] = [
                            self.container_helper["indices"][filename][0],
                            self.container_helper["indices"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id]["Box"] = box_bg
                        #
                        if self.file_type == "STD":
                            self.container_helper["STD"][filename]["BG"][self.bg_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": [box_bg, box_bg_ratio]}
                            self.container_helper["positions"]["BG STD"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.bg_id])
                        elif self.file_type == "SMPL":
                            self.container_helper["SMPL"][filename]["BG"][self.bg_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": [box_bg, box_bg_ratio]}
                            self.container_helper["positions"]["BG SMPL"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.bg_id])
                    elif var.get() == 2:    # SIG
                        if self.file_type == "STD":
                            if len(self.container_helper["positions"]["SIG STD"][filename]) > 0:
                                self.sig_id = self.container_helper["positions"]["SIG STD"][filename][-1][4]
                        elif self.file_type == "SMPL":
                            if len(self.container_helper["positions"]["SIG SMPL"][filename]) > 0:
                                self.sig_id = self.container_helper["positions"]["SIG SMPL"][filename][-1][4]
                        self.sig_id += 1
                        self.sig_idlist.append(self.sig_id)
                        self.container_helper["limits SIG"][self.file]["ID"].append(self.sig_id)
                        self.container_helper["limits SIG"][self.file]["type"].append("custom")
                        self.container_helper["positions"]["SIG"][filename].append(
                            [round(self.container_helper["positions"][filename][0], 4),
                             round(self.container_helper["positions"][filename][1], 4)])
                        self.container_listboxes[self.file_type][filename]["SIG"][0].insert(
                            tk.END, "SIG"+str(self.sig_id)+" ["+str(self.container_helper["positions"][filename][0])+"-"
                                           +str(self.container_helper["positions"][filename][1])+"]")
                        #
                        if ratio_mode == False:
                            box_sig = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.brown_dark)
                            box_sig_ratio = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.brown_dark)
                            #
                            self.container_helper["limits SIG"][self.file][str(self.sig_id)] = box_sig
                            self.container_helper["limits SIG Ratio"][self.file][str(self.sig_id)] = box_sig_ratio
                            #
                            self.canvas.draw()
                            self.canvas_ratio.draw()
                        else:
                            box_sig_ratio = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.brown_dark)
                            box_sig = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.brown_dark)
                            #
                            self.container_helper["limits SIG Ratio"][self.file][str(self.sig_id)] = box_sig_ratio
                            self.container_helper["limits SIG"][self.file][str(self.sig_id)] = box_sig
                            #
                            self.canvas_ratio.draw()
                            self.canvas.draw()
                        #
                        self.indices_sig = self.container_helper["indices"][filename]
                        #
                        self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id] = {}
                        self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id]["Times"] = [
                            self.container_helper["positions"][filename][0],
                            self.container_helper["positions"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id]["Positions"] = [
                            self.container_helper["indices"][filename][0],
                            self.container_helper["indices"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id]["Box"] = box_sig
                        #
                        if self.file_type == "STD":
                            self.container_helper["STD"][filename]["SIG"][self.sig_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": [box_sig, box_sig_ratio]}
                            self.container_helper["positions"]["SIG STD"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.sig_id])
                        elif self.file_type == "SMPL":
                            self.container_helper["SMPL"][filename]["SIG"][self.sig_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": [box_sig, box_sig_ratio]}
                            self.container_helper["positions"]["SIG SMPL"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.sig_id])
                    elif var.get() == 3:    # SPK
                        isotope_list = []
                        for isotope in self.list_isotopes:
                            if isotope not in self.container_helper[self.file_type][filename]["SPK"]:
                                self.container_helper[self.file_type][filename]["SPK"][isotope] = {}
                            if self.container_var["plotting"][isotope][1].get() == 1:
                                isotope_list.append(isotope)
                        for isotope in isotope_list:
                            if len(self.container_helper[self.file_type][filename]["SPK"][isotope]) == 0:
                                self.spk_id = 1
                            else:
                                self.spk_id = int(len(self.container_helper[self.file_type][filename]["SPK"][isotope]) + 1)
                        isotope = "".join(isotope_list)
                        self.spk_idlist.append(self.spk_id)
                        self.container_helper["limits SPK"][self.file]["ID"].append(self.spk_id)
                        self.container_helper["limits SPK"][self.file]["type"].append("custom")
                        self.container_helper["limits SPK"][self.file]["info"].append([isotope, self.spk_id])
                        self.container_helper["positions"]["SPK"][filename].append(
                            [round(self.container_helper["positions"][filename][0], 4),
                             round(self.container_helper["positions"][filename][1], 4)])
                        #
                        if len(isotope_list) > 1:
                            color_var = self.yellow_dark
                        else:
                            color_var = self.isotope_colors[isotope]
                        self.container_listboxes[self.file_type][filename]["SPK"][0].insert(
                            tk.END, "["+", ".join(isotope_list)+"] #"+str(self.spk_id)+" ["+str(
                                self.container_helper["positions"][filename][0])+"-"+str(
                                self.container_helper["positions"][filename][1])+"]")
                        #
                        if ratio_mode == False:
                            box_spk = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.125, color=color_var)
                            self.container_helper["limits SPK"][self.file][str(self.spk_id)] = box_spk
                            #
                            self.canvas.draw()
                        else:
                            box_spk_ratio = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.125, color=color_var)
                            box_spk = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.125, color=color_var)
                            #
                            self.container_helper["limits SPK Ratio"][self.file][str(self.spk_id)] = box_spk_ratio
                            self.container_helper["limits SPK"][self.file][str(self.spk_id)] = box_spk
                            #
                            self.canvas_ratio.draw()
                            self.canvas.draw()
                        #
                        self.container_files[self.file_type][self.filename_short]["SPK"][self.spk_id] = {}
                        for isotope in isotope_list:
                            if isotope not in self.spikes_isotopes[self.file_type][filename]:
                                self.spikes_isotopes[self.file_type][filename][isotope] = []
                                self.spikes_isotopes[self.file_type][filename][isotope].append([self.container_helper["indices"][filename][0],
                                                                      self.container_helper["indices"][filename][1]])
                            else:
                                self.spikes_isotopes[self.file_type][filename][isotope].append([self.container_helper["indices"][filename][0],
                                                                      self.container_helper["indices"][filename][1]])
                            #
                            self.container_files[self.file_type][self.filename_short]["SPK"][self.spk_id][
                                "Isotope"] = isotope
                            self.container_files[self.file_type][self.filename_short]["SPK"][self.spk_id][
                                "Times"] = [
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1]]
                            self.container_files[self.file_type][self.filename_short]["SPK"][self.spk_id][
                                "Positions"] = [
                                self.container_helper["indices"][filename][0],
                                self.container_helper["indices"][filename][1]]
                            self.container_files[self.file_type][self.filename_short]["SPK"][self.spk_id][
                                "Box"] = box_spk
                            #
                            if self.file_type == "STD":
                                self.container_helper["STD"][filename]["SPK"][isotope][self.spk_id] = {
                                    "Times": [self.container_helper["positions"][filename][0],
                                              self.container_helper["positions"][filename][1]],
                                    "Positions": [self.container_helper["indices"][filename][0],
                                                  self.container_helper["indices"][filename][1]],
                                    "Object": box_spk}
                            elif self.file_type == "SMPL":
                                self.container_helper["SMPL"][filename]["SPK"][isotope][self.spk_id] = {
                                    "Times": [self.container_helper["positions"][filename][0],
                                              self.container_helper["positions"][filename][1]],
                                    "Positions": [self.container_helper["indices"][filename][0],
                                                  self.container_helper["indices"][filename][1]],
                                    "Object": box_spk}
                    #
                    elif var.get() == 4:    # MAT
                        if self.file_type == "STD":
                            if len(self.container_helper["positions"]["MAT STD"][filename]) > 0:
                                self.mat_id = self.container_helper["positions"]["MAT STD"][filename][-1][4]
                        elif self.file_type == "SMPL":
                            if len(self.container_helper["positions"]["MAT SMPL"][filename]) > 0:
                                self.mat_id = self.container_helper["positions"]["MAT SMPL"][filename][-1][4]
                        self.mat_id += 1
                        self.mat_idlist.append(self.mat_id)
                        self.container_helper["limits MAT"][self.file]["ID"].append(self.mat_id)
                        self.container_helper["limits MAT"][self.file]["type"].append("custom")
                        self.container_helper["positions"]["MAT"][filename].append(
                            [round(self.container_helper["positions"][filename][0], 4),
                             round(self.container_helper["positions"][filename][1], 4)])
                        self.container_listboxes[self.file_type][filename]["MAT"][0].insert(
                            tk.END, "MAT"+str(self.mat_id)+" ["+str(self.container_helper["positions"][filename][0])+"-"
                                    +str(self.container_helper["positions"][filename][1])+"]")
                        #
                        if ratio_mode == False:
                            box_mat = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.brown_dark)
                            self.container_helper["limits MAT"][self.file][str(self.mat_id)] = box_mat
                            #
                            self.canvas.draw()
                        else:
                            box_mat = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.brown_dark)
                            self.container_helper["limits MAT Ratio"][self.file][str(self.mat_id)] = box_mat
                            #
                            self.canvas_ratio.draw()
                        #
                        self.indices_mat = self.container_helper["indices"][filename]
                        #
                        self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id] = {}
                        self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id]["Times"] = [
                            self.container_helper["positions"][filename][0],
                            self.container_helper["positions"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id]["Positions"] = [
                            self.container_helper["indices"][filename][0],
                            self.container_helper["indices"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id]["Box"] = box_mat
                        #
                        if self.file_type == "STD":
                            self.container_helper["STD"][filename]["MAT"][self.mat_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": box_mat}
                            self.container_helper["positions"]["MAT STD"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.mat_id])
                        elif self.file_type == "SMPL":
                            self.container_helper["SMPL"][filename]["MAT"][self.mat_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": box_mat}
                            self.container_helper["positions"]["MAT SMPL"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.mat_id])
                    #
                    elif var.get() == 5:  # INCL
                        if self.file_type == "STD":
                            if len(self.container_helper["positions"]["INCL STD"][filename]) > 0:
                                self.incl_id = self.container_helper["positions"]["INCL STD"][filename][-1][4]
                        elif self.file_type == "SMPL":
                            if len(self.container_helper["positions"]["INCL SMPL"][filename]) > 0:
                                self.incl_id = self.container_helper["positions"]["INCL SMPL"][filename][-1][4]
                        self.incl_id += 1
                        self.incl_idlist.append(self.incl_id)
                        self.container_helper["limits INCL"][self.file]["ID"].append(self.incl_id)
                        self.container_helper["limits INCL"][self.file]["type"].append("custom")
                        self.container_helper["positions"]["INCL"][filename].append(
                            [round(self.container_helper["positions"][filename][0], 4),
                             round(self.container_helper["positions"][filename][1], 4)])
                        self.container_listboxes[self.file_type][filename]["INCL"][0].insert(
                            tk.END, "INCL" + str(self.incl_id) + " [" + str(
                                self.container_helper["positions"][filename][0]) + "-"
                                    + str(self.container_helper["positions"][filename][1]) + "]")
                        #
                        if ratio_mode == False:
                            box_incl = self.ax.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.slate_grey_dark)
                            self.container_helper["limits INCL"][self.file][str(self.incl_id)] = box_incl
                            #
                            self.canvas.draw()
                        else:
                            box_incl = self.ax_ratio.axvspan(
                                self.container_helper["positions"][filename][0],
                                self.container_helper["positions"][filename][1], alpha=0.25, color=self.slate_grey_dark)
                            self.container_helper["limits INCL Ratio"][self.file][str(self.incl_id)] = box_incl
                            #
                            self.canvas_ratio.draw()
                        #
                        self.indices_incl = self.container_helper["indices"][filename]
                        #
                        self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id] = {}
                        self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id]["Times"] = [
                            self.container_helper["positions"][filename][0],
                            self.container_helper["positions"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id][
                            "Positions"] = [
                            self.container_helper["indices"][filename][0],
                            self.container_helper["indices"][filename][1]]
                        self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id][
                            "Box"] = box_incl
                        #
                        if self.file_type == "STD":
                            self.container_helper["STD"][filename]["INCL"][self.incl_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": box_incl}
                            self.container_helper["positions"]["INCL STD"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.incl_id])
                        elif self.file_type == "SMPL":
                            self.container_helper["SMPL"][filename]["INCL"][self.incl_id] = {
                                "Times": [self.container_helper["positions"][filename][0],
                                          self.container_helper["positions"][filename][1]],
                                "Positions": [self.container_helper["indices"][filename][0],
                                              self.container_helper["indices"][filename][1]],
                                "Object": box_incl}
                            self.container_helper["positions"]["INCL SMPL"][filename].append(
                                [self.container_helper["positions"][filename][0],
                                 self.container_helper["positions"][filename][1],
                                 self.container_helper["indices"][filename][0],
                                 self.container_helper["indices"][filename][1],
                                 self.incl_id])
                #
                    elif var.get() == 0:
                        pass
            else:
                pass
            #
        else:
            if var.get() == 1:
                if len(self.container_helper["positions"][filename]) == 2 and len(self.container_helper["indices"][filename]) == 2:
                    self.container_helper["positions"][filename].clear()
                    self.container_helper["indices"][filename].clear()
                #
                x_nearest = min(self.times, key=lambda x: abs(x-event.xdata))
                self.container_helper["positions"][filename].append(x_nearest)
                self.container_helper["indices"][filename].append(self.times[self.times == x_nearest].index[0])
                #
                if len(self.container_helper["positions"][filename])+len(self.container_helper["indices"][filename]) == 4:
                    if var.get() == 1:
                        self.se_id += 1
                        self.se_idlist.append(self.se_id)
                        self.positions_se.append([round(self.container_helper["positions"][filename][0], 4), round(self.container_helper["positions"][filename][1], 4)])
                        self.lb_se.insert(tk.END, "Spikes"+str(self.se_id)+" ["+str(self.container_helper["positions"][filename][0])+"-"+
                                                       str(self.container_helper["positions"][filename][1])+"]"+" ["+str(self.container_helper["indices"][filename][0]) + "-"+
                                                       str(self.container_helper["indices"][filename][1]) +"]")
                        box_se = self.ax.axvspan(self.container_helper["positions"][filename][0], self.container_helper["positions"][filename][1], alpha=0.25,
                                                 color="#fff6a4")
                        self.limits_se[str(self.se_id)] = box_se
                        self.canvas_se.draw()
                    elif var.get() == 0:
                        pass
            else:
                pass
    #
    def delete_interval(self, var):
        filename = self.file.split("/")[-1]
        #
        if var.get() == 1:  # BG
            item = self.container_listboxes[self.file_type][filename]["BG"][0].curselection()
            index = self.container_helper["limits BG"][self.file]["ID"][item[0]]
            self.container_helper["limits BG"][self.file]["ID"].remove(index)
            #
            self.container_listboxes[self.file_type][filename]["BG"][0].delete(tk.ANCHOR)
            if self.file_type == "STD":
                for object in self.container_helper["STD"][filename]["BG"][index]["Object"]:
                    object.set_visible(False)
                #
                self.canvas.draw()
                self.canvas_ratio.draw()
                self.container_helper["STD"][filename]["BG"].pop(index)
                for item in self.container_helper["positions"]["BG STD"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["BG STD"][filename].remove(item)
            elif self.file_type == "SMPL":
                for object in self.container_helper["STD"][filename]["BG"][index]["Object"]:
                    object.set_visible(False)
                #
                self.canvas.draw()
                self.canvas_ratio.draw()
                self.container_helper["SMPL"][filename]["BG"].pop(index)
                for item in self.container_helper["positions"]["BG SMPL"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["BG SMPL"][filename].remove(item)
        #
        elif var.get() == 2:    # SIG
            #
            #item = self.lb_sig.curselection()
            item = self.container_listboxes[self.file_type][filename]["SIG"][0].curselection()
            index = self.container_helper["limits SIG"][self.file]["ID"][item[0]]
            self.container_helper["limits SIG"][self.file]["ID"].remove(index)
            #
            #self.lb_sig.delete(tk.ANCHOR)
            self.container_listboxes[self.file_type][filename]["SIG"][0].delete(tk.ANCHOR)
            if self.file_type == "STD":
                for object in self.container_helper["STD"][filename]["SIG"][index]["Object"]:
                    object.set_visible(False)
                #self.container_helper["STD"][filename]["SIG"][index]["Object"].set_visible(False)
                self.canvas.draw()
                self.canvas_ratio.draw()
                self.container_helper["STD"][filename]["SIG"].pop(index)
                for item in self.container_helper["positions"]["SIG STD"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["SIG STD"][filename].remove(item)
            elif self.file_type == "SMPL":
                for object in self.container_helper["SMPL"][filename]["SIG"][index]["Object"]:
                    object.set_visible(False)
                #self.container_helper["SMPL"][filename]["SIG"][index]["Object"].set_visible(False)
                self.canvas.draw()
                self.canvas_ratio.draw()
                self.container_helper["SMPL"][filename]["SIG"].pop(index)
                for item in self.container_helper["positions"]["SIG SMPL"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["SIG SMPL"][filename].remove(item)
        #
        elif var.get() == 3:    # SPK
            #
            #item = self.lb_spk.curselection()
            item = self.container_listboxes[self.file_type][filename]["SPK"][0].curselection()
            isotope = self.container_helper["limits SPK"][self.file]["info"][item[0]][0]
            index = self.container_helper["limits SPK"][self.file]["info"][item[0]][1]
            self.container_helper["limits SPK"][self.file]["info"].pop(item[0])
            self.container_helper["limits SPK"][self.file]["ID"].remove(index)
            #
            #self.lb_spk.delete(tk.ANCHOR)
            self.container_listboxes[self.file_type][filename]["SPK"][0].delete(tk.ANCHOR)
            if len(isotope) < 6:
                if self.file_type == "STD":
                    self.container_helper["STD"][filename]["SPK"][isotope][index]["Object"].set_visible(False)
                    self.canvas.draw()
                    self.container_helper["STD"][filename]["SPK"][isotope].pop(index)
                    for item in self.container_helper["positions"]["SPK STD"][filename]:
                        if index == item[-1]:
                            self.container_helper["positions"]["SPK STD"][filename].remove(item)
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename]["SPK"][isotope][index]["Object"].set_visible(False)
                    self.canvas.draw()
                    self.container_helper["SMPL"][filename]["SPK"][isotope].pop(index)
                    for item in self.container_helper["positions"]["SPK SMPL"][filename]:
                        if index == item[-1]:
                            self.container_helper["positions"]["SPK SMPL"][filename].remove(item)
            else:
                self.container_helper[self.file_type][filename]["SPK"][self.list_isotopes[0]][index]["Object"].set_visible(False)
                self.canvas.draw()
                for isotope in self.list_isotopes:
                    self.container_helper[self.file_type][filename]["SPK"][isotope].pop(index)
        #
        elif var.get() == 4:    # MAT
            #
            item = self.container_listboxes[self.file_type][filename]["MAT"][0].curselection()
            index = self.container_helper["limits MAT"][self.file]["ID"][item[0]]
            self.container_helper["limits MAT"][self.file]["ID"].remove(index)
            #
            self.container_listboxes[self.file_type][filename]["MAT"][0].delete(tk.ANCHOR)
            if self.file_type == "STD":
                self.container_helper["STD"][filename]["MAT"][index]["Object"].set_visible(False)
                self.canvas.draw()
                self.container_helper["STD"][filename]["MAT"].pop(index)
                for item in self.container_helper["positions"]["MAT STD"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["MAT STD"][filename].remove(item)
            elif self.file_type == "SMPL":
                self.container_helper["SMPL"][filename]["MAT"][index]["Object"].set_visible(False)
                self.canvas.draw()
                self.container_helper["SMPL"][filename]["MAT"].pop(index)
                for item in self.container_helper["positions"]["MAT SMPL"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["MAT SMPL"][filename].remove(item)
        #
        elif var.get() == 5:    # INCL
            #
            item = self.container_listboxes[self.file_type][filename]["INCL"][0].curselection()
            index = self.container_helper["limits INCL"][self.file]["ID"][item[0]]
            self.container_helper["limits INCL"][self.file]["ID"].remove(index)
            #
            self.container_listboxes[self.file_type][filename]["INCL"][0].delete(tk.ANCHOR)
            if self.file_type == "STD":
                self.container_helper["STD"][filename]["INCL"][index]["Object"].set_visible(False)
                self.canvas.draw()
                self.container_helper["STD"][filename]["INCL"].pop(index)
                for item in self.container_helper["positions"]["INCL STD"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["INCL STD"][filename].remove(item)
            elif self.file_type == "SMPL":
                self.container_helper["SMPL"][filename]["INCL"][index]["Object"].set_visible(False)
                self.canvas.draw()
                self.container_helper["SMPL"][filename]["INCL"].pop(index)
                for item in self.container_helper["positions"]["INCL SMPL"][filename]:
                    if index == item[-1]:
                        self.container_helper["positions"]["INCL SMPL"][filename].remove(item)
    #
    def update_edited_datasets(self, mode="MA"):
        filename = self.file.split("/")[-1]
        if mode == "MA":
            intervals_bg = []
            intervals_sig = []
            #
            for key, value in self.container_helper[self.file_type][filename]["BG"].items():
                intervals_bg.append(value["Positions"])
            for key, value in self.container_helper[self.file_type][filename]["SIG"].items():
                intervals_sig.append(value["Positions"])
            #
            merged_intervals_bg = ES(variable=np.array(intervals_bg)).merge_times()
            merged_intervals_sig = ES(variable=np.array(intervals_sig)).merge_times()
            self.container_files[self.file_type][filename]["BG limits"] = merged_intervals_bg
            self.container_files[self.file_type][filename]["SIG limits"] = merged_intervals_sig
            #
            for key_01, value_01 in self.container_measurements["SELECTED"][filename].items():
                if key_01 != "Time":
                    for key_02, value_02 in value_01.items():
                        for interval in merged_intervals_bg:
                            if key_01 == "RAW":
                                value_02["BG"].extend(
                                    self.container_measurements["RAW"][filename][key_02][interval[0]:interval[1]+1])
                            elif key_01 == "SMOOTHED":
                                try:
                                    value_02["BG"].extend(
                                        self.container_measurements["EDITED"][filename][key_02][
                                        interval[0]:interval[1] + 1])
                                except:
                                    value_02["BG"].extend(np.ones(1000))
                        for interval in merged_intervals_sig:
                            if key_01 == "RAW":
                                value_02["SIG"].extend(
                                    self.container_measurements["RAW"][filename][key_02][interval[0]:interval[1]+1])
                            elif key_01 == "SMOOTHED":
                                try:
                                    value_02["SIG"].extend(
                                        self.container_measurements["EDITED"][filename][key_02][
                                        interval[0]:interval[1] + 1])
                                except:
                                    value_02["SIG"].extend(np.ones(1000))
        elif mode in ["FI", "MI"]:
            intervals_bg = []
            intervals_mat = []
            intervals_incl = []
            #
            for key, value in self.container_helper[self.file_type][filename]["BG"].items():
                intervals_bg.append(value["Positions"])
            for key, value in self.container_helper[self.file_type][filename]["MAT"].items():
                intervals_mat.append(value["Positions"])
            for key, value in self.container_helper[self.file_type][filename]["INCL"].items():
                intervals_incl.append(value["Positions"])
            #
            merged_intervals_bg = ES(variable=np.array(intervals_bg)).merge_times()
            merged_intervals_mat = ES(variable=np.array(intervals_mat)).merge_times()
            merged_intervals_incl = ES(variable=np.array(intervals_incl)).merge_times()
            self.container_files[self.file_type][filename]["BG limits"] = merged_intervals_bg
            self.container_files[self.file_type][filename]["MAT limits"] = merged_intervals_mat
            self.container_files[self.file_type][filename]["INCL limits"] = merged_intervals_incl
            #
            for key_01, value_01 in self.container_measurements["SELECTED"][filename].items():
                if key_01 != "Time":
                    for key_02, value_02 in value_01.items():
                        for interval in merged_intervals_bg:
                            if key_01 == "RAW":
                                value_02["BG"].extend(
                                    self.container_measurements["RAW"][filename][key_02][interval[0]:interval[1] + 1])
                            elif key_01 == "SMOOTHED":
                                try:
                                    value_02["BG"].extend(
                                        self.container_measurements["EDITED"][filename][key_02][
                                        interval[0]:interval[1] + 1])
                                except:
                                    value_02["BG"].extend(np.ones(1000))
                        for interval in merged_intervals_mat:
                            if key_01 == "RAW":
                                value_02["MAT"].extend(
                                    self.container_measurements["RAW"][filename][key_02][interval[0]:interval[1] + 1])
                            elif key_01 == "SMOOTHED":
                                try:
                                    value_02["MAT"].extend(
                                        self.container_measurements["EDITED"][filename][key_02][
                                        interval[0]:interval[1] + 1])
                                except:
                                    value_02["MAT"].extend(np.ones(1000))
                        for interval in merged_intervals_incl:
                            if key_01 == "RAW":
                                value_02["INCL"].extend(
                                    self.container_measurements["RAW"][filename][key_02][interval[0]:interval[1] + 1])
                            elif key_01 == "SMOOTHED":
                                try:
                                    value_02["INCL"].extend(
                                        self.container_measurements["EDITED"][filename][key_02][
                                        interval[0]:interval[1] + 1])
                                except:
                                    value_02["INCL"].extend(np.ones(1000))
    #
    def smooth_all_isotopes(self):
        #
        if len(self.container_helper["positions"][self.filename_short]) == 2 \
                and len(self.container_helper["indices"][self.filename_short]) == 2:
            self.container_helper["positions"][self.filename_short].clear()
            self.container_helper["indices"][self.filename_short].clear()
        #
        isotope_list = []
        for isotope in self.list_isotopes:
            isotope_list.append(isotope)
            if isotope not in self.container_helper[self.file_type][self.filename_short]["SPK"]:
                self.container_helper[self.file_type][self.filename_short]["SPK"][isotope] = {}
            if len(self.container_helper[self.file_type][self.filename_short]["SPK"][isotope]) == 0:
                self.spk_id = 1
            else:
                self.spk_id = int(len(self.container_helper[self.file_type][self.filename_short]["SPK"][isotope]) + 1)
        #
        start_time = self.times.iloc[0]
        end_time = self.times.iloc[-1]
        self.container_helper["positions"][self.filename_short].extend([round(start_time, 4), round(end_time, 4)])
        self.container_helper["indices"][self.filename_short].extend([self.times[self.times == start_time].index[0],
                                                                      self.times[self.times == end_time].index[0]])
        #
        isotope = "".join(isotope_list)
        self.spk_idlist.append(self.spk_id)
        self.container_helper["limits SPK"][self.file]["ID"].append(self.spk_id)
        self.container_helper["limits SPK"][self.file]["type"].append("custom")
        self.container_helper["limits SPK"][self.file]["info"].append([isotope, self.spk_id])
        self.container_helper["positions"]["SPK"][self.filename_short].append(
            [round(self.container_helper["positions"][self.filename_short][0], 4),
             round(self.container_helper["positions"][self.filename_short][1], 4)])
        #
        if len(isotope_list) > 1:
            color_var = self.yellow_dark
        else:
            color_var = self.isotope_colors[isotope]
        self.container_listboxes[self.file_type][self.filename_short]["SPK"][0].insert(
            tk.END, "["+", ".join(isotope_list)+"] #"+str(self.spk_id)+" ["+str(
                self.container_helper["positions"][self.filename_short][0])+"-"+str(
                self.container_helper["positions"][self.filename_short][1])+"]")
        box_spk = self.ax.axvspan(self.container_helper["positions"][self.filename_short][0],
                                  self.container_helper["positions"][self.filename_short][1], alpha=0.125,
                                  color=color_var)
        self.container_helper["limits SPK"][self.file][str(self.spk_id)] = box_spk
        self.canvas.draw()
        #
        for isotope in isotope_list:
            if isotope not in self.spikes_isotopes[self.file_type][self.filename_short]:
                self.spikes_isotopes[self.file_type][self.filename_short][isotope] = []
                self.spikes_isotopes[self.file_type][self.filename_short][isotope].append([self.container_helper["indices"][self.filename_short][0],
                                                      self.container_helper["indices"][self.filename_short][1]])
            else:
                self.spikes_isotopes[self.file_type][self.filename_short][isotope].append([self.container_helper["indices"][self.filename_short][0],
                                                      self.container_helper["indices"][self.filename_short][1]])
            if self.file_type == "STD":
                self.container_helper["STD"][self.filename_short]["SPK"][isotope][self.spk_id] = {
                    "Times": [self.container_helper["positions"][self.filename_short][0],
                              self.container_helper["positions"][self.filename_short][1]],
                    "Positions": [self.container_helper["indices"][self.filename_short][0],
                                  self.container_helper["indices"][self.filename_short][1]],
                    "Object": box_spk}
            elif self.file_type == "SMPL":
                self.container_helper["SMPL"][self.filename_short]["SPK"][isotope][self.spk_id] = {
                    "Times": [self.container_helper["positions"][self.filename_short][0],
                              self.container_helper["positions"][self.filename_short][1]],
                    "Positions": [self.container_helper["indices"][self.filename_short][0],
                                  self.container_helper["indices"][self.filename_short][1]],
                    "Object": box_spk}
    #
    def do_spike_elimination_all(self, file_type, settings="settings"):
        if file_type == "STD":
            for file_short in self.container_lists["STD"]["Short"]:
                #
                isotopes_spiked_list = [*self.spikes_isotopes[file_type][file_short]]
                corrected_isotopes = []
                not_corrected_isotopes = []
                #
                for isotope in self.list_isotopes:
                    if bool(self.spikes_isotopes[file_type][file_short]) == True:
                        for isotope_spiked, intervals in self.spikes_isotopes[file_type][file_short].items():
                            if isotope in isotopes_spiked_list:
                                if isotope not in corrected_isotopes:
                                    corrected_isotopes.append(isotope)
                                    spike_intervals = np.array(intervals)
                                    merged_intervals = ES(variable=spike_intervals).merge_times()
                                    for interval in merged_intervals:
                                        data_smoothed, indices_outl = ES(
                                            variable=self.container_measurements["RAW"][file_short][isotope][
                                                     interval[0]:interval[1]]).find_outlier(
                                            limit=float(self.container_var[settings]["SE Deviation"].get()),
                                            threshold=float(self.container_var[settings]["SE Threshold"].get()),
                                            interval=interval,
                                            data_total=self.container_measurements["RAW"][file_short],
                                            isotope=isotope)
                                        self.container_measurements["EDITED"][file_short][
                                            isotope] = data_smoothed
                                else:
                                    pass
                            else:
                                if isotope not in not_corrected_isotopes:
                                    not_corrected_isotopes.append(isotope)
                                    self.container_measurements["EDITED"][file_short][isotope] = \
                                        self.container_measurements["RAW"][file_short][isotope]
                                else:
                                    pass
                    else:
                        if isotope not in not_corrected_isotopes:
                            not_corrected_isotopes.append(isotope)
                            self.container_measurements["EDITED"][file_short][isotope] = \
                                self.container_measurements["RAW"][file_short][isotope]
                        else:
                            pass
                #
        elif file_type == "SMPL":
            for file_short in self.container_lists["SMPL"]["Short"]:
                #
                isotopes_spiked_list = [*self.spikes_isotopes[file_type][file_short]]
                corrected_isotopes = []
                not_corrected_isotopes = []
                #
                for isotope in self.list_isotopes:
                    if bool(self.spikes_isotopes[file_type][file_short]) == True:
                        for isotope_spiked, intervals in self.spikes_isotopes[file_type][file_short].items():
                            if isotope in isotopes_spiked_list:
                                if isotope not in corrected_isotopes:
                                    corrected_isotopes.append(isotope)
                                    spike_intervals = np.array(intervals)
                                    merged_intervals = ES(variable=spike_intervals).merge_times()
                                    for interval in merged_intervals:
                                        data_smoothed, indices_outl = ES(
                                            variable=self.container_measurements["RAW"][file_short][isotope][
                                                     interval[0]:interval[1]]).find_outlier(
                                            limit=float(self.container_var[settings]["SE Deviation"].get()),
                                            threshold=float(self.container_var[settings]["SE Threshold"].get()),
                                            interval=interval,
                                            data_total=self.container_measurements["RAW"][file_short],
                                            isotope=isotope)
                                        self.container_measurements["EDITED"][file_short][
                                            isotope] = data_smoothed
                                else:
                                    pass
                            else:
                                if isotope not in not_corrected_isotopes:
                                    not_corrected_isotopes.append(isotope)
                                    self.container_measurements["EDITED"][file_short][isotope] = \
                                        self.container_measurements["RAW"][file_short][isotope]
                                else:
                                    pass
                    else:
                        if isotope not in not_corrected_isotopes:
                            not_corrected_isotopes.append(isotope)
                            self.container_measurements["EDITED"][file_short][isotope] = \
                                self.container_measurements["RAW"][file_short][isotope]
                        else:
                            pass
                #
    #
    def do_spike_elimination(self, var_setting="settings"):
        #
        isotopes_spiked_list = [*self.spikes_isotopes[self.file_type][self.filename_short]]
        corrected_isotopes = []
        not_corrected_isotopes = []
        #
        for isotope in self.list_isotopes:
            if bool(self.spikes_isotopes[self.file_type][self.filename_short]) == True:
                for isotope_spiked, intervals in self.spikes_isotopes[self.file_type][self.filename_short].items():
                    if isotope in isotopes_spiked_list:
                        if isotope not in corrected_isotopes:
                            corrected_isotopes.append(isotope)
                            spike_intervals = np.array(intervals)
                            merged_intervals = ES(variable=spike_intervals).merge_times()
                            for interval in merged_intervals:
                                data_smoothed, indices_outl = ES(
                                    variable=self.container_measurements["RAW"][self.filename_short][isotope][interval[0]:interval[1]]).find_outlier(
                                    limit=float(self.container_var[var_setting]["SE Deviation"].get()),
                                    threshold=float(self.container_var[var_setting]["SE Threshold"].get()),
                                    interval=interval, data_total=self.container_measurements["RAW"][self.filename_short],
                                    isotope=isotope)
                                self.container_measurements["EDITED"][self.filename_short][isotope] = data_smoothed
                        else:
                            pass
                    else:
                        if isotope not in not_corrected_isotopes:
                            not_corrected_isotopes.append(isotope)
                            self.container_measurements["EDITED"][self.filename_short][isotope] = \
                                self.container_measurements["RAW"][self.filename_short][isotope]
                        else:
                            pass
            else:
                if isotope not in not_corrected_isotopes:
                    not_corrected_isotopes.append(isotope)
                    self.container_measurements["EDITED"][self.filename_short][isotope] = \
                        self.container_measurements["RAW"][self.filename_short][isotope]
                else:
                    pass
        #
        ## DIAGRAM
        for isotope in self.list_isotopes:
            ln = self.ax.plot(
                self.times, self.container_measurements["EDITED"][self.filename_short][isotope], label=isotope,
                color=self.isotope_colors[isotope], visible=True)
            self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Smoothed"][isotope] = ln
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["SMOOTHED"][isotope].set(1)
        self.diagrams_setup[self.file_type][self.filename_short]["CANVAS"].draw()
    #
    def show_smoothed_data(self):
        ## DIAGRAM
        for isotope in self.list_isotopes:
            ln = self.diagrams_setup[self.file_type][self.filename_short]["AX"].plot(
                self.times, self.container_measurements["EDITED"][self.filename_short][isotope], label=isotope,
                color=self.isotope_colors[isotope], visible=True)
            self.diagrams_setup[self.file_type][self.filename_short]["Time Signal Smoothed"][isotope] = ln
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["SMOOTHED"][isotope].set(1)
        self.diagrams_setup[self.file_type][self.filename_short]["CANVAS"].draw()
    #
    def export_calculation_report(self, file_type="Sample Files", data_type="SMOOTHED"):
        #
        header = ["filename"]
        #
        categories = ["Intensity Ratio", "Sensitivity", "Concentration", "RSF", "LOD"]
        for index, file_std in enumerate(self.container_lists["STD"]["Short"]):
            for category in categories:
                for isotope in self.list_isotopes:
                    self.container_report[file_std]["Mean"][category][isotope] = round(
                        np.mean(self.container_results["STD"]["SMOOTHED"][isotope][category][index]), 6)
        for index, file_smpl in enumerate(self.container_lists["SMPL"]["Short"]):
            for category in categories:
                for isotope in self.list_isotopes:
                    self.container_report[file_smpl]["Mean"][category][isotope] = round(
                        np.mean(self.container_results["SMPL"]["SMOOTHED"][isotope][category][index]), 6)
        for category in categories:
            for isotope in self.list_isotopes:
                self.container_report["Total STD"]["Mean"][category][isotope] = round(
                    np.mean(self.container_results["STD"]["SMOOTHED"][isotope][category]), 6)
                self.container_report["Total SMPL"]["Mean"][category][isotope] = round(
                    np.mean(self.container_results["SMPL"]["SMOOTHED"][isotope][category]), 6)
        for isotope in self.list_isotopes:
            header.append(isotope)
        #
        filename = "../outputs/Report_"
        filename = filename.__add__(self.container_var["settings"]["Source ID"].get())
        filename = filename.__add__(".csv")
        #
        with open(filename, "w", newline="") as report_file:
            writer = csv.DictWriter(report_file, fieldnames=header, delimiter=";")
            report_file.write("CALCULATION REPORT\n")
            report_file.write("\n")
            report_file.write("AUTHOR:;" + str(self.container_var["settings"]["Author"].get()) + "\n")
            report_file.write("SOURCE ID:;" + str(self.container_var["settings"]["Source ID"].get()) + "\n")
            report_file.write("\n")
            #
            ## STANDARD FILES
            # Intensity Ratios
            report_file.write("SIGNAL INTENSITY RATIO (arithmetic mean)\n")
            report_file.write("Standard Files\n")
            writer.writeheader()
            for file_std in self.container_lists["STD"]["Short"]:
                writer.writerow(self.container_report[file_std]["Mean"]["Intensity Ratio"])
            writer.writerow(self.container_report["Total STD"]["Mean"]["Intensity Ratio"])
            report_file.write("\n")
            # Sensitivity
            report_file.write("SENSITIVITY (arithmetic mean)\n")
            report_file.write("Standard Files\n")
            writer.writeheader()
            for file_std in self.container_lists["STD"]["Short"]:
                writer.writerow(self.container_report[file_std]["Mean"]["Sensitivity"])
            writer.writerow(self.container_report["Total STD"]["Mean"]["Sensitivity"])
            report_file.write("\n")
            # Concentration
            report_file.write("CONCENTRATION (arithmetic mean)\n")
            report_file.write("Standard Files\n")
            writer.writeheader()
            for file_std in self.container_lists["STD"]["Short"]:
                writer.writerow(self.container_report[file_std]["Mean"]["Concentration"])
            writer.writerow(self.container_report["Total STD"]["Mean"]["Concentration"])
            report_file.write("\n")
            # Relative Sensitivity Factor (RSF)
            report_file.write("RELATIVE SENSITIVITY FACTOR RSF (arithmetic mean)\n")
            report_file.write("Standard Files\n")
            writer.writeheader()
            for file_std in self.container_lists["STD"]["Short"]:
                writer.writerow(self.container_report[file_std]["Mean"]["RSF"])
            writer.writerow(self.container_report["Total STD"]["Mean"]["RSF"])
            report_file.write("\n")
            # Limit of Detection (LOD)
            report_file.write("LIMIT OF DETECTION LOD (arithmetic mean)\n")
            report_file.write("Standard Files\n")
            writer.writeheader()
            for file_std in self.container_lists["STD"]["Short"]:
                writer.writerow(self.container_report[file_std]["Mean"]["LOD"])
            writer.writerow(self.container_report["Total STD"]["Mean"]["LOD"])
            report_file.write("\n")
            #
            ## SAMPLE FILES
            # Intensity Ratios
            report_file.write("SIGNAL INTENSITY RATIO (arithmetic mean)\n")
            report_file.write("Sample Files\n")
            writer.writeheader()
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                writer.writerow(self.container_report[file_smpl]["Mean"]["Intensity Ratio"])
            writer.writerow(self.container_report["Total SMPL"]["Mean"]["Intensity Ratio"])
            report_file.write("\n")
            # Sensitivity
            report_file.write("SENSITIVITY (arithmetic mean)\n")
            report_file.write("Sample Files\n")
            writer.writeheader()
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                writer.writerow(self.container_report[file_smpl]["Mean"]["Sensitivity"])
            writer.writerow(self.container_report["Total SMPL"]["Mean"]["Sensitivity"])
            report_file.write("\n")
            # Concentration
            report_file.write("CONCENTRATION (arithmetic mean)\n")
            report_file.write("Sample Files\n")
            writer.writeheader()
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                writer.writerow(self.container_report[file_smpl]["Mean"]["Concentration"])
            writer.writerow(self.container_report["Total SMPL"]["Mean"]["Concentration"])
            report_file.write("\n")
            # Relative Sensitivity Factor (RSF)
            report_file.write("RELATIVE SENSITIVITY FACTOR RSF (arithmetic mean)\n")
            report_file.write("Sample Files\n")
            writer.writeheader()
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                writer.writerow(self.container_report[file_smpl]["Mean"]["RSF"])
            writer.writerow(self.container_report["Total SMPL"]["Mean"]["RSF"])
            report_file.write("\n")
            # Limit of Detection (LOD)
            report_file.write("LIMIT OF DETECTION LOD (arithmetic mean)\n")
            report_file.write("Sample Files\n")
            writer.writeheader()
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                writer.writerow(self.container_report[file_smpl]["Mean"]["LOD"])
            writer.writerow(self.container_report["Total SMPL"]["Mean"]["LOD"])
            report_file.write("\n")
    #
    def titanium_in_quartz_geothermometer(self, data): # e.g. data = self.container_results["STD"]["RAW"]
        for isotope, value in data.items():
            print(isotope, value)
    #
    def delete_csv(self, var_lb, var_list):
        if var_lb == self.lb_std:
            var_list = self.list_std
        elif var_lb == self.lb_smpl:
            var_list = self.list_smpl
        item = var_lb.curselection()
        var_list.remove(var_list[item[0]])
        var_lb.delete(tk.ANCHOR)
    #
    def show_diagrams(self, filename):
        isotope = self.list_isotopes[self.container_var["ma_dataexploration"]["RB"].get()]
        isotope_is = self.container_var["ma_dataexploration"]["Option IS"].get()
        #
        results_ir = self.calculate_intensity_ratios(filename=filename, isotope=isotope, isotope_is=isotope_is)
        results_xi = self.calculate_sensitivity(filename=filename, isotope=isotope, isotope_is=isotope_is)
        results_c = self.calculate_concentration(filename=filename, isotope=isotope, isotope_is=isotope_is,
                                                 sensitivities=results_xi)
        #
        self.fig = Figure(figsize=(8, 8), facecolor=self.green_light)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        #
        self.ax1.hist(x=self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope]["SIG"],
                      color=self.isotope_colors[isotope], edgecolor="black")
        self.ax1.set_xlabel("Signal Intensity (cps "+str(isotope)+")", labelpad=0.5)
        self.ax1.set_ylabel("Frequency (#)", labelpad=0.5)
        self.ax1.grid(True)
        self.ax1.set_axisbelow(True)
        #
        self.ax2.scatter(x=self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope_is]["SIG"],
                         y=self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope]["SIG"],
                         color=self.isotope_colors[isotope], edgecolor="black", alpha=0.67)
        self.ax2.set_xlabel("Signal Intensity (cps "+str(isotope_is)+")", labelpad=0.5)
        self.ax2.set_ylabel("Signal Intensity (cps "+str(isotope)+")", labelpad=0.5)
        self.ax2.grid(True)
        self.ax2.set_axisbelow(True)
        #
        self.ax3.hist(x=results_ir, color=self.isotope_colors[isotope], edgecolor="black")
        self.ax3.set_xlabel("Intensity Ratio (cps "+str(isotope)+")/(cps "+str(isotope_is)+")", labelpad=0.5)
        self.ax3.set_ylabel("Frequency (#)", labelpad=0.5)
        self.ax3.grid(True)
        self.ax3.set_axisbelow(True)
        #
        self.ax4.scatter(x=results_xi, y=results_c, color=self.isotope_colors[isotope], edgecolor="black", alpha=0.67)
        self.ax4.set_xlabel("Sensitivity (cps/ppm)", labelpad=0.5)
        self.ax4.set_ylabel("Concentration (ppm)", labelpad=0.5)
        self.ax4.grid(True)
        self.ax4.set_axisbelow(True)
        #
        self.fig.subplots_adjust(bottom=0.125, top=0.975, left=0.055, right=0.975)
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().grid(row=0, column=42, rowspan=38, columnspan=48, sticky="nesw")
        self.toolbarFrame = tk.Frame(master=self.parent)
        self.toolbarFrame.grid(row=38, column=42, rowspan=2, columnspan=48, sticky="w")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.config(background=self.green_light)
        self.toolbar._message_label.config(background=self.green_light)
        self.toolbar.winfo_children()[-2].config(background=self.green_light)
    #
    def calculate_intensity_ratios(self, filename, isotope, isotope_is):
        data_i = np.array(self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope]["SIG"])
        data_is = np.array(self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope_is]["SIG"])
        results = data_i/data_is
        #
        return results
    #
    def calculate_sensitivity(self, filename, isotope, isotope_is):
        if filename in self.container_lists["STD"]["Short"]:
            intensities_i = np.array(self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope]["SIG"])
            intensities_is = np.array(self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope_is]["SIG"])
            key_i = re.search("(\D+)(\d+)", isotope)
            element_i = key_i.group(1)
            key_is = re.search("(\D+)(\d+)", isotope_is)
            element_is = key_is.group(1)
            concentration_i = self.srm_actual[self.container_var["ma_dataexploration"]["Option SRM"].get()][element_i]
            concentration_is = self.srm_actual[self.container_var["ma_dataexploration"]["Option SRM"].get()][element_is]
            results = intensities_i/intensities_is * concentration_is/concentration_i
        elif filename in self.container_lists["SMPL"]["Short"]:
            filetype = "SMPL"
            limits_sig = self.container_files[filetype][filename]["SIG limits"]
            time_values = []
            for interval_sig in limits_sig:
                times = self.container_measurements["SELECTED"][filename]["Time"][interval_sig[0]:interval_sig[1]+1]
                time_values.extend(times)
            times_shifted = self.smpl_times[filename]["Delta"] + np.array(time_values)
            results = self.xi_opt[isotope][0]*times_shifted + self.xi_opt[isotope][1]
        #
        return results
    #
    def calculate_concentration(self, filename, isotope, isotope_is, sensitivities):
        if filename in self.container_lists["STD"]["Short"]:
            key_i = re.search("(\D+)(\d+)", isotope)
            element_i = key_i.group(1)
            concentration_i = self.srm_actual[self.container_var["ma_dataexploration"]["Option SRM"].get()][element_i]
            results = np.ones(len(sensitivities))*concentration_i
        elif filename in self.container_lists["SMPL"]["Short"]:
            intensities_i = np.array(self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope]["SIG"])
            intensities_is = np.array(self.container_measurements["SELECTED"][filename]["SMOOTHED"][isotope_is]["SIG"])
            sensitivities_i = sensitivities
            concentration_is = float(self.container_files["SMPL"][filename]["IS Concentration"].get())
            #
            results = intensities_i/intensities_is * concentration_is/sensitivities_i
        #
        return results
    #
    def show_histogram(self, filename):
        # if self.container_var["plotting"][filename_short]["RB"][1].get() == 0:
        #     if self.file_type == "STD":
        #         if self.fast_track_std == True:
        #             self.fig = self.container_diagrams[self.file_type][filename_short]["FIG"]
        #             self.ax = self.container_diagrams[self.file_type][filename_short]["AX"]
        #         else:
        #             self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
        #             self.ax = self.fig.add_subplot()
        #             self.container_diagrams[self.file_type][filename_short]["FIG"] = self.fig
        #             self.container_diagrams[self.file_type][filename_short]["AX"] = self.ax
        #     elif self.file_type == "SMPL":
        #         if self.fast_track_smpl == True:
        #             self.fig = self.container_diagrams[self.file_type][filename_short]["FIG"]
        #             self.ax = self.container_diagrams[self.file_type][filename_short]["AX"]
        #         else:
        #             self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
        #             self.ax = self.fig.add_subplot()
        #             self.container_diagrams[self.file_type][filename_short]["FIG"] = self.fig
        #             self.container_diagrams[self.file_type][filename_short]["AX"] = self.ax
        self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
        self.ax = self.fig.add_subplot()
        sns.set_theme()

        for isotope in self.list_isotopes:
            hist = sns.histplot(data=self.container_measurements["EDITED"][filename][isotope]*10**(-6), multiple="stack", ax=self.ax)
            #self.lines["raw"][isotope] = ln
        self.ax.grid(True)
        #self.ax.set_yscale("log")
        #self.ax.set_xlim(left=0, right=x_max)
        #self.ax.set_xticks(np.arange(0, x_max, 10))
        #self.ax.set_ylim(top=1.5*y_max)
        self.ax.set_axisbelow(True)
        #self.ax.set_xlabel("Time (s)", labelpad=0.5)
        #self.ax.set_ylabel("Signal (cps)", labelpad=0.5)

        self.fig.subplots_adjust(bottom=0.125, top=0.975, left=0.075, right=0.975)

        legend = self.ax.legend(fontsize="x-small", framealpha=1.0, edgecolor="white",
                                bbox_to_anchor=(0.125, 0.015), loc=3, borderaxespad=0,
                                bbox_transform=plt.gcf().transFigure, ncol=int(len(self.list_isotopes)/2 + 1),
                                facecolor="white")
        plt.rcParams["savefig.facecolor"] = "white"
        plt.rcParams["savefig.dpi"] = 300

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().grid(row=0, column=50, rowspan=38, columnspan=60, sticky="nesw")
        self.toolbarFrame = tk.Frame(master=self.parent)
        self.toolbarFrame.grid(row=38, column=50, rowspan=2, columnspan=60, sticky="w")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.config(background=self.green_light)
        self.toolbar._message_label.config(background=self.green_light)
        self.toolbar.winfo_children()[-2].config(background=self.green_light)

        #self.container_files[self.file_type][parts[-1]]["Time Signal Plot"] = [self.canvas, self.toolbarFrame]
        #self.container_files[self.file_type][parts[-1]]["Plot"] = True
        #self.container_diagrams[self.file_type][filename_short]["CANVAS"] = self.canvas
        #self.container_diagrams[self.file_type][filename_short]["TOOLBARFRAME"] = self.toolbarFrame
    #
    def save_settings(self):
        #
        print("container_helper:")
        print(self.container_helper["STD"])
        print(self.container_helper["SMPL"])
        print("container_files:")
        print(self.container_files["STD"])
        print(self.container_files["SMPL"])
        #
        save_file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        #
        ## STANDARD FILES
        save_file.write("STANDARD FILES (LONG)"+"\n")
        for file_std in self.list_std:
            filename_std_short = file_std.split("/")[-1]
            str_std = str(file_std)+";"+str(self.container_files["STD"][filename_std_short]["SRM"].get())+";"\
                      +str(self.container_files["STD"][filename_std_short]["IS"].get())+";"+str("BG")+";"
            for key, item in self.container_helper["STD"][filename_std_short]["BG"].items():
                str_std += str(key)+";"
                str_std += str(item["Times"])+";"+str(item["Positions"])+";"
            str_std += str("SIG") + ";"
            for key, item in self.container_helper["STD"][filename_std_short]["SIG"].items():
                str_std += str(key)+";"
                str_std += str(item["Times"])+";"+str(item["Positions"])+";"
            str_std += str("SPK") + ";"
            for isotope, item_isotope in self.container_helper["STD"][filename_std_short]["SPK"].items():
                str_std += str(isotope) + ";"
                for id_key, id_item in item_isotope.items():
                    str_std += str(id_key)+";"
                    str_std += str(id_item["Times"])+";"+str(id_item["Positions"])+";"
            str_std += "\n"
            save_file.write(str_std)
            # save_file.write(
            #     str(file_std)+";"+str(self.container_files["STD"][filename_std_short]["SRM"].get())+";"
            #     +str(self.container_files["STD"][filename_std_short]["IS"].get())+"\n")
        save_file.write("\n")
        #
        ## SAMPLE FILES
        save_file.write("SAMPLE FILES (LONG)"+"\n")
        if len(self.list_smpl) > 0:
            for file_smpl in self.list_smpl:
                filename_smpl_short = file_smpl.split("/")[-1]
                str_smpl = str(file_smpl) + ";" + str(self.container_files["SMPL"][filename_smpl_short]["SRM"].get()) \
                           + ";" + str(self.container_files["SMPL"][filename_smpl_short]["IS"].get()) + ";" + str("BG") \
                           + ";"
                for key, item in self.container_helper["SMPL"][filename_smpl_short]["BG"].items():
                    str_smpl += str(key) + ";"
                    str_smpl += str(item["Times"]) + ";" + str(item["Positions"]) + ";"
                str_smpl += str("SIG") + ";"
                for key, item in self.container_helper["SMPL"][filename_smpl_short]["SIG"].items():
                    str_smpl += str(key) + ";"
                    str_smpl += str(item["Times"]) + ";" + str(item["Positions"]) + ";"
                str_smpl += str("SPK") + ";"
                for isotope, item_isotope in self.container_helper["SMPL"][filename_smpl_short]["SPK"].items():
                    str_smpl += str(isotope) + ";"
                    for id_key, id_item in item_isotope.items():
                        str_smpl += str(id_key) + ";"
                        str_smpl += str(id_item["Times"]) + ";" + str(id_item["Positions"]) + ";"
                str_smpl += "\n"
                save_file.write(str_smpl)
                # save_file.write(
                #     str(file_smpl)+";"+str(self.container_files["SMPL"][filename_smpl_short]["IS"].get())+";"
                #     +str(self.container_files["SMPL"][filename_smpl_short]["IS Concentration"].get())+"\n")
        else:
            save_file.write(str(None)+"\n")
        save_file.write("\n")
        #
        ## ISOTOPES
        save_file.write("ISOTOPES" + "\n")
        for key, item in self.container_files["SRM"].items():
            save_file.write(str(key)+";"+str(item.get())+"\n")
        save_file.write("\n")
        #
        ## SETTINGS
        save_file.write("SETTINGS" + "\n")
        save_file.write(str("Mineral") + ";" + str(self.container_var["mineral"].get()) + "\n")
        save_file.write(str("Default IS STD") + ";" + str(self.container_var["IS"]["Default STD"].get()) + "\n")
        save_file.write(str("Default IS SMPL") + ";" + str(self.container_var["IS"]["Default SMPL"].get()) + "\n")
        save_file.write(str("Default BG Start")+";"+str(self.container_var["settings"]["Time BG Start"].get())+"\n")
        save_file.write(str("Default BG End")+";"+str(self.container_var["settings"]["Time BG End"].get())+"\n")
        save_file.write(str("Default SIG Start")+";"+str(self.container_var["settings"]["Time SIG Start"].get())+"\n")
        save_file.write(str("Default SIG End")+";"+str(self.container_var["settings"]["Time SIG End"].get())+"\n")
        save_file.write(str("Author")+";"+str(self.container_var["settings"]["Author"].get())+"\n")
        save_file.write(str("Source ID")+";"+str(self.container_var["settings"]["Source ID"].get())+"\n")
        save_file.write("\n")
        #
        ## END
        save_file.write("END")
        #
        save_file.close()
    #
    def load_settings(self):
        filename = filedialog.askopenfilename()
        #
        try:
            file_loaded = open(str(filename), "r")
            loaded_lines = file_loaded.readlines()
            #
            n_settings = 0
            index = 0
            strings = ["STANDARD FILES (LONG)", "SAMPLE FILES (LONG)", "ISOTOPES", "SETTINGS", "END"]
            index_container = {}
            while n_settings < len(strings):
                index_container[strings[n_settings]] = 0
                index = 0
                flag = 0
                for line in open(str(filename), "r"):
                    if strings[n_settings] in line:
                        flag = 1
                        break
                    else:
                        index += 1
                #
                if flag == 0:
                    pass
                else:
                    index_container[strings[n_settings]] += index
                    n_settings += 1
            #
            ## STANDARD FILES (STD)
            for i in range(index_container["STANDARD FILES (LONG)"]+1, index_container["SAMPLE FILES (LONG)"]-1):
                line_std = str(loaded_lines[i].strip())
                splitted_std = line_std.split(";")
                filename_std = str(splitted_std[0])
                filename_std_short = filename_std.split("/")[-1]
                srm_std = str(splitted_std[1])
                is_std = str(splitted_std[2])
                #
                self.list_std.append(filename_std)
                self.lb_std.insert(tk.END, str(filename_std_short))
                self.container_var["SRM"][filename_std] = tk.StringVar()
                self.container_var["SRM"][filename_std].set(srm_std)
                self.container_var["STD"][filename_std] = {}
                self.container_var["STD"][filename_std]["IS"] = tk.StringVar()
                self.container_var["STD"][filename_std]["IS"].set(is_std)
            #
            ## SAMPLE FILES (SMPL)
            for i in range(index_container["SAMPLE FILES (LONG)"]+1, index_container["ISOTOPES"]-1):
                line_smpl = str(loaded_lines[i].strip())
                splitted_smpl = line_smpl.split(";")
                filename_smpl = str(splitted_smpl[0])
                filename_smpl_short = filename_smpl.split("/")[-1]
                is_smpl = str(splitted_smpl[1])
                is_conc_smpl = str(splitted_smpl[2])
                #
                self.list_smpl.append(filename_smpl)
                self.lb_smpl.insert(tk.END, str(filename_smpl_short))
                self.container_var["SMPL"][filename_smpl] = {}
                self.container_var["SMPL"][filename_smpl]["IS"] = tk.StringVar()
                self.container_var["SMPL"][filename_smpl]["IS"].set(is_smpl)
            #
            ## ISOTOPES (ISO)
            for i in range(index_container["ISOTOPES"]+1, index_container["SETTINGS"]-1):
                line_iso = str(loaded_lines[i].strip())
                splitted_iso = line_iso.split(";")
                isotope = str(splitted_iso[0])
                srm_iso = str(splitted_iso[1])
                #
                self.list_isotopes.append(isotope)
            #
            ## SETTINGS
            for i in range(index_container["SETTINGS"] + 1, index_container["END"] - 1):
                line_setup = str(loaded_lines[i].strip())
                splitted_setup = line_setup.split(";")
                if splitted_setup[0] == "Mineral":
                    self.container_var["mineral"].set(splitted_setup[1])
                elif splitted_setup[0] == "Default IS STD":
                    self.container_var["IS"]["Default STD"].set(splitted_setup[1])
                elif splitted_setup[0] == "Default IS SMPL":
                    self.container_var["IS"]["Default SMPL"].set(splitted_setup[1])
                elif splitted_setup[0] == "Default BG Start":
                    self.container_var["settings"]["Time BG Start"].set(splitted_setup[1])
                    self.container_settings["MA"]["Start BG"].set(splitted_setup[1])
                elif splitted_setup[0] == "Default BG End":
                    self.container_var["settings"]["Time BG End"].set(splitted_setup[1])
                    self.container_settings["MA"]["End BG"].set(splitted_setup[1])
                elif splitted_setup[0] == "Default SIG Start":
                    self.container_var["settings"]["Time SIG Start"].set(splitted_setup[1])
                    self.container_settings["MA"]["Start SIG"].set(splitted_setup[1])
                elif splitted_setup[0] == "Default SIG End":
                    self.container_var["settings"]["Time SIG End"].set(splitted_setup[1])
                    self.container_settings["MA"]["End SIG"].set(splitted_setup[1])
                elif splitted_setup[0] == "Author":
                    self.container_var["settings"]["Author"].set(splitted_setup[1])
                elif splitted_setup[0] == "Source ID":
                    self.container_var["settings"]["Source ID"].set(splitted_setup[1])
            #
            file_loaded.close()
            self.file_loaded = True
        #
        except FileNotFoundError:
            pass
    #
    def restart_pysills(self):
        self.parent.destroy()
        root = tk.Tk()
        PySILLS(root)
        root.mainloop()
    #
    def change_id_file(self, var_id, filename, filetype):
        parts = filename.split("/")
        self.container_var[filetype][filename]["ID"].set(var_id)
        self.container_files[filetype][parts[-1]]["ID"].set(var_id)
    #
    def set_integration_window(self, filename_short, var_key, event):
        if self.container_var["plotting"][filename_short]["RB"][0].get() == 0:
            self.container_var["plotting"][filename_short]["Entry"]["Start"].set("Please set signal category!")
            self.container_var["plotting"][filename_short]["Entry"]["End"].set("Please set signal category!")
        else:
            if var_key == "Start":
                if len(self.container_helper["positions"][filename_short]) == 2 and len(self.container_helper["indices"][filename_short]) == 2:
                    self.container_helper["positions"][filename_short].clear()
                    self.container_helper["indices"][filename_short].clear()
                #
                time_start = float(self.container_var["plotting"][filename_short]["Entry"]["Start"].get())
                time_nearest = min(self.times, key=lambda x: abs(x - time_start))
                #
                self.container_helper["positions"][filename_short].append(time_nearest)
                self.container_helper["indices"][filename_short].append(self.times[self.times == time_nearest].index[0])
                self.container_var["plotting"][filename_short]["Entry"]["Start"].set(time_nearest)
            elif var_key == "End":
                time_end = float(self.container_var["plotting"][filename_short]["Entry"]["End"].get())
                time_nearest = min(self.times, key=lambda x: abs(x - time_end))
                #
                self.container_helper["positions"][filename_short].append(time_nearest)
                self.container_helper["indices"][filename_short].append(self.times[self.times == time_nearest].index[0])
                self.container_var["plotting"][filename_short]["Entry"]["End"].set(time_nearest)
            #
            if self.container_var["plotting"][filename_short]["RB"][0].get() == 1 and len(self.container_helper["positions"][filename_short]) == 2: # Background
                #
                if self.file_type == "STD":
                    if len(self.container_helper["positions"]["BG STD"][filename_short]) > 0:
                        self.bg_id = self.container_helper["positions"]["BG STD"][filename_short][-1][4]
                elif self.file_type == "SMPL":
                    if len(self.container_helper["positions"]["BG SMPL"][filename_short]) > 0:
                        self.bg_id = self.container_helper["positions"]["BG SMPL"][filename_short][-1][4]
                #
                self.bg_id += 1
                self.bg_idlist.append(self.bg_id)
                self.container_helper["limits BG"][self.file]["ID"].append(self.bg_id)
                self.container_helper["limits BG"][self.file]["type"].append("custom")
                self.container_helper["positions"]["BG"][filename_short].append(
                    [round(self.container_helper["positions"][filename_short][0], 4),
                     round(self.container_helper["positions"][filename_short][1], 4)])
                self.container_listboxes[self.file_type][filename_short]["BG"][0].insert(
                    tk.END, "BG" + str(self.bg_id) + " [" + str(
                        self.container_helper["positions"][filename_short][0]) + "-" +
                            str(self.container_helper["positions"][filename_short][1]) + "]")
                #
                box_bg = self.ax.axvspan(self.container_helper["positions"][filename_short][0],
                                         self.container_helper["positions"][filename_short][1], alpha=0.25,
                                         color=self.blue_dark)
                box_bg_ratio = self.ax_ratio.axvspan(self.container_helper["positions"][filename_short][0],
                                         self.container_helper["positions"][filename_short][1], alpha=0.25,
                                         color=self.blue_dark)
                #
                self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                self.container_helper["limits BG Ratio"][self.file][str(self.bg_id)] = box_bg_ratio
                self.canvas.draw()
                self.indices_bg = self.container_helper["indices"][filename_short]
                #
                self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id] = {}
                self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id]["Times"] = [
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id]["Positions"] = [
                    self.container_helper["indices"][filename_short][0],
                    self.container_helper["indices"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["BG"][self.bg_id]["Box"] = box_bg
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename_short]["BG"][self.bg_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": [box_bg, box_bg_ratio]}
                    self.container_helper["positions"]["BG STD"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.bg_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename_short]["BG"][self.bg_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": [box_bg, box_bg_ratio]}
                    self.container_helper["positions"]["BG SMPL"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.bg_id])
                #
                self.container_var["plotting"][filename_short]["RB"][0].set(0)
                self.container_helper["positions"][filename_short].clear()
                self.container_helper["indices"][filename_short].clear()
                self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                #
            elif self.container_var["plotting"][filename_short]["RB"][0].get() == 4 and len(self.container_helper["positions"][filename_short]) == 2: # Matrix
                #
                if self.file_type == "STD":
                    if len(self.container_helper["positions"]["MAT STD"][filename_short]) > 0:
                        self.mat_id = self.container_helper["positions"]["MAT STD"][filename_short][-1][4]
                elif self.file_type == "SMPL":
                    if len(self.container_helper["positions"]["MAT SMPL"][filename_short]) > 0:
                        self.mat_id = self.container_helper["positions"]["MAT SMPL"][filename_short][-1][4]
                #
                self.mat_id += 1
                self.mat_idlist.append(self.mat_id)
                self.container_helper["limits MAT"][self.file]["ID"].append(self.mat_id)
                self.container_helper["limits MAT"][self.file]["type"].append("custom")
                self.container_helper["positions"]["MAT"][filename_short].append(
                    [round(self.container_helper["positions"][filename_short][0], 4),
                     round(self.container_helper["positions"][filename_short][1], 4)])
                self.container_listboxes[self.file_type][filename_short]["MAT"][0].insert(
                    tk.END, "MAT" + str(self.mat_id) + " [" + str(
                        self.container_helper["positions"][filename_short][0]) + "-" +
                            str(self.container_helper["positions"][filename_short][1]) + "]")
                box_mat = self.ax.axvspan(
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1], alpha=0.25, color=self.brown_dark)
                self.container_helper["limits MAT"][self.file][str(self.mat_id)] = box_mat
                self.canvas.draw()
                self.indices_mat = self.container_helper["indices"][filename_short]
                #
                self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id] = {}
                self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id]["Times"] = [
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id]["Positions"] = [
                    self.container_helper["indices"][filename_short][0],
                    self.container_helper["indices"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["MAT"][self.mat_id]["Box"] = box_mat
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename_short]["MAT"][self.mat_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": box_mat}
                    self.container_helper["positions"]["MAT STD"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.mat_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename_short]["MAT"][self.mat_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": box_mat}
                    self.container_helper["positions"]["MAT SMPL"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.mat_id])
                #
                self.container_var["plotting"][filename_short]["RB"][0].set(0)
                self.container_helper["positions"][filename_short].clear()
                self.container_helper["indices"][filename_short].clear()
                self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                #
            elif self.container_var["plotting"][filename_short]["RB"][0].get() == 5 and len(self.container_helper["positions"][filename_short]) == 2: # Inclusion
                #
                if self.file_type == "STD":
                    if len(self.container_helper["positions"]["INCL STD"][filename_short]) > 0:
                        self.incl_id = self.container_helper["positions"]["INCL STD"][filename_short][-1][4]
                elif self.file_type == "SMPL":
                    if len(self.container_helper["positions"]["INCL SMPL"][filename_short]) > 0:
                        self.incl_id = self.container_helper["positions"]["INCL SMPL"][filename_short][-1][4]
                self.incl_id += 1
                self.incl_idlist.append(self.incl_id)
                self.container_helper["limits INCL"][self.file]["ID"].append(self.incl_id)
                self.container_helper["limits INCL"][self.file]["type"].append("custom")
                self.container_helper["positions"]["INCL"][filename_short].append(
                    [round(self.container_helper["positions"][filename_short][0], 4),
                     round(self.container_helper["positions"][filename_short][1], 4)])
                self.container_listboxes[self.file_type][filename_short]["INCL"][0].insert(
                    tk.END, "INCL" + str(self.incl_id) + " [" + str(
                        self.container_helper["positions"][filename_short][0]) + "-"
                            + str(self.container_helper["positions"][filename_short][1]) + "]")
                #
                box_incl = self.ax.axvspan(
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1], alpha=0.25, color=self.slate_grey_dark)
                self.container_helper["limits INCL"][self.file][str(self.incl_id)] = box_incl
                self.canvas.draw()
                #
                self.indices_incl = self.container_helper["indices"][filename_short]
                #
                self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id] = {}
                self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id]["Times"] = [
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id][
                    "Positions"] = [
                    self.container_helper["indices"][filename_short][0],
                    self.container_helper["indices"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["INCL"][self.incl_id][
                    "Box"] = box_incl
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename_short]["INCL"][self.incl_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": box_incl}
                    self.container_helper["positions"]["INCL STD"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.incl_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename_short]["INCL"][self.incl_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": box_incl}
                    self.container_helper["positions"]["INCL SMPL"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.incl_id])
                #
                self.container_var["plotting"][filename_short]["RB"][0].set(0)
                self.container_helper["positions"][filename_short].clear()
                self.container_helper["indices"][filename_short].clear()
                self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                #
            elif self.container_var["plotting"][filename_short]["RB"][0].get() == 2 and len(self.container_helper["positions"][filename_short]) == 2: # Signal
                #
                if self.file_type == "STD":
                    if len(self.container_helper["positions"]["SIG STD"][filename_short]) > 0:
                        self.sig_id = self.container_helper["positions"]["SIG STD"][filename_short][-1][4]
                elif self.file_type == "SMPL":
                    if len(self.container_helper["positions"]["SIG SMPL"][filename_short]) > 0:
                        self.sig_id = self.container_helper["positions"]["SIG SMPL"][filename_short][-1][4]
                #
                self.sig_id += 1
                self.sig_idlist.append(self.sig_id)
                self.container_helper["limits SIG"][self.file]["ID"].append(self.sig_id)
                self.container_helper["limits SIG"][self.file]["type"].append("custom")
                self.container_helper["positions"]["SIG"][filename_short].append(
                    [round(self.container_helper["positions"][filename_short][0], 4),
                     round(self.container_helper["positions"][filename_short][1], 4)])
                self.container_listboxes[self.file_type][filename_short]["SIG"][0].insert(
                    tk.END, "SIG" + str(self.sig_id) + " [" + str(
                        self.container_helper["positions"][filename_short][0]) + "-" +
                            str(self.container_helper["positions"][filename_short][1]) + "]")
                #
                box_sig = self.ax.axvspan(
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1], alpha=0.25, color=self.brown_dark)
                box_sig_ratio = self.ax_ratio.axvspan(
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1], alpha=0.25, color=self.brown_dark)
                #
                self.container_helper["limits SIG"][self.file][str(self.sig_id)] = box_sig
                self.container_helper["limits SIG Ratio"][self.file][str(self.sig_id)] = box_sig_ratio
                self.canvas.draw()
                self.indices_sig = self.container_helper["indices"][filename_short]
                #
                self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id] = {}
                self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id]["Times"] = [
                    self.container_helper["positions"][filename_short][0],
                    self.container_helper["positions"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id]["Positions"] = [
                    self.container_helper["indices"][filename_short][0],
                    self.container_helper["indices"][filename_short][1]]
                self.container_files[self.file_type][self.filename_short]["SIG"][self.sig_id]["Box"] = box_sig
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename_short]["SIG"][self.sig_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": [box_sig, box_sig_ratio]}
                    self.container_helper["positions"]["SIG STD"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.sig_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename_short]["SIG"][self.sig_id] = {
                        "Times": [self.container_helper["positions"][filename_short][0],
                                  self.container_helper["positions"][filename_short][1]],
                        "Positions": [self.container_helper["indices"][filename_short][0],
                                      self.container_helper["indices"][filename_short][1]],
                        "Object": [box_sig, box_sig_ratio]}
                    self.container_helper["positions"]["SIG SMPL"][filename_short].append(
                        [self.container_helper["positions"][filename_short][0],
                         self.container_helper["positions"][filename_short][1],
                         self.container_helper["indices"][filename_short][0],
                         self.container_helper["indices"][filename_short][1],
                         self.sig_id])
                #
                self.container_var["plotting"][filename_short]["RB"][0].set(0)
                self.container_helper["positions"][filename_short].clear()
                self.container_helper["indices"][filename_short].clear()
                self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                #
    #
    def change_id_default(self, var_id, filetype):
        if filetype == "STD":
            for file_std in self.list_std:
                parts = file_std.split("/")
                self.container_var["STD"][file_std]["ID"].set(var_id)
                self.container_files["STD"][parts[-1]]["ID"].set(var_id)
        elif filetype == "SMPL":
            for file_smpl in self.list_smpl:
                parts = file_smpl.split("/")
                self.container_var["SMPL"][file_smpl]["ID"].set(var_id)
                self.container_files["SMPL"][parts[-1]]["ID"].set(var_id)
    #
    ####################
    ## DATA PROCESSING #
    ####################
    #
    def open_csv(self, datatype):
        if datatype == "STD":
            if "Default_STD_01.csv" in self.list_std:
                self.list_std.clear()
            var_list = self.list_std
            var_listbox = self.lb_std
        elif datatype == "SMPL":
            if "Default_SMPL_01.csv" in self.list_smpl:
                self.list_smpl.clear()
            var_list = self.list_smpl
            var_listbox = self.lb_smpl
        #
        filename = filedialog.askopenfilenames(
            parent=self.parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
            initialdir=os.getcwd())
        for i in filename:
            if i not in var_list:
                var_list.append(i)
                file_parts = i.split("/")
                var_listbox.insert(tk.END, file_parts[-1])

    #
    def import_concentration_data(self):
        filename = filedialog.askopenfilenames(
            parent=self.parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")), initialdir=os.getcwd())
        df = pd.read_csv(filename[0], sep=";", header=0, engine="python")
        data_concentration = dict(zip(df.element, df.concentration))
        #
        self.container_var["isotopes"]["default"].set("Select IS")
        self.var_entr_09.set(0.0)
        if len(self.container_var["mineralchemistry"]) > 0:
            self.container_var["mineralchemistry"].clear()
        self.container_var["mineralchemistry"].extend(list(data_concentration.keys()))
        self.container_var["mineralchemistry"].sort()
        #
        possible_is = []
        #self.mineral_chem = {}
        self.mineral_chem["Unknown"] = {}
        for element in self.container_var["mineralchemistry"]:
            for isotope in self.list_isotopes:
                key = re.search("(\D+)(\d+)", isotope)
                if element == key.group(1):
                    possible_is.append(isotope)
                    self.mineral_chem["Unknown"][element] = data_concentration[element]
        #
        self.opt_is_std_def["menu"].delete(0, "end")
        self.opt_is_smpl_def["menu"].delete(0, "end")
        #
        for index, isotope in enumerate(possible_is):
            for file in self.list_std:
                if index == 0:
                    self.container_optionmenu["STD"][file]["menu"].delete(0, "end")
                self.container_optionmenu["STD"][file]["menu"].add_command(
                    label=isotope, command=lambda element=isotope, file=file: self.change_std_is(element, file))
                if self.file_loaded is False:
                    self.container_var["STD"][file]["IS"].set("Select IS")
            for file in self.list_smpl:
                if index == 0:
                    self.container_optionmenu["SMPL"][file]["menu"].delete(0, "end")
                self.container_optionmenu["SMPL"][file]["menu"].add_command(
                    label=isotope, command=lambda element=isotope, file=file,
                                                  mineral=self.container_var["mineral"].get():
                    self.change_smpl_is(element, file, mineral))
                if self.file_loaded is False:
                    self.container_var["SMPL"][file]["IS"].set("Select IS")
            #
            self.opt_is_std_def["menu"].add_command(
                label=isotope, command=lambda element=isotope, mineral="Unknown":
                self.change_std_is_default(element, mineral))
            self.opt_is_smpl_def["menu"].add_command(
                label=isotope, command=lambda element=isotope, mineral="Unknown":
                self.change_smpl_is_default(element, mineral))
    #
    ##############################
    ## FLUID INCLUSION ANALYSIS ##
    ##############################
    #
    #
    def sub_fluidinclusions_settings(self):
        #
        ## Cleaning
        if self.demo_view == False:
            categories = ["SRM", "plotting", "PSE", "ma_setting", "ma_datareduction", "ma_dataexploration",
                          "fi_datareduction"]
        else:
            categories = ["SRM", "plotting", "PSE", "ma_setting", "ma_datareduction", "ma_dataexploration",
                          "fi_datareduction"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Radiobutton"]) > 0:
                for item in self.container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Checkbox"]) > 0:
                for item in self.container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Listbox"]) > 0:
                for item in self.container_elements[category]["Listbox"]:
                    item.grid_remove()
        try:
            self.canvas.get_tk_widget().grid_forget()
            self.toolbarFrame.grid_forget()
        except AttributeError:
            pass
        try:
            self.canvas_drift.get_tk_widget().grid_forget()
            self.toolbarFrame_drift.grid_forget()
        except AttributeError:
            pass
        #
        ## Reconstruction
        if self.demo_view == False:
            try:
                for lbl_item in self.container_elements["fi_setting"]["Label"]:
                    lbl_item.grid()
                for btn_item in self.container_elements["fi_setting"]["Button"]:
                    btn_item.grid()
                for rb_item in self.container_elements["fi_setting"]["Radiobutton"]:
                    rb_item.grid()
                for optmen_item in self.container_elements["fi_setting"]["Option Menu"]:
                    optmen_item.grid()
                for entr_item in self.container_elements["fi_setting"]["Entry"]:
                    entr_item.grid()
                for entr_item in self.container_elements["fi_setting"]["Frame"]:
                    entr_item.grid()
            except:
                print("Error! Reconstruction failed!")
        else:
            for category in ["Label", "Button", "Option Menu", "Entry", "Frame"]:
                self.container_elements["fi_setting"][category].clear()
            self.list_isotopes.clear()
            del self.palette_complete
            del self.isotope_colors
            del self.times
            self.container_files["SRM"].clear()
            self.container_files["STD"].clear()
            self.container_files["SMPL"].clear()
            self.container_helper["STD"].clear()
            self.container_helper["SMPL"].clear()
            self.container_lists["STD"]["Long"].clear()
            self.container_lists["STD"]["Short"].clear()
            self.container_lists["SMPL"]["Long"].clear()
            self.container_lists["SMPL"]["Short"].clear()
            #
            list_std = ["Default_STD_01.csv", "Default_STD_02.csv", "Default_STD_03.csv", "Default_STD_04.csv",
                        "Default_STD_05.csv", "Default_STD_06.csv"]
            for item in list_std:
                self.container_var["STD"].pop(item, None)
                self.container_helper["positions"]["SPK"].pop(item, None)
            list_smpl = ["Default_SMPL_01.csv", "Default_SMPL_02.csv", "Default_SMPL_03.csv", "Default_SMPL_04.csv",
                         "Default_SMPL_05.csv", "Default_SMPL_06.csv", "Default_SMPL_07.csv", "Default_SMPL_08.csv",
                         "Default_SMPL_09.csv", "Default_SMPL_10.csv"]
            for item in list_smpl:
                self.container_var["SMPL"].pop(item, None)
                self.container_helper["positions"]["SPK"].pop(item, None)
            self.window_created["fi_setting"] = False
            self.demo_view = False
        #
        try:
            dataset_exmpl = Data(filename=self.list_std[0])
            df_exmpl = dataset_exmpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            self.times = df_exmpl.iloc[:, 0]
            self.list_isotopes = list(df_exmpl.columns.values)
            self.list_isotopes.pop(0)
            self.container_lists["ISOTOPES"] = self.list_isotopes
            self.palette_complete = sns.color_palette("nipy_spectral", n_colors=len(self.list_isotopes)).as_hex()
            if bool(self.container_files["SRM"]) == False:
                self.isotope_colors = {}
                for index, isotope in enumerate(self.list_isotopes):
                    self.container_files["SRM"][isotope] = tk.StringVar()
                    self.isotope_colors[isotope] = self.palette_complete[index]
        except:
            #
            path = os.getcwd()
            parent = os.path.dirname(path)
            fi_demo_files = {"ALL": [], "STD": [], "SMPL": []}
            demo_files = os.listdir(path=parent + str("/demo_files/"))
            for file in demo_files:
                if file.startswith("demo_fi"):
                    path_complete = os.path.join(parent+str("/demo_files/"), file)
                    path_raw = pathlib.PureWindowsPath(path_complete)
                    fi_demo_files["ALL"].append(str(path_raw.as_posix()))
            fi_demo_files["ALL"].sort()
            # fi_demo_files["STD"].extend(fi_demo_files["ALL"][:2])
            # fi_demo_files["STD"].extend(fi_demo_files["ALL"][-2:])
            # fi_demo_files["SMPL"].extend(fi_demo_files["ALL"][2:-2])
            fi_demo_files["STD"].extend(fi_demo_files["ALL"][:1])
            fi_demo_files["STD"].extend(fi_demo_files["ALL"][-1:])
            fi_demo_files["SMPL"].extend(fi_demo_files["ALL"][2:4])
            #
            self.list_std = fi_demo_files["STD"]
            self.list_smpl = fi_demo_files["SMPL"]
            #
            for file_std in self.list_std:
                file_parts = file_std.split("/")
                self.lb_std.insert(tk.END, file_parts[-1])
            for file_smpl in self.list_smpl:
                file_parts = file_smpl.split("/")
                self.lb_smpl.insert(tk.END, file_parts[-1])
            #
            dataset_exmpl = Data(filename=self.list_std[0])
            df_exmpl = dataset_exmpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            self.times = df_exmpl.iloc[:, 0]
            self.list_isotopes = list(df_exmpl.columns.values)
            self.list_isotopes.pop(0)
            self.container_lists["ISOTOPES"] = self.list_isotopes
            self.palette_complete = sns.color_palette("nipy_spectral", n_colors=len(self.list_isotopes)).as_hex()
            if bool(self.container_files["SRM"]) == False:
                self.isotope_colors = {}
                for index, isotope in enumerate(self.list_isotopes):
                    self.container_files["SRM"][isotope] = tk.StringVar()
                    self.isotope_colors[isotope] = self.palette_complete[index]
            #
            self.demo_view = False
        #
        ## Labels
        start_col_std = 21
        start_col_smpl = 51
        start_col_iso = 72
        start_row_settings_01 = 20
        #
        if len(self.container_elements["fi_setting"]["Label"]) == 0:
            lbl_fi_setting_01 = SE(
                parent=self.parent, row_id=0, column_id=start_col_std, n_rows=1, n_columns=29, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Standard Files)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_02 = SE(
                parent=self.parent, row_id=0, column_id=start_col_smpl, n_rows=1, n_columns=20, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Sample Files)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_03 = SE(
                parent=self.parent, row_id=0, column_id=start_col_iso, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Isotopes)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_18 = SE(
                parent=self.parent, row_id=start_row_settings_01+3, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Standard Reference Material (SRM)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_19 = SE(
                parent=self.parent, row_id=start_row_settings_01+4, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_20 = SE(
                parent=self.parent, row_id=start_row_settings_01+5, column_id=21, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Isotopes", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_21 = SE(
                parent=self.parent, row_id=start_row_settings_01+11, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Quantification Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_quantification_06 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 13, column_id=21, n_rows=2, n_columns=8,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Quantification Method", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_04 = SE(
                parent=self.parent, row_id=start_row_settings_01+3, column_id=38, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Default Time Windows (Background)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_05 = SE(
                parent=self.parent, row_id=start_row_settings_01+4, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_06 = SE(
                parent=self.parent, row_id=start_row_settings_01+5, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_07 = SE(
                parent=self.parent, row_id=start_row_settings_01+6, column_id=38, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Default Time Windows (Matrix)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_08 = SE(
                parent=self.parent, row_id=start_row_settings_01+7, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_09 = SE(
                parent=self.parent, row_id=start_row_settings_01+8, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_10 = SE(
                parent=self.parent, row_id=start_row_settings_01+12, column_id=38, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Spike Elimination)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_11 = SE(
                parent=self.parent, row_id=start_row_settings_01+13, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Deviation", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_12 = SE(
                parent=self.parent, row_id=start_row_settings_01+14, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Threshold", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_13 = SE(
                parent=self.parent, row_id=start_row_settings_01+15, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE,fontsize="sans 10 bold")
            lbl_fi_setting_14 = SE(
                parent=self.parent, row_id=start_row_settings_01+16, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_15 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 17, column_id=38, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Settings (Additional Information)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_16 = SE(
                parent=self.parent, row_id=start_row_settings_01+18, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Author", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_17 = SE(
                parent=self.parent, row_id=start_row_settings_01+19, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Source ID", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_25 = SE(
                parent=self.parent, row_id=0, column_id=start_col_iso+12, n_rows=1, n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Ionization", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_26 = SE(
                parent=self.parent, row_id=start_row_settings_01+15, column_id=21, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Assemblage Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_27 = SE(
                parent=self.parent, row_id=start_row_settings_01+16, column_id=21, n_rows=1, n_columns=8,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_28 = SE(
                parent=self.parent, row_id=start_row_settings_01+17, column_id=21, n_rows=1, n_columns=8,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_29 = SE(
                parent=self.parent, row_id=start_row_settings_01+9, column_id=38, n_rows=1, n_columns=17, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Default Time Windows (Inclusion)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_30 = SE(
                parent=self.parent, row_id=start_row_settings_01+10, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_fi_setting_31 = SE(
                parent=self.parent, row_id=start_row_settings_01+11, column_id=38, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_filler = SE(
                parent=self.parent, row_id=start_row_settings_01 + 18, column_id=21, n_rows=2, n_columns=17,
                fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_32 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 6, column_id=21, n_rows=1, n_columns=17,
                fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Host Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_33 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 18, column_id=21, n_rows=1, n_columns=17,
                fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Dwell Times Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_34 = SE(
                parent=self.parent, row_id=start_row_settings_01 + 19, column_id=21, n_rows=1, n_columns=8,
                fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text=" Isotope Dwell Times", relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            self.container_elements["fi_setting"]["Label"].extend(
                [lbl_fi_setting_01, lbl_fi_setting_02, lbl_fi_setting_03, lbl_fi_setting_04, lbl_fi_setting_05,
                 lbl_fi_setting_06, lbl_fi_setting_07, lbl_fi_setting_08, lbl_fi_setting_09, lbl_fi_setting_10,
                 lbl_fi_setting_11, lbl_fi_setting_12, lbl_fi_setting_13, lbl_fi_setting_14, lbl_fi_setting_15,
                 lbl_fi_setting_16, lbl_fi_setting_17, lbl_fi_setting_18, lbl_fi_setting_19, lbl_fi_setting_20,
                 lbl_fi_setting_21, lbl_fi_setting_25, lbl_fi_setting_26, lbl_fi_setting_27, lbl_fi_setting_28,
                 lbl_fi_setting_29, lbl_fi_setting_30, lbl_fi_setting_31, lbl_filler, lbl_quantification_06, lbl_32,
                 lbl_33, lbl_34])
            #
            # Ionization Energy
            self.var_entr_10 = tk.StringVar()
            self.container_var["fi_setting"]["Ionization Energy"] = self.var_entr_10
            entr_10 = SE(
                parent=self.parent, row_id=int(1+ len(self.list_isotopes)), column_id=start_col_iso+12, n_rows=1,
                n_columns=5, fg=self.green_light,
                bg=self.green_dark).create_simple_entry(var=self.var_entr_10, text_default="15.760")
            #
            gui_categories = ["Label", "Button", "Option Menu", "Entry", "Frame", "Radiobutton", "Checkbox", "Listbox",
                              "Canvas"]
            #
            if self.window_created["fi_setting"] == False:
                ##################
                # STANDARD FILES #
                ##################
                if len(self.list_std) > 0:
                    for index, file in enumerate(self.list_std):
                        #
                        parts = file.split("/")
                        filename_short = parts[-1]
                        #
                        self.container_gui[filename_short] = {}
                        for gui_category in gui_categories:
                            self.container_gui[filename_short][gui_category] = {}
                            self.container_gui[filename_short][gui_category]["General"] = []
                            self.container_gui[filename_short][gui_category]["Specific"] = []
                        #
                        self.container_helper["limits BG"][file] = {}
                        self.container_helper["limits BG"][file]["ID"] = []
                        self.container_helper["limits BG"][file]["type"] = []
                        self.container_helper["limits MAT"][file] = {}
                        self.container_helper["limits MAT"][file]["ID"] = []
                        self.container_helper["limits MAT"][file]["type"] = []
                        self.container_helper["limits INCL"][file] = {}
                        self.container_helper["limits INCL"][file]["ID"] = []
                        self.container_helper["limits INCL"][file]["type"] = []
                        self.container_helper["limits SPK"][file] = {}
                        self.container_helper["limits SPK"][file]["ID"] = []
                        self.container_helper["limits SPK"][file]["type"] = []
                        self.container_helper["limits SPK"][file]["info"] = []
                        self.container_helper["positions"]["SPK"][filename_short] = []
                        self.spikes_isotopes["STD"][filename_short] = {}
                        if self.file_loaded is False:
                            self.container_var["STD"][file] = {}
                            self.container_var["STD"][file]["IS"] = tk.StringVar()
                            self.container_var["STD"][file]["IS"].set("Select IS")
                            self.container_var["STD"][file]["ID"] = tk.StringVar()
                            self.container_var["STD"][file]["ID"].set("A")
                        #
                        categories = ["FIG", "AX", "CANVAS", "TOOLBARFRAME"]
                        self.container_diagrams["STD"][filename_short] = {}
                        self.container_listboxes["STD"][filename_short] = {}
                        self.diagrams_setup["STD"][filename_short] = {}
                        for category in categories:
                            self.container_diagrams["STD"][filename_short][category] = None
                            self.diagrams_setup["STD"][filename_short][category] = None
                        categories = ["Time Signal Raw", "Time Signal Smoothed", "Histogram", "Scatter"]
                        for category in categories:
                            self.diagrams_setup["STD"][filename_short][category] = {}
                        categories = ["BG", "MAT", "INCL", "SPK", "ISORAT"]
                        for category in categories:
                            self.container_listboxes["STD"][filename_short][category] = None
                        #
                        self.container_report[filename_short] = {}
                        self.container_report[filename_short]["Mean"] = {}
                        self.container_report[filename_short]["Error"] = {}
                        categories_02 = ["Intensity Ratio", "Sensitivity", "Concentration", "RSF", "LOD"]
                        for category_02 in categories_02:
                            self.container_report[filename_short]["Mean"][category_02] = {}
                            self.container_report[filename_short]["Error"][category_02] = {}
                            self.container_report[filename_short]["Mean"][category_02]["filename"] = filename_short
                            self.container_report[filename_short]["Error"][category_02]["filename"] = filename_short
                        #
                        if len(self.container_lists["STD"]["Long"]) < len(self.list_std):
                            self.container_lists["STD"]["Long"].append(file)
                            self.container_lists["STD"]["Short"].append(filename_short)
                            self.container_helper["STD"][filename_short] = {}
                            self.container_helper["STD"][filename_short]["BG"] = {}
                            self.container_helper["STD"][filename_short]["MAT"] = {}
                            self.container_helper["STD"][filename_short]["INCL"] = {}
                            self.container_helper["STD"][filename_short]["SPK"] = {}
                        if filename_short not in self.container_files["STD"]:
                            self.container_files["STD"][filename_short] = {}
                            self.container_files["STD"][filename_short]["SRM"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["IS"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["IS Concentration"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["ID"] = tk.StringVar()
                            self.container_files["STD"][filename_short]["ID"].set("A")
                            self.container_files["STD"][filename_short]["Plot"] = False
                            self.container_files["STD"][filename_short]["Time Signal Plot"] = None
                            self.container_files["STD"][filename_short]["Histogram Plot"] = None
                            self.container_files["STD"][filename_short]["Scatter Plot"] = None
                            self.container_files["STD"][filename_short]["BG"] = {}
                            self.container_files["STD"][filename_short]["MAT"] = {}
                            self.container_files["STD"][filename_short]["INCL"] = {}
                            self.container_files["STD"][filename_short]["SPK"] = {}
                            #
                            self.container_var["plotting"][filename_short] = {}
                            self.container_var["plotting"][filename_short]["Entry"] = {}
                            self.container_var["plotting"][filename_short]["Entry"]["Start"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                            self.container_var["plotting"][filename_short]["Entry"]["End"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                            self.container_var["plotting"][filename_short]["Checkboxes"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "BG"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "MAT"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "INCL"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "SPK"] = tk.IntVar()
                            #
                            self.container_helper["positions"]["BG STD"][filename_short] = []
                            self.container_helper["positions"]["MAT STD"][filename_short] = []
                            self.container_helper["positions"]["INCL STD"][filename_short] = []
                            self.container_helper["positions"]["SPK STD"][filename_short] = []
                            #
                        #
                        if file not in self.container_var["SRM"] and self.file_loaded is False:
                            self.container_var["SRM"][file] = tk.StringVar()
                            self.container_var["SRM"][file].set("Select SRM")
                        #
                        lbl_std = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std, n_rows=1, n_columns=8,
                            fg=self.green_light, bg=self.green_medium).create_simple_label(
                            text=filename_short, relief=tk.GROOVE, fontsize="sans 10 bold")
                        #
                        self.container_elements["fi_setting"]["Label"].append(lbl_std)
                        #
                        btn_fi_setting_std = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+25, n_rows=1, n_columns=3,
                            fg=self.green_dark, bg=self.green_medium).create_simple_button(
                            text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                            command=lambda filename=self.list_std[index]: self.sub_fluidinclusions_plotting(filename))
                        #
                        self.container_elements["fi_setting"]["Button"].append(btn_fi_setting_std)
                        #
                        frm_std = SE(parent=self.parent, row_id=1+index, column_id=start_col_std+28, n_rows=1,
                                     n_columns=1, fg=self.green_light, bg=self.sign_red).create_frame()
                        #
                        self.container_elements["fi_setting"]["Frame"].append(frm_std)
                        self.container_var["STD"][file]["Frame"] = frm_std
                        #
                        ## Option Menus
                        # Standard Reference Material
                        if self.container_var["SRM"][file].get() != "Select SRM":
                            var_text = self.container_var["SRM"][file].get()
                            self.container_files["STD"][filename_short]["SRM"].set(var_text)
                        else:
                            var_text = "Select SRM"
                        opt_menu_srm = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+8, n_rows=1, n_columns=9,
                            fg=self.green_dark, bg=self.green_medium).create_option_srm(
                            var_srm=self.container_var["SRM"][file],text_set=var_text, fg_active=self.green_dark,
                            bg_active=self.red_dark, command=lambda var_srm=self.container_var["SRM"][file], file=file:
                            self.change_srm_std(var_srm, file))
                        #
                        self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_srm)
                        #
                        # Internal Standard
                        if self.container_var["STD"][file]["IS"].get() != "Select IS":
                            var_text = self.container_var["STD"][file]["IS"].get()
                        else:
                            var_text = "Select IS"
                        opt_menu_std = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+17, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["STD"][file]["IS"], option_list=self.list_isotopes,
                            text_set=var_text, fg_active=self.green_dark, bg_active=self.red_dark,
                            command=lambda element=self.container_var["STD"][file]["IS"], file=file:
                            self.change_std_is(element, file))
                        #
                        self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_std)
                        self.container_optionmenu["STD"][file] = opt_menu_std
                        #
                        # Sample ID
                        if self.container_var["STD"][file]["ID"].get() != "A":
                            var_text = self.container_var["STD"][file]["ID"].get()
                        else:
                            var_text = "A"
                        opt_menu_std_id = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_std+21, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["STD"][file]["ID"], option_list=self.list_alphabet,
                            text_set=var_text, fg_active=self.green_dark, bg_active=self.red_dark,
                            command=lambda var_id=self.container_var["STD"][file]["ID"], filename=file,
                                           filetype="STD": self.change_id_file(var_id, filename, filetype))
                        #
                        self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_std_id)
                    #
                if len(self.list_smpl) > 0:
                    for index, file in enumerate(self.list_smpl):
                        #
                        parts = file.split("/")
                        filename_short = parts[-1]
                        #
                        self.container_gui[filename_short] = {}
                        for gui_category in gui_categories:
                            self.container_gui[filename_short][gui_category] = {}
                            self.container_gui[filename_short][gui_category]["General"] = []
                            self.container_gui[filename_short][gui_category]["Specific"] = []
                        #
                        self.container_helper["limits BG"][file] = {}
                        self.container_helper["limits BG"][file]["ID"] = []
                        self.container_helper["limits BG"][file]["type"] = []
                        self.container_helper["limits MAT"][file] = {}
                        self.container_helper["limits MAT"][file]["ID"] = []
                        self.container_helper["limits MAT"][file]["type"] = []
                        self.container_helper["limits INCL"][file] = {}
                        self.container_helper["limits INCL"][file]["ID"] = []
                        self.container_helper["limits INCL"][file]["type"] = []
                        self.container_helper["limits SPK"][file] = {}
                        self.container_helper["limits SPK"][file]["ID"] = []
                        self.container_helper["limits SPK"][file]["type"] = []
                        self.container_helper["limits SPK"][file]["info"] = []
                        self.container_helper["positions"]["SPK"][filename_short] = []
                        self.spikes_isotopes["SMPL"][filename_short] = {}
                        if self.file_loaded is False:
                            self.container_var["SMPL"][file] = {}
                            self.container_var["SMPL"][file]["IS"] = tk.StringVar()
                            self.container_var["SMPL"][file]["IS"].set("Select IS")
                            self.container_var["SMPL"][file]["ID"] = tk.StringVar()
                            self.container_var["SMPL"][file]["ID"].set("B")
                        #
                        categories = ["FIG", "AX", "CANVAS", "TOOLBARFRAME"]
                        self.container_diagrams["SMPL"][filename_short] = {}
                        self.diagrams_setup["SMPL"][filename_short] = {}
                        self.container_listboxes["SMPL"][filename_short] = {}
                        for category in categories:
                            self.container_diagrams["SMPL"][filename_short][category] = None
                            self.diagrams_setup["SMPL"][filename_short][category] = None
                        categories = ["Time Signal Raw", "Time Signal Smoothed", "Histogram", "Scatter"]
                        for category in categories:
                            self.diagrams_setup["SMPL"][filename_short][category] = {}
                        categories = ["BG", "MAT", "INCL", "SPK", "ISORAT"]
                        for category in categories:
                            self.container_listboxes["SMPL"][filename_short][category] = None
                        #
                        self.container_report[filename_short] = {}
                        self.container_report[filename_short]["Mean"] = {}
                        self.container_report[filename_short]["Error"] = {}
                        categories_02 = ["Intensity Ratio", "Sensitivity", "Concentration", "RSF", "LOD"]
                        for category_02 in categories_02:
                            self.container_report[filename_short]["Mean"][category_02] = {}
                            self.container_report[filename_short]["Error"][category_02] = {}
                            self.container_report[filename_short]["Mean"][category_02]["filename"] = filename_short
                            self.container_report[filename_short]["Error"][category_02]["filename"] = filename_short
                        #
                        if len(self.container_lists["SMPL"]["Long"]) < len(self.list_smpl):
                            self.container_lists["SMPL"]["Long"].append(file)
                            self.container_lists["SMPL"]["Short"].append(filename_short)
                            self.container_helper["SMPL"][filename_short] = {}
                            self.container_helper["SMPL"][filename_short]["BG"] = {}
                            self.container_helper["SMPL"][filename_short]["MAT"] = {}
                            self.container_helper["SMPL"][filename_short]["INCL"] = {}
                            self.container_helper["SMPL"][filename_short]["SPK"] = {}
                        if filename_short not in self.container_files["SMPL"]:
                            self.container_files["SMPL"][filename_short] = {}
                            self.container_files["SMPL"][filename_short]["SRM"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["IS"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["IS Concentration"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["ID"] = tk.StringVar()
                            self.container_files["SMPL"][filename_short]["ID"].set("B")
                            self.container_files["SMPL"][filename_short]["Plot"] = False
                            self.container_files["SMPL"][filename_short]["Time Signal Plot"] = None
                            self.container_files["SMPL"][filename_short]["Histogram Plot"] = None
                            self.container_files["SMPL"][filename_short]["Scatter Plot"] = None
                            self.container_files["SMPL"][filename_short]["BG"] = {}
                            self.container_files["SMPL"][filename_short]["MAT"] = {}
                            self.container_files["SMPL"][filename_short]["INCL"] = {}
                            self.container_files["SMPL"][filename_short]["SPK"] = {}
                            #
                            self.container_var["plotting"][filename_short] = {}
                            self.container_var["plotting"][filename_short]["Entry"] = {}
                            self.container_var["plotting"][filename_short]["Entry"]["Start"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["Start"].set("0.0")
                            self.container_var["plotting"][filename_short]["Entry"]["End"] = tk.StringVar()
                            self.container_var["plotting"][filename_short]["Entry"]["End"].set("0.0")
                            self.container_var["plotting"][filename_short]["Checkboxes"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"] = {}
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "BG"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "MAT"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "INCL"] = tk.IntVar()
                            self.container_var["plotting"][filename_short]["Checkboxes"]["INTERVALS"][
                                "SPK"] = tk.IntVar()
                        #
                        lbl_smpl = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl, n_rows=1, n_columns=8,
                            fg=self.green_light, bg=self.green_medium).create_simple_label(
                            text=filename_short, relief=tk.GROOVE, fontsize="sans 10 bold")
                        #
                        self.container_elements["fi_setting"]["Label"].append(lbl_smpl)
                        #
                        btn_fi_setting_smpl = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl+16, n_rows=1, n_columns=3,
                            fg=self.green_dark, bg=self.green_medium).create_simple_button(
                            text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                            command=lambda filename=self.list_smpl[index]: self.sub_fluidinclusions_plotting(filename))
                        #
                        self.container_elements["fi_setting"]["Button"].append(btn_fi_setting_smpl)
                        #
                        frm_smpl = SE(parent=self.parent, row_id=1+index, column_id=start_col_smpl+19, n_rows=1,
                                      n_columns=1, fg=self.green_light, bg=self.sign_red).create_frame()
                        #
                        self.container_elements["fi_setting"]["Frame"].append(frm_smpl)
                        self.container_var["SMPL"][file]["Frame"] = frm_smpl
                        #
                        ## Option Menus
                        self.container_var["isotopes"][file] = tk.StringVar()
                        # Internal Standard
                        if self.container_var["SMPL"][file]["IS"].get() != "Select IS":
                            var_text = self.container_var["SMPL"][file]["IS"].get()
                        else:
                            var_text = "Select IS"
                        opt_menu_iso = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl+8, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["SMPL"][file]["IS"], option_list=self.list_isotopes,
                            text_set=var_text, fg_active=self.green_dark,  bg_active=self.red_dark,
                            command=lambda element=self.container_var["SMPL"][file]["IS"], file=file,
                                           mineral=self.container_var["mineral"].get():
                            self.change_smpl_is(element, file, mineral))
                        #
                        self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_iso)
                        self.container_optionmenu["SMPL"][file] = opt_menu_iso
                        #
                        # Sample ID
                        if self.container_var["SMPL"][file]["ID"].get() != "B":
                            var_text = self.container_var["SMPL"][file]["ID"].get()
                        else:
                            var_text = "B"
                        opt_menu_smpl_id = SE(
                            parent=self.parent, row_id=1+index, column_id=start_col_smpl+12, n_rows=1, n_columns=4,
                            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                            var_iso=self.container_var["SMPL"][file]["ID"], option_list=self.list_alphabet,
                            text_set=var_text, fg_active=self.green_dark, bg_active=self.red_dark,
                            command=lambda var_id=self.container_var["SMPL"][file]["ID"], filename=file,
                                           filetype="SMPL": self.change_id_file(var_id, filename, filetype))
                        #
                        self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_smpl_id)
                        #
                if len(self.list_std) > 0 or len(self.list_smpl) > 0:
                    if len(self.list_isotopes) < 20:
                        for index, isotope in enumerate(self.list_isotopes):
                            self.container_results["STD"]["RAW"][isotope] = {}
                            self.container_results["STD"]["SMOOTHED"][isotope] = {}
                            self.container_results["SMPL"]["RAW"][isotope] = {}
                            self.container_results["SMPL"]["SMOOTHED"][isotope] = {}
                            #
                            self.container_var["dwell_times"]["Entry"][isotope] = tk.StringVar()
                            self.container_var["dwell_times"]["Entry"][isotope].set("0.01")
                            #
                            ## Labels
                            rgb = mcolors.to_rgb(self.isotope_colors[isotope])
                            brightness = np.sqrt(0.299*(rgb[0] * 255)**2 + 0.587*(rgb[1]*255)**2 + 0.114*(rgb[2]*255)**2)
                            if brightness < 128:
                                color_fg = "white"
                            else:
                                color_fg = "black"
                            # LABELS
                            lbl_iso = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso, fg=color_fg, n_rows=1,
                                n_columns=3, bg=self.isotope_colors[isotope]).create_simple_label(
                                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
                            #
                            key_element = re.search("(\D+)(\d+)", isotope)
                            element = key_element.group(1)
                            self.container_var["charge"][isotope] = {"textvar": tk.StringVar()}
                            #
                            if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                                self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.red_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            else:
                                self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.blue_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            #
                            self.container_elements["fi_setting"]["Label"].extend([lbl_iso, lbl_charge])
                            #
                            ## Option Menus
                            # Standard Reference Material
                            self.container_var["SRM"][isotope] = tk.StringVar()
                            if self.container_var["SRM"]["default"][0].get() != "Select SRM":
                                var_text = self.container_var["SRM"]["default"][0].get()
                                self.container_files["SRM"][isotope].set(var_text)
                            else:
                                var_text = "Select SRM"
                            opt_menu_srm = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso+3, n_rows=1, n_columns=9,
                                fg=self.green_dark, bg=self.green_medium).create_option_srm(
                                var_srm=self.container_var["SRM"][isotope], text_set=var_text, fg_active=self.green_dark,
                                bg_active=self.red_dark,
                                command=lambda var_srm=self.container_var["SRM"][isotope], isotope=isotope:
                                self.change_srm_iso(var_srm, isotope))
                            #
                            self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_srm)
                            #
                    else:
                        for index, isotope in enumerate(self.list_isotopes):
                            self.container_results["STD"]["RAW"][isotope] = {}
                            self.container_results["STD"]["SMOOTHED"][isotope] = {}
                            self.container_results["SMPL"]["RAW"][isotope] = {}
                            self.container_results["SMPL"]["SMOOTHED"][isotope] = {}
                            #
                            self.container_var["dwell_times"]["Entry"][isotope] = tk.StringVar()
                            self.container_var["dwell_times"]["Entry"][isotope].set("0.01")
                            #
                            ## Labels
                            rgb = mcolors.to_rgb(self.isotope_colors[isotope])
                            brightness = np.sqrt(0.299*(rgb[0]*255)**2 + 0.587*(rgb[1]*255)**2 + 0.114*(rgb[2]*255)**2)
                            if brightness < 128:
                                color_fg = "white"
                            else:
                                color_fg = "black"
                            # LABELS
                            lbl_iso = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso, fg=color_fg, n_rows=1,
                                n_columns=3, bg=self.isotope_colors[isotope]).create_simple_label(
                                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
                            #
                            key_element = re.search("(\D+)(\d+)", isotope)
                            element = key_element.group(1)
                            self.container_var["charge"][isotope] = {"textvar": tk.StringVar()}
                            #
                            if float(self.var_entr_10.get()) >= float(self.ionization_energies["First"][element]) and float(self.var_entr_10.get()) >= float(self.ionization_energies["Second"][element]):
                                self.container_var["charge"][isotope]["textvar"].set("2+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.red_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            else:
                                self.container_var["charge"][isotope]["textvar"].set("1+ charged")
                                lbl_charge = SE(
                                    parent=self.parent, row_id=1+index, column_id=start_col_iso+12, n_rows=1, n_columns=5,
                                    fg=self.green_dark, bg=self.blue_medium).create_simple_label(
                                    text=self.container_var["charge"][isotope]["textvar"], relief=tk.GROOVE, fontsize="sans 10 bold",
                                    textvariable=True)
                                self.container_var["charge"][isotope]["labelvar"] = lbl_charge
                            self.container_elements["fi_setting"]["Label"].extend([lbl_iso, lbl_charge])
                            ## Option Menus
                            self.container_var["SRM"][isotope] = tk.StringVar()
                            if self.container_var["SRM"]["default"][0].get() != "Select SRM":
                                var_text = self.container_var["SRM"]["default"][0].get()
                                self.container_files["SRM"][isotope].set(var_text)
                            else:
                                var_text = "Select SRM"
                            opt_menu_srm = SE(
                                parent=self.parent, row_id=1+index, column_id=start_col_iso+3, n_rows=1, n_columns=9,
                                fg=self.green_dark, bg=self.green_medium).create_option_srm(
                                var_srm=self.container_var["SRM"][isotope], text_set=var_text, fg_active=self.green_dark,
                                bg_active=self.red_dark,
                                command=lambda var_srm=self.container_var["SRM"][isotope], isotope=isotope:
                                self.change_srm_iso(var_srm, isotope))
                            #
                            self.container_elements["fi_setting"]["Option Menu"].append(opt_menu_srm)
                #
                ## Buttons
                btn_std_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 15, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_simple_button(
                    text="Apply to all", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=lambda filetype="STD", mode="FI": self.fast_track(filetype, mode))
                btn_smpl_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 16, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_simple_button(
                    text="Apply to all", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=lambda filetype="SMPL", mode="FI": self.fast_track(filetype, mode))
                btn_load_conc = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 12, column_id=21, n_rows=1, n_columns=8,
                    fg=self.green_dark, bg=self.green_medium).create_simple_button(
                    text="Load IS Data", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=self.import_concentration_data)
                btn_salt = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 12, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_simple_button(
                    text="Salt Correction", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=lambda gui_elements=self.gui_elements: FluidInclusions(
                        parent=self.parent, list_isotopes=self.list_isotopes, srm_actual=self.srm_actual,
                        container_var=self.container_var, container_lists=self.container_lists,
                        container_measurements=self.container_measurements, container_files=self.container_files,
                        xi_std_time=self.xi_std_time,
                        container_results=self.container_results).create_salt_correction_window(gui_elements))
                btn_method = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 14, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_simple_button(
                    text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=lambda gui_elements=self.gui_elements,
                                   var_method=self.container_var["fi_setting"]["Method"]: FluidInclusions(
                        parent=self.parent, list_isotopes=self.list_isotopes, srm_actual=self.srm_actual,
                        container_var=self.container_var, container_lists=self.container_lists,
                        container_measurements=self.container_measurements, container_files=self.container_files,
                        xi_std_time=self.xi_std_time,
                        container_results=self.container_results).create_method_settings_window(
                        gui_elements, var_method))
                btn_dwell = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 19, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_simple_button(
                    text="Setup", bg_active=self.red_dark, fg_active=self.green_dark,
                    command=self.create_dwell_time_window)
                #
                self.container_elements["fi_setting"]["Button"].extend(
                    [btn_std_01, btn_smpl_01, btn_load_conc, btn_salt, btn_method, btn_dwell])
                #
                ## RADIOBUTTONS
                rb_oxide = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 7, column_id=21, n_rows=1, n_columns=3,
                    fg=self.green_light, bg=self.green_medium).create_radiobutton(
                    var_rb=self.container_var["fi_setting"]["Host Setup Selection"], value_rb=1,
                    color_bg=self.green_medium, fg=self.green_light, text="", sticky="nesw", relief=tk.GROOVE)
                #
                rb_sulfide = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 8, column_id=21, n_rows=1, n_columns=3,
                    fg=self.green_light, bg=self.green_medium).create_radiobutton(
                    var_rb=self.container_var["fi_setting"]["Host Setup Selection"], value_rb=2,
                    color_bg=self.green_medium, fg=self.green_light, text="", sticky="nesw", relief=tk.GROOVE)
                #
                rb_halide = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 9, column_id=21, n_rows=1, n_columns=3,
                    fg=self.green_light, bg=self.green_medium).create_radiobutton(
                    var_rb=self.container_var["fi_setting"]["Host Setup Selection"], value_rb=3,
                    color_bg=self.green_medium, fg=self.green_light, text="", sticky="nesw", relief=tk.GROOVE)
                #
                rb_mineral = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 10, column_id=21, n_rows=1, n_columns=3,
                    fg=self.green_light, bg=self.green_medium).create_radiobutton(
                    var_rb=self.container_var["fi_setting"]["Host Setup Selection"], value_rb=4,
                    color_bg=self.green_medium, fg=self.green_light, text="", sticky="nesw", relief=tk.GROOVE)
                #
                self.container_elements["fi_setting"]["Radiobutton"].extend(
                    [rb_oxide, rb_sulfide, rb_halide, rb_mineral])
                #
                ## Entries
                # Time Interval Background
                if self.container_var["fi_setting"]["Time BG Start"].get() != "Set start time":
                    var_text = self.container_var["fi_setting"]["Time BG Start"].get()
                else:
                    var_text = "Set start time"
                entr_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+4, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Time BG Start"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["fi_setting"]["Time BG Start"], times=self.times,
                                   category_01="FI", category_02="Start BG":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                #
                if self.container_var["fi_setting"]["Time BG End"].get() != "Set end time":
                    var_text = self.container_var["fi_setting"]["Time BG End"].get()
                else:
                    var_text = "Set end time"
                entr_02 = SE(
                    parent=self.parent, row_id=start_row_settings_01+5, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Time BG End"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["fi_setting"]["Time BG End"], times=self.times,
                                   category_01="FI", category_02="End BG":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                #
                # Time Interval Matrix
                if self.container_var["fi_setting"]["Time MAT Start"].get() != "Set start time":
                    var_text = self.container_var["fi_setting"]["Time MAT Start"].get()
                else:
                    var_text = "Set start time"
                entr_03 = SE(
                    parent=self.parent, row_id=start_row_settings_01+7, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Time MAT Start"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["fi_setting"]["Time MAT Start"], times=self.times,
                                   category_01="FI",  category_02="Start MAT":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                #
                if self.container_var["fi_setting"]["Time MAT End"].get() != "Set end time":
                    var_text = self.container_var["fi_setting"]["Time MAT End"].get()
                else:
                    var_text = "Set end time"
                entr_04 = SE(
                    parent=self.parent, row_id=start_row_settings_01+8, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Time MAT End"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["fi_setting"]["Time MAT End"], times=self.times,
                                   category_01="FI", category_02="End MAT":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                #
                # Time Interval Inclusion
                if self.container_var["fi_setting"]["Time INCL Start"].get() != "Set start time":
                    var_text = self.container_var["fi_setting"]["Time INCL Start"].get()
                else:
                    var_text = "Set start time"
                entr_11 = SE(
                    parent=self.parent, row_id=start_row_settings_01+10, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Time INCL Start"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["fi_setting"]["Time INCL Start"], times=self.times,
                                   category_01="FI", category_02="Start INCL":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                #
                if self.container_var["fi_setting"]["Time INCL End"].get() != "Set end time":
                    var_text = self.container_var["fi_setting"]["Time INCL End"].get()
                else:
                    var_text = "Set end time"
                entr_12 = SE(
                    parent=self.parent, row_id=start_row_settings_01+11, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Time INCL End"], text_default=var_text,
                    command=lambda event, var_t=self.container_var["fi_setting"]["Time INCL End"], times=self.times,
                                   category_01="FI", category_02="End INCL":
                    self.find_nearest_time(var_t, times, category_01, category_02, event))
                #
                # Deviation and Threshold
                var_entr_05 = tk.StringVar()
                self.container_var["fi_setting"]["SE Deviation"] = var_entr_05
                entr_05 = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 13, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=var_entr_05, text_default="10",
                    command=lambda event, var=var_entr_05, category_01="MA", category_02="Deviation":
                    self.set_entry_value(var, category_01, category_02, event))
                #
                var_entr_06 = tk.StringVar()
                self.container_var["fi_setting"]["SE Threshold"] = var_entr_06
                entr_06 = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 14, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=var_entr_06, text_default="1000",
                    command=lambda event, var=var_entr_06, category_01="MA", category_02="Threshold":
                    self.set_entry_value(var, category_01, category_02, event))
                #
                # Author and Source ID
                var_entr_07 = tk.StringVar()
                self.container_var["fi_setting"]["Author"] = var_entr_07
                entr_07 = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 18, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=var_entr_07, text_default="J. Doe",
                    command=lambda event, var=var_entr_07, category_01="MA", category_02="Author":
                    self.set_entry_value(var, category_01, category_02, event))
                #
                var_entr_08 = tk.StringVar()
                self.container_var["fi_setting"]["Source ID"] = var_entr_08
                entr_08 = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 19, column_id=46, n_rows=1, n_columns=9,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=var_entr_08, text_default="RUR01",
                    command=lambda event, var=var_entr_08, category_01="MA", category_02="Source ID":
                    self.set_entry_value(var, category_01, category_02, event))
                #
                if self.container_var["fi_setting"]["Oxide Concentration"].get() != "100":
                    var_text = self.container_var["fi_setting"]["Oxide Concentration"].get()
                else:
                    var_text = "100"
                entr_oxide = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 7, column_id=24, n_rows=1, n_columns=5,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Oxide Concentration"], text_default=var_text)
                #
                if self.container_var["fi_setting"]["Sulfide Concentration"].get() != "100":
                    var_text = self.container_var["fi_setting"]["Sulfide Concentration"].get()
                else:
                    var_text = "100"
                entr_sulfide = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 8, column_id=24, n_rows=1, n_columns=5,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Sulfide Concentration"], text_default=var_text)
                #
                if self.container_var["fi_setting"]["Halide Concentration"].get() != "100":
                    var_text = self.container_var["fi_setting"]["Halide Concentration"].get()
                else:
                    var_text = "100"
                entr_halide = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 9, column_id=24, n_rows=1, n_columns=5,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Halide Concentration"], text_default=var_text)
                #
                if self.container_var["fi_setting"]["Mineral Concentration"].get() != "100":
                    var_text = self.container_var["fi_setting"]["Mineral Concentration"].get()
                else:
                    var_text = "100"
                entr_mineral = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 10, column_id=24, n_rows=1, n_columns=5,
                    fg=self.green_light, bg=self.green_dark).create_simple_entry(
                    var=self.container_var["fi_setting"]["Mineral Concentration"], text_default=var_text)
                #
                self.container_elements["fi_setting"]["Entry"].extend(
                    [entr_01, entr_02, entr_03, entr_04, entr_05, entr_06, entr_07, entr_08, entr_10, entr_11, entr_12,
                     entr_oxide, entr_sulfide, entr_halide, entr_mineral])
                #
                if self.container_var["SRM"]["default"][0].get() != "Select SRM":
                    var_text = self.container_var["SRM"]["default"][0].get()
                else:
                    var_text = "Select SRM"
                #
                opt_menu_srm_default_01 = SE(
                    parent=self.parent, row_id=start_row_settings_01+4, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_srm(
                    var_srm=self.container_var["SRM"]["default"][0], text_set=var_text, fg_active=self.green_dark,
                    bg_active=self.red_dark, command=lambda var_srm=self.container_var["SRM"]["default"][0]:
                    self.change_srm_default(var_srm))
                opt_menu_srm_default_02 = SE(
                    parent=self.parent, row_id=start_row_settings_01+5, column_id=29, n_rows=1, n_columns=9, fg=self.green_dark,
                    bg=self.green_medium).create_option_srm(
                    var_srm=self.container_var["SRM"]["default"][1], text_set=var_text, fg_active=self.green_dark,
                    bg_active=self.red_dark, command=lambda var_srm=self.container_var["SRM"]["default"][1]:
                    self.change_srm_default(var_srm, key="isotope"))
                #
                if self.container_var["mineral"].get() != "Select Mineral":
                    var_text = self.container_var["mineral"].get()
                else:
                    var_text = "Select Mineral"
                opt_menu_mineral = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 10, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_mineral(
                    var_min=self.container_var["mineral"], text_set=var_text, fg_active=self.green_dark,
                    bg_active=self.red_dark, option_list=self.mineral_list,
                    command=lambda var_min=self.container_var["mineral"], fluidinclusion=True:
                    self.select_mineral_is(var_min, fluidinclusion))
                #
                list_opt_gas = ["Helium", "Neon", "Argon", "Krypton", "Xenon", "Radon"]
                opt_laser = SE(
                    parent=self.parent, row_id=int(1 + len(self.list_isotopes)), column_id=start_col_iso, n_rows=1,
                    n_columns=12, fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["LASER"], option_list=list_opt_gas, text_set="Argon",
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda var_opt=self.container_var["LASER"]: self.change_carrier_gas(var_opt))
                #
                ## Quantification Method
                self.build_plugin_list()
                opt_methods = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 13, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["fi_setting"]["Method"],
                    option_list=self.container_lists["Plugins FI"]["Names"], text_set="Select Method",
                    fg_active=self.green_dark, bg_active=self.red_dark)
                #
                self.container_elements["fi_setting"]["Option Menu"].extend(
                    [opt_menu_srm_default_01, opt_menu_srm_default_02, opt_laser, opt_methods, opt_menu_mineral])
                #
                if self.container_var["ID"]["Default STD"].get() != "A":
                    var_text = self.container_var["ID"]["Default STD"].get()
                else:
                    var_text = "A"
                self.opt_id_std_def = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 16, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["ID"]["Default STD"], option_list=self.list_alphabet, text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda var_id=self.container_var["ID"]["Default STD"],
                                   filetype="STD": self.change_id_default(var_id, filetype))
                #
                if self.container_var["ID"]["Default SMPL"].get() != "B":
                    var_text = self.container_var["ID"]["Default SMPL"].get()
                else:
                    var_text = "B"
                self.opt_id_smpl_def = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 17, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["ID"]["Default SMPL"], option_list=self.list_alphabet, text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark,
                    command=lambda var_id=self.container_var["ID"]["Default SMPL"],
                                   filetype="SMPL": self.change_id_default(var_id, filetype))
                #
                self.container_elements["fi_setting"]["Option Menu"].extend([self.opt_id_std_def, self.opt_id_smpl_def])
                #
                ## HOST SETTINGS
                if self.container_var["fi_setting"]["Oxide"].get() != "Select Oxide":
                    var_text = self.container_var["fi_setting"]["Oxide"].get()
                else:
                    var_text = "Select Oxide"
                opt_oxides = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 7, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["fi_setting"]["Oxide"],
                    option_list=self.container_lists["Oxides"], text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark)
                #
                if self.container_var["fi_setting"]["Sulfide"].get() != "Select Sulfide":
                    var_text = self.container_var["fi_setting"]["Sulfide"].get()
                else:
                    var_text = "Select Sulfide"
                opt_sulfides = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 8, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["fi_setting"]["Sulfide"],
                    option_list=self.container_lists["Sulfides"], text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark)
                #
                if self.container_var["fi_setting"]["Halide"].get() != "Select Halide":
                    var_text = self.container_var["fi_setting"]["Halide"].get()
                else:
                    var_text = "Select Halide"
                opt_halides = SE(
                    parent=self.parent, row_id=start_row_settings_01 + 9, column_id=29, n_rows=1, n_columns=9,
                    fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                    var_iso=self.container_var["fi_setting"]["Halide"],
                    option_list=self.container_lists["Halides"], text_set=var_text,
                    fg_active=self.green_dark, bg_active=self.red_dark)
                #
                self.container_elements["fi_setting"]["Option Menu"].extend([opt_oxides, opt_sulfides, opt_halides])
                #
                ## ADDITIONAL OPERATIONS DUE TO FILE LOADING
                if self.file_loaded is True:
                    self.select_mineral_is(var_min=self.container_var["mineral"].get())
                #
                self.window_created["fi_setting"] = True
        #
        else:
            pass
        #
    def sub_fluidinclusions_plotting(self, filename):
        #
        if filename in self.list_std:
            self.file_type = "STD"
        elif filename in self.list_smpl:
            self.file_type = "SMPL"
        #
        ## Cleaning
        categories = ["fi_setting"]
        for category in categories:
            if len(self.container_elements[category]["Label"]) > 0:
                for item in self.container_elements[category]["Label"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Button"]) > 0:
                for item in self.container_elements[category]["Button"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Option Menu"]) > 0:
                for item in self.container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Entry"]) > 0:
                for item in self.container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(self.container_elements[category]["Frame"]) > 0:
                for item in self.container_elements[category]["Frame"]:
                    item.grid_remove()
        #
        try:
            parts = filename.split("/")
            self.container_files[self.file_type][parts[-1]]["Time Signal Plot"].draw()
        except:
            pass
        #
        self.file = filename
        parts = filename.split("/")
        filename_short = parts[-1]
        self.filename_short = filename_short
        df_data = self.load_and_assign_data(filename=filename)
        self.times = df_data.iloc[:, 0]
        icp_measurements = np.array([[df_data[isotope] for isotope in self.list_isotopes]])
        x_max = np.amax(self.times)
        y_max = np.amax(icp_measurements)
        if self.container_files[self.file_type][filename_short]["Plot"] == False:
            self.bg_id = 0
            self.bg_idlist = []
            self.mat_id = 0
            self.mat_idlist = []
            self.incl_id = 0
            self.incl_idlist = []
            self.spk_id = 0
            self.spk_idlist = []
            self.lines = {}
            self.lines["raw"] = {}
            self.lines["edited"] = {}
            if filename_short not in self.container_helper["positions"]:
                self.container_helper["positions"]["BG"][filename_short] = []
                self.container_helper["positions"]["BG SMPL"] = {}
                self.container_helper["positions"]["BG SMPL"][filename_short] = []
                self.container_helper["positions"]["MAT"][filename_short] = []
                self.container_helper["positions"]["MAT SMPL"] = {}
                self.container_helper["positions"]["MAT SMPL"][filename_short] = []
                self.container_helper["positions"]["INCL"][filename_short] = []
                self.container_helper["positions"]["INCL SMPL"] = {}
                self.container_helper["positions"]["INCL SMPL"][filename_short] = []
                self.container_helper["positions"]["SPK"][filename_short] = []
                self.container_helper["positions"]["SPK SMPL"] = {}
                self.container_helper["positions"]["SPK SMPL"][filename_short] = []
                self.container_helper["positions"][filename_short] = []
                self.container_helper["indices"][filename_short] = []
            #
            if filename_short not in self.container_measurements["RAW"]:
                self.container_measurements["RAW"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short] = {}
                self.container_measurements["SELECTED"][filename_short]["RAW"] = {}
                self.container_measurements["SELECTED"][filename_short]["SMOOTHED"] = {}
                self.container_measurements["EDITED"][filename_short] = {}
                self.container_measurements["RAW"]["Time"] = self.times.tolist()
                self.container_measurements["SELECTED"][filename_short]["Time"] = self.times.tolist()
                self.container_measurements["EDITED"]["Time"] = self.times.tolist()
                for isotope in self.list_isotopes:
                    self.container_measurements["RAW"][filename_short][isotope] = df_data[isotope].tolist()
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["MAT"] = []
                    self.container_measurements["SELECTED"][filename_short]["RAW"][isotope]["INCL"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope] = {}
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["BG"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["MAT"] = []
                    self.container_measurements["SELECTED"][filename_short]["SMOOTHED"][isotope]["INCL"] = []
                    self.container_measurements["EDITED"][filename_short][isotope] = {}
                    self.container_measurements["EDITED"][filename_short][isotope]["BG"] = []
                    self.container_measurements["EDITED"][filename_short][isotope]["MAT"] = []
                    self.container_measurements["EDITED"][filename_short][isotope]["INCL"] = []
            #
            ## FRAMES
            frm_bg = SE(
                parent=self.parent, row_id=29, column_id=21, n_rows=1, n_columns=9, fg=self.blue_light,
                bg=self.blue_dark).create_frame(relief=tk.FLAT)
            frm_mat = SE(
                parent=self.parent, row_id=29, column_id=30, n_rows=1, n_columns=9, fg=self.brown_light,
                bg=self.brown_dark).create_frame(relief=tk.FLAT)
            frm_incl = SE(
                parent=self.parent, row_id=29, column_id=39, n_rows=1, n_columns=9, fg=self.slate_grey_light,
                bg=self.slate_grey_dark).create_frame(relief=tk.FLAT)
            frm_spkelim = SE(
                parent=self.parent, row_id=29, column_id=48, n_rows=1, n_columns=9, fg=self.yellow_light,
                bg=self.yellow_dark).create_frame(relief=tk.FLAT)
            frm_isorat = SE(
                parent=self.parent, row_id=29, column_id=57, n_rows=1, n_columns=9, fg=self.slate_grey_light,
                bg=self.slate_grey_light).create_frame(relief=tk.FLAT)
            frm_spke_bg = SE(
                parent=self.parent, row_id=1, column_id=87, n_rows=len(self.list_isotopes), n_columns=2,
                fg=self.yellow_medium, bg=self.yellow_medium).create_frame()
            #
            self.container_elements["plotting"]["Frame"].extend(
                [frm_bg, frm_mat, frm_incl, frm_spkelim, frm_isorat, frm_spke_bg])
            self.container_gui[filename_short]["Frame"]["General"].extend(
                [frm_bg, frm_mat, frm_incl, frm_spkelim, frm_isorat, frm_spke_bg])
            #
            ## LABELS
            lbl_file = SE(
                parent=self.parent, row_id=0, column_id=80, n_rows=1, n_columns=9, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text=filename_short, relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_spk = SE(
                parent=self.parent, row_id=33, column_id=66, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Spike Elimination", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_disply = SE(
                parent=self.parent, row_id=30, column_id=66, n_rows=1, n_columns=12, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="Plot Selection", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_start = SE(
                parent=self.parent, row_id=36, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Start (Time)", relief=tk.GROOVE, fontsize="sans 10 bold")
            lbl_end = SE(
                parent=self.parent, row_id=37, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="End (Time)", relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            self.container_elements["plotting"]["Label"].extend(
                [lbl_file, lbl_spk, lbl_disply, lbl_start, lbl_end])
            self.container_gui[filename_short]["Label"]["General"].extend(
                [lbl_file, lbl_spk, lbl_disply, lbl_start, lbl_end])
            #
            ## ENTRY
            #
            entr_start = SE(
                parent=self.parent, row_id=36, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_entry(
                var=self.container_var["plotting"][filename_short]["Entry"]["Start"], text_default="0.0",
                command=lambda event, filename_short=filename_short, var_key="Start":
                self.set_integration_window(filename_short, var_key, event))
            entr_end = SE(
                parent=self.parent, row_id=37, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_dark).create_simple_entry(
                var=self.container_var["plotting"][filename_short]["Entry"]["End"], text_default="0.0",
                command=lambda event, filename_short=filename_short, var_key="End":
                self.set_integration_window(filename_short, var_key, event))
            #
            self.container_elements["plotting"]["Entry"].extend([entr_start, entr_end])
            self.container_gui[filename_short]["Entry"]["General"].extend([entr_start, entr_end])
            #
            for index, isotope in enumerate(self.list_isotopes):
                rgb = mcolors.to_rgb(self.isotope_colors[isotope])
                brightness = np.sqrt(
                    0.299 * (rgb[0] * 255) ** 2 + 0.587 * (rgb[1] * 255) ** 2 + 0.114 * (rgb[2] * 255) ** 2)
                if brightness < 128:
                    color_fg = "white"
                else:
                    color_fg = "black"
                # LABELS
                lbl_iso = SE(parent=self.parent, row_id=1 + index, column_id=80, fg=color_fg, n_rows=1, n_columns=3,
                             bg=self.isotope_colors[isotope]).create_simple_label(text=isotope)
                #
                self.container_elements["plotting"]["Label"].append(lbl_iso)
                self.container_gui[filename_short]["Label"]["General"].append(lbl_iso)
                #
                # CHECKBOXES
                self.container_var["plotting"][isotope] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
                self.container_var["plotting"][isotope][0].set(1)
                self.container_var["plotting"][isotope][1].set(0)
                self.container_var["plotting"][isotope][2].set(0)
                self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope] = tk.IntVar()
                self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope] = tk.IntVar()
                self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"][isotope] = tk.IntVar()
                self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope].set(1)
                self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope].set(0)
                self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"][isotope].set(0)
                #
                frm_iso_bg = SE(parent=self.parent, row_id=1 + index, column_id=83, n_rows=1, n_columns=4,
                                fg=self.isotope_colors[isotope], bg=self.isotope_colors[isotope]).create_frame()
                self.container_elements["plotting"]["Frame"].append(frm_iso_bg)
                self.container_gui[filename_short]["Frame"]["General"].append(frm_iso_bg)
                cb_iso = SE(
                    parent=self.parent, row_id=1 + index, column_id=83, fg=color_fg, n_rows=1, n_columns=2,
                    bg=self.isotope_colors[isotope]).create_simple_checkbox(
                    var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope], text="",
                    set_sticky="", command=lambda
                        var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["RAW"][isotope],
                        name=isotope: self.change_visibility(var_cb, name))
                cb_isosmoothed = SE(
                    parent=self.parent, row_id=1 + index, column_id=85, fg=color_fg, n_rows=1, n_columns=2,
                    bg=self.isotope_colors[isotope]).create_simple_checkbox(
                    var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope],
                    text="",
                    set_sticky="", command=lambda
                        var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["SMOOTHED"][isotope],
                        name=isotope: self.change_visibility(var_cb, name))
                cb_spk = SE(
                    parent=self.parent, row_id=1 + index, column_id=87, fg=color_fg, n_rows=1, n_columns=2,
                    bg=self.yellow_medium).create_simple_checkbox(
                    var_cb=self.container_var["plotting"][filename_short]["Checkboxes"]["SPIKES"][isotope], text="",
                    set_sticky="")
                #
                self.container_elements["plotting"]["Checkbox"].extend([cb_iso, cb_spk, cb_isosmoothed])
                self.container_gui[filename_short]["Checkbox"][isotope] = []
                self.container_gui[filename_short]["Checkbox"][isotope].extend([cb_iso, cb_spk, cb_isosmoothed])
            #
            ## RADIOBUTTONS
            self.container_var["plotting"][filename_short]["RB"] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
            rb_bg = SE(
                parent=self.parent, row_id=29, column_id=21, n_rows=1, n_columns=6, fg=self.blue_light,
                bg=self.blue_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=1, color_bg=self.blue_dark,
                fg=self.blue_light, text="Background", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=1: self.change_radiobutton(var, value))
            rb_mat = SE(
                parent=self.parent, row_id=29, column_id=30, n_rows=1, n_columns=6, fg=self.brown_light,
                bg=self.brown_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=4,
                color_bg=self.brown_dark,
                fg=self.brown_light, text="Matrix", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=4: self.change_radiobutton(var, value))
            rb_incl = SE(
                parent=self.parent, row_id=29, column_id=39, n_rows=1, n_columns=6, fg=self.slate_grey_light,
                bg=self.slate_grey_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=5,
                color_bg=self.slate_grey_dark,
                fg=self.slate_grey_light, text="Inclusion", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=5: self.change_radiobutton(var, value))
            rb_spk = SE(
                parent=self.parent, row_id=29, column_id=48, n_rows=1, n_columns=6, fg=self.yellow_light,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=3,
                color_bg=self.yellow_dark,
                fg=self.yellow_light, text="Spike Elimination", sticky="nesw", relief=tk.GROOVE,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0],
                               value=3: self.change_radiobutton(var, value))
            rb_nslctn = SE(
                parent=self.parent, row_id=28, column_id=21, n_rows=1, n_columns=36, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][0], value_rb=0,
                color_bg=self.green_medium,
                fg=self.green_light, text="No Selection", sticky="nesw", relief=tk.GROOVE)
            rb_01 = SE(
                parent=self.parent, row_id=28, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][1], value_rb=0,
                color_bg=self.green_medium,
                fg=self.green_light, text="Raw Data", sticky="nesw", relief=tk.GROOVE,
                command=lambda var_rb=self.container_var["plotting"][filename_short]["RB"][1]: self.change_rb_value(
                    var_rb))
            rb_02 = SE(
                parent=self.parent, row_id=29, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][1], value_rb=1,
                color_bg=self.green_medium,
                fg=self.green_light, text="Smoothed Data", sticky="nesw", relief=tk.GROOVE,
                command=lambda var_rb=self.container_var["plotting"][filename_short]["RB"][1]: self.change_rb_value(
                    var_rb))
            rb_03 = SE(
                parent=self.parent, row_id=31, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=0,
                color_bg=self.green_medium,
                fg=self.green_light, text="Time-Signal Plot", sticky="nesw", relief=tk.GROOVE)
            rb_06 = SE(
                parent=self.parent, row_id=31, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=3,
                color_bg=self.green_medium,
                fg=self.green_light, text="Time-Ratio Plot", sticky="nesw", relief=tk.GROOVE)
            rb_04 = SE(
                parent=self.parent, row_id=32, column_id=66, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=1,
                color_bg=self.green_medium,
                fg=self.green_light, text="Histogram", sticky="nesw", relief=tk.GROOVE)
            rb_05 = SE(
                parent=self.parent, row_id=32, column_id=72, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["plotting"][filename_short]["RB"][2], value_rb=2,
                color_bg=self.green_medium,
                fg=self.green_light, text="Scatter Plot", sticky="nesw", relief=tk.GROOVE)
            #
            self.container_elements["plotting"]["Radiobutton"].extend(
                [rb_bg, rb_mat, rb_incl, rb_spk, rb_nslctn, rb_01, rb_02, rb_03, rb_04, rb_05, rb_06])
            self.container_gui[filename_short]["Radiobutton"]["General"].extend(
                [rb_bg, rb_mat, rb_incl, rb_spk, rb_nslctn, rb_01, rb_02, rb_03, rb_04, rb_05, rb_06])
            #
            ## CHECKBOXES
            self.container_var["plotting"]["Integration Window"] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"].set(1)
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["MAT"].set(1)
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["INCL"].set(1)
            self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"].set(1)
            self.container_var["plotting"]["Integration Window"][0].set(1)
            self.container_var["plotting"]["Integration Window"][1].set(1)
            self.container_var["plotting"]["Integration Window"][2].set(1)
            cb_iw_bg = SE(
                parent=self.parent, row_id=29, column_id=27, fg=self.blue_light, n_rows=1, n_columns=3,
                bg=self.blue_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["BG"]:
                self.change_visibility_iw(var_cb))
            cb_iw_mat = SE(
                parent=self.parent, row_id=29, column_id=36, fg=self.brown_light, n_rows=1, n_columns=3,
                bg=self.brown_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["MAT"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["MAT"]:
                self.change_visibility_iw(var_cb))
            cb_iw_incl = SE(
                parent=self.parent, row_id=29, column_id=45, fg=self.red_light, n_rows=1, n_columns=3,
                bg=self.slate_grey_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["INCL"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["INCL"]:
                self.change_visibility_iw(var_cb))
            cb_iw_spk = SE(
                parent=self.parent, row_id=29, column_id=54, fg=self.yellow_light, n_rows=1, n_columns=3,
                bg=self.yellow_dark).create_simple_checkbox(
                var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"],
                text="Show", set_sticky="", own_color=True, command=lambda
                    var_cb=self.container_var["plotting"][self.filename_short]["Checkboxes"]["INTERVALS"]["SPK"]:
                self.change_visibility_iw(var_cb))
            #
            self.container_elements["plotting"]["Checkbox"].extend([cb_iw_bg, cb_iw_mat, cb_iw_incl, cb_iw_spk])
            self.container_gui[filename_short]["Checkbox"]["General"].extend([cb_iw_bg, cb_iw_mat, cb_iw_incl,
                                                                              cb_iw_spk])
            #
            ## BUTTONS
            btn_back = SE(
                parent=self.parent, row_id=38, column_id=66, n_rows=2, n_columns=12, fg=self.green_dark,
                bg=self.red_dark).create_simple_button(
                text="Back to Settings", bg_active=self.green_dark, fg_active=self.green_light,
                command=self.sub_fluidinclusions_settings)
            btn_rmv = SE(
                parent=self.parent, row_id=28, column_id=57, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.red_dark).create_simple_button(
                text="Remove Interval", bg_active=self.green_dark, fg_active=self.green_light,
                command=lambda var=self.container_var["plotting"][filename_short]["RB"][0]: self.delete_interval(
                    var))
            btn_all = SE(
                parent=self.parent, row_id=28, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Show All", bg_active=self.red_dark, fg_active=self.green_dark, command=self.show_all_lines)
            btn_none = SE(
                parent=self.parent, row_id=29, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Show None", bg_active=self.red_dark, fg_active=self.green_dark, command=self.hide_all_lines)
            btn_smthall = SE(
                parent=self.parent, row_id=34, column_id=66, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="All Isotopes", bg_active=self.red_dark, fg_active=self.green_dark,
                command=self.smooth_all_isotopes)
            btn_smoothit = SE(
                parent=self.parent, row_id=34, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Smooth it", bg_active=self.red_dark, fg_active=self.green_dark,
                command=lambda var_setting="fi_setting": self.do_spike_elimination(var_setting))
            btn_cnfrm = SE(
                parent=self.parent, row_id=35, column_id=72, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Confirm Edits", bg_active=self.red_dark, fg_active=self.green_dark,
                command=lambda filename=self.file, filetype=self.file_type: self.confirm_edits(filename, filetype))
            btn_showspkelim = SE(
                parent=self.parent, row_id=35, column_id=66, n_rows=1, n_columns=6, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Update Data", bg_active=self.red_dark, fg_active=self.green_dark,
                command=lambda mode="FI": self.update_edited_datasets(mode))
            #
            self.container_elements["plotting"]["Button"].extend(
                [btn_back, btn_rmv, btn_all, btn_none, btn_smthall, btn_cnfrm, btn_showspkelim, btn_smoothit])
            self.container_gui[filename_short]["Button"]["General"].extend(
                [btn_back, btn_rmv, btn_all, btn_none, btn_smthall, btn_cnfrm, btn_showspkelim, btn_smoothit])
            #
            ## LISTBOXES and TREEVIEWS
            lb_bg, scrollbar_bg_x, scrollbar_bg_y = SE(
                parent=self.parent, row_id=30, column_id=21, n_rows=10, n_columns=9, fg=self.blue_dark,
                bg=self.blue_light).create_simple_listbox_grid()
            lb_mat, scrollbar_mat_x, scrollbar_mat_y = SE(
                parent=self.parent, row_id=30, column_id=30, n_rows=10, n_columns=9, fg=self.brown_dark,
                bg=self.brown_light).create_simple_listbox_grid()
            lb_incl, scrollbar_incl_x, scrollbar_incl_y = SE(
                parent=self.parent, row_id=30, column_id=39, n_rows=10, n_columns=9, fg=self.slate_grey_dark,
                bg=self.slate_grey_light).create_simple_listbox_grid()
            lb_spk, scrollbar_spk_x, scrollbar_spk_y = SE(
                parent=self.parent, row_id=30, column_id=48, n_rows=10, n_columns=9, fg=self.yellow_dark,
                bg=self.yellow_light).create_simple_listbox_grid()
            lb_isorat = SE(
                parent=self.parent, row_id=30, column_id=57, n_rows=10, n_columns=9, fg=self.slate_grey_dark,
                bg=self.slate_grey_light).create_treeview()
            #
            self.container_elements["plotting"]["Listbox"].extend([lb_bg, scrollbar_bg_x, scrollbar_bg_y,
                                                                   lb_mat, scrollbar_mat_x, scrollbar_mat_y,
                                                                   lb_incl, scrollbar_incl_x, scrollbar_incl_y,
                                                                   lb_spk, scrollbar_spk_x, scrollbar_spk_y,
                                                                   lb_isorat])
            self.container_listboxes[self.file_type][filename_short]["BG"] = [lb_bg, scrollbar_bg_x, scrollbar_bg_y]
            self.container_listboxes[self.file_type][filename_short]["MAT"] = [lb_mat, scrollbar_mat_x, scrollbar_mat_y]
            self.container_listboxes[self.file_type][filename_short]["INCL"] = [lb_incl, scrollbar_incl_x,
                                                                                scrollbar_incl_y]
            self.container_listboxes[self.file_type][filename_short]["SPK"] = [lb_spk, scrollbar_spk_x,
                                                                               scrollbar_spk_y]
            self.container_listboxes[self.file_type][filename_short]["ISORAT"] = lb_isorat
            #
            ## OPTION MENU
            if filename in self.container_var["STD"]:
                if self.container_var["STD"][filename]["IS"].get() != "Select IS":
                    var_text = self.container_var["STD"][filename]["IS"].get()
                    var_iso = self.container_var["STD"][filename]["IS"]
                    self.calculate_and_place_isotope_ratios(
                        var_is=self.container_var["STD"][filename]["IS"].get(), data=df_data, lb=lb_isorat, mode="FI")
                else:
                    var_iso = self.container_var["STD"][filename]
                    var_text = "Select IS"
            else:
                if self.container_var["SMPL"][filename]["IS"].get() != "Select IS":
                    var_text = self.container_var["SMPL"][filename]["IS"].get()
                    var_iso = self.container_var["SMPL"][filename]["IS"]
                    self.calculate_and_place_isotope_ratios(
                        var_is=self.container_var["SMPL"][filename]["IS"].get(), data=df_data, lb=lb_isorat, mode="FI")
                else:
                    var_iso = self.container_var["SMPL"][filename]["IS"]
                    var_text = "Select IS"
            opt_is = SE(
                parent=self.parent, row_id=29, column_id=57, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=var_iso, option_list=self.list_isotopes, text_set=var_text, fg_active=self.green_dark,
                bg_active=self.red_dark, command=lambda var_is=var_iso, data=df_data, lb=lb_isorat:
                self.calculate_and_place_isotope_ratios(var_is, data, lb))
            #
            self.container_elements["plotting"]["Option Menu"].append(opt_is)
            self.container_gui[filename_short]["Option Menu"]["General"].append(opt_is)
            #
            ## DIAGRAM
            if self.container_var["plotting"][filename_short]["RB"][1].get() == 0:
                if self.file_type == "STD":
                    if self.fast_track_std == True:
                        self.fig = self.diagrams_setup[self.file_type][filename_short]["FIG"]
                        self.ax = self.diagrams_setup[self.file_type][filename_short]["AX"]
                    else:
                        self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax = self.fig.add_subplot()
                        self.diagrams_setup[self.file_type][filename_short]["FIG"] = self.fig
                        self.diagrams_setup[self.file_type][filename_short]["AX"] = self.ax
                elif self.file_type == "SMPL":
                    if self.fast_track_smpl == True:
                        self.fig = self.container_diagrams[self.file_type][filename_short]["FIG"]
                        self.ax = self.container_diagrams[self.file_type][filename_short]["AX"]
                        self.fig = self.diagrams_setup[self.file_type][filename_short]["FIG"]
                        self.ax = self.diagrams_setup[self.file_type][filename_short]["AX"]
                    else:
                        self.fig = Figure(figsize=(10, 5), facecolor=self.green_light)
                        self.ax = self.fig.add_subplot()
                        self.container_diagrams[self.file_type][filename_short]["FIG"] = self.fig
                        self.container_diagrams[self.file_type][filename_short]["AX"] = self.ax
                        self.diagrams_setup[self.file_type][filename_short]["FIG"] = self.fig
                        self.diagrams_setup[self.file_type][filename_short]["AX"] = self.ax
                #
                for isotope in self.list_isotopes:
                    ln = self.ax.plot(
                        self.times, df_data[isotope], label=isotope, color=self.isotope_colors[isotope],
                        visible=True)
                    self.lines["raw"][isotope] = ln
                    self.diagrams_setup[self.file_type][filename_short]["Time Signal Raw"][isotope] = ln
                self.ax.grid(True)
                self.ax.set_yscale("log")
                self.ax.set_xlim(left=0, right=x_max)
                self.ax.set_xticks(np.arange(0, x_max, 10))
                self.ax.set_ylim(top=1.5 * y_max)
                self.ax.set_axisbelow(True)
                self.ax.set_xlabel("Time (s)", labelpad=0.5)
                self.ax.set_ylabel("Signal (cps)", labelpad=0.5)

                self.fig.subplots_adjust(bottom=0.125, top=0.975, left=0.075, right=0.975)

                legend = self.ax.legend(fontsize="x-small", framealpha=1.0, edgecolor="white",
                                        bbox_to_anchor=(0.10, 0.010), loc=3, borderaxespad=0,
                                        bbox_transform=plt.gcf().transFigure,
                                        ncol=int(len(self.list_isotopes) / 2 + 1),
                                        facecolor="white")
                plt.rcParams["savefig.facecolor"] = "white"
                plt.rcParams["savefig.dpi"] = 300

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
                self.canvas.get_tk_widget().grid(
                    row=0, column=21, rowspan=26, columnspan=59, sticky="nesw")
                self.toolbarFrame = tk.Frame(master=self.parent)
                self.toolbarFrame.grid(
                    row=26, column=21, rowspan=2, columnspan=59, sticky="w")
                self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
                self.toolbar.config(background=self.green_light)
                self.toolbar._message_label.config(background=self.green_light)
                self.toolbar.winfo_children()[-2].config(background=self.green_light)

                self.container_files[self.file_type][filename_short]["Time Signal Plot"] = [self.canvas,
                                                                                            self.toolbarFrame]
                self.container_files[self.file_type][filename_short]["Plot"] = True
                self.diagrams_setup[self.file_type][filename_short]["CANVAS"] = self.canvas
                self.diagrams_setup[self.file_type][filename_short]["TOOLBARFRAME"] = self.toolbarFrame
                #
                if self.container_settings["FI"]["Start BG"].get() != "":
                    filename = self.file.split("/")[-1]
                    x_nearest_start = min(self.times, key=lambda x: abs(
                        x - float(self.container_settings["FI"]["Start BG"].get())))
                    x_nearest_end = min(self.times,
                                        key=lambda x: abs(x - float(self.container_settings["FI"]["End BG"].get())))
                    index_start = self.times[self.times == x_nearest_start].index[0]
                    index_end = self.times[self.times == x_nearest_end].index[0]
                    #
                    self.bg_id += 1
                    self.container_listboxes[self.file_type][filename]["BG"][0].insert(
                        tk.END,
                        "BG" + str(self.bg_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                    box_bg = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                    self.container_helper["limits BG"][self.file]["ID"].append(self.bg_id)
                    self.container_helper["limits BG"][self.file]["type"].append("custom")
                    self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                    self.canvas.draw()
                    #
                    if self.file_type == "STD":
                        self.container_helper["STD"][filename]["BG"][self.bg_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": box_bg}
                        self.container_helper["positions"]["BG STD"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
                    elif self.file_type == "SMPL":
                        self.container_helper["SMPL"][filename]["BG"][self.bg_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": box_bg}
                        self.container_helper["positions"]["BG SMPL"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
                if self.container_settings["FI"]["Start MAT"].get() != "":
                    filename = self.file.split("/")[-1]
                    x_nearest_start = min(self.times,
                                          key=lambda x: abs(
                                              x - float(self.container_settings["FI"]["Start MAT"].get())))
                    x_nearest_end = min(self.times,
                                        key=lambda x: abs(
                                            x - float(self.container_settings["FI"]["End MAT"].get())))
                    index_start = self.times[self.times == x_nearest_start].index[0]
                    index_end = self.times[self.times == x_nearest_end].index[0]
                    #
                    self.mat_id += 1
                    self.container_listboxes[self.file_type][filename]["MAT"][0].insert(
                        tk.END,
                        "MAT" + str(self.mat_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                    box_mat = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                    self.container_helper["limits MAT"][self.file]["ID"].append(self.mat_id)
                    self.container_helper["limits MAT"][self.file]["type"].append("custom")
                    self.container_helper["limits MAT"][self.file][str(self.mat_id)] = box_mat
                    self.canvas.draw()
                    #
                    if self.file_type == "STD":
                        self.container_helper["STD"][filename]["MAT"][self.mat_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": box_mat}
                        self.container_helper["positions"]["MAT STD"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.mat_id])
                    elif self.file_type == "SMPL":
                        self.container_helper["SMPL"][filename]["MAT"][self.mat_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": box_mat}
                        self.container_helper["positions"]["MAT SMPL"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.mat_id])
                if self.container_settings["FI"]["Start INCL"].get() != "":
                    filename = self.file.split("/")[-1]
                    x_nearest_start = min(self.times,
                                          key=lambda x: abs(
                                              x - float(self.container_settings["FI"]["Start INCL"].get())))
                    x_nearest_end = min(self.times,
                                        key=lambda x: abs(
                                            x - float(self.container_settings["FI"]["End INCL"].get())))
                    index_start = self.times[self.times == x_nearest_start].index[0]
                    index_end = self.times[self.times == x_nearest_end].index[0]
                    #
                    self.incl_id += 1
                    self.container_listboxes[self.file_type][filename]["INCL"][0].insert(
                        tk.END,
                        "INCL" + str(self.incl_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                    box_incl = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.slate_grey_dark)
                    self.container_helper["limits INCL"][self.file]["ID"].append(self.incl_id)
                    self.container_helper["limits INCL"][self.file]["type"].append("custom")
                    self.container_helper["limits INCL"][self.file][str(self.incl_id)] = box_incl
                    self.canvas.draw()
                    #
                    if self.file_type == "STD":
                        self.container_helper["STD"][filename]["INCL"][self.incl_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": box_incl}
                        self.container_helper["positions"]["INCL STD"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.incl_id])
                    elif self.file_type == "SMPL":
                        self.container_helper["SMPL"][filename]["INCL"][self.incl_id] = {
                            "Times": [x_nearest_start, x_nearest_end],
                            "Positions": [index_start, index_end],
                            "Object": box_incl}
                        self.container_helper["positions"]["INCL SMPL"][filename].append(
                            [x_nearest_start, x_nearest_end, index_start, index_end, self.incl_id])
                if self.file_type == "STD" and self.fast_track_std == True:
                    self.container_listboxes[self.file_type][filename_short]["SPK"][0].insert(
                        tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                            self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][
                                0])
                                + "-" + str(self.container_helper["STD"][filename_short]["SPK"][
                                                self.list_isotopes[0]][1]["Times"][1]) + "]")
                    box_spk = self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1][
                        "Object"]
                    self.diagrams_setup[self.file_type][filename_short]["CANVAS"].draw()
                    self.show_smoothed_data()
                elif self.file_type == "SMPL" and self.fast_track_smpl == True:
                    self.container_listboxes[self.file_type][filename_short]["SPK"][0].insert(
                        tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                            self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][
                                0])
                                + "-" + str(self.container_helper["SMPL"][filename_short]["SPK"][
                                                self.list_isotopes[0]][1]["Times"][1]) + "]")
                    box_spk = self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1][
                        "Object"]
                    self.diagrams_setup[self.file_type][filename_short]["CANVAS"].draw()
                    self.show_smoothed_data()
            #
            self.canvas.mpl_connect(
                "button_press_event", lambda event, var=self.container_var["plotting"][filename_short]["RB"][0],
                                             filename=filename_short, ratio_mode=False:
                self.onclick(var, filename, ratio_mode, event))
        else:
            ## Reconstruction
            try:
                # FRAMES
                for frm_item in self.container_gui[filename_short]["Frame"]["General"]:
                    frm_item.grid()
                # LABELS
                for lbl_item in self.container_gui[filename_short]["Label"]["General"]:
                    lbl_item.grid()
                # CHECKBOXES
                for cb_item in self.container_gui[filename_short]["Checkbox"]["General"]:
                    cb_item.grid()
                for isotope in self.list_isotopes:
                    for cb_iso_item in self.container_gui[filename_short]["Checkbox"][isotope]:
                        cb_iso_item.grid()
                # RADIOBUTTONS
                for rbtn_item in self.container_gui[filename_short]["Radiobutton"]["General"]:
                    rbtn_item.grid()
                # BUTTONS
                for btn_item in self.container_gui[filename_short]["Button"]["General"]:
                    btn_item.grid()
                # ENTRY
                for entr_item in self.container_gui[filename_short]["Entry"]["General"]:
                    entr_item.grid()
                # OPTION MENUS
                for optmn_item in self.container_gui[filename_short]["Option Menu"]["General"]:
                    optmn_item.grid()
                #
                for lb_item in self.container_listboxes[self.file_type][filename_short]["BG"]:
                    lb_item.grid()
                for lb_item in self.container_listboxes[self.file_type][filename_short]["MAT"]:
                    lb_item.grid()
                for lb_item in self.container_listboxes[self.file_type][filename_short]["INCL"]:
                    lb_item.grid()
                for lb_item in self.container_listboxes[self.file_type][filename_short]["SPK"]:
                    lb_item.grid()
                self.container_listboxes[self.file_type][filename_short]["ISORAT"].grid()
                #
                self.fig = self.diagrams_setup[self.file_type][filename_short]["FIG"]
                self.ax = self.diagrams_setup[self.file_type][filename_short]["AX"]
                self.canvas = self.diagrams_setup[self.file_type][filename_short]["CANVAS"]
                self.toolbarFrame = self.diagrams_setup[self.file_type][filename_short]["TOOLBARFRAME"]
                self.canvas.get_tk_widget().grid(row=0, column=21, rowspan=26, columnspan=59, sticky="nesw")
                self.toolbarFrame.grid(row=26, column=21, rowspan=2, columnspan=59, sticky="w")
                #
            except:
                print("Error! Fehler mit Plotting Recreation")
            #
            if self.container_settings["FI"]["Start BG"].get() != "" \
                    and len(self.container_helper[self.file_type][filename_short]["BG"]) == 0:
                filename = self.file.split("/")[-1]
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(x - float(self.container_settings["FI"]["Start BG"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(x - float(self.container_settings["FI"]["End BG"].get())))
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.bg_id += 1
                self.container_listboxes[self.file_type][filename]["BG"][0].insert(
                    tk.END, "BG" + str(self.bg_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                box_bg = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.blue_dark)
                self.container_helper["limits BG"][self.file]["ID"].append(self.bg_id)
                self.container_helper["limits BG"][self.file]["type"].append("custom")
                self.container_helper["limits BG"][self.file][str(self.bg_id)] = box_bg
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename]["BG"][self.bg_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": box_bg}
                    self.container_helper["positions"]["BG STD"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename]["BG"][self.bg_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": box_bg}
                    self.container_helper["positions"]["BG SMPL"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.bg_id])
            #
            if self.container_settings["FI"]["Start MAT"].get() != "":
                filename = self.file.split("/")[-1]
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(
                                          x - float(self.container_settings["FI"]["Start MAT"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(
                                        x - float(self.container_settings["FI"]["End MAT"].get())))
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.mat_id += 1
                self.container_listboxes[self.file_type][filename]["MAT"][0].insert(
                    tk.END,
                    "MAT" + str(self.mat_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                box_mat = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.brown_dark)
                self.container_helper["limits MAT"][self.file]["ID"].append(self.mat_id)
                self.container_helper["limits MAT"][self.file]["type"].append("custom")
                self.container_helper["limits MAT"][self.file][str(self.mat_id)] = box_mat
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename]["MAT"][self.mat_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": box_mat}
                    self.container_helper["positions"]["MAT STD"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.mat_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename]["MAT"][self.mat_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": box_mat}
                    self.container_helper["positions"]["MAT SMPL"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.mat_id])
            #
            if self.container_settings["FI"]["Start INCL"].get() != "":
                filename = self.file.split("/")[-1]
                x_nearest_start = min(self.times,
                                      key=lambda x: abs(
                                          x - float(self.container_settings["FI"]["Start INCL"].get())))
                x_nearest_end = min(self.times,
                                    key=lambda x: abs(
                                        x - float(self.container_settings["FI"]["End INCL"].get())))
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.incl_id += 1
                self.container_listboxes[self.file_type][filename]["INCL"][0].insert(
                    tk.END,
                    "INCL" + str(self.incl_id) + " [" + str(x_nearest_start) + "-" + str(x_nearest_end) + "]")
                box_incl = self.ax.axvspan(x_nearest_start, x_nearest_end, alpha=0.25, color=self.slate_grey_dark)
                self.container_helper["limits INCL"][self.file]["ID"].append(self.incl_id)
                self.container_helper["limits INCL"][self.file]["type"].append("custom")
                self.container_helper["limits INCL"][self.file][str(self.incl_id)] = box_incl
                #
                if self.file_type == "STD":
                    self.container_helper["STD"][filename]["INCL"][self.incl_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": box_incl}
                    self.container_helper["positions"]["INCL STD"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.incl_id])
                elif self.file_type == "SMPL":
                    self.container_helper["SMPL"][filename]["INCL"][self.incl_id] = {
                        "Times": [x_nearest_start, x_nearest_end],
                        "Positions": [index_start, index_end],
                        "Object": box_incl}
                    self.container_helper["positions"]["INCL SMPL"][filename].append(
                        [x_nearest_start, x_nearest_end, index_start, index_end, self.incl_id])
            #
            if self.file_type == "STD" and self.fast_track_std == True \
                    and self.container_listboxes[self.file_type][filename_short]["SPK"][0].size() == 0:
                x_nearest_start = float(
                    self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                x_nearest_end = float(
                    self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][1])
                index_start = self.times[self.times == x_nearest_start].index[0]
                index_end = self.times[self.times == x_nearest_end].index[0]
                #
                self.container_listboxes[self.file_type][filename_short]["SPK"][0].insert(
                    tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                        self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                            + "-" + str(self.container_helper["STD"][filename_short]["SPK"][
                                            self.list_isotopes[0]][1]["Times"][1]) + "]")
                box_spk = self.container_helper["STD"][filename_short]["SPK"][self.list_isotopes[0]][1]["Object"]
            elif self.file_type == "SMPL" and self.fast_track_smpl == True \
                    and self.container_listboxes[self.file_type][filename_short]["SPK"][0].size() == 0:
                self.container_listboxes["SMPL"][filename_short]["SPK"][0].insert(
                    tk.END, "[" + ", ".join(self.list_isotopes) + "] #" + str(1) + " [" + str(
                        self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Times"][0])
                            + "-" + str(self.container_helper["SMPL"][filename_short]["SPK"][
                                            self.list_isotopes[0]][1]["Times"][1]) + "]")
                box_spk = self.container_helper["SMPL"][filename_short]["SPK"][self.list_isotopes[0]][1]["Object"]
            #
            self.diagrams_setup[self.file_type][filename_short]["CANVAS"].draw()
            #
            if self.fast_track_std == True:
                self.show_smoothed_data()
            if self.fast_track_smpl == True:
                self.show_smoothed_data()
    #
    def build_plugin_list(self, mode="fi"):
        path = os.getcwd()
        parent = os.path.dirname(path)
        list_files = os.listdir(path=parent+str("/plugins/"))
        for file in list_files:
            if mode == "fi":
                key = re.search("(fi_method_)(\w+)", file)
                if key:
                    if key.group(1) == "fi_method_":
                        name_parts = key.group(2).split("_")
                        name = ""
                        for index, part in enumerate(name_parts):
                            if index < len(name_parts)-1:
                                name += str(part.capitalize()+" ")
                            else:
                                name += str(part.capitalize())
                        self.container_lists["Plugins FI"]["Names"].append(name)
                        self.container_lists["Plugins FI"]["Files"].append(file)
            elif mode == "mi":
                key = re.search("(mi_method_)(\w+)", file)
                if key:
                    if key.group(1) == "mi_method_":
                        name_parts = key.group(2).split("_")
                        name = ""
                        for index, part in enumerate(name_parts):
                            if index < len(name_parts) - 1:
                                name += str(part.capitalize() + " ")
                            else:
                                name += str(part.capitalize())
                        self.container_lists["Plugins MI"]["Names"].append(name)
                        self.container_lists["Plugins MI"]["Files"].append(file)
            elif mode == "se":
                key = re.search("(se_method_)(\w+)", file)
                if key:
                    if key.group(1) == "se_method_":
                        name_parts = key.group(2).split("_")
                        name = ""
                        for index, part in enumerate(name_parts):
                            if index < len(name_parts) - 1:
                                name += str(part.capitalize() + " ")
                            else:
                                name += str(part.capitalize())
                        self.container_lists["Plugins SE"]["Names"].append(name)
                        self.container_lists["Plugins SE"]["Files"].append(file)
        #
        ## TESTING
        # print("TESTING: Plugin Detection")
        # key_list = ["Plugins FI", "Plugins MI", "Plugins SE"]
        # for key in key_list:
        #     print(key)
        #     for key2, values in self.container_lists[key].items():
        #         print(key2, values)
        #
        #
    def create_dwell_time_window(self):
        ## Window Settings
        window_dwell = tk.Toplevel(self.parent)
        window_dwell.title("Salt Correction")
        window_dwell.geometry("600x400+0+0")
        window_dwell.resizable(False, False)
        window_dwell["bg"] = self.green_light
        #
        window_width = 600
        window_heigth = 400
        row_min = 25
        n_rows = int(window_heigth / row_min)
        column_min = 20
        n_columns = int(window_width / column_min)
        #
        for x in range(n_columns):
            tk.Grid.columnconfigure(window_dwell, x, weight=1)
        for y in range(n_rows):
            tk.Grid.rowconfigure(window_dwell, y, weight=1)
        #
        # Rows
        for i in range(0, n_rows):
            window_dwell.grid_rowconfigure(i, minsize=row_min)
        # Columns
        for i in range(0, n_columns):
            window_dwell.grid_columnconfigure(i, minsize=column_min)
        #
        n_isotopes = len(self.container_lists["ISOTOPES"])
        n_columns = 3
        a = n_isotopes / n_columns
        a_int = int(a)
        b = n_isotopes - (n_columns - 1) * a_int
        #
        ## Labels
        lbl_01 = SE(
            parent=window_dwell, row_id=0, column_id=0, n_rows=1, n_columns=2*n_columns*4, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Dwell Time Setup", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_02 = SE(
            parent=window_dwell, row_id=1, column_id=0, n_rows=1, n_columns=8, fg=self.green_light,
            bg=self.green_medium).create_simple_label(
            text="Default Dwell Time", relief=tk.GROOVE, fontsize="sans 10 bold")
        #
        self.container_elements["dwell_times"]["Label"].extend([lbl_01, lbl_02])
        #
        if self.container_var["dwell_times"]["Entry"]["Default"].get() != "0.01":
            var_text = self.container_var["dwell_times"]["Entry"]["Default"].get()
        else:
            var_text = "0.01"
        entr_dwell = SE(
            parent=window_dwell, row_id=1, column_id=8, n_rows=1, n_columns=4,
            fg=self.green_light, bg=self.green_dark).create_simple_entry(
            var=self.container_var["dwell_times"]["Entry"]["Default"], text_default=var_text,
            command=lambda event, var_isotope=None, mode="Default":
            self.change_dwell_times(var_isotope, mode, event))
        #
        self.container_elements["dwell_times"]["Entry"].append(entr_dwell)
        #
        for index, isotope in enumerate(self.container_lists["ISOTOPES"][:b]):
            lbl_isotope = SE(
                parent=window_dwell, row_id=3 + index, column_id=0, n_rows=1, n_columns=4, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            if self.container_var["dwell_times"]["Entry"][isotope].get() != "0.01":
                var_text = self.container_var["dwell_times"]["Entry"][isotope].get()
            else:
                var_text = "0.01"
            entr_dwell = SE(
                parent=window_dwell, row_id=3 + index, column_id=4, n_rows=1, n_columns=4,
                fg=self.green_light, bg=self.green_dark).create_simple_entry(
                var=self.container_var["dwell_times"]["Entry"][isotope], text_default=var_text,
                command=lambda event, var_isotope=isotope, mode="Specific":
                self.change_dwell_times(var_isotope, mode, event))
            #
            self.container_elements["dwell_times"]["Label"].append(lbl_isotope)
            self.container_elements["dwell_times"]["Entry"].append(entr_dwell)
            #
        for index, isotope in enumerate(self.container_lists["ISOTOPES"][b:int(b+a_int)]):
            lbl_isotope = SE(
                parent=window_dwell, row_id=3 + index, column_id=8, n_rows=1, n_columns=4, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            if self.container_var["dwell_times"]["Entry"][isotope].get() != "0.01":
                var_text = self.container_var["dwell_times"]["Entry"][isotope].get()
            else:
                var_text = "0.01"
            entr_dwell = SE(
                parent=window_dwell, row_id=3 + index, column_id=12, n_rows=1, n_columns=4,
                fg=self.green_light, bg=self.green_dark).create_simple_entry(
                var=self.container_var["dwell_times"]["Entry"][isotope], text_default=var_text,
                command=lambda event, var_isotope=isotope, mode="Specific":
                self.change_dwell_times(var_isotope, mode, event))
            #
            self.container_elements["dwell_times"]["Label"].append(lbl_isotope)
            self.container_elements["dwell_times"]["Entry"].append(entr_dwell)
            #
        for index, isotope in enumerate(self.container_lists["ISOTOPES"][-a_int:]):
            lbl_isotope = SE(
                parent=window_dwell, row_id=3 + index, column_id=16, n_rows=1, n_columns=4, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            if self.container_var["dwell_times"]["Entry"][isotope].get() != "0.01":
                var_text = self.container_var["dwell_times"]["Entry"][isotope].get()
            else:
                var_text = "0.01"
            entr_dwell = SE(
                parent=window_dwell, row_id=3 + index, column_id=20, n_rows=1, n_columns=4,
                fg=self.green_light, bg=self.green_dark).create_simple_entry(
                var=self.container_var["dwell_times"]["Entry"][isotope], text_default=var_text,
                command=lambda event, var_isotope=isotope, mode="Specific":
                self.change_dwell_times(var_isotope, mode, event))
            #
            self.container_elements["dwell_times"]["Label"].append(lbl_isotope)
            self.container_elements["dwell_times"]["Entry"].append(entr_dwell)
    #
    def change_dwell_times(self, var_isotope, mode, event):
        if mode == "Default":
            value = self.container_var["dwell_times"]["Entry"]["Default"].get()
            for isotope in self.container_lists["ISOTOPES"]:
                self.container_var["dwell_times"]["Entry"][isotope].set(value)
        elif mode == "Specific":
            value = self.container_var["dwell_times"]["Entry"][var_isotope].get()
            self.container_var["dwell_times"]["Entry"][var_isotope].set(value)
    #
if __name__ == "__main__":
    root = tk.Tk()
    PySILLS(root)
    root.mainloop()