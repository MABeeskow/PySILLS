#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# gui_grid.py
# Maximilian Beeskow
# 15.09.2021
# ----------------------
#
## MODULES
from modules import data, plotting
from modules import standard
from modules.simple_signals import SimpleSignals as SimplSig
from modules.complex_signals import ComplexSignals as CS
from modules.standard import StandardReferenceMaterials as SRM
from modules.sample import InternalStandard as IS
from modules.results import IsotopeRatios as IR
from modules.results import SimpleSignals as SS
from modules import sample
from modules import statistics
import numpy as np
import scipy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, font
from tkinter import filedialog, Text
import tkinter.filedialog as fd
import os, re
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import time
import sys

# LISTS
list_standards = []
data_standards = []
list_samples = []
data_samples = []

# CLASSES
class PySILLS:
    #
    def __init__(self, root, color_bg, files_standard, files_sample):
        # Input Variables
        self.root = root
        self.color_bg = color_bg
        self.files_standard = files_standard
        self.files_sample = files_sample
        #
        # New Variables
        self.positions_bg = []
        self.positions_sig = []
        self.positions_mat = []
        self.srm_found = []
        self.srm_files_indiv = []
        self.srm_std = {}
        self.std_eliminated = {}
        self.smpl_eliminated = {}
        self.times_iw_std = {}
        self.times_iw_smpl = {}
        #
        # Calculation Settings Window
        self.last_entries_time = {"start": tk.StringVar(), "end": tk.StringVar()}
        self.var_entries_time = {"BG": {"start": tk.StringVar(), "end": tk.StringVar()},
                                 "SIG": {"start": tk.StringVar(), "end": tk.StringVar()}}
        self.default_times = {"BG": {}, "SIG": {}}
        #
        for file in self.files_standard:
            parts = file.split("/")
            self.srm_files_indiv.append([file])
            self.srm_std[file] = 0
            self.std_eliminated[file] = {}
            self.times_iw_std[file] = {}
            self.times_iw_std[file]["BG"] = []
            self.times_iw_std[file]["SIG"] = []
            for item in ["BG", "SIG"]:
                self.default_times[item][file] = {"start": tk.StringVar(), "end": tk.StringVar()}
        self.concentrations_is = []
        self.smpl_is_selected = []
        for file in self.files_sample:
            self.smpl_is_selected.append([file, tk.StringVar()])
            self.smpl_eliminated[file] = {}
            self.times_iw_smpl[file] = {}
            self.times_iw_smpl[file]["BG"] = []
            self.times_iw_smpl[file]["SIG"] = []
            for item in ["BG", "SIG"]:
                self.default_times[item][file] = {"start": tk.StringVar(), "end": tk.StringVar()}
        self.srm_isotopes_indiv = []
        self.is_smpl = {}
        self.is_found = []
        self.srm_values = {}
        self.test_data = []
        # Results
        self.results_srm = []
        self.results_intensities = []
        self.results_sensitivities = []
        self.results_concentrations = []
        self.xi_opt = {}
        # self.times_iw_std = {}
        # self.times_iw_smpl = {}
        self.srm_isotopes = {}  # contains the isotopes with assigned SRMs
        self.signal_cleaned = {}
        self.file_actual = files_sample[0]
        #
        dataset_exmpl = data.Data(filename=files_standard[0])
        self.df_exmpl = dataset_exmpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        #
        self.isotopes = list(self.df_exmpl.columns.values)
        self.isotopes.pop(0)
        self.isotopes = np.array(self.isotopes)
        self.times = self.df_exmpl.iloc[:, 0]
        self.isotopes_all = []
        palette_complete = sns.color_palette("nipy_spectral", n_colors=len(self.isotopes)).as_hex()
        j = 0
        for isotope in self.isotopes:
            self.srm_isotopes_indiv.append([isotope, tk.StringVar()])
            self.srm_isotopes[isotope] = 0
            self.isotopes_all.append([isotope, palette_complete[j]])
            j += 1
        self._values = {isotope: self.df_exmpl[isotope] for isotope in self.isotopes}
        #
        self.general_information = {}
        self.general_information["author"] = tk.StringVar()
        self.general_information["origin"] = tk.StringVar()
        #
        # Menubar
        self.create_menubar()
        #
        btn_6 = tk.Button(self.root, text="Save project", fg="#22252D", bg=self.color_bg, highlightthickness=0)
        btn_6.grid(row=10, column=9, rowspan=2, columnspan=2, sticky="nesw")
    #
    def create_menubar(self):
        # MENU
        menu = tk.Menu(self.root)
        self.root.config(menu=menu, bg=self.color_bg)
        #
        ## SIMPLE SIGNALS
        #
        simple_signals_menu = tk.Menu(menu)
        simple_signals_reduction = tk.Menu(menu)
        simple_signals_exploration = tk.Menu(menu)
        menu.add_cascade(label="Simple Signals", menu=simple_signals_menu)
        #
        simple_signals_menu.add_command(label="Calculation Settings",
                                        command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).make_simple_signals_window_settings())
        #
        simple_signals_reduction.add_command(label="Show Concentrations",
                                        command=lambda parent=self.root, color_bg=self.color_bg,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_def=self.positions_sig, times_def_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual: SS(parent, color_bg, signal,
                                                                                        isotopes, times, times_def, times_def_bg,
                                                                                        files_std, files_smpl, file_actual).calculate_concentrations())
        #
        simple_signals_reduction.add_command(label="Concentrations", command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).make_simple_signals_window_concentrations())
        #
        simple_signals_menu.add_cascade(label="Data Reduction", menu=simple_signals_reduction, underline=0)
        #
        simple_signals_exploration.add_command(label="Standard Reference Material",
                                command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).make_simple_signals_window_srm())
        #
        simple_signals_exploration.add_command(label="Isotopic Ratios",
                        command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).data_exploration_signal_ratios())
        #
        simple_signals_exploration.add_command(label="Show Sensitivities",
                                        command=lambda parent=self.root, color_bg=self.color_bg,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_def=self.positions_sig, times_def_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual: SS(parent, color_bg, signal,
                                                                                        isotopes, times, times_def, times_def_bg,
                                                                                        files_std, files_smpl, file_actual).calculate_sensitivities())
        #
        simple_signals_exploration.add_command(label="Sensitivities", command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).make_simple_signals_window_sensitivities())
        #
        simple_signals_exploration.add_command(label="Show Relative Sensitivity Factor",
                                               command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).make_simple_signals_window_rsf())
        #
        simple_signals_menu.add_cascade(label="Data Exploration", menu=simple_signals_exploration, underline=0)
        #
        ## Complex SIGNALS
        #
        complex_signals_menu = tk.Menu(menu)
        menu.add_cascade(label="Complex Signals", menu=complex_signals_menu)
        #
        complex_signals_menu.add_command(label="Standard Reference Material",
                                        command=lambda parent=self.root, color_bg=self.color_bg,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned,
                                                       var_entries_time=self.var_entries_time,
                                                       default_times = self.default_times,
                                                       general_information=self.general_information:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, srm_files_indiv, srm_found,
                                                 results_srm, results_intensities, results_sensitivities,
                                                 results_concentrations, concentrations_is, smpl_is_selected,
                                                 srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned,
                                                 var_entries_time, default_times, general_information).make_simple_signals_window_srm())
        #
        complex_signals_menu.add_command(label="Show Isotopic Ratios",
                                command=lambda parent=self.root,
                                               color_bg=self.color_bg,
                                               signal=self._values, isotopes=self.isotopes: IR(parent, color_bg,
                                                                                              signal, isotopes))
        #
        complex_signals_menu.add_command(label="Segment 1 (Background)", command=lambda parent=self.root, color_bg=self.color_bg,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual, test_data=self.test_data: CS(parent, color_bg, signal,
                                                                                        isotopes, times, times_iw_bg, times_iw_sig, files_std, files_smpl, file_actual, test_data).make_complex_signals_window_SIG1())
        complex_signals_menu.add_command(label="Segment 2+3 (Matrix)", command=lambda parent=self.root, color_bg=self.color_bg,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_def=self.positions_sig, times_def_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual, test_data=self.test_data: CS(parent, color_bg, signal,
                                                                                        isotopes, times, times_def, times_def_bg, files_std, files_smpl, file_actual, test_data).make_complex_signals_window())
        #
        complex_signals_menu.add_command(label="Segment 3 (Inclusion)")
        #
        complex_concentrations_menu = tk.Menu(complex_signals_menu, tearoff=0)
        #
        complex_concentrations_menu.add_command(label="Concentrations")
        #
        complex_concentrations_menu.add_command(label="Matrix-only Tracer")
        #
        complex_concentrations_menu.add_command(label="2nd Internal Standard")
        #
        complex_signals_menu.add_cascade(label="Sample Quantification", menu=complex_concentrations_menu)
        #
        complex_signals_menu.add_command(label="Relative Sensitivity Factor")
        #
        complex_signals_menu.add_command(label="Limit of Detections")
        #

class Plotting:
    def __init__(self, root, data_input, color_bg, geometry_values, dates, times,
                 files_list, files_standard, files_sample, file_actual):
        self.lines = {}
        self.limits_bg = {}
        self.limits_sig = {}
        self.limits_mat = {}
        self.limits_spikes = {}
        self.pos = []
        self.helper_positions = []
        self.helper_indices = []
        self.positions_bg = []
        self.positions_sig = []
        self.positions_mat = []
        self.spike_intervals = []
        self.position_spikes = []
        self.indices_bg = []
        self.indices_bg_alt = []
        self.indices_sig = []
        self.indices_sig_alt = []
        self.indices_mat = []
        self.bg_id = 0
        self.sig_id = 0
        self.mat_id = 0
        self.bg_idlist = []
        self.sig_idlist = []
        self.mat_idlist = []
        self.n_bg = []
        self.n_sig = []
        self.n_mat = []
        self.states_bg = []
        self.states_sig = []
        self.states_mat = []
        self.alkali_metals = []
        self.alkaline_earth_metals = []
        self.transition_metals = []
        self.lanthanides = []
        self.actinides = []
        self.metals = []
        self.metalloids = []
        self.non_metals = []
        self.halogenes = []
        self.noble_gases = []
        self.geometry_values = geometry_values
        self.datestamps = dates
        self.timestamps = times
        self.files_list = files_list
        self.files_standard = files_standard
        self.files_sample = files_sample
        self.file_actual = file_actual

        self.test_data = []
        # SRM variables
        self.srm_found = []
        self.srm_values = {}
        self.srm_files_indiv = []
        for file in self.files_standard:
            parts = file.split("/")
            #self.srm_files_indiv.append([parts[-1]])
            self.srm_files_indiv.append([file])
        #
        # Results
        self.results_srm = []
        self.results_intensities = []
        self.results_sensitivities = []
        self.results_concentrations = []
        #
        ## Calculation Settings (ALL)
        self.signal_cleaned = {}
        self.concentrations_is = []
        self.smpl_is_selected = []
        for file in self.files_sample:
            self.smpl_is_selected.append([file, tk.StringVar()])
        self.srm_isotopes_indiv = []

        self.std_eliminated = {}
        self.smpl_eliminated = {}
        self.is_smpl = {}
        self.is_found = []
        self.srm_std = {}
        self.srm_isotopes = {}  # contains the isotopes with assigned SRMs
        self.times_iw_std = {}
        self.times_iw_smpl = {}
        for file in self.files_standard:
            self.times_iw_std[file] = 0
            self.srm_std[file] = 0
            self.std_eliminated[file] = {}
        for file in self.files_sample:
            self.is_smpl[file] = 0
            self.times_iw_smpl[file] = 0
            self.smpl_eliminated[file] = {}
        #
        ## Sensitivity
        self.xi_opt = {}
        #
        # print("Selected File:", self.file_actual)
        # print("Files Standard:", self.files_standard)
        # print("Files Sample:", self.files_sample)

        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        try:
            if self.canvas:
                self.canvas.destroy()
            if self.toolbar:
                self.toolbar.destroy()
        except AttributeError:
            pass

        self.canvas = None
        self.toolbar = None
        #
        self.color_background = color_bg
        self.root = root

        self.data = data_input
        self.times = self.data.iloc[:, 0]
        self.time_step = [self.times[i]-self.times[i-1] for i in range(1, len(self.times))]
        self.time_step.insert(0, self.times[0])
        self.time_step = np.around(self.time_step, 3)
        # print("Time step:", self.time_step)

        self.names = list(self.data.columns.values)
        self.names.pop(0)
        self.find_elements(isotopes=self.names)

        for isotope in self.names:
            self.srm_isotopes_indiv.append([isotope, tk.StringVar()])
            self.srm_isotopes[isotope] = 0

        # CHEMISTRY
        palette_complete = sns.color_palette("nipy_spectral", n_colors=len(self.names)).as_hex()
        palette_alkali_metals = sns.light_palette("seagreen", n_colors=len(self.alkali_metals)).as_hex()
        palette_alkaline_earth_metals = sns.light_palette("darkgreen", n_colors=len(self.alkaline_earth_metals)).as_hex()
        palette_transition_metals = sns.light_palette("royalblue", n_colors=len(self.transition_metals)).as_hex()
        palette_lanthanides = sns.light_palette("skyblue", n_colors=len(self.lanthanides)).as_hex()
        palette_actinides = sns.light_palette("teal", n_colors=len(self.actinides)).as_hex()
        palette_metals = sns.light_palette("mediumorchid", n_colors=len(self.metals)).as_hex()
        palette_metalloids = sns.light_palette("magenta", n_colors=len(self.metalloids)).as_hex()
        palette_non_metals = sns.light_palette("firebrick", n_colors=len(self.non_metals)).as_hex()
        palette_halogenes = sns.light_palette("orangered", n_colors=len(self.halogenes)).as_hex()
        palette_noble_gases = sns.light_palette("gold", n_colors=len(self.noble_gases)).as_hex()
        for i in range(len(palette_alkali_metals)):
            self.alkali_metals[i].append(palette_alkali_metals[i])
        for i in range(len(palette_alkaline_earth_metals)):
            self.alkaline_earth_metals[i].append(palette_alkaline_earth_metals[i])
        for i in range(len(palette_transition_metals)):
            self.transition_metals[i].append(palette_transition_metals[i])
        for i in range(len(palette_lanthanides)):
            self.lanthanides[i].append(palette_lanthanides[i])
        for i in range(len(palette_actinides)):
            self.actinides[i].append(palette_actinides[i])
        for i in range(len(palette_metals)):
            self.metals[i].append(palette_metals[i])
        for i in range(len(palette_metalloids)):
            self.metalloids[i].append(palette_metalloids[i])
        for i in range(len(palette_non_metals)):
            self.non_metals[i].append(palette_non_metals[i])
        for i in range(len(palette_halogenes)):
            self.halogenes[i].append(palette_halogenes[i])
        for i in range(len(palette_noble_gases)):
            self.noble_gases[i].append(palette_noble_gases[i])
        # print("C h e m i s t r y:")
        # print("Alkali metals:", self.alkali_metals)
        # print("Alkaline earth metals:", self.alkaline_earth_metals)
        # print("Transition metals:", self.transition_metals)
        # print("Lanthanides:", self.lanthanides)
        # print("Actinides:", self.actinides)
        # print("Metals:", self.metals)
        # print("Metalloids:", self.metalloids)
        # print("Non-metals:", self.non_metals)
        # print("Halogenes:", self.halogenes)
        # print("Noble gases:", self.noble_gases)
        self.isotopes = []
        self.isotopes_all = []
        # print(palette_complete)
        j = 0
        for name in self.names:
            self.isotopes_all.append([name, palette_complete[j]])
            j += 1
            for i in range(len(self.alkali_metals)):
                if name == self.alkali_metals[i][1]:
                    self.isotopes.append([name, self.alkali_metals[i][2]])
            for i in range(len(self.alkaline_earth_metals)):
                if name == self.alkaline_earth_metals[i][1]:
                    self.isotopes.append([name, self.alkaline_earth_metals[i][2]])
            for i in range(len(self.transition_metals)):
                if name == self.transition_metals[i][1]:
                    self.isotopes.append([name, self.transition_metals[i][2]])
            for i in range(len(self.lanthanides)):
                if name == self.lanthanides[i][1]:
                    self.isotopes.append([name, self.lanthanides[i][2]])
            for i in range(len(self.actinides)):
                if name == self.actinides[i][1]:
                    self.isotopes.append([name, self.actinides[i][2]])
            for i in range(len(self.metals)):
                if name == self.metals[i][1]:
                    self.isotopes.append([name, self.metals[i][2]])
            for i in range(len(self.metalloids)):
                if name == self.metalloids[i][1]:
                    self.isotopes.append([name, self.metalloids[i][2]])
            for i in range(len(self.non_metals)):
                if name == self.non_metals[i][1]:
                    self.isotopes.append([name, self.non_metals[i][2]])
            for i in range(len(self.halogenes)):
                if name == self.halogenes[i][1]:
                    self.isotopes.append([name, self.halogenes[i][2]])
            for i in range(len(self.noble_gases)):
                if name == self.noble_gases[i][1]:
                    self.isotopes.append([name, self.noble_gases[i][2]])
        # for i in range(len(self.names)):
        #     print(i, self.names[i], self.isotopes[i])
        # for i in range(len(self.names)):
        #     print(i, self.isotopes_all[i])

        # SETUP AREA A
        padx_value = 0
        pady_value = 0
        ipadx_value = 1
        ipady_value = 1
        width_a = 1160
        height_a = 700
        width_a1 = 3*self.geometry_values[0][0] + self.geometry_values[0][1]
        height_a1 = height_a
        width_a2 = self.geometry_values[0][3] + self.geometry_values[0][4]
        height_a2 = 25
        width_a3 = self.geometry_values[0][3]
        height_a5 = self.geometry_values[1][2] + self.geometry_values[1][3]
        width_a6 = width_a2
        width_a7 = width_a6
        width_b2 = 240
        height_b3 = 315
        width_b5 = 2*self.geometry_values[0][6]
        width_b8 = width_b5
        height_b8 = self.geometry_values[1][2] + self.geometry_values[1][3]
        width_b9 = self.geometry_values[0][6]
        width_b10 = width_b9
        height_b9 = self.geometry_values[1][0]

        self.a1 = tk.Frame(self.root, bg=self.color_background, width=width_a1, height=height_a1)
        self.a1.grid(row=0, column=0, rowspan=8, columnspan=5, padx=padx_value, pady=pady_value,
                     ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        self.a5 = tk.Frame(self.root, bg=self.color_background, width=width_a2, height=height_a5)
        self.a5.grid(row=4, column=5, columnspan=2, rowspan=2, padx=padx_value, pady=pady_value,
                     ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

        self.b8 = tk.Frame(self.root, bg=self.color_background, width=width_b8, height=height_b8)
        self.b8.grid(row=4, column=9, columnspan=2, rowspan=2, padx=padx_value, pady=pady_value,
                     ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        self.b9 = tk.Frame(self.root, bg=self.color_background, width=width_b9, height=height_b9)
        self.b9.grid(row=6, column=9, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")
        self.b10 = tk.Frame(self.root, bg=self.color_background, width=width_b10, height=height_b9)
        self.b10.grid(row=6, column=10, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")
        self.b11 = tk.Frame(self.root, bg=self.color_background, width=width_b10, height=height_b9)
        self.b11.grid(row=7, column=9, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")
        self.b12 = tk.Frame(self.root, bg=self.color_background, width=width_b10, height=height_b9)
        self.b12.grid(row=7, column=10, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")

        label_b8_01 = tk.Label(self.b8, text="Chemical overview")
        label_b8_01.pack()
        if len(self.alkali_metals) > 0:
            label_b8_02 = tk.Label(self.b8, text="Alkali metals:\n"+", ".join(map(str, np.array(self.alkali_metals,
                                                                                                dtype=object)[:, 1])))
        else:
            label_b8_02 = tk.Label(self.b8, text="Alkali metals:")
        label_b8_02.pack()
        if len(self.alkaline_earth_metals) > 0:
            label_b8_03 = tk.Label(self.b8, text="Earth alkaline metals:\n"+
                                                 ", ".join(map(str, np.array(self.alkaline_earth_metals,
                                                                             dtype=object)[:, 1])))
        else:
            label_b8_03 = tk.Label(self.b8, text="Earth alkaline metals:")
        label_b8_03.pack()
        if len(self.transition_metals) > 0:
            label_b8_04 = tk.Label(self.b8, text="Transition metals:\n"+
                                                 ", ".join(map(str, np.array(self.transition_metals,
                                                                             dtype=object)[:, 1])))
        else:
            label_b8_04 = tk.Label(self.b8, text="Transition metals:")
        label_b8_04.pack()
        if len(self.lanthanides) > 0:
            label_b8_05 = tk.Label(self.b8, text="Lanthanides:\n"+", ".join(map(str, np.array(self.lanthanides,
                                                                                             dtype=object)[:, 1])))
        else:
            label_b8_05 = tk.Label(self.b8, text="Lanthanides:")
        label_b8_05.pack()
        if len(self.actinides) > 0:
            label_b8_06 = tk.Label(self.b8, text="Actinides:\n"+", ".join(map(str, np.array(self.actinides,
                                                                                             dtype=object)[:, 1])))
        else:
            label_b8_06 = tk.Label(self.b8, text="Actinides:")
        label_b8_06.pack()
        if len(self.metals) > 0:
            label_b8_07 = tk.Label(self.b8, text="Metals:\n"+", ".join(map(str, np.array(self.metals,
                                                                                             dtype=object)[:, 1])))
        else:
            label_b8_07 = tk.Label(self.b8, text="Metals:")
        label_b8_07.pack()
        if len(self.metalloids) > 0:
            label_b8_08 = tk.Label(self.b8, text="Metalloids:\n"+", ".join(map(str, np.array(self.metalloids,
                                                                                             dtype=object)[:, 1])))
        else:
            label_b8_08 = tk.Label(self.b8, text="Metalloids:")
        label_b8_08.pack()
        if len(self.non_metals) > 0:
            label_b8_09 = tk.Label(self.b8, text="Non-metals:\n"+", ".join(map(str, np.array(self.non_metals,
                                                                                             dtype=object)[:, 1])))
        else:
            label_b8_09 = tk.Label(self.b8, text="Non-metals:")
        label_b8_09.pack()
        if len(self.halogenes) > 0:
            label_b8_10 = tk.Label(self.b8, text="Halogenes:\n"+", ".join(map(str, np.array(self.halogenes,
                                                                                            dtype=object)[:, 1])))
        else:
            label_b8_10 = tk.Label(self.b8, text="Halogenes:")
        label_b8_10.pack()
        # if len(self.noble_gases) > 0:
        #     label_b8_11 = tk.Label(self.b8, text="Noble gases:\n"+str(np.array(self.noble_gases, dtype=object)[:, 0]))
        # else:
        #     label_b8_11 = tk.Label(self.b8, text="Noble gases:\n")
        # label_b8_11.pack()
        label_b8_11 = tk.Label(self.b8, text="")
        label_b8_11.pack()
        label_b8_12 = tk.Label(self.b8, text="Measuring date:\n"+"/".join(map(str, self.datestamps[0])))
        label_b8_12.pack()
        label_b8_13 = tk.Label(self.b8, text="Measured time:\n"+":".join(map(str, self.timestamps[0]))+" - "+
                                             ":".join(map(str, self.timestamps[1])))
        label_b8_13.pack()

        label_b8_15 = tk.Label(self.root, text="Author:")
        label_b8_15.grid(row=6, column=9, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")
        self.author = tk.StringVar()
        self.entry_b8_01 = tk.Entry(self.root, textvariable=self.author)
        self.entry_b8_01.grid(row=6, column=10, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")
        self.entry_b8_01.bind("<Return>", lambda event, var=self.author: self.on_return(var, event))
        self.sample_origin = tk.StringVar()
        label_b8_16 = tk.Label(self.root, text="Sample origin:")
        label_b8_16.grid(row=7, column=9, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")
        self.entry_b8_02 = tk.Entry(self.root, textvariable=self.sample_origin)
        self.entry_b8_02.bind("<Return>", lambda event, var=self.sample_origin: self.on_return(var, event))
        self.entry_b8_02.grid(row=7, column=10, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                     sticky="nesw")

        self._states = {name: tk.BooleanVar(name=name) for name in self.names}
        self._values = {name: self.data[name] for name in self.names}
        self.values = np.array([[self.data[name] for name in self.names]])
        self.x_max = np.amax(self.times)
        self.y_max = np.amax(self.values)

        self.var_spikes = tk.IntVar()
        btn_a2 = tk.Button(self.root, text="Spike elimination", fg="#22252D", bg=self.color_background,
                           command=lambda data_input=self._values: self.spike_elimination(data_input))
        btn_a2.grid(row=0, column=5, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
                     ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        btn_a3 = tk.Button(self.root, text="Show all", fg="#22252D", bg=self.color_background,
                           command=lambda: self.cb_select_all(states=self._states))
        btn_a3.grid(row=2, column=5, rowspan=2, padx=padx_value, pady=pady_value,
                     ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        btn_a4 = tk.Button(self.root, text="Show none", fg="#22252D", bg=self.color_background,
                           command=lambda: self.cb_deselect_all(states=self._states))
        btn_a4.grid(row=2, column=6, rowspan=2, padx=padx_value, pady=pady_value,
                     ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

        # Settings C
        width_c1 = self.geometry_values[0][0]
        width_c2 = self.geometry_values[0][1]
        width_c11 = self.geometry_values[0][2] + self.geometry_values[0][3] + self.geometry_values[0][4]
        height_c1 = 2*self.geometry_values[1][0]
        height_c2 = 6*height_c1
        height_c11 = 8*height_c1

        c2 = tk.Frame(self.root, bg=self.color_background, width=width_c1, height=height_c2)
        c2.grid(row=10, column=0, rowspan=6, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                sticky="nesw")
        c4 = tk.Frame(self.root, bg=self.color_background, width=width_c1, height=height_c2)
        c4.grid(row=10, column=1, rowspan=6, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                sticky="nesw")
        c6 = tk.Frame(self.root, bg=self.color_background, width=width_c1, height=height_c2)
        c6.grid(row=10, column=2, rowspan=6, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value,
                sticky="nesw")
        c11 = tk.Frame(self.root, bg=self.color_background, width=width_c11, height=height_c11)
        c11.grid(row=8, column=4, rowspan=8, columnspan=3, padx=padx_value, pady=pady_value,
                 ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

        # Radiobuttons C
        self.var_c = tk.IntVar()
        self.var_c.set(4)
        btn_c1 = tk.Radiobutton(self.root, text="Background", variable=self.var_c, value=1, bg="salmon",
                                activebackground="salmon", command=lambda: self.select_radiobutton(var=self.var_c))
        btn_c1.grid(row=8, column=0, rowspan=2, sticky="nesw")
        btn_c3 = tk.Radiobutton(self.root, text="Signal", variable=self.var_c, value=2, bg="cornflowerblue",
                                activebackground="cornflowerblue", command=lambda: self.select_radiobutton(var=self.var_c))
        btn_c3.grid(row=8, column=1, rowspan=2, sticky="nesw")
        btn_c5 = tk.Radiobutton(self.root, text="Matrix", variable=self.var_c, value=3, bg="lightgreen",
                                activebackground="lightgreen", command=lambda: self.select_radiobutton(var=self.var_c))
        btn_c5.grid(row=8, column=2, rowspan=2, sticky="nesw")
        btn_c7 = tk.Radiobutton(self.root, text="None", variable=self.var_c, value=4, bg="gray",
                                activebackground="gray", command=lambda: self.select_radiobutton(var=self.var_c))
        btn_c7.grid(row=8, column=3, rowspan=2, sticky="nesw")

        # Buttons C
        btn_c8 = tk.Button(self.root, text="Remove interval", fg="#22252D", bg=self.color_background,
                           command=lambda var=self.var_c: self.delete_csv(var))
        btn_c8.grid(row=10, column=3, rowspan=2, sticky="nesw")

        # Options menu
        label_c9 = tk.Label(self.root, text="Internal standard:")
        label_c9.grid(row=12, column=3, rowspan=2, sticky="nesw")
        self.isotopes = np.array(self.isotopes)
        option_list = self.isotopes[:, 0]
        self.internal_standard = tk.StringVar(self.root)
        self.internal_standard.set(option_list[0])
        opt = tk.OptionMenu(self.root, self.internal_standard, *option_list,
                            command=self.option_changed)
        opt.grid(row=14, column=3, rowspan=2, sticky="nesw")


        # Listboxes C
        name_platform = sys.platform
        if name_platform == "darwin":
            foreground = "black"
        elif name_platform == "linux":
            foreground = "white"
        elif name_platform == "win32":
            foreground = "black"
        self.background_listbox = self.create_list(parent=c2, val_width=width_c1, val_height=height_c2)
        self.signal_listbox = self.create_list(parent=c4, val_width=width_c1, val_height=height_c2)
        self.matrix_listbox = self.create_list(parent=c6, val_width=width_c1, val_height=height_c2)

        # Treeviews C
        ttk.Style().configure("Treeview", background=self.color_background, foreground="black",
                              fieldbackground=self.color_background)
        myFont = font.Font(size="11", weight="normal")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=myFont, background="gray", pressed_color="gray",
                        highlight_color="gray", foreground=foreground)
        style.map("Treeview.Heading", background = [("pressed", "!focus", "gray"),
                                                    ("active", "gray"), ("disabled", self.color_background)])
        columns = ("#1", "#2")
        self.ratios_treeview = ttk.Treeview(c11, columns=columns, show="headings")
        self.ratios_treeview.heading("#1", text="Isotope ratio")
        self.ratios_treeview.column("#1", minwidth=0, width=130, stretch=tk.NO)
        self.ratios_treeview.heading("#2", text="Value")
        self.ratios_treeview.column("#2", minwidth=0, width=130, stretch=tk.NO)
        self.ratios_treeview.pack()

        # Menubar
        self.create_menubar()

        self.fig = Figure(figsize=(10, 5), facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot()

        # Plotting the diagram
        i = 0
        for name, state in self._states.items():
            state.set(True)
            cb = tk.Checkbutton(master=self.a5, variable=state, text=name,
                                height=1, width=15, anchor=tk.W, bg=self.color_background)
            cb.pack()
            state.trace_add("write", self._value_changed)
            if state.get():
                ln = self.ax.plot(self.times, self._values[name], label=name,
                                  color=self.isotopes_all[i][1], visible=True)
                self.lines[name] = ln
                i += 1
        self.ax.grid(True)
        self.ax.set_yscale("log")
        self.ax.set_xlim(left=0, right=self.x_max)
        self.ax.set_xticks(np.arange(0, self.x_max, 10))
        self.ax.set_ylim(top=1.5*self.y_max)
        self.ax.set_axisbelow(True)
        self.ax.set_xlabel("Time (s)", labelpad=0.5)
        self.ax.set_ylabel("Signal (cps)", labelpad=0.5)

        self.fig.subplots_adjust(bottom=0.125, top=0.975, left=0.075, right=0.975)

        self.ax.legend(fontsize="x-small", framealpha=1.0, bbox_to_anchor=(0.125, 0.015), loc=3, borderaxespad=0,
                  bbox_transform=plt.gcf().transFigure, ncol=int(len(self._states)/2+1))
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.a1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.a1)
        self.toolbar.config(background=self.color_background)
        self.toolbar._message_label.config(background=self.color_background)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect('button_press_event', lambda event, var=self.var_c: self.onclick(var, event))
        #self.canvas.mpl_connect('button_press_event', lambda event, var=self.var_spikes: self.on_click_spikes(var,
        #                                                                                                      event))

    def create_menubar(self):
        # MENU
        menu = tk.Menu(self.root)
        self.root.config(menu=menu, bg=self.color_background)
        #
        ## SIMPLE SIGNALS
        #
        simple_signals_menu = tk.Menu(menu)
        simple_signals_reduction = tk.Menu(menu)
        simple_signals_exploration = tk.Menu(menu)
        menu.add_cascade(label="Simple Signals", menu=simple_signals_menu)
        #
        simple_signals_menu.add_command(label="Calculation Settings",
                                        command=lambda parent=self.root, color_bg=self.color_background,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual,
                                                       test_data=self.test_data, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, file_actual, test_data,
                                                 srm_files_indiv, srm_found, results_srm, results_intensities,
                                                 results_sensitivities, results_concentrations,
                                                 concentrations_is, smpl_is_selected, srm_isotopes_indiv, xi_opt,
                                                 times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned).make_simple_signals_window_settings())
        #
        simple_signals_reduction.add_command(label="Show Concentrations",
                                        command=lambda parent=self.root, color_bg=self.color_background,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_def=self.positions_sig, times_def_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual: SS(parent, color_bg, signal,
                                                                                        isotopes, times, times_def, times_def_bg,
                                                                                        files_std, files_smpl, file_actual).calculate_concentrations())
        #
        simple_signals_reduction.add_command(label="Concentrations", command=lambda parent=self.root, color_bg=self.color_background,
                                                                                    isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual,
                                                       test_data=self.test_data, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, file_actual, test_data,
                                                 srm_files_indiv, srm_found, results_srm, results_intensities,
                                                 results_sensitivities, results_concentrations,
                                                 concentrations_is, smpl_is_selected, srm_isotopes_indiv, xi_opt,
                                                 times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned).make_simple_signals_window_concentrations())
        #
        simple_signals_menu.add_cascade(label="Data Reduction", menu=simple_signals_reduction, underline=0)
        #
        simple_signals_exploration.add_command(label="Standard Reference Material",
                                command=lambda parent=self.root, color_bg=self.color_background,
                                               isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual,
                                                       test_data=self.test_data, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, file_actual, test_data,
                                                 srm_files_indiv, srm_found, results_srm, results_intensities,
                                                 results_sensitivities, results_concentrations,
                                                 concentrations_is, smpl_is_selected, srm_isotopes_indiv, xi_opt,
                                                 times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned).make_simple_signals_window_srm())
        #
        simple_signals_exploration.add_command(label="Show Isotopic Ratios",
                        command=lambda parent=self.root,
                                       color_bg=self.color_background,
                                       signal=self._values, isotopes=self.isotopes: IR(parent, color_bg,
                                                                                      signal, isotopes))
        #
        simple_signals_exploration.add_command(label="Show Sensitivities",
                                        command=lambda parent=self.root, color_bg=self.color_background,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_def=self.positions_sig, times_def_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual: SS(parent, color_bg, signal,
                                                                                        isotopes, times, times_def, times_def_bg,
                                                                                        files_std, files_smpl, file_actual).calculate_sensitivities())
        #
        simple_signals_exploration.add_command(label="Sensitivities", command=lambda parent=self.root, color_bg=self.color_background,
                                                                                     isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual,
                                                       test_data=self.test_data, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, file_actual, test_data,
                                                 srm_files_indiv, srm_found, results_srm, results_intensities,
                                                 results_sensitivities, results_concentrations,
                                                 concentrations_is, smpl_is_selected, srm_isotopes_indiv, xi_opt,
                                                 times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned).make_simple_signals_window_sensitivities())
        #
        simple_signals_exploration.add_command(label="Show Relative Sensitivity Factor",
                                               command=lambda parent=self.root, color_bg=self.color_background,
                                                              isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual,
                                                       test_data=self.test_data, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, file_actual, test_data,
                                                 srm_files_indiv, srm_found, results_srm, results_intensities,
                                                 results_sensitivities, results_concentrations,
                                                 concentrations_is, smpl_is_selected, srm_isotopes_indiv, xi_opt,
                                                 times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned).make_simple_signals_window_rsf())
        #
        simple_signals_menu.add_cascade(label="Data Exploration", menu=simple_signals_exploration, underline=0)
        #
        ## Complex SIGNALS
        #
        complex_signals_menu = tk.Menu(menu)
        menu.add_cascade(label="Complex Signals", menu=complex_signals_menu)
        #
        complex_signals_menu.add_command(label="Standard Reference Material",
                                        command=lambda parent=self.root, color_bg=self.color_background,
                                                       isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg,
                                                       times_iw_mat=self.positions_mat, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual,
                                                       test_data=self.test_data, srm_files_indiv=self.srm_files_indiv,
                                                       srm_found=self.srm_found, results_srm=self.results_srm,
                                                       results_intensities=self.results_intensities,
                                                       results_sensitivities=self.results_sensitivities,
                                                       results_concentrations=self.results_concentrations,
                                                       concentrations_is=self.concentrations_is,
                                                       smpl_is_selected=self.smpl_is_selected,
                                                       srm_isotopes_indiv=self.srm_isotopes_indiv, xi_opt=self.xi_opt,
                                                       times_iw_std=self.times_iw_std, times_iw_smpl=self.times_iw_smpl,
                                                       is_smpl=self.is_smpl, srm_isotopes=self.srm_isotopes,
                                                       srm_std=self.srm_std, isotopes_colors=self.isotopes_all,
                                                       std_eliminated=self.std_eliminated,
                                                       smpl_eliminated=self.smpl_eliminated, is_found=self.is_found,
                                                       srm_values=self.srm_values, signal_cleaned=self.signal_cleaned:
                                        SimplSig(parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig,
                                                 times_iw_mat, files_std, files_smpl, file_actual, test_data,
                                                 srm_files_indiv, srm_found, results_srm, results_intensities,
                                                 results_sensitivities, results_concentrations,
                                                 concentrations_is, smpl_is_selected, srm_isotopes_indiv, xi_opt,
                                                 times_iw_std, times_iw_smpl, is_smpl,
                                                 srm_isotopes, srm_std, isotopes_colors, std_eliminated,
                                                 smpl_eliminated, is_found, srm_values, signal_cleaned).make_simple_signals_window_srm())
        #
        complex_signals_menu.add_command(label="Show Isotopic Ratios",
                                command=lambda parent=self.root,
                                               color_bg=self.color_background,
                                               signal=self._values, isotopes=self.isotopes: IR(parent, color_bg,
                                                                                              signal, isotopes))
        #
        complex_signals_menu.add_command(label="Segment 1 (Background)", command=lambda parent=self.root, color_bg=self.color_background,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_iw_sig=self.positions_sig, times_iw_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual, test_data=self.test_data: CS(parent, color_bg, signal,
                                                                                        isotopes, times, times_iw_bg, times_iw_sig, files_std, files_smpl, file_actual, test_data).make_complex_signals_window_SIG1())
        complex_signals_menu.add_command(label="Segment 2+3 (Matrix)", command=lambda parent=self.root, color_bg=self.color_background,
                                                       signal=self._values, isotopes=self.isotopes, times=self.times,
                                                       times_def=self.positions_sig, times_def_bg=self.positions_bg, files_std=self.files_standard,
                                                       files_smpl=self.files_sample, file_actual=self.file_actual, test_data=self.test_data: CS(parent, color_bg, signal,
                                                                                        isotopes, times, times_def, times_def_bg, files_std, files_smpl, file_actual, test_data).make_complex_signals_window())
        #
        complex_signals_menu.add_command(label="Segment 3 (Inclusion)")
        #
        complex_concentrations_menu = tk.Menu(complex_signals_menu, tearoff=0)
        #
        complex_concentrations_menu.add_command(label="Concentrations")
        #
        complex_concentrations_menu.add_command(label="Matrix-only Tracer")
        #
        complex_concentrations_menu.add_command(label="2nd Internal Standard")
        #
        complex_signals_menu.add_cascade(label="Sample Quantification", menu=complex_concentrations_menu)
        #
        complex_signals_menu.add_command(label="Relative Sensitivity Factor")
        #
        complex_signals_menu.add_command(label="Limit of Detections")
        #
    def on_return(self, var, event):
        if var:
            print(var.get())

    def option_changed(self, op):
        item = self.signal_listbox.curselection()
        data.DataReduction(isotopes=self.isotopes[:, 0],
                           signals=self._values).calculate_signal_rations(internal_standard=self.internal_standard.get(),
                                                                          signal_indices=self.indices_sig_alt[item[0]],
                                                                          treeview=self.ratios_treeview)

    def find_elements(self, isotopes):
        alkali_metals = ["Li", "Na", "K", "Rb", "Cs", "Fr"]
        alkaline_earth_metals = ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"]
        transition_metals = ["Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh",
                             "Pd", "Ag", "Cd", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Rf", "Db", "Sg",
                             "Bh", "Hs", "Mt", "Ds", "Rg", "Cn"]
        lanthanides = ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]
        actinides = ["Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"]
        metals = ["Al", "Ga", "In", "Tl", "Nh", "Sn", "Pb", "Fl", "Bi", "Mc", "Lv"]
        metalloids = ["B", "Si", "Ge", "As", "Sb", "Te", "Po"]
        non_metals = ["H", "C", "N", "O", "P", "S", "Se"]
        halogenes = ["F", "Cl", "Br", "I", "At", "Ts"]
        noble_gases = ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"]

        for isotope in isotopes:
            element = re.search("(\D+)(\d+)", isotope)
            if element:
                if element.group(1) in alkali_metals:
                    self.alkali_metals.append([element.group(1), element.group(0)])
                elif element.group(1) in alkaline_earth_metals:
                    self.alkaline_earth_metals.append([element.group(1), element.group(0)])
                elif element.group(1) in transition_metals:
                    self.transition_metals.append([element.group(1), element.group(0)])
                elif element.group(1) in lanthanides:
                    self.lanthanides.append([element.group(1), element.group(0)])
                elif element.group(1) in actinides:
                    self.actinides.append([element.group(1), element.group(0)])
                elif element.group(1) in metals:
                    self.metals.append([element.group(1), element.group(0)])
                elif element.group(1) in metalloids:
                    self.metalloids.append([element.group(1), element.group(0)])
                elif element.group(1) in non_metals:
                    self.non_metals.append([element.group(1), element.group(0)])
                elif element.group(1) in halogenes:
                    self.halogenes.append([element.group(1), element.group(0)])
                elif element.group(1) in noble_gases:
                    self.noble_gases.append([element.group(1), element.group(0)])
            else:
                print("Nothing found!")
        # print("Alkali metals:", self.alkali_metals)
        # print("Alkaline earth metals:", self.alkaline_earth_metals)
        # print("Transition metals:", self.transition_metals)
        # print("Lanthanides:", self.lanthanides)
        # print("Actinides:", self.actinides)
        # print("Metals:", self.metals)
        # print("Metalloids:", self.metalloids)
        # print("Non-metals:", self.non_metals)
        # print("Halogenes:", self.halogenes)
        # print("Noble gases:", self.noble_gases)

    def on_click_spikes(self, var, event):
        if var.get():
            print("Variable", var.get())
            x_nearest = min(self.times, key=lambda x:abs(x-event.xdata))
            self.spike_intervals.append([x_nearest])
            print("Spikes:", self.spike_intervals)
        if (len(self.spike_intervals) % 2) == 0:
            index_start = self.times.index(self.spike_intervals[-2])
            index_end = self.times.index(self.spike_intervals[-1])
            print("Start", index_start)
            print("End", index_end)

    def onclick(self, var, event):
        if len(self.helper_positions) == 2 and len(self.helper_indices) == 2:
            self.helper_positions.clear()
            self.helper_indices.clear()
        #
        x_nearest = min(self.times, key=lambda x: abs(x-event.xdata))
        self.helper_positions.append(x_nearest)
        self.helper_indices.append(self.times[self.times == x_nearest].index[0])
        #
        if len(self.helper_positions)+len(self.helper_indices) == 4:
            if var.get() == 1:
                self.bg_id += 1
                self.bg_idlist.append(self.bg_id)
                self.positions_bg.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
                self.background_listbox.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(self.helper_positions[0])+"-"+
                                               str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
                                               str(self.helper_indices[1]) +"]")
                box_bg = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25, color="red")
                self.limits_bg[str(self.bg_id)] = box_bg
                self.canvas.draw()
            elif var.get() == 2:
                self.sig_id += 1
                self.sig_idlist.append(self.sig_id)
                self.positions_sig.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
                self.indices_sig_alt.append([self.helper_indices[0], self.helper_indices[1]])
                self.signal_listbox.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(self.helper_positions[0])+"-"+
                                               str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
                                               str(self.helper_indices[1]) +"]")
                box_sig = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25, color="blue")
                self.limits_sig[str(self.sig_id)] = box_sig
                self.canvas.draw()
            elif var.get() == 3:
                self.mat_id += 1
                self.mat_idlist.append(self.mat_id)
                self.positions_mat.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
                self.matrix_listbox.insert(tk.END, "MAT"+str(self.mat_id)+" ["+str(self.helper_positions[0])+"-"+
                                               str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
                                               str(self.helper_indices[1]) +"]")
                box_mat = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25, color="green")
                self.limits_mat[str(self.mat_id)] = box_mat
                self.canvas.draw()

    def _value_changed(self, name, _, op):
        if self._states[name].get():
            self.lines[name][0].set_visible(True)
        else:
            self.lines[name][0].set_visible(False)
        self.canvas.draw()

    def cb_select_all(self, states):
        for state in states.values():
            state.set(True)
        state.trace_add("write", self._value_changed)
    #
    def cb_deselect_all(self, states):
        for state in states.values():
            state.set(False)
        state.trace_add("write", self._value_changed)

    def plot_csv(self, parent, listbox, list_data, color_bg, geometries, list_standard, list_sample, event):
        color_background = color_bg
        geometry_values = geometries
        t = time.process_time()
        id = listbox.curselection()
        dataset = data.Data(filename=list_data[id[0]])
        file_selected = list_data[id[0]]
        df = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        dates, times = data.Data(filename=list_data[id[0]]).import_as_list()
        Plotting(root=parent, data_input=df, color_bg=color_background, geometry_values=geometry_values,
                 dates=dates, times=times, files_list=list_data, files_standard=list_standard,
                 files_sample=list_sample, file_actual=file_selected)
        elapsed_time = time.process_time() - t
        print("Execution time:", elapsed_time)

    def select_radiobutton(self, var):
        variable = var.get()

    def create_list(self, parent, val_width, val_height):
        listbox = tk.Listbox(parent, bg=self.color_background, width=val_width, height=val_height)
        scrollbar_y = tk.Scrollbar(parent, orient="vertical")
        scrollbar_x = tk.Scrollbar(parent, orient="horizontal")
        listbox.config(yscrollcommand = scrollbar_y.set, xscrollcommand = scrollbar_x.set)
        scrollbar_y.config(command = listbox.yview)
        scrollbar_x.config(command = listbox.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        listbox.pack(side="left", fill="both")
        scrollbar_y.pack(side="right", fill="y")
        return listbox

    def delete_csv(self, var):
        if var.get() == 1:
            item = self.background_listbox.curselection()
            self.positions_bg.remove(self.positions_bg[item[0]])
            self.background_listbox.delete(tk.ANCHOR)
            self.limits_bg[str(self.bg_idlist[item[0]])].set_visible(False)
            self.canvas.draw()
            del self.bg_idlist[item[0]]
        elif var.get() == 2:
            item = self.signal_listbox.curselection()
            self.positions_sig.remove(self.positions_sig[item[0]])
            self.indices_sig_alt.remove(self.indices_sig_alt[item[0]])
            self.signal_listbox.delete(tk.ANCHOR)
            self.limits_sig[str(self.sig_idlist[item[0]])].set_visible(False)
            self.canvas.draw()
            del self.sig_idlist[item[0]]
        elif var.get() == 3:
            item = self.matrix_listbox.curselection()
            self.positions_mat.remove(self.positions_mat[item[0]])
            self.matrix_listbox.delete(tk.ANCHOR)
            self.limits_mat[str(self.mat_idlist[item[0]])].set_visible(False)
            self.canvas.draw()
            del self.mat_idlist[item[0]]
        #
        return self.positions_bg, self.positions_sig, self.positions_mat

    def add_limits(self, var):
        if var.get() == 1:
            position = Plotting.onclick()
            print("1", position)
        elif var.get() == 2:
            position = Plotting.onclick()
            print("2", position)
        elif var.get() == 3:
            position = Plotting.onclick()
            print("3", position)
    #
    def spike_elimination(self, data_input):
        for isotope in self.names:
            print("Isotope:", isotope)
            spikes = statistics.OutlierAnalysis(data_input=data_input[isotope].values).grubbs_test_two_sided()
        self.auto_segmentation(data_input=data_input)
    #
    def auto_segmentation(self, data_input):
        keys = ["Li7", "Mg24", "Ti49", "Zn66", "Rb85", "Sr88", "Cs133", "Ba137", "Pb208"]
        for key in keys:
            if key in self.isotopes:
                segments_bg = statistics.Segmentation(data_input=data_input[key],
                                                   isotopes=self.isotopes).find_background_segments(isotope=key)
                statistics.Segmentation(data_input=data_input[key],
                                        isotopes=self.isotopes).calculate_change(bg1_end=segments_bg[0][1],
                                                                                 bg2_start=segments_bg[1][0])
    #
    def new_window(title="Another window"):
        toplevel = tk.Toplevel()
        toplevel.title(title)
        toplevel.focus_set()

# FUNCTIONS
def main():

    def newFile():
        print("New File!")

    def openFile():
        name = filedialog.askopenfile()
        print(name)

    def create_list(parent, val_width, val_height):
        listbox = tk.Listbox(parent, bg=color_background, width=val_width, height=val_height)
        scrollbar_y = tk.Scrollbar(parent, orient="vertical")
        scrollbar_x = tk.Scrollbar(parent, orient="horizontal")
        listbox.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.config(command=listbox.yview)
        scrollbar_x.config(command=listbox.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        listbox.pack(side="left", fill="both")
        scrollbar_y.pack(side="right", fill="y")
        return listbox

    def add_limits(var):
        if var.get() == 1:
            position = Plotting.onclick()
            print("1", position)
        elif var.get() == 2:
            position = Plotting.onclick()
            print("2", position)
        elif var.get() == 3:
            position = Plotting.onclick()
            print("3", position)

    def open_csv(var):
        filename = fd.askopenfilenames(parent=root, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        if var.get() == 1:
            for i in filename:
                if i not in list_standards:
                    list_standards.append(i)
                    file_parts = i.split("/")
                    standard_listbox.insert(tk.END, file_parts[-1])
        elif var.get() == 2:
            for i in filename:
                if i not in list_samples:
                    list_samples.append(i)
                    file_parts = i.split("/")
                    sample_listbox.insert(tk.END, file_parts[-1])
        return filename

    def delete_csv(var):
        if var.get() == 1:
            item = standard_listbox.curselection()
            list_standards.remove(list_standards[item[0]])
            standard_listbox.delete(tk.ANCHOR)
        elif var.get() == 2:
            item = sample_listbox.curselection()
            list_samples.remove(list_samples[item[0]])
            sample_listbox.delete(tk.ANCHOR)
        return list_standards, list_samples

    def saveFile():
        name = filedialog.asksaveasfile()

    def load_file():
        name = filedialog.askopenfilename()

    def save_as_filename():
        files = [("All files", "*.*"),
                 ("Python files", "*.py"),
                 ("Text document", "*.txt"),
                 ("PySILLS file", "*.pysills")]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files)

    def newWindow():
        toplevel = tk.Toplevel()
        toplevel.title('Another window')
        toplevel.focus_set()

    def new_window(title="Another window"):
        toplevel = tk.Toplevel()
        toplevel.title(title)
        toplevel.focus_set()

    def select_radiobutton(var):
        variable = var.get()

    def start_pysills():
        PySILLS(root=root, color_bg=color_background, files_standard=list_standards, files_sample=list_samples)

    # VARIABLES

    # SYSTEM CHECK
    name_os = os.name
    name_platform = sys.platform
    if name_platform == "darwin":
        color_background = "#FFFFFF"
        button_color_bg = "lightgrey"
    elif name_platform == "linux":
        color_background = "#DADBD9"
    elif name_platform == "win32":
        color_background = "#F0F0EE"

    # FRAME
    root = tk.Tk()
    root.geometry("1600x900")
    root.title("PySILLS")
    root.resizable(0, 0)

    # GEOMETRY
    geometries = []
    width_c0 = 250
    width_c3 = 150
    width_c4 = 110
    width_c5 = 70
    width_c6 = 80
    width_c7 = 100
    width_c9 = 120
    height_r0 = 25
    height_r1 = height_r0
    height_r2 = 300
    height_r3 = 250
    height_r4 = 25
    height_r5 = height_r4
    height_r6 = height_r0
    height_r7 = height_r6
    height_r8 = height_r6
    height_r9 = height_r6
    heights = [height_r0, height_r1, height_r2, height_r3, height_r4, height_r5, height_r6, height_r7, height_r8,
               height_r9]
    geometries.append([width_c0, width_c3, width_c4, width_c5, width_c6, width_c7, width_c9])
    geometries.append(heights)

    # Settings A
    # Settings B
    width_b1 = width_c7
    width_b5 = 2*width_c9
    width_b6 = 2*width_b1
    height_b1 = height_r0
    height_b5 = 4*height_b1
    height_b6 = height_r2
    height_b9 = height_r3
    height_b10 = height_r4
    # Settings C
    height_c1 = height_r0
    height_c2 = 6*height_c1
    # Settings D
    width_d1 = 2*width_c7
    width_d5 = 2*width_c9
    height_d = height_r0


    for x in range(11):
        tk.Grid.columnconfigure(root, x, weight=1)
    for y in range(16):
        tk.Grid.rowconfigure(root, y, weight=1)

    # GENERAL SETUP
    for i in range(0, 3):
        root.grid_columnconfigure(i, minsize=width_c0)
    root.grid_columnconfigure(3, minsize=width_c3)
    root.grid_columnconfigure(4, minsize=width_c4)
    root.grid_columnconfigure(5, minsize=width_c5)
    root.grid_columnconfigure(6, minsize=width_c6)
    for i in range(7, 9):
        root.grid_columnconfigure(i, minsize=width_c7)
    for i in range(9, 11):
        root.grid_columnconfigure(i, minsize=width_c9)

    for i in range(0, 4):
        root.grid_rowconfigure(i, minsize=height_r0)
    root.grid_rowconfigure(4, minsize=height_r2)
    root.grid_rowconfigure(5, minsize=height_r3)
    for i in range(6, 16):
        root.grid_rowconfigure(i, minsize=height_r4)

    ## GENERAL SETTINGS
    padx_value = 0
    pady_value = 0
    ipadx_value = 1
    ipady_value = 1

    ## AREA A
    a = tk.Frame(root, bg=color_background, width=1160, height=700)
    a.grid(row=0, column=0, rowspan=8, columnspan=7, padx=padx_value, pady=pady_value, ipadx=0, ipady=0, sticky="nesw")

    if name_platform == "darwin":
        pysills_logo_1 = tk.PhotoImage(file="../documentation/images/PySILLS_Logo_large_MacOS.png")
    elif name_platform == "linux":
        pysills_logo_1 = tk.PhotoImage(file="../documentation/images/PySILLS_Logo_large.png")
    elif name_platform == "win32":
        pysills_logo_1 = tk.PhotoImage(file="../documentation/images/PySILLS_Logo_large_Win32.png")
    pysills_logo_1 = pysills_logo_1.subsample(1, 1)
    logo_1 = tk.Label(a, image=pysills_logo_1, borderwidth=0, highlightthickness=0).pack(fill=tk.BOTH, expand=tk.YES)

    ## AREA B
    b5 = tk.Frame(root, bg=color_background, width=width_b5, height=height_b5)
    b5.grid(row=0, column=9, columnspan=2, rowspan=4, padx=padx_value, pady=pady_value,
            ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    b6 = tk.Frame(root, bg=color_background, width=width_b6, height=height_b6)
    b6.grid(row=4, column=7, columnspan=2, padx=padx_value, pady=pady_value,
            ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    b7 = tk.Frame(root, bg=color_background, width=width_b6, height=height_b6)
    b7.grid(row=5, column=7, rowspan=3, columnspan=2, padx=padx_value, pady=pady_value,
            ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

    # Radiobuttons B
    var_b = tk.IntVar()
    var_b.set(1)
    r1 = tk.Radiobutton(root, text="Standard", variable=var_b, value=1, command=lambda: select_radiobutton(var=var_b))
    r1.grid(row=2, column=7, rowspan=2, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    r2 = tk.Radiobutton(root, text="Sample", variable=var_b, value=2, command=lambda: select_radiobutton(var=var_b))
    r2.grid(row=2, column=8, rowspan=2, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

    btn_b1 = tk.Button(root, text="Add", fg="#22252D", bg=color_background, highlightthickness=0, command=lambda: open_csv(var=var_b))
    btn_b2 = tk.Button(root, text="Remove", fg="#22252D", bg=color_background, highlightthickness=0, command=lambda: delete_csv(var=var_b))
    btn_b1.grid(row=0, column=7, rowspan=2, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    btn_b2.grid(row=0, column=8, rowspan=2, padx=padx_value, pady=pady_value, ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

    if name_platform == "darwin":
        pysills_logo_2 = tk.PhotoImage(file="../documentation/images/PySILLS_Logo_small_MacOS.png")
    elif name_platform == "linux":
        pysills_logo_2 = tk.PhotoImage(file="../documentation/images/PySILLS_Logo_small.png")
    elif name_platform == "win32":
        pysills_logo_2 = tk.PhotoImage(file="../documentation/images/PySILLS_Logo_small_Win32.png")
    pysills_logo_2 = pysills_logo_2.subsample(6, 6)

    btn_logo = tk.Button(root, image=pysills_logo_2, highlightthickness=0, command=start_pysills)
    btn_logo.grid(row=0, column=9, columnspan=2, rowspan=4, padx=padx_value, pady=pady_value,
            ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

    # Listboxes B
    standard_listbox = create_list(parent=b6, val_width=width_b6, val_height=height_b6)
    sample_listbox = create_list(parent=b7, val_width=width_b6, val_height=height_b6)

    standard_listbox.bind("<Double-1>", lambda event, parent=root, listbox=standard_listbox, list_data=list_standards,
                                               color_bg=color_background, geometries=geometries,
                                               list_standard=list_standards, list_sample=list_samples: Plotting.plot_csv("", parent, listbox, list_data, color_bg, geometries, list_standard, list_sample, event))
    sample_listbox.bind("<Double-1>", lambda event, parent=root, listbox=sample_listbox, list_data=list_samples,
                                             color_bg=color_background, geometries=geometries,
                                             list_standard=list_standards, list_sample=list_samples: Plotting.plot_csv("", parent, listbox, list_data, color_bg, geometries, list_standard, list_sample, event))

    ## AREA C
    c = tk.Frame(root, bg=color_background, width=1160, height=200)
    c.grid(row=8, column=0, rowspan=8, columnspan=7, padx=padx_value, pady=pady_value, ipadx=0, ipady=0, sticky="nesw")

    ## AREA D
    # Buttons
    btn_1 = tk.Button(root, text="Calculation settings", fg="#22252D", bg=color_background, highlightthickness=0,
                      command=newWindow)
    btn_1.grid(row=8, column=7, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
               ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    btn_2 = tk.Button(root, text="Documentation", fg="#22252D", bg=color_background, highlightthickness=0,
                      command=newWindow)
    btn_2.grid(row=10, column=7, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
               ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    btn_3 = tk.Button(root, text="Frequently Asked Questions", fg="#22252D", bg=color_background, highlightthickness=0,
                      command=newWindow)
    btn_3.grid(row=12, column=7, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
               ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    btn_5 = tk.Button(root, text="Load project", fg="#22252D", bg=color_background, highlightthickness=0,
                      command=load_file)
    btn_5.grid(row=8, column=9, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
               ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    # btn_6 = tk.Button(root, text="Save project", fg="#22252D", bg=color_background, highlightthickness=0,
    #                   command=save_as_filename)
    # btn_6.grid(row=10, column=9, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
    #            ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
    btn_7 = tk.Button(root, text="Quit PySILLS", fg="#22252D", bg=color_background, highlightthickness=0,
                      command=root.quit)
    btn_7.grid(row=12, column=9, rowspan=2, columnspan=2, padx=padx_value, pady=pady_value,
               ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")

    root.mainloop()

# PROGRAM
if __name__ == "__main__":
    main()


