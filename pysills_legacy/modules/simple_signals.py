#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# complex_signals.py
# Maximilian Beeskow
# 14.09.2021
# ----------------------
#
## MODULES
import os, datetime, time
import csv
import tkinter as tk
from tkinter import ttk, font
import tkinter.filedialog as fd
from modules.gui_elements import SimpleElements as SE
from modules.chemistry import PeriodicSystemOfElements as PSE
from modules.chemistry import PeriodicSystem as PS
from modules import data
from modules.essential_functions import Essentials, EssentialsSRM
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.colors as mcolors
#
## CLASSES
class SimpleSignals:
    #
    def __init__(self, parent, color_bg, isotopes, times, times_iw_bg, times_iw_sig, times_iw_mat,
                 files_std, files_smpl, srm_files_indiv, srm_found, results_srm,
                 results_intensities, results_sensitivities, results_concentrations, concentrations_is,
                 smpl_is_selected, srm_isotopes_indiv, xi_opt, times_iw_std, times_iw_smpl, is_smpl, srm_isotopes,
                 srm_std, isotopes_colors, std_eliminiated, smpl_eliminated, is_found, srm_values, signal_cleaned,
                 var_entries_time, default_times, general_information):
        self.parent = parent
        self.color_bg = color_bg
        self.color_fg = "black"
        self.isotopes_colors = isotopes_colors
        self.isotopes = isotopes
        self.times = times
        self.times_iw_bg = times_iw_bg
        self.times_iw_sig = times_iw_sig
        self.times_iw_mat = times_iw_mat
        self.files_std = files_std
        self.files_smpl = files_smpl
        #
        self.pse_list = PSE().get_element_names()
        self.n_isotopes = len(self.isotopes)
        self.measured_isotopes = self.isotopes
        #
        self.index_start_bg = 0
        self.index_end_bg = 10
        self.indices_bg = [self.index_start_bg, self.index_end_bg]
        self.index_start_sig = 0
        self.index_end_sig = len(self.times)-1
        self.indices_sig = [self.index_start_sig, self.index_end_sig]
        #
        self.srm_values_display = np.zeros(len(self.pse_list))
        self.srm_values = srm_values
        self.var_srm_display = tk.StringVar()
        self.var_srm_display.set("Select SRM")
        self.var_srm_default = tk.StringVar()
        self.var_srm_default.set("Select SRM")
        self.var_srm_isotopes_default = tk.StringVar()
        self.var_srm_isotopes_default.set("Select SRM")
        self.var_srm_indiv = []
        self.var_srm_isotope_indiv = []
        self.srm_values_indiv = []
        self.positions_bg_std = {}
        self.positions_bg_smpl = {}
        self.positions_sig_std = {}
        self.positions_sig_smpl = {}
        self.limits_sig = {}
        self.limits_bg = {}
        self.sig_idlist = {}
        self.srm_files_indiv = srm_files_indiv
        self.srm_found = srm_found
        # Results
        self.results_srm = results_srm
        self.results_intensities = results_intensities
        self.results_sensitivities = results_sensitivities
        self.results_concentrations = results_concentrations
        #
        # Calculation Settings
        self.signal_cleaned = signal_cleaned
        self.concentrations_is = concentrations_is
        self.smpl_is_selected = smpl_is_selected
        self.srm_isotopes_indiv = srm_isotopes_indiv
        self.time_iw_std = times_iw_std
        self.time_iw_smpl = times_iw_smpl
        self.is_smpl = is_smpl
        self.srm_isotopes = srm_isotopes
        self.srm_std = srm_std
        self.std_eliminated = std_eliminiated
        self.smpl_eliminated = smpl_eliminated
        self.is_found = is_found
        self.default_times = default_times
        #
        # Optimization coefficients of xi
        self.xi_opt = xi_opt
        #
        # Calculation Settings Window
        self.var_entries_time = var_entries_time
        self.last_entry_t_start = tk.StringVar()
        #
        for file in self.files_std:
            self.var_srm_indiv.append([file, tk.StringVar()])
            self.positions_bg_std[file] = []
            self.positions_sig_std[file] = []
            self.limits_bg[file] = {}
            self.limits_sig[file] = {}
            self.sig_idlist[file] = []
            self.limits_bg[file]["ID"] = []
            self.limits_sig[file]["ID"] = []
            self.limits_bg[file]["type"] = []
            self.limits_sig[file]["type"] = []
        for file in self.files_smpl:
            self.positions_bg_smpl[file] = []
            self.positions_sig_smpl[file] = []
            self.limits_bg[file] = {}
            self.limits_sig[file] = {}
            self.sig_idlist[file] = []
            self.limits_bg[file]["ID"] = []
            self.limits_sig[file]["ID"] = []
            self.limits_bg[file]["type"] = []
            self.limits_sig[file]["type"] = []
        for isotope in self.isotopes:
            self.var_srm_isotope_indiv.append([isotope, tk.StringVar()])
        self.spike_settings = {}
        self.spike_settings["deviation"] = tk.StringVar()
        self.spike_settings["threshold"] = tk.StringVar()
        self.general_information = general_information
    #
    def make_simple_signals_window_srm(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.srm_label_container = []
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(2*200 + 4*50 + 4*130 + 2*15)
        height = int(23*30 + 1*15)
        self.srm_window = tk.Toplevel(self.parent)
        self.srm_window.geometry(str(width)+"x"+str(height))
        self.srm_window.title("Simple Signals - Standard Reference Material")
        #
        for y in range(24):
            tk.Grid.rowconfigure(self.srm_window, y, weight=1)
        for x in range(12):
            tk.Grid.columnconfigure(self.srm_window, x, weight=1)
        #
        # Rows
        for i in range(0, 23):
            self.srm_window.grid_rowconfigure(i, minsize=30)
        self.srm_window.grid_rowconfigure(23, minsize=15)
        # Columns
        for i in range(0, 2):
            self.srm_window.grid_columnconfigure(i, minsize=200)
        self.srm_window.grid_columnconfigure(2, minsize=15)
        for i in range(3, 11, 2):
            self.srm_window.grid_columnconfigure(i, minsize=50)
        for i in range(4, 12, 2):
            self.srm_window.grid_columnconfigure(i, minsize=130)
        self.srm_window.grid_columnconfigure(11, minsize=15)
        #
        ################################################################################################################
        ## LABELS ######################################################################################################
        #
        # self.files_std_short = []
        # for file in self.files_std:
        #     parts = file.split("/")
        #     self.files_std_short.append(parts[-1])
        # for i in range(len(self.files_std_short)):
        #     SE(parent=self.srm_window, row_id=i+2, column_id=0, fg=self.color_fg,
        #        bg=self.color_bg).create_label(text=self.files_std_short[i])
        #
        j = 0
        k = 0
        for i in range(len(self.pse_list)):
            SE(parent=self.srm_window, row_id=j, column_id=k+3, fg=self.color_fg,
               bg=self.color_bg).create_label(text=self.pse_list[i])
            SE(parent=self.srm_window, row_id=j, column_id=k+4, fg=self.color_fg,
               bg=self.color_bg).create_label_variable(label_container=self.srm_label_container, relief=tk.SUNKEN)
            j += 1
            if j > 22:
                k += 2
                j = 0
        #
        ################################################################################################################
        ## Buttons #####################################################################################################
        #
        SE(parent=self.srm_window, row_id=0, column_id=1, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Load SRM", command=lambda parent=self.srm_window: self.load_srm_from_csv(parent))
        #
        ################################################################################################################
        ## Option Menu #################################################################################################
        #
        # Places the SRM option menu, which shows the concentration values
        SE(parent=self.srm_window, row_id=0, column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_option_srm(var_srm=self.var_srm_display, text_set="Show SRM",
                                               command=lambda op, var_srm=self.var_srm_display:
                                               self.option_changed_srm(var_srm, op))
        # Places the SRM option menu, which sets the default SRM for the individuel standard files
        # SE(parent=self.srm_window, row_id=1, column_id=0, n_columns=2, fg=self.color_fg,
        #    bg=self.color_bg).create_option_srm(var_srm=self.var_srm_default, text_set="Select SRM",
        #                                        command=lambda op, var_srm_default=self.var_srm_default:
        #                                        self.change_option_srm_default(var_srm_default, op))
        # Places the SRM option menues, which let the user select a individuel SRM dataset for every standard file
        # i = 0
        # for var_srm in self.var_srm_indiv:
        #     SE(parent=self.srm_window, row_id=2+i, column_id=1, fg=self.color_fg,
        #    bg=self.color_bg).create_option_srm(var_srm=var_srm[1], text_set="Select SRM", command=lambda op, var_srm=var_srm[1], index=i: self.change_option_srm(var_srm, index, op))
        #     i += 1
    #
    def change_option_srm(self, var_srm, index, op, settings=True):
        if len(self.srm_files_indiv[index]) > 1:
            self.srm_files_indiv[index] = self.srm_files_indiv[index][:1]
            self.srm_files_indiv[index].append(var_srm.get())
            self.srm_std[self.srm_files_indiv[index][0]] = var_srm.get()
        else:
            self.srm_files_indiv[index].append(var_srm.get())
            self.srm_std[self.srm_files_indiv[index][0]] = var_srm.get()
        srm_found_helper = np.array(self.srm_files_indiv)[:, 1]
        for item in srm_found_helper:
            if item not in self.srm_found:
                self.srm_found.append(item)
                self.srm_values[item] = {}
                EssentialsSRM().place_srm_values(srm_name=item, srm_dict=self.srm_values)
        for item in self.srm_found:
            if item not in srm_found_helper:
                self.srm_found.remove(item)
                self.srm_values.pop(item, None)
        #
        if settings == True:
            self.opt_menu_srm_isotopes.destroy()
            self.opt_menu_srm_isotopes = SE(parent=self.settings_window, row_id=int(len(self.measured_isotopes)+1),
                                            column_id=12, fg=self.color_fg,
                                            bg=self.color_bg).create_option_srm(var_srm=self.var_srm_isotopes_default,
                                                                                text_set=self.srm_found[0],
                                                                                option_list=self.srm_found,
                                                                                command=lambda op, var_default=self.var_srm_isotopes_default,
                                                                                               var_indiv=self.srm_isotopes_indiv:
                                                                                self.change_option_default_isotopes(var_default, var_indiv, op))
            #
            for i in range(len(self.srm_isotopes_container)):
                self.srm_isotopes_container[i].destroy()
            self.srm_isotopes_container.clear()
            i = 0
            for item in self.srm_isotopes_indiv:
                opt_menu_srm_isotope = SE(parent=self.settings_window, row_id=1+i, column_id=12, fg=self.color_fg,
                                          bg=self.color_bg).create_option_srm(var_srm=item[1], text_set=self.srm_found[0],
                                                                              option_list=self.srm_found,
                                                                              command=lambda op, var_srm=item[1],
                                                                                             index=i: self.change_option_isotopes(var_srm, index, op))
                self.srm_isotopes_container.append(opt_menu_srm_isotope)
                i += 1
    #
    def change_option_srm_default(self, var_srm_default, op, settings=True):
        i = 0
        for var_srm in self.var_srm_indiv:
            var_srm[1].set(var_srm_default.get())
            self.srm_std[var_srm[0]] = var_srm_default.get()
            if len(self.srm_files_indiv[i]) == 1:
                self.srm_files_indiv[i].append(var_srm_default.get())
            else:
                self.srm_files_indiv[i].pop(1)
                self.srm_files_indiv[i].append(var_srm_default.get())
            i += 1
        srm_found_helper = np.array(self.srm_files_indiv)[:, 1]
        self.srm_found.clear()
        self.srm_values.clear()
        for item in srm_found_helper:
            if item not in self.srm_found:
                self.srm_found.append(item)
                self.srm_values[item] = {}
                EssentialsSRM().place_srm_values(srm_name=item, srm_dict=self.srm_values)
        #
        if settings == True:
            self.opt_menu_srm_isotopes.destroy()
            self.opt_menu_srm_isotopes = SE(parent=self.settings_window, row_id=int(len(self.measured_isotopes)+1),
                                            column_id=12, fg=self.color_fg,
                                            bg=self.color_bg).create_option_srm(var_srm=self.var_srm_isotopes_default,
                                                                                text_set=self.srm_found[0],
                                                                                option_list=self.srm_found,
                                                                                command=lambda op, var_default=self.var_srm_isotopes_default,
                                                                                               var_indiv=self.srm_isotopes_indiv:
                                                                                self.change_option_default_isotopes(var_default, var_indiv, op))
            #
            for i in range(len(self.srm_isotopes_container)):
                self.srm_isotopes_container[i].destroy()
            self.srm_isotopes_container.clear()
            i = 0
            for item in self.srm_isotopes_indiv:
                opt_menu_srm_isotope = SE(parent=self.settings_window, row_id=1+i, column_id=12, fg=self.color_fg,
                                          bg=self.color_bg).create_option_srm(var_srm=item[1], text_set=self.srm_found[0],
                                                                              option_list=self.srm_found,
                                                                              command=lambda op, var_srm=item[1],
                                                                                             index=i: self.change_option_isotopes(var_srm, index, op))
                self.srm_isotopes_container.append(opt_menu_srm_isotope)
                i += 1
            #
            for item in self.srm_isotopes_indiv:
                item[1].set(self.var_srm_isotopes_default.get())
                self.srm_isotopes[item[0]] = self.var_srm_isotopes_default.get()
    #
    def option_changed_srm(self, var_srm, op):
        #
        path = os.getcwd()
        parent = os.path.dirname(path)
        if var_srm.get() == "NIST 606":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_606.csv"))
        elif var_srm.get() == "NIST 610":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610.csv"))
        elif var_srm.get() == "NIST 610 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_GeoReM.csv"))
        elif var_srm.get() == "NIST 610 (Spandler)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_Spandler.csv"))
        elif var_srm.get() == "NIST 611":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611.csv"))
        elif var_srm.get() == "NIST 611 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611_GeoReM.csv"))
        elif var_srm.get() == "NIST 612":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612.csv"))
        elif var_srm.get() == "NIST 612 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612_GeoReM.csv"))
        elif var_srm.get() == "NIST 613":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613.csv"))
        elif var_srm.get() == "NIST 613 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613_GeoReM.csv"))
        elif var_srm.get() == "NIST 614":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614.csv"))
        elif var_srm.get() == "NIST 614 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614_GeoReM.csv"))
        elif var_srm.get() == "NIST 615":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615.csv"))
        elif var_srm.get() == "NIST 615 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615_GeoReM.csv"))
        elif var_srm.get() == "NIST 616":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616.csv"))
        elif var_srm.get() == "NIST 616 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616_GeoReM.csv"))
        elif var_srm.get() == "NIST 617":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617.csv"))
        elif var_srm.get() == "NIST 617 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617_GeoReM.csv"))
        elif var_srm.get() == "USGS BCR-2G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_BCR2G_GeoReM.csv"))
        elif var_srm.get() == "USGS GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSD1G_GeoReM.csv"))
        elif var_srm.get() == "USGS GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSE1G_GeoReM.csv"))
        elif var_srm.get() == "B6":
            data_srm = data.general().importSRM(filename=parent+str("/lib/B6.csv"))
        #
        for i in range(len(self.pse_list)):
            self.srm_label_container[i].configure(text=0.0)
        for item in data_srm:
            for i in range(len(self.pse_list)):
                if self.pse_list[i] == item[0]:
                    self.srm_label_container[i].configure(text=item[1])
    #
    def load_srm_from_csv(self, parent):
        filename = fd.askopenfilenames(parent=parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        data_srm = data.general().importSRM(filename=filename[0])
        #
        for i in range(len(self.pse_list)):
            self.srm_label_container[i].configure(text=0.0)
        for item in data_srm:
            for i in range(len(self.pse_list)):
                if self.pse_list[i] == item[0]:
                    self.srm_label_container[i].configure(text=item[1])
    #
    ####################################################################################################################
    # WINDOW - CALCULATION SETTINGS ####################################################################################
    ####################################################################################################################
    #
    def make_simple_signals_window_settings(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        if len(self.concentrations_is) > 0:
            self.concentrations_is = []
        self.entries_smpl_container = []
        self.srm_isotopes_container = []
        #
        order_std = []
        order_smpl = []
        for file_std in self.files_std:
            dates, times = data.Data(filename=file_std).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            order_std.append([file_std, t_start])
        for file_smpl in self.files_smpl:
            dates, times = data.Data(filename=file_smpl).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            order_smpl.append([file_smpl, t_start])
        order_std = np.array(order_std)
        order_smpl = np.array(order_smpl)
        self.files_std = order_std[order_std[:, 1].argsort()][:, 0].tolist()
        self.files_smpl = order_smpl[order_smpl[:, 1].argsort()][:, 0].tolist()
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(150 + 200 + 60 + 2*15 + 150 + 145 + 160 + 60 + 2*15 + 80 + 200 + 15)
        if self.n_isotopes >= 22:
            height = int(30 + self.n_isotopes*30 + 30 + 15)
        elif len(self.files_smpl) < self.n_isotopes:
            height = int((self.n_isotopes + 6)*30 + 15)
        elif len(self.files_smpl) >= self.n_isotopes:
            height = int((len(self.files_smpl) + 5)*30 + 15)
        elif int(len(self.files_std)+14) > len(self.files_smpl) or int(len(self.files_std)+14) > self.n_isotopes:
            height = int((int(len(self.files_std)+14))*30 + 15)
        #
        self.settings_window = tk.Toplevel(self.parent)
        self.settings_window.geometry(str(width)+"x"+str(height))
        self.settings_window.title("Simple Signals: Calculation Settings")
        #
        if self.n_isotopes >= 22:
            for y in range(int(3+self.n_isotopes)):
                tk.Grid.rowconfigure(self.settings_window, y, weight=1)
        elif len(self.files_smpl) < self.n_isotopes:
            for y in range(int(self.n_isotopes + 7)):
                tk.Grid.rowconfigure(self.settings_window, y, weight=1)
        elif len(self.files_smpl) >= self.n_isotopes:
            for y in range(int(len(self.files_smpl) + 6)):
                tk.Grid.rowconfigure(self.settings_window, y, weight=1)
        elif int(len(self.files_std)+14) > len(self.files_smpl) or int(len(self.files_std)+14) > self.n_isotopes:
            for y in range(int(len(self.files_std)+15)):
                tk.Grid.rowconfigure(self.settings_window, y, weight=1)
        for x in range(14):
            tk.Grid.columnconfigure(self.settings_window, x, weight=1)
        #
        # Rows
        if self.n_isotopes >= 22:
            for i in range(0, int(2+self.n_isotopes)):
                self.settings_window.grid_rowconfigure(i, minsize=30)
            self.settings_window.grid_rowconfigure(int(1+self.n_isotopes+2), minsize=15)
        elif len(self.files_smpl) < self.n_isotopes:
            for i in range(0, int(self.n_isotopes+6)):
                self.settings_window.grid_rowconfigure(i, minsize=30)
            self.settings_window.grid_rowconfigure(int(self.n_isotopes+6), minsize=15)
        elif len(self.files_smpl) >= self.n_isotopes:
            for i in range(0, int(len(self.files_smpl)+5)):
                self.settings_window.grid_rowconfigure(i, minsize=30)
            self.settings_window.grid_rowconfigure(int(len(self.files_smpl)+5), minsize=15)
        elif int(len(self.files_std)+14) > len(self.files_smpl) or int(len(self.files_std)+14) > self.n_isotopes:
            for i in range(0, int(len(self.files_std)+14)):
                self.settings_window.grid_rowconfigure(i, minsize=30)
            self.settings_window.grid_rowconfigure(int(len(self.files_std)+15), minsize=15)
        # Columns
        self.settings_window.grid_columnconfigure(0, minsize=150)
        self.settings_window.grid_columnconfigure(1, minsize=200)
        self.settings_window.grid_columnconfigure(2, minsize=60)
        self.settings_window.grid_columnconfigure(3, minsize=15)
        self.settings_window.grid_columnconfigure(4, minsize=15)
        self.settings_window.grid_columnconfigure(5, minsize=150)
        self.settings_window.grid_columnconfigure(6, minsize=145)
        self.settings_window.grid_columnconfigure(7, minsize=160)
        self.settings_window.grid_columnconfigure(8, minsize=60)
        self.settings_window.grid_columnconfigure(9, minsize=15)
        self.settings_window.grid_columnconfigure(10, minsize=15)
        self.settings_window.grid_columnconfigure(11, minsize=80)
        self.settings_window.grid_columnconfigure(12, minsize=200)
        self.settings_window.grid_columnconfigure(13, minsize=15)
        #
        ################################################################################################################
        ## Labels ######################################################################################################
        #
        SE(parent=self.settings_window, row_id=0, column_id=0, n_columns=4, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Settings (Standard Files)")
        SE(parent=self.settings_window, row_id=0, column_id=5, n_columns=5, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Settings (Sample Files)")
        SE(parent=self.settings_window, row_id=0, column_id=11, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Settings (Measured Isotopes)")
        #
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+3), column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Default Time Window (Background)")
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+4), column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Start")
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+5), column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_label(text="End")
        #
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+6), column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Default Time Window (Signal)")
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+7), column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Start")
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+8), column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_label(text="End")
        #
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+9), column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Settings (Spike Elimination)")
        #
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+13), column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Author")
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+14), column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Source ID")
        #
        i = 0
        for file in self.files_std:
            parts = file.split("/")
            SE(parent=self.settings_window, row_id=1+i, column_id=0, fg=self.color_fg,
            bg=self.color_bg).create_label(text=parts[-1])
            SE(parent=self.settings_window, row_id=1+i, column_id=3, fg=self.color_fg,
            bg="red").create_frame()
            i += 1
        #
        i = 0
        for file in self.files_smpl:
            parts = file.split("/")
            SE(parent=self.settings_window, row_id=1+i, column_id=5, fg=self.color_fg,
            bg=self.color_bg).create_label(text=parts[-1])
            SE(parent=self.settings_window, row_id=1+i, column_id=9, fg=self.color_fg,
            bg="red").create_frame()
            i += 1
        #
        i = 0
        for isotope in self.measured_isotopes:
            SE(parent=self.settings_window, row_id=1+i, column_id=11, fg=self.color_fg,
            bg=self.color_bg).create_label(text=isotope)
            i += 1
        #
        ################################################################################################################
        ## Entries #####################################################################################################
        #
        ## Entry Column for the IS concentrations for every single sample file
        self.create_entries_column_smpl(parent=self.settings_window, row_id=1, column_id=7,
                                        entries_container=self.concentrations_is)
        self.create_entries_default(parent=self.settings_window, row_id=int(len(self.files_smpl)+1), column_id=7)
        #
        self.create_simple_entries(parent=self.settings_window, row_id=int(len(self.files_std)+4), column_id=1,
                                   pos="start", command=True, segment="BG")
        self.create_simple_entries(parent=self.settings_window, row_id=int(len(self.files_std)+5), column_id=1,
                                   pos="end", command=True, segment="BG")
        #
        self.create_simple_entries(parent=self.settings_window, row_id=int(len(self.files_std)+7), column_id=1,
                                   pos="start", command=True, segment="SIG")
        self.create_simple_entries(parent=self.settings_window, row_id=int(len(self.files_std)+8), column_id=1,
                                   pos="end", command=True, segment="SIG")
        #
        self.create_entry_with_label(parent=self.settings_window, row_id=int(len(self.files_std)+10), column_id=0,
                                     var=self.spike_settings["deviation"], labeltext="10", key="deviation")
        self.create_entry_with_label(parent=self.settings_window, row_id=int(len(self.files_std)+11), column_id=0,
                                     var=self.spike_settings["threshold"], labeltext="1000", key="threshold")
        self.create_entry_with_label(parent=self.settings_window, row_id=int(len(self.files_std)+13), column_id=0,
                                     var=self.general_information["author"], labeltext="", key="author")
        self.create_entry_with_label(parent=self.settings_window, row_id=int(len(self.files_std)+14), column_id=0,
                                     var=self.general_information["origin"], labeltext="", key="origin")
        #
        ################################################################################################################
        ## Buttons #####################################################################################################
        #
        for i in range(len(self.files_std)):
            SE(parent=self.settings_window, row_id=i+1, column_id=2, fg=self.color_fg,
               bg=self.color_bg).create_button(text="Plot",
                                               command=lambda index=i, file_type="STD":
                                               self.make_simple_signals_window_plot_time_signal(index, file_type))
        #
        SE(parent=self.settings_window, row_id=int(len(self.files_smpl)+2), column_id=7, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Load IS Concentrations",
                                           command=lambda parent=self.settings_window: self.load_concentration_csv(parent))
        #
        for i in range(len(self.files_smpl)):
            SE(parent=self.settings_window, row_id=i+1, column_id=8, fg=self.color_fg,
               bg=self.color_bg).create_button(text="Plot", command=lambda index=i, file_type="SMPL",
                                                                           var_is=self.smpl_is_selected[i][1]:
                                               self.make_simple_signals_window_plot_time_signal(index, file_type, var_is))
        #
        ################################################################################################################
        ## Option Menus ################################################################################################
        #
        ## IS Option Column
        option_list_is = self.measured_isotopes
        for i in range(len(self.files_smpl)):
            self.smpl_is_selected[i][1].set(option_list_is[0])
            opt_menu_is = tk.OptionMenu(self.settings_window, self.smpl_is_selected[i][1], *option_list_is,
                                        command=lambda op, var_indiv=self.smpl_is_selected[i][1], index=i,
                                                       mode="IS SMPL": self.change_option_settings(var_indiv, index,
                                                                                                   mode, op))
            opt_menu_is.grid(row=1+i, column=6, sticky="nesw")
        ## IS Option Default
        self.var_is_default = tk.StringVar()
        self.create_option_is_default(parent=self.settings_window, row_id=int(len(self.files_smpl)+1), column_id=6,
                                      var_is_default=self.var_is_default,
                                      command=lambda op, var_default=self.var_is_default,
                                                     var_indiv=self.smpl_is_selected, mode="IS SMPL":
                                      self.change_option_default_settings(var_default, var_indiv, mode, op))
        ## Gangue Option Default
        self.var_mineral = tk.StringVar()
        self.create_option_gangue(parent=self.settings_window, row_id=int(len(self.files_smpl)+3), column_id=7,
                                  var_mineral=self.var_mineral,
                                  command=lambda op, parent=self.settings_window,
                                                 var_mineral=self.var_mineral: self.select_mineral(parent, var_mineral,
                                                                                                   op))
        #
        ## SRM Option Column for every standard file
        i = 0
        for var_srm in self.var_srm_indiv:
            SE(parent=self.settings_window, row_id=1+i, column_id=1, fg=self.color_fg,
           bg=self.color_bg).create_option_srm(var_srm=var_srm[1], text_set="Select SRM",
                                               command=lambda op, var_srm=var_srm[1], index=i:
                                               self.change_option_srm(var_srm, index, op))
            i += 1
        ## SRM Option Default for all standard files
        SE(parent=self.settings_window, row_id=int(len(self.files_std)+1), column_id=1, fg=self.color_fg,
           bg=self.color_bg).create_option_srm(var_srm=self.var_srm_default, text_set="Select SRM",
                                               command=lambda op, var_srm_default=self.var_srm_default:
                                               self.change_option_srm_default(var_srm_default, op))
        ## SRM Option Column for every isotope
        i = 0
        for srm_isotopes_indiv in self.srm_isotopes_indiv:
            opt_menu_srm_isotope = SE(parent=self.settings_window, row_id=1+i, column_id=12, fg=self.color_fg,
           bg=self.color_bg).create_option_srm(var_srm=srm_isotopes_indiv[1], text_set="Select SRM",
                                               command=lambda op, var_srm=srm_isotopes_indiv[1],
                                                              index=i: self.change_option_isotopes(var_srm, index, op))
            self.srm_isotopes_container.append(opt_menu_srm_isotope)
            i += 1
        ## SRM Option Default for all isotopes
        self.opt_menu_srm_isotopes = SE(parent=self.settings_window, row_id=int(len(self.measured_isotopes)+1),
                                        column_id=12, fg=self.color_fg,
           bg=self.color_bg).create_option_srm(var_srm=self.var_srm_isotopes_default, text_set="Select SRM",
                                               command=lambda op, var_default=self.var_srm_isotopes_default,
                                                              var_indiv=self.srm_isotopes_indiv:
                                               self.change_option_default_isotopes(var_default, var_indiv, op))
    #
    def make_simple_signals_window_sensitivities(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.concentration_container = []
        self.intensities_container = [[], [], []]
        self.sensitivity_container = [[], [], []]
        self.is_container = []
        self.srm_container = []
        self.var_is = tk.StringVar()
        self.var_is_default = tk.StringVar()
        #self.var_srm_default = tk.StringVar()
        # Radiobuttons
        self.var_rb = tk.IntVar()
        for item in self.srm_found:
            self.results_srm.append([item, {}])
        for item in self.srm_found:
            self.place_srm_values(var_srm=item)
        #
        self.times_measurement = []
        i = 0
        self.total_time = 0
        self.time_delta_to_start = []
        dates_0, times_0 = data.Data(filename=self.files_std[0]).import_as_list()
        t_start_0 = datetime.timedelta(hours=int(times_0[0][0]), minutes=int(times_0[0][1]), seconds=int(times_0[0][2]))
        for file in self.files_std:
            dates, times = data.Data(filename=file).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            t_end = datetime.timedelta(hours=int(times[1][0]), minutes=int(times[1][1]), seconds=int(times[1][2]))
            t_delta = (t_end - t_start).total_seconds()
            t_delta_0 = (t_start - t_start_0).total_seconds()
            self.total_time += float(t_delta)
            self.times_measurement.append([self.srm_files_indiv[i][0], str(t_start), str(t_end), str(t_delta)])
            self.time_delta_to_start.append([self.srm_files_indiv[i][0], float(t_delta_0)])
            i += 1
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(80 + 100 + 80 + 100 + 15 + 80 + 120 + 6*120 + 140 + 200 + 60 + 15)
        height = int(2*20 + (self.n_isotopes+1)*30 + 15)
        self.xi_window = tk.Toplevel(self.parent)
        self.xi_window.geometry(str(width)+"x"+str(height))
        self.xi_window.title("Simple Signals: Data Exploration - Sensitivities")
        #
        for y in range(26):
            tk.Grid.rowconfigure(self.xi_window, y, weight=1)
        for x in range(17):
            tk.Grid.columnconfigure(self.xi_window, x, weight=1)
        #
        # Rows
        for i in range(0, 2):
            self.xi_window.grid_rowconfigure(i, minsize=20)
        for i in range(2, int(2+self.n_isotopes+1)):
            self.xi_window.grid_rowconfigure(i, minsize=30)
        self.xi_window.grid_rowconfigure(int(2+self.n_isotopes+1), minsize=15)
        # Columns
        self.xi_window.grid_columnconfigure(0, minsize=80)
        self.xi_window.grid_columnconfigure(1, minsize=100)
        self.xi_window.grid_columnconfigure(2, minsize=80)
        self.xi_window.grid_columnconfigure(3, minsize=100)
        self.xi_window.grid_columnconfigure(4, minsize=15)
        self.xi_window.grid_columnconfigure(5, minsize=80)
        self.xi_window.grid_columnconfigure(6, minsize=120)
        for i in range(7, 13):
            self.xi_window.grid_columnconfigure(i, minsize=120)
        self.xi_window.grid_columnconfigure(13, minsize=140)
        self.xi_window.grid_columnconfigure(14, minsize=200)
        self.xi_window.grid_columnconfigure(15, minsize=60)
        self.xi_window.grid_columnconfigure(16, minsize=15)
        #
        ################################################################################################################
        ## Labels ######################################################################################################
        #
        SE(parent=self.xi_window, row_id=0, column_id=0, n_rows=2, n_columns=4, fg=self.color_fg,
           bg=self.color_bg).create_label(text="General Settings")
        #
        # Places the names of the measured isotopes
        SE(parent=self.xi_window, row_id=0, column_id=5, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Isotopes")
        SE(parent=self.xi_window, row_id=2, column_id=5, fg=self.color_fg,
           bg=self.color_bg).create_isotope_column(input_isotopes=self.isotopes)
        #
        # Places the label for the Concentration column
        SE(parent=self.xi_window, row_id=0, column_id=6, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Concentration C")
        #
        # Places the labels for the Intensities column
        SE(parent=self.xi_window, row_id=0, column_id=7, n_columns=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Intensity I")
        SE(parent=self.xi_window, row_id=1, column_id=7, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.xi_window, row_id=1, column_id=8, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.xi_window, row_id=1, column_id=9, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Ratio")
        #
        # Places the labels for the Sensitivities column
        SE(parent=self.xi_window, row_id=0, column_id=10, n_columns=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Sensitivity \u03BE")
        SE(parent=self.xi_window, row_id=1, column_id=10, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.xi_window, row_id=1, column_id=11, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.xi_window, row_id=1, column_id=12, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Drift Change")
        #
        # Places the Internal Standard label
        SE(parent=self.xi_window, row_id=0, column_id=13, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Internal Standard")
        # Places the SRM label
        SE(parent=self.xi_window, row_id=0, column_id=14, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Found SRM")
        #
        SE(parent=self.xi_window, row_id=0, column_id=15, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Display")
        #
        ################################################################################################################
        ## Entries #####################################################################################################
        #
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=6,
                                          entries_container=self.concentration_container)
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=7,
                                          entries_container=self.intensities_container[0])
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=8,
                                          entries_container=self.intensities_container[1])
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=9,
                                          entries_container=self.intensities_container[2])
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=10,
                                          entries_container=self.sensitivity_container[0])
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=11,
                                          entries_container=self.sensitivity_container[1])
        self.create_entries_column_simple(parent=self.xi_window, row_id=2, column_id=12,
                                          entries_container=self.sensitivity_container[2])
        #
        ################################################################################################################
        ## Buttons #####################################################################################################
        #
        # Places the "Advanced Statistics" Button
        SE(parent=self.xi_window, row_id=5, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Advanced Statistics")
        # Places the "Relative Sensitivities" Button
        SE(parent=self.xi_window, row_id=6, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Relative Sensitivities")
        # Places the "Drift Correction" Button
        SE(parent=self.xi_window, row_id=5, column_id=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Drift Correction")
        # Places the "Export Sensitivity Report" Button
        SE(parent=self.xi_window, row_id=6, column_id=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Export Sensitivity Report")
        #
        ################################################################################################################
        ## Time Window Entires #########################################################################################
        #
        self.make_time_window_entries(parent=self.xi_window, row_id=3, column_id=0, mode="BG")
        self.make_time_window_entries(parent=self.xi_window, row_id=3, column_id=2, mode="SIG")
        #
        ################################################################################################################
        ## Option Menus ################################################################################################
        #
        # Places the option menu for the time integration window of the signal
        self.var_iw_bg = SE(parent=self.xi_window, row_id=2, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_option_times(part="BG", times_seg=self.times_iw_bg,
                                                 command=lambda op, part="BG": self.select_time_window(part, op))
        self.var_iw_sig = SE(parent=self.xi_window, row_id=2, column_id=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_option_times(part="SIG", times_seg=self.times_iw_sig,
                                                 command=lambda op, part="SIG": self.select_time_window(part, op))
        #
        # Places the option menus for the internal standard
        # Default
        SE(parent=self.xi_window, row_id=int(2+self.n_isotopes), column_id=13, fg=self.color_fg,
           bg=self.color_bg).create_option_is(var_is=self.var_is, var_is_default=self.var_is_default,
                                              isotopes=self.isotopes,
                                              command=lambda variable=self.var_is_default, var_indiv=self.is_container,
                                                             n_isotopes=self.n_isotopes:
                                              Essentials(variable).change_default_option(var_indiv, n_isotopes))
        self.create_option_is_column(parent=self.xi_window, row_id=2, column_id=13, is_container=self.is_container)
        #
        # Places the option menus for the found SRMs
        # Default
        SE(parent=self.xi_window, row_id=int(2+self.n_isotopes), column_id=14, fg=self.color_fg,
           bg=self.color_bg).create_option_srm_default(var_srm_default=self.var_srm_default, found_srm=self.srm_found,
                                              command=lambda op, var_is=self.is_container[i],
                                                             var_srm=self.var_srm_default:
                                              self.change_option_srm_xi_default(var_is, var_srm, op))
        self.create_option_srm_column(parent=self.xi_window, row_id=2, column_id=14, srm_container=self.srm_container,
                                      found_srm=self.srm_found)
        #
        ################################################################################################################
        ## Radio Buttons ###############################################################################################
        #
        SE(parent=self.xi_window, row_id=2, column_id=15, fg=self.color_fg,
           bg=self.color_bg).create_radiobutton_column(var_rb=self.var_rb, isotopes=self.isotopes)
        #
    #
    def make_simple_signals_window_concentrations(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.var_is_conc = tk.StringVar()
        self.var_srm_conc = tk.StringVar()
        self.var_rb = tk.IntVar()
        #
        self.intensity_container_mu = {}
        self.intensity_container_sigma = {}
        self.sensitivity_container_mu = {}
        self.sensitivity_container_sigma = {}
        self.concentration_container_mu = {}
        self.concentration_container_sigma = {}
        self.rsf_container_mu = {}
        self.rsf_container_sigma = {}
        self.lod_container_mu = {}
        self.lod_container_sigma = {}
        #
        ## Result container
        self.results_intensity_ratios_indiv = {}
        self.results_sensitivities_indiv = {}
        self.results_concentrations_indiv = {}
        self.results_rsf_indiv = {}
        self.results_lod_indiv = {}
        self.results_intensity_ratios_final = {}
        self.results_sensitivities_final = {}
        self.results_concentrations_final = {}
        self.results_rsf_final = {}
        self.results_lod_final = {}
        #
        for file_smpl in self.files_smpl:
            self.results_intensity_ratios_indiv[file_smpl] = {}
            self.results_sensitivities_indiv[file_smpl] = {}
        #
        is_found_helper = []
        for item in self.smpl_is_selected:
            is_found_helper.append(item[1].get())
        for item in is_found_helper:
            if item not in self.is_found:
                self.is_found.append(item)
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(2*100 + 2*70 + 15 + 80 + 10*90 + 60 * 15)
        height = int(2*20 + self.n_isotopes*30 + 15)
        self.conc_window = tk.Toplevel(self.parent)
        self.conc_window.geometry(str(width)+"x"+str(height))
        self.conc_window.title("Simple Signals: Data Reduction - Concentrations")
        #
        for y in range(int(3+self.n_isotopes)):
            tk.Grid.rowconfigure(self.conc_window, y, weight=1)
        for x in range(17):
            tk.Grid.columnconfigure(self.conc_window, x, weight=1)
        #
        # Rows
        for i in range(0, 2):
            self.conc_window.grid_rowconfigure(i, minsize=20)
        for i in range(2, int(2+self.n_isotopes)):
            self.conc_window.grid_rowconfigure(i, minsize=30)
        self.conc_window.grid_rowconfigure(int(3+self.n_isotopes), minsize=15)
        # Columns
        for i in range(0, 2):
            self.conc_window.grid_columnconfigure(i, minsize=100)
        for i in range(2, 4):
            self.conc_window.grid_columnconfigure(i, minsize=70)
        self.conc_window.grid_columnconfigure(4, minsize=15)
        self.conc_window.grid_columnconfigure(5, minsize=80)
        for i in range(6, 16):
            self.conc_window.grid_columnconfigure(i, minsize=90)
        self.conc_window.grid_columnconfigure(16, minsize=60)
        self.conc_window.grid_columnconfigure(17, minsize=15)
        #
        ################################################################################################################
        ## Labels ######################################################################################################
        #
        SE(parent=self.conc_window, row_id=0, column_id=0, n_rows=2, n_columns=4, fg=self.color_fg,
           bg=self.color_bg).create_label(text="General Settings")
        SE(parent=self.conc_window, row_id=0, column_id=5, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Isotope")
        SE(parent=self.conc_window, row_id=2, column_id=5, fg=self.color_fg,
           bg=self.color_bg).create_isotope_column(input_isotopes=self.isotopes)
        SE(parent=self.conc_window, row_id=0, column_id=6, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Intensity Ratios I/I(IS)")
        SE(parent=self.conc_window, row_id=1, column_id=6, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.conc_window, row_id=1, column_id=7, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.conc_window, row_id=0, column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Sensitivity \u03BE")
        SE(parent=self.conc_window, row_id=1, column_id=8, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.conc_window, row_id=1, column_id=9, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.conc_window, row_id=0, column_id=10, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Concentration C")
        SE(parent=self.conc_window, row_id=1, column_id=10, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.conc_window, row_id=1, column_id=11, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.conc_window, row_id=0, column_id=12, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Relative Sensitivity Factor RSF")
        SE(parent=self.conc_window, row_id=1, column_id=12, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.conc_window, row_id=1, column_id=13, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.conc_window, row_id=0, column_id=14, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Limit of Detection LOD")
        SE(parent=self.conc_window, row_id=1, column_id=14, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.conc_window, row_id=1, column_id=15, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.conc_window, row_id=0, column_id=16, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Display")
        #
        ################################################################################################################
        ## Buttons #####################################################################################################
        #
        # Places the "Advanced Statistics" Button
        SE(parent=self.conc_window, row_id=3, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Advanced Statistics")
        SE(parent=self.conc_window, row_id=3, column_id=2, n_rows=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Calculation Report", command=self.create_concentration_report)
        SE(parent=self.conc_window, row_id=4, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Drift Correction", command=self.drift_correction_window)
        #
        ################################################################################################################
        ## Option Menus ################################################################################################
        #
        self.create_option_srm_single(parent=self.conc_window, row_id=2, column_id=0, n_columns=2,
                                      var_srm=self.var_srm_conc, found_srm=self.srm_found,
                                      command=lambda op, var=self.var_srm_conc: self.check_variable(var, op))
        self.create_option_is_single(parent=self.conc_window, row_id=2, column_id=2, n_columns=2,
                                     found_is=self.is_found, command=lambda op: self.fill_entries_conc_window(op))
        #
        ################################################################################################################
        ## Radio Buttons ###############################################################################################
        #
        SE(parent=self.conc_window, row_id=2, column_id=16, fg=self.color_fg,
           bg=self.color_bg).create_radiobutton_column(var_rb=self.var_rb, isotopes=self.isotopes)
        #
        ################################################################################################################
        ## Entries #####################################################################################################
        #
        self.create_entries(parent=self.conc_window, row_id=2, column_id=6,
                            entries_container=self.intensity_container_mu)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=7,
                            entries_container=self.intensity_container_sigma)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=8,
                            entries_container=self.sensitivity_container_mu)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=9,
                            entries_container=self.sensitivity_container_sigma)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=10,
                            entries_container=self.concentration_container_mu)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=11,
                            entries_container=self.concentration_container_sigma)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=12,
                            entries_container=self.rsf_container_mu)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=13,
                            entries_container=self.rsf_container_sigma)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=14,
                            entries_container=self.lod_container_mu)
        self.create_entries(parent=self.conc_window, row_id=2, column_id=15,
                            entries_container=self.lod_container_sigma)
    #
    def make_simple_signals_window_rsf(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #

        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(2*200 + 4*50 + 4*130 + 2*15)
        height = int(23*30 + 1*15)
        self.rsf_window = tk.Toplevel(self.parent)
        self.rsf_window.geometry(str(width)+"x"+str(height))
        self.rsf_window.title("Simple Signals - Standard Reference Material")
        #
        print("Standard Files (SRM Settings):", self.srm_files_indiv)
        print("Intensity Results:", )
        for i in range(self.n_isotopes):
            print(self.results_intensities[i])
    #
    ####################################################################################################################
    ## ESSENTIAL FUNCTIONS #############################################################################################
    ####################################################################################################################
    #
    def select_time_window(self, part, op):
        isotopes = self.isotopes[:, 0]
        if part == "BG":
            if self.var_iw_bg.get() != "No Time Intervals":
                key = re.search("(\d+\.\d+)" + " - " + "(\d+\.\d+)", self.var_iw_bg.get())
                t_start = float(key.group(1))
                t_end = float(key.group(2))
                #
                t_id_start = self.times[self.times == t_start].index[0]
                t_id_end = self.times[self.times == t_end].index[0]
                #
                self.indices_bg[0] = t_id_start
                self.indices_bg[1] = t_id_end
                self.entr_t_start_bg.delete(0, tk.END)
                self.entr_t_start_bg.insert(0, t_start)
                self.entr_t_end_bg.delete(0, tk.END)
                self.entr_t_end_bg.insert(0, t_end)
                #
        elif part == "MAT":
            if self.var_iw_mat.get() != "No Time Intervals":
                key = re.search("(\d+\.\d+)" + " - " + "(\d+\.\d+)", self.var_iw_mat.get())
                t_start = float(key.group(1))
                t_end = float(key.group(2))
                #
                t_id_start = self.times[self.times == t_start].index[0]
                t_id_end = self.times[self.times == t_end].index[0]
                #
                self.indices_mat[0] = t_id_start
                self.indices_mat[1] = t_id_end
                self.entr_t_start_mat.delete(0, tk.END)
                self.entr_t_start_mat.insert(0, t_start)
                self.entr_t_end_mat.delete(0, tk.END)
                self.entr_t_end_mat.insert(0, t_end)
        elif part == "SIG":
            if self.var_iw_sig.get() != "No Time Intervals":
                key = re.search("(\d+\.\d+)" + " - " + "(\d+\.\d+)", self.var_iw_sig.get())
                t_start = float(key.group(1))
                t_end = float(key.group(2))
                #
                t_id_start = self.times[self.times == t_start].index[0]
                t_id_end = self.times[self.times == t_end].index[0]
                #
                self.indices_sig[0] = t_id_start
                self.indices_sig[1] = t_id_end
                self.entr_t_start_sig.delete(0, tk.END)
                self.entr_t_start_sig.insert(0, t_start)
                self.entr_t_end_sig.delete(0, tk.END)
                self.entr_t_end_sig.insert(0, t_end)
        #
        i = 0
        for isotope in self.measured_isotopes:
            self.intensity_calculations(var_i=isotope, var_is=self.is_container[i].get(), var_srm=self.srm_container[i].get(), index=i)
            self.sensitivities_calculations(var_i=isotope, var_is=self.is_container[i].get(), var_srm=self.srm_container[i].get(), index=i)
            i += 1
    #
    def place_srm_values(self, var_srm):
        #
        path = os.getcwd()
        parent = os.path.dirname(path)
        if var_srm == "NIST 606":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_606.csv"))
        elif var_srm == "NIST 610":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610.csv"))
        elif var_srm == "NIST 610 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_GeoReM.csv"))
        elif var_srm == "NIST 610 (Spandler)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_Spandler.csv"))
        elif var_srm == "NIST 611":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611.csv"))
        elif var_srm == "NIST 611 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611_GeoReM.csv"))
        elif var_srm == "NIST 612":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612.csv"))
        elif var_srm == "NIST 612 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612_GeoReM.csv"))
        elif var_srm == "NIST 613":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613.csv"))
        elif var_srm == "NIST 613 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613_GeoReM.csv"))
        elif var_srm == "NIST 614":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614.csv"))
        elif var_srm == "NIST 614 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614_GeoReM.csv"))
        elif var_srm == "NIST 615":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615.csv"))
        elif var_srm == "NIST 615 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615_GeoReM.csv"))
        elif var_srm == "NIST 616":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616.csv"))
        elif var_srm == "NIST 616 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616_GeoReM.csv"))
        elif var_srm == "NIST 617":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617.csv"))
        elif var_srm == "NIST 617 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617_GeoReM.csv"))
        elif var_srm == "USGS BCR-2G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_BCR2G_GeoReM.csv"))
        elif var_srm == "USGS GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSD1G_GeoReM.csv"))
        elif var_srm == "USGS GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSE1G_GeoReM.csv"))
        #
        for item in self.results_srm:
            for isotope in self.measured_isotopes:
                for element, c_std in data_srm:
                    key_i = re.search("(\D+)(\d+)", isotope)
                    if key_i.group(1) == element:
                        if item[0] == var_srm:
                            item.append([isotope, c_std])
                            item[1][isotope] = c_std
        for item in self.results_srm:
            for isotope in self.measured_isotopes:
                if isotope not in item[1]:
                    item[1][isotope] = 0.0
    #
    def place_concentrations_srm(self, var_srm, index):
        for item in self.results_srm:
            if var_srm == item[0]:
                for values in item[2:]:
                    if values[0] == self.measured_isotopes[index]:
                        self.concentration_container[index][2].delete(0, tk.END)
                        self.concentration_container[index][2].insert(0, values[1])
                if self.measured_isotopes[index] not in np.array(item[2:])[:, 0]:
                    self.concentration_container[index][2].delete(0, tk.END)
                    self.concentration_container[index][2].insert(0, 0.0)
    #
    def change_option_srm_xi_default(self, var_is, var_srm, op):
        for i in range(self.n_isotopes):
            self.srm_container[i].set(var_srm.get())
            self.intensity_calculations(var_i=self.measured_isotopes[i], var_is=var_is.get(), var_srm=var_srm.get(),
                                        index=i)
            self.place_concentrations_srm(var_srm=var_srm.get(), index=i)
            self.sensitivities_calculations(var_i=self.measured_isotopes[i], var_is=var_is.get(), var_srm=var_srm.get(),
                                            index=i)

    #
    def change_option_srm_xi(self, var_i, var_is, var_srm, index, op):
        self.intensity_calculations(var_i=var_i, var_is=var_is.get(), var_srm=var_srm.get(), index=index)
        self.place_concentrations_srm(var_srm=var_srm.get(), index=index)
        self.sensitivities_calculations(var_i=self.measured_isotopes[index], var_is=var_is.get(), var_srm=var_srm.get(),
                                            index=index)
    #
    def sensitivities_calculations(self, var_i, var_is, var_srm, index):
        files_helper = []
        results_helper = [[], []]
        xi_time = []
        #
        for item in self.srm_files_indiv:
            if var_srm in item:
                files_helper.append(item[0])
        #
        for item in self.results_srm:
            if item[0] == var_srm:
                for file in files_helper:
                    dataset_std = data.Data(filename=file)
                    df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    #
                    intensity_i_bg = df_std[var_i][self.indices_bg[0]:self.indices_bg[1]+1].mean()
                    intensity_is_bg = df_std[var_is][self.indices_bg[0]:self.indices_bg[1]+1].mean()
                    intensity_i_sig = df_std[var_i][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                    intensity_is_sig = df_std[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                    intensity_i = intensity_i_sig - intensity_i_bg
                    intensity_is = intensity_is_sig - intensity_is_bg
                    #
                    concentration_i = item[1][var_i]
                    concentration_is = item[1][var_is]
                    if concentration_i > 0:
                        xi = intensity_i/intensity_is * concentration_is/concentration_i
                    else:
                        xi = 0.0
                    results_helper[0].append(xi)
                    results_helper[1].append(xi)
                    #
                    for item_times in self.time_delta_to_start:
                        if file in item_times:
                            xi_time.append([item_times[1], xi])
                    #
                    xi_histo = []
                    if self.measured_isotopes[self.var_rb.get()] == var_i:
                        if concentration_i > 0:
                            for i in range(self.indices_sig[0], self.indices_sig[1]+1):
                                for j in range(self.indices_bg[0], self.indices_bg[1]+1):
                                    if df_std[var_is][i]-df_std[var_is][j] > 0:
                                        intensity_i_extra = df_std[var_i][i]-df_std[var_i][j]
                                        intensity_is_extra = df_std[var_is][i]-df_std[var_is][j]
                                        value = intensity_i_extra/intensity_is_extra * concentration_is/concentration_i
                                        if value > 0:
                                            xi_histo.append(value)
                        # self.make_histo_plot(Y=xi_histo, parent=self.xi_window, row_id=7, column_id=0,
                        #      n_rows=int(2+self.n_isotopes+2-7), n_columns=5, value_mean=np.mean(results_helper[0]),
                        #                      var_i=var_i, xi_time=xi_time)
        if self.measured_isotopes[self.var_rb.get()] == var_i:
            self.make_histo_plot(Y=xi_histo, parent=self.xi_window, row_id=7, column_id=0,
                             n_rows=int(2+self.n_isotopes+2-7), n_columns=5, value_mean=np.mean(results_helper[0]),
                                             var_i=var_i, xi_time=xi_time)
        #
        # Mean
        self.sensitivity_container[0][index][2].delete(0, tk.END)
        self.sensitivity_container[0][index][2].insert(0, round(np.mean(results_helper[0]), 6))
        if len(files_helper) > 1:
            # Standard Deviation
            self.sensitivity_container[1][index][2].delete(0, tk.END)
            self.sensitivity_container[1][index][2].insert(0, round(np.std(results_helper[0], ddof=1), 6))
            # Drift Change
            if results_helper[1][0] != 0.0:
                self.sensitivity_container[2][index][2].delete(0, tk.END)
                self.sensitivity_container[2][index][2].insert(0, round((results_helper[1][-1]/results_helper[1][0]-1)*100, 6))
            else:
                self.sensitivity_container[2][index][2].delete(0, tk.END)
                self.sensitivity_container[2][index][2].insert(0, 0.0)
        else:
            # Standard Deviation
            self.sensitivity_container[1][index][2].delete(0, tk.END)
            self.sensitivity_container[1][index][2].insert(0, 0.0)
            # Drift Change
            self.sensitivity_container[2][index][2].delete(0, tk.END)
            self.sensitivity_container[2][index][2].insert(0, 0.0)
        #
        self.sensitivity_container.append([self.measured_isotopes[index], np.mean(results_helper[0]), np.std(results_helper[0], ddof=1), np.mean(results_helper[1])])
        #
    def intensity_calculations(self, var_i, var_is, var_srm, index):
        files_helper = []
        results_helper = [[], []]
        #
        for item in self.srm_files_indiv:
            if var_srm in item:
                files_helper.append(item[0])
        #
        for file in files_helper:
            dataset_std = data.Data(filename=file)
            df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            #
            intensity_i_bg_raw = df_std[var_i][self.indices_bg[0]:self.indices_bg[1]+1]
            intensity_is_bg_raw = df_std[var_is][self.indices_bg[0]:self.indices_bg[1]+1]
            intensity_i_bg = intensity_i_bg_raw.mean()
            intensity_is_bg = intensity_is_bg_raw.mean()
            intensity_i_sig_raw = df_std[var_i][self.indices_sig[0]:self.indices_sig[1]+1]
            intensity_is_sig_raw = df_std[var_is][self.indices_sig[0]:self.indices_sig[1]+1]
            intensity_i_sig = intensity_i_sig_raw.mean() - intensity_i_bg
            intensity_is_sig = intensity_is_sig_raw.mean() - intensity_is_bg
            results_helper[0].append(intensity_i_sig)
            results_helper[1].append(intensity_i_sig/intensity_is_sig)
        #
        # Mean
        self.intensities_container[0][index][2].delete(0, tk.END)
        self.intensities_container[0][index][2].insert(0, round(np.mean(results_helper[0]), 6))
        # Standard Deviation
        if len(files_helper) > 1:
            self.intensities_container[1][index][2].delete(0, tk.END)
            self.intensities_container[1][index][2].insert(0, round(np.std(results_helper[0], ddof=1), 6))
        else:
            self.intensities_container[1][index][2].delete(0, tk.END)
            self.intensities_container[1][index][2].insert(0, 0.0)
        # Intensity Ratio
        self.intensities_container[2][index][2].delete(0, tk.END)
        self.intensities_container[2][index][2].insert(0, round(np.mean(results_helper[1]), 6))
        #
        self.results_intensities.append([self.measured_isotopes[index], np.mean(results_helper[0]), np.std(results_helper[0], ddof=1), np.mean(results_helper[1])])
    #
    def create_option_srm_column(self, parent, row_id, column_id, srm_container, found_srm, n_rows=1, n_columns=1):
        option_list_srm = found_srm
        for i in range(self.n_isotopes):
            srm_container.append(tk.StringVar())
            srm_container[i].set("Select SRM")
            opt_menu = tk.OptionMenu(parent, srm_container[i], *option_list_srm,
                                     command=lambda op, var_i=self.measured_isotopes[i], var_is=self.is_container[i], var_srm=srm_container[i],
                                                    index=i: self.change_option_srm_xi(var_i, var_is, var_srm, index, op))
            opt_menu.grid(row=row_id+i, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def create_option_srm_single(self, parent, row_id, column_id, var_srm, found_srm, n_rows=1, n_columns=1, command=None):
        option_list_srm = found_srm
        var_srm.set(option_list_srm[0])
        if command == None:
            opt_menu = tk.OptionMenu(parent, var_srm, *option_list_srm)
        else:
            opt_menu = tk.OptionMenu(parent, var_srm, *option_list_srm, command=command)
        opt_menu.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def create_option_is_single(self, parent, row_id, column_id, found_is, n_rows=1, n_columns=1, command=None):
        option_list_is = found_is
        #self.var_is_conc = tk.StringVar()
        self.var_is_conc.set("Select isotope")
        if command == None:
            opt_menu = tk.OptionMenu(parent, self.var_is_conc, *option_list_is)
        else:
            opt_menu = tk.OptionMenu(parent, self.var_is_conc, *option_list_is, command=command)
        opt_menu.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def create_option_is_column(self, parent, row_id, column_id, is_container, n_rows=1, n_columns=1):
        option_list_is = self.measured_isotopes
        for i in range(self.n_isotopes):
            is_container.append(tk.StringVar())
            is_container[i].set("Select isotope")
            opt_menu_is = tk.OptionMenu(parent, is_container[i], *option_list_is, command=lambda variable=is_container[i], index=i: Essentials(variable).change_option(index))
            opt_menu_is.grid(row=row_id+i, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def create_entries_column_simple(self, parent, row_id, column_id, entries_container):
        i = 0
        for isotope in self.measured_isotopes:
            variable = tk.StringVar()
            variable.set(0.0)
            entries_container.append([isotope, variable, tk.Entry(parent, textvariable=variable)])
            entries_container[i][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            i += 1
    #
    def create_entries(self, parent, row_id, column_id, entries_container):
        i = 0
        for isotope in self.measured_isotopes:
            variable = tk.StringVar()
            variable.set(0.0)
            entries_container[isotope] = [isotope, variable, tk.Entry(parent, textvariable=variable)]
            entries_container[isotope][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            i += 1
    #
    def create_entries_column_smpl(self, parent, row_id, column_id, entries_container):
        i = 0
        for file in self.files_smpl:
            parts = file.split("/")
            variable = tk.StringVar()
            variable.set(0.0)
            entries_container.append([parts[-1], variable, tk.Entry(parent, textvariable=variable)])
            entries_container[i][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            i += 1
    #
    def create_entries_default(self, parent, row_id, column_id, mode="Settings"):
        self.entry_default = []
        variable = tk.StringVar()
        variable.set(0.0)
        self.entry_default.append(variable)
        self.entry_default.append(tk.Entry(parent, textvariable=variable))
        self.entry_default[1].grid(row=row_id, column=column_id, sticky="nesw")
        if mode == "Settings":
            self.entry_default[1].bind("<Return>", lambda event, entr=self.concentrations_is, var=self.entry_default[0]: self. place_concentrations_default(entr, var, event))
    #
    def place_concentrations_default(self, entr, var, event):
        i = 0
        for item in entr:
            item[2].delete(0, tk.END)
            item[2].insert(0, var.get())
            self.is_smpl[self.files_smpl[i]][1] = var.get()
            i += 1
        print(self.is_smpl)
    #
    def create_option_is_default(self, parent, row_id, column_id, var_is_default, n_rows=1, n_columns=1, command=None):
        option_list_is = self.measured_isotopes
        var_is_default.set(option_list_is[0])
        if command == None:
            opt_menu_is = tk.OptionMenu(parent, var_is_default, *option_list_is)
        else:
            opt_menu_is = tk.OptionMenu(parent, var_is_default, *option_list_is, command=command)
        opt_menu_is.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    #
    def create_option_gangue(self, parent, row_id, column_id, var_mineral, n_rows=1, n_columns=1, command=None):
        option_list_min = ["Quartz", "Calcite", "Fluorite"]
        var_mineral.set("Select Mineral")
        if command == None:
            opt_menu_min = tk.OptionMenu(parent, var_mineral, *option_list_min)
        else:
            opt_menu_min = tk.OptionMenu(parent, var_mineral, *option_list_min, command=command)
        opt_menu_min.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def select_mineral(self, parent, var_mineral, op):
        self.measured_elements = []
        self.is_conc_helper = {}
        if var_mineral.get() == "Quartz":
            oxygen = PS(name="O").get_data()
            silicon = PS(name="Si").get_data()
            quartz = silicon[2] + 2*oxygen[2]
            w_O = (2*oxygen[2])/quartz
            w_Si = 1 - w_O
            w_Si_ppm = w_Si*1000000
            self.is_conc_helper[silicon[0]] = w_Si_ppm
            self.measured_elements.append(silicon[0])
        elif var_mineral.get() == "Calcite":
            carbon = PS(name="C").get_data()
            oxygen = PS(name="O").get_data()
            calcium = PS(name="Ca").get_data()
            calcite = calcium[2] + carbon[2] + 3*oxygen[2]
            w_C = (carbon[2])/calcite
            w_O = (3*oxygen[2])/calcite
            w_Ca = 1 - w_O - w_C
            w_Ca_ppm = w_Ca*1000000
            self.is_conc_helper[calcium[0]] = w_Ca_ppm
            self.measured_elements.append(calcium[0])
        elif var_mineral.get() == "Fluorite":
            flourine = PS(name="F").get_data()
            calcium = PS(name="Ca").get_data()
            fluorite = calcium[2] + 2*flourine[2]
            w_F = (calcium[2])/fluorite
            w_Ca = 1 - w_F
            w_Ca_ppm = w_Ca*1000000
            self.is_conc_helper[calcium[0]] = w_Ca_ppm
            self.measured_elements.append(calcium[0])
        label = tk.Label(parent, text="Measured elements:\n"+", ".join(map(str, np.array(self.measured_elements))))
        label["anchor"] = tk.W
        label.grid(row=int(len(self.files_smpl)+4), column=7, columnspan=2, sticky="nesw")
    #
    def change_option_srm_isotopes_default(self, var_srm_isotope_default, op):
        i = 0
        for var_srm in self.var_srm_isotope_indiv:
            var_srm[1].set(var_srm_isotope_default.get())
            self.srm_isotopes[self.measured_isotopes[i]] = var_srm_isotope_default.get()
            i += 1
    #
    ## Functions that control the optionmenus
    #
    def change_option_isotopes(self, var_indiv, index, op):
        self.srm_isotopes[self.measured_isotopes[index]] = var_indiv.get()
    #
    def change_option_default_isotopes(self, var_default, var_indiv, op):
        i = 0
        for var in var_indiv:
            var[1].set(var_default.get())
            self.srm_isotopes[self.measured_isotopes[i]] = var_default.get()
            i += 1
    #
    def change_option_srm_isotope(self, var_srm, index, op):
        self.srm_isotopes[self.measured_isotopes[index]] = var_srm.get()
    #
    def change_option_default_srm(self, var_default, var_indiv, op):
        i = 0
        for item in var_indiv:
            item[1].set(var_default.get())
            self.srm_isotopes[self.measured_isotopes[i]] = var_default.get()
            i += 1
    #
    def change_option_settings(self, var_indiv, index, mode, op):
        if mode == "SRM Isotopes":
            self.srm_isotopes[self.measured_isotopes[index]] = var_indiv.get()
        elif mode == "IS SMPL":
            key = re.search("(\D+)(\d+)", var_indiv.get())
            if key.group(1) in self.measured_elements:
                self.concentrations_is[index][2].delete(0, tk.END)
                self.concentrations_is[index][2].insert(0, self.is_conc_helper[key.group(1)])
                self.is_smpl[self.files_smpl[index]] = [var_indiv.get(), self.is_conc_helper[key.group(1)]]
            else:
                self.concentrations_is[index][2].delete(0, tk.END)
                self.concentrations_is[index][2].insert(0, 0.0)
                self.is_smpl[self.files_smpl[index]] = [var_indiv.get(), 0.0]
    #
    def change_option_default_settings(self, var_default, var_indiv, mode, op):
        i = 0
        for item in var_indiv:
            item[1].set(var_default.get())
            if mode == "SRM Isotopes":
                self.srm_isotopes[self.measured_isotopes[i]] = var_default.get()
            elif mode == "IS SMPL":
                key = re.search("(\D+)(\d+)", var_default.get())
                if key.group(1) in self.measured_elements:
                    self.concentrations_is[i][2].delete(0, tk.END)
                    self.concentrations_is[i][2].insert(0, self.is_conc_helper[key.group(1)])
                    self.is_smpl[self.files_smpl[i]] = [var_default.get(), self.is_conc_helper[key.group(1)]]
                else:
                    self.concentrations_is[i][2].delete(0, tk.END)
                    self.concentrations_is[i][2].insert(0, 0.0)
                    self.is_smpl[self.files_smpl[i]] = [var_default.get(), 0.0]
            i += 1
    #
    def change_default_option(self, var_default, var_indiv, op):
        for item in var_indiv:
            item[1].set(var_default.get())
    #
    def change_default_option_2(self, var_default, var_indiv):
        for item in var_indiv:
            item[1].set(var_default.get())
    #
    def load_concentration_csv(self, parent):
        self.is_conc_helper = {}
        filename = fd.askopenfilenames(parent=parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        data_input = data.general().importSRM(filename=filename[0])
        self.measured_elements = np.array(data_input)[:, 0]
        for item in data_input:
            self.is_conc_helper[item[0]] = item[1]
        label = tk.Label(parent, text="Measured elements:\n"+", ".join(map(str, np.array(self.measured_elements))))
        label["anchor"] = tk.W
        label.grid(row=int(len(self.files_smpl)+4), column=6, columnspan=2, sticky="nesw")
    #
    def make_time_window_entries(self, parent, row_id, column_id, mode):
        #
        lbl_01 = tk.Label(parent, text="Time Start")
        lbl_01.grid(row=row_id, column=column_id, sticky="nesw")
        lbl_02 = tk.Label(parent, text="Time End")
        lbl_02.grid(row=row_id+1, column=column_id, sticky="nesw")
        #
        if mode == "BG":
            self.t_start_bg = tk.StringVar()
            self.t_start_bg.set(self.times.iloc[0])
            self.entr_t_start_bg = tk.Entry(parent, textvariable=self.t_start_bg)
            self.entr_t_start_bg.grid(row=row_id, column=column_id+1, sticky="nesw")
            self.entr_t_start_bg.bind("<Return>", lambda event, entr_t=self.entr_t_start_bg, var_t=self.t_start_bg,
                                                        position="start", mode="BG": self.change_time_entry(entr_t, var_t, position, mode, event))
            self.t_end_bg = tk.StringVar()
            self.t_end_bg.set(self.times.iloc[10])
            self.entr_t_end_bg = tk.Entry(parent, textvariable=self.t_end_bg)
            self.entr_t_end_bg.grid(row=row_id+1, column=column_id+1, sticky="nesw")
            self.entr_t_end_bg.bind("<Return>", lambda event, entr_t=self.entr_t_end_bg, var_t=self.t_end_bg,
                                                        position="end", mode="BG": self.change_time_entry(entr_t, var_t, position, mode, event))
        elif mode == "SIG":
            self.t_start_sig = tk.StringVar()
            self.t_start_sig.set(self.times.iloc[0])
            self.entr_t_start_sig = tk.Entry(parent, textvariable=self.t_start_sig)
            self.entr_t_start_sig.grid(row=row_id, column=column_id+1, sticky="nesw")
            self.entr_t_start_sig.bind("<Return>", lambda event, entr_t=self.entr_t_start_sig, var_t=self.t_start_sig,
                                                        position="start", mode="SIG": self.change_time_entry(entr_t, var_t, position, mode, event))
            self.t_end_sig = tk.StringVar()
            self.t_end_sig.set(self.times.iloc[-1])
            self.entr_t_end_sig = tk.Entry(parent, textvariable=self.t_end_sig)
            self.entr_t_end_sig.grid(row=row_id+1, column=column_id+1, sticky="nesw")
            self.entr_t_end_sig.bind("<Return>", lambda event, entr_t=self.entr_t_end_sig, var_t=self.t_end_sig,
                                                        position="end", mode="SIG": self.change_time_entry(entr_t, var_t, position, mode, event))
    #
    def change_time_entry(self, entr_t, var_t, position, mode, event):
        t_nearest = min(self.times, key=lambda x: abs(x - float(var_t.get())))
        entr_t.delete(0, tk.END)
        entr_t.insert(0, t_nearest)
        t_id = self.times[self.times == t_nearest].index[0]
        #
        if mode == "BG":
            if position == "start":
                self.indices_bg[0] = t_id
            elif position == "end":
                self.indices_bg[1] = t_id
        elif mode == "SIG":
            if position == "start":
                self.indices_sig[0] = t_id
            elif position == "end":
                self.indices_sig[1] = t_id
        elif mode == "MAT":
            if position == "start":
                self.indices_mat[0] = t_id
            elif position == "end":
                self.indices_mat[1] = t_id
        #
        i = 0
        for isotope in self.measured_isotopes:
            self.intensity_calculations(var_i=isotope, var_is=self.is_container[i].get(), var_srm=self.srm_container[i].get(), index=i)
            self.sensitivities_calculations(var_i=isotope, var_is=self.is_container[i].get(), var_srm=self.srm_container[i].get(), index=i)
            i += 1
    #
    def set_default_time_window(self, var, entr, event):
        t_nearest = min(self.times, key=lambda x: abs(x - float(var.get())))
        entr.delete(0, tk.END)
        entr.insert(0, t_nearest)
    #
    def find_nearest_time_conc(self, entr, var, pos, event, mode="SIG", t_iw=None):
        #
        if t_iw == None:
            t_nearest = min(self.times, key=lambda x: abs(x - float(var.get())))
            entr.delete(0, tk.END)
            entr.insert(0, t_nearest)
            t_id = self.times[self.times == t_nearest].index[0]
            #
            if pos == "start":
                if mode == "SIG":
                    self.indices_sig[0] = t_id
                else:
                    self.indices_bg[0] = t_id
            else:
                if mode == "SIG":
                    self.indices_sig[1] = t_id
                else:
                    self.indices_bg[1] = t_id
        else:
            t_id_start = self.times[self.times == t_iw[0]].index[0]
            t_id_end = self.times[self.times == t_iw[1]].index[0]
            if mode == "SIG":
                self.indices_sig[0] = t_id_start
                self.indices_sig[1] = t_id_end
                #
                self.entr_t_start_sig.delete(0, tk.END)
                self.entr_t_start_sig.insert(0, t_iw[0])
                self.entr_t_end_sig.delete(0, tk.END)
                self.entr_t_end_sig.insert(0, t_iw[1])
            else:
                self.indices_bg[0] = t_id_start
                self.indices_bg[1] = t_id_end
                #
                self.entr_t_start_bg.delete(0, tk.END)
                self.entr_t_start_bg.insert(0, t_iw[0])
                self.entr_t_end_bg.delete(0, tk.END)
                self.entr_t_end_bg.insert(0, t_iw[1])
        #
        i = 0
        for isotope in self.measured_isotopes:
            self.intensity_calculations(var_i=isotope, var_is=self.is_container[i].get(), var_srm=self.srm_container[i].get(), index=i)
            self.sensitivities_calculations(var_i=isotope, var_is=self.is_container[i].get(), var_srm=self.srm_container[i].get(), index=i)
            i += 1
    #
    def make_histo_plot(self, Y, parent, row_id, column_id, n_rows, n_columns, value_mean, var_i, xi_time):
        #
        try:
            self.fig_histo.clf()
            self.ax_histo.cla()
            self.canvas_histo.get_tk_widget().pack_forget()
        except AttributeError:
            pass

        try:
            if self.canvas_histo:
                self.canvas_histo.destroy()
        except AttributeError:
            pass
        #
        self.canvas_histo = None
        self.fig_histo = Figure(figsize=(12, 8), facecolor=self.color_bg)
        self.ax_histo_t = self.fig_histo.add_subplot(211)
        self.ax_histo_b = self.fig_histo.add_subplot(212)
        #
        xi_time = np.array(xi_time)
        x = xi_time[:, 0]
        y = xi_time[:, 1]
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        self.xi_opt[var_i] = np.array([m, c])
        y_regr = m*x + c
        #
        self.ax_histo_t.scatter(x, y)
        self.ax_histo_t.plot(x, y_regr, linestyle="dashed")
        self.ax_histo_t.grid(True)
        self.ax_histo_t.set_title("Sensitivity drift of "+str(var_i), fontsize=11)
        self.ax_histo_t.set_ylabel("Sensitivity $\\xi$ (cps/ppm)", labelpad=0.5)
        self.ax_histo_t.set_xlabel("Time (s)", labelpad=0.5)
        self.ax_histo_t.set_axisbelow(True)
        #
        self.ax_histo_b.axvline(value_mean, color="tomato", linestyle="dashed")
        self.ax_histo_b.hist(Y, bins=16, edgecolor="black")
        self.ax_histo_b.grid(True)
        self.ax_histo_b.set_yscale("log")
        self.ax_histo_b.set_axisbelow(True)
        self.ax_histo_b.set_title("Histogram of "+str(var_i), fontsize=11)
        self.ax_histo_b.set_ylabel("Frequency", labelpad=0.5)
        self.ax_histo_b.set_xlabel("Sensitivity $\\xi$", labelpad=0.5)
        self.fig_histo.subplots_adjust(left=0.2, hspace=0.4)

        self.plotting_area_histo = tk.Frame(parent, bg=self.color_bg)
        self.plotting_area_histo.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        self.canvas_histo = FigureCanvasTkAgg(self.fig_histo, master=self.plotting_area_histo)
        self.canvas_histo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #
    def select_plot_button(self, index, file_type):
        self.make_simple_signals_window_plot_time_signal(index=index, file_type=file_type)
    #
    ####################################################################################################################
    # WINDOW - PLOT (Integration Windows) ##############################################################################
    ####################################################################################################################
    #
    def make_simple_signals_window_plot_time_signal(self, index, file_type, var_is=None):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.file_type = file_type
        self.var_is = var_is

        self.var_rb = tk.IntVar()
        self.var_rb_plt = tk.IntVar()
        #
        if self.file_type == "STD":
            self.file = self.files_std[index]
        elif self.file_type == "SMPL":
            self.file = self.files_smpl[index]
        #
        parts = self.file.split("/")
        file_name_short = parts[-1]
        #
        self.lines = {}
        #
        self.helper_positions = []
        self.helper_indices = []
        self.bg_id = 0
        self.sig_id = 0
        self.bg_idlist = []
        self.positions_bg = []
        self.positions_sig = []
        self.indices_bg_alt = []
        #self.limits_bg = {}
        self.se_id = 0
        self.se_idlist = []
        self.positions_se = []
        self.indices_se_alt = []
        self.limits_se = {}
        self.spikes_isotopes = {}
        self.values_time_helper = {}
        self.values_time_helper["start"] = 0
        self.values_time_helper["end"] = 0
        #
        self.colors_lines = {}
        #
        self.signal_cleaned[self.file] = {}
        #
        if self.n_isotopes >= 22:
            row_id_btn_helper = self.n_isotopes
        else:
            row_id_btn_helper = 22
        #
        # Plot
        dataset = data.Data(filename=self.file)
        self.df_file = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        times = self.df_file.iloc[:, 0]
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(3*190 + 250 + 140 + 3*70 + 80 + 2*60 + 15)
        if self.n_isotopes >= 22:
            height = int((self.n_isotopes+6)*30 + 90 + 15)
        else:
            height = int(28*30 + 90 + 15)
        self.plot_ts_window = tk.Toplevel(self.parent)
        self.plot_ts_window.geometry(str(width)+"x"+str(height))
        self.plot_ts_window.title("Simple Signals: Time-Signal Diagram")
        #
        if self.n_isotopes >= 22:
            for y in range(int(self.n_isotopes+8)):
                tk.Grid.rowconfigure(self.plot_ts_window, y, weight=1)
        else:
            for y in range(30):
                tk.Grid.rowconfigure(self.plot_ts_window, y, weight=1)
        for x in range(12):
            tk.Grid.columnconfigure(self.plot_ts_window, x, weight=1)
        #
        # Rows
        if self.n_isotopes >= 22:
            for i in range(0, int(self.n_isotopes+6)):
                self.plot_ts_window.grid_rowconfigure(i, minsize=30)
            self.plot_ts_window.grid_rowconfigure(int(self.n_isotopes+6), minsize=90)
            self.plot_ts_window.grid_rowconfigure(int(self.n_isotopes+7), minsize=15)
        else:
            for i in range(0, 28):
                self.plot_ts_window.grid_rowconfigure(i, minsize=30)
            self.plot_ts_window.grid_rowconfigure(28, minsize=90)
            self.plot_ts_window.grid_rowconfigure(29, minsize=15)
        # Columns
        for i in range(0, 3):
            self.plot_ts_window.grid_columnconfigure(i, minsize=190)
        self.plot_ts_window.grid_columnconfigure(3, minsize=250)
        self.plot_ts_window.grid_columnconfigure(4, minsize=140)
        for i in range(5, 8):
            self.plot_ts_window.grid_columnconfigure(i, minsize=70)
        self.plot_ts_window.grid_columnconfigure(8, minsize=80)
        self.plot_ts_window.grid_columnconfigure(9, minsize=60)
        self.plot_ts_window.grid_columnconfigure(10, minsize=60)
        self.plot_ts_window.grid_columnconfigure(11, minsize=15)
        #
        ################################################################################################################
        ## Labels ######################################################################################################
        #
        SE(parent=self.plot_ts_window, row_id=0, column_id=8, n_columns=2, fg=self.color_fg,
            bg=self.color_bg).create_label(text="Measured isotopes")
        SE(parent=self.plot_ts_window, row_id=0, column_id=10, fg=self.color_fg,
            bg=self.color_bg).create_label(text="Spikes")
        i = 0
        for isotope in self.measured_isotopes:
            rgb = mcolors.to_rgb(self.isotopes_colors[i][1])
            brightness = np.sqrt(0.299*(rgb[0]*255)**2 + 0.587*(rgb[1]*255)**2 + 0.114*(rgb[2]*255)**2)
            if brightness < 128:
                color_fg = "white"
            else:
                color_fg = "black"
            SE(parent=self.plot_ts_window, row_id=1+i, column_id=8, fg=color_fg,
            bg=self.isotopes_colors[i][1]).create_label(text=isotope)
            i += 1
        #
        if self.n_isotopes >= 22:
            SE(parent=self.plot_ts_window, row_id=int(1+self.n_isotopes), column_id=3, n_rows=2, fg=self.color_fg,
                bg=self.color_bg).create_label(text="Isotopic Ratios")
        else:
            SE(parent=self.plot_ts_window, row_id=23, column_id=3, n_rows=2, fg=self.color_fg,
                bg=self.color_bg).create_label(text="Isotopic Ratios")
        #
        ################################################################################################################
        ## Radiobuttons ################################################################################################
        #
        if self.n_isotopes >= 22:
            row_id_rb = int(1+self.n_isotopes)
        else:
            row_id_rb = 23
        SE(parent=self.plot_ts_window, row_id=row_id_rb, column_id=0, n_rows=2, fg=self.color_fg,
            bg=self.color_bg).create_radiobutton(var_rb=self.var_rb, value_rb=1, color_bg="salmon", relief=tk.GROOVE,
                                                 text="Background")
        SE(parent=self.plot_ts_window, row_id=row_id_rb, column_id=1, n_rows=2, fg=self.color_fg,
            bg=self.color_bg).create_radiobutton(var_rb=self.var_rb, value_rb=2, color_bg="cornflowerblue", relief=tk.GROOVE,
                                                 text="Signal")
        SE(parent=self.plot_ts_window, row_id=row_id_rb, column_id=2, n_rows=2, fg=self.color_fg,
            bg=self.color_bg).create_radiobutton(var_rb=self.var_rb, value_rb=3, color_bg="khaki", relief=tk.GROOVE,
                                                 text="Spike Intervals")
        SE(parent=self.plot_ts_window, row_id=row_id_rb, column_id=4, fg=self.color_fg,
            bg=self.color_bg).create_radiobutton(var_rb=self.var_rb, value_rb=0, color_bg=self.color_bg,
                                                 text="No Segmentation", sticky="w")
        #
        ################################################################################################################
        ## Checkboxes ##################################################################################################
        #
        i = 0
        self.var_cb = {}
        self.var_cb_spikes = {}
        for isotope in self.measured_isotopes:
            self.var_cb[isotope] = tk.IntVar()
            self.var_cb[isotope].set(1)
            cb = tk.Checkbutton(self.plot_ts_window, text="", variable=self.var_cb[isotope], onvalue=1, offvalue=0,
                                command=lambda var_cb=self.var_cb[isotope], index=i: self.change_checkbox(var_cb, index))
            cb.grid(row=1+i, column=9, sticky="nesw")
            #
            self.var_cb_spikes[isotope] = tk.IntVar()
            self.var_cb_spikes[isotope].set(0)
            cb = tk.Checkbutton(self.plot_ts_window, text="", variable=self.var_cb_spikes[isotope], onvalue=1, offvalue=0)
            cb.grid(row=1+i, column=10, sticky="nesw")
            #
            i += 1
        #
        ################################################################################################################
        ## Listboxes ###################################################################################################
        #
        if self.n_isotopes >= 22:
            row_id_lb = int(self.n_isotopes+3)
        else:
            row_id_lb = 25
        self.lb_bg = SE(parent=self.plot_ts_window, row_id=row_id_lb, column_id=0, n_rows=4,
                        fg=self.color_fg, bg=self.color_bg).create_listbox(val_width=250, val_height=180)
        self.lb_sig = SE(parent=self.plot_ts_window, row_id=row_id_lb, column_id=1, n_rows=4,
                        fg=self.color_fg, bg=self.color_bg).create_listbox(val_width=250, val_height=180)
        self.lb_se = SE(parent=self.plot_ts_window, row_id=row_id_lb, column_id=2, n_rows=4,
                        fg=self.color_fg, bg=self.color_bg).create_listbox(val_width=250, val_height=180)
        self.tv_ir = self.make_treeview_ir(parent=self.plot_ts_window, row_id=row_id_lb, column_id=3,
                                           n_rows=4, n_columns=1)
        #
        ################################################################################################################
        ## BUTTONS #####################################################################################################
        #
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+1), column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Show all", command=self.select_all_isotopes)
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+2), column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Show none", command=self.deselect_all_isotopes)
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+3), column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Spike Elimination",
                                           command=lambda index=index, file_type=self.file_type:
                                           self.make_simple_signals_window_plot_spikes(index, file_type))
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+4), column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Smooth all", command=lambda times=times: self.smooth_all_isotopes(times))
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+5), column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Confirm", command=lambda index=index: self.do_spike_elimination(index))
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+2), column_id=4, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Remove Interval", command=lambda var=self.var_rb: self.delete_csv(var))
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+1), column_id=5, n_columns=3, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Time - Signal Ratio Plot")
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+2), column_id=5, n_columns=3, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Mass Spectrum")
        #
        ################################################################################################################
        ## Entries #####################################################################################################
        #
        self.create_time_entries(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+3), column_id=5, n_columns=2,
                                 var_rb=self.var_rb, times=times)
        #
        ################################################################################################################
        ## Plot ########################################################################################################
        #
        x_max = np.amax(times)
        y_max = self.df_file.max().max()
        #
        self.fig = Figure(figsize=(10, 5), facecolor=self.color_bg)
        self.ax = self.fig.add_subplot()
        i = 0
        for isotope in self.measured_isotopes:
            ln = self.ax.plot(times, self.df_file[isotope], label=isotope, visible=True, color=self.isotopes_colors[i][1])
            self.colors_lines[isotope] = self.isotopes_colors[i][1]
            self.lines[isotope] = ln
            i += 1
        self.ax.grid(True)
        self.ax.set_yscale("log")
        self.ax.set_xlim(left=0, right=x_max)
        self.ax.set_xticks(np.arange(0, x_max, 10))
        self.ax.set_ylim(top=1.5*y_max)
        self.ax.set_axisbelow(True)
        self.ax.set_title("Time-Signal plot of "+str(file_name_short))
        self.ax.set_xlabel("Time (s)", labelpad=0.5)
        self.ax.set_ylabel("Signal Intensity (cps)", labelpad=0.5)
        #
        self.fig.subplots_adjust(bottom=0.125, top=0.95, left=0.075, right=0.975)
        self.ax.legend(fontsize="x-small", framealpha=1.0, bbox_to_anchor=(0.125, 0.015), loc=3, borderaxespad=0,
                  bbox_transform=plt.gcf().transFigure, ncol=int(len(self.var_cb)/2+1))
        plt.rcParams["savefig.facecolor"]="white"
        plt.rcParams["savefig.dpi"]=300
        #
        if self.n_isotopes >= 22:
            row_span_plt = self.n_isotopes
        else:
            row_span_plt = 22
        self.plotting_area = tk.Frame(self.plot_ts_window, bg=self.color_bg)
        self.plotting_area.grid(row=0, column=0, rowspan=row_span_plt+1, columnspan=7, sticky="nesw")
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotting_area)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plotting_area)
        self.toolbar.config(background=self.color_bg)
        self.toolbar._message_label.config(background=self.color_bg)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
        if type(self.var_entries_time["BG"]["start"].get()) != "Set start time" or type(self.var_entries_time["SIG"]["start"].get()) != "Set start time":
            self.set_default_time_window_bg(times=times)
        else:
            pass
        #
        self.canvas.mpl_connect("button_press_event", lambda event, var=self.var_rb: self.onclick(var, event))
        #
        ################################################################################################################
        ## MISCALLENOUS ################################################################################################
        #
        self.calculate_signal_ratios(var_is=self.var_is)
        #
    #
    def change_checkbox(self, var_cb, index):
        if var_cb.get() == 1:
            self.lines[self.measured_isotopes[index]][0].set_visible(True)
        else:
            self.lines[self.measured_isotopes[index]][0].set_visible(False)
        self.canvas.draw()
    #
    def remember_defined_windows(self):
        # BG
        pass
    #
    def set_default_time_window_bg(self, times):
        keys_list_bg = list(self.limits_bg[self.file].keys())
        if len(keys_list_bg) == 2:
            if self.var_entries_time["BG"]["start"].get() != "Set start time":
                x_nearest_start = min(times, key=lambda x: abs(x-float(self.var_entries_time["BG"]["start"].get())))
                x_nearest_end = min(times, key=lambda x: abs(x-float(self.var_entries_time["BG"]["end"].get())))
                #
                helper_positions = [x_nearest_start, x_nearest_end]
                helper_indices = [times[times == x_nearest_start].index[0], times[times == x_nearest_end].index[0]]
                #
                self.bg_id += 1
                self.bg_idlist.append(self.bg_id)
                self.positions_bg.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
                # self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(helper_positions[0])+"-"
                #                   +str(helper_positions[1])+"]"+" ["+str(helper_indices[0]) + "-"
                #                   +str(helper_indices[1])+"]")
                self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(helper_positions[0])+"-"
                                  +str(helper_positions[1])+"]")
                box_bg = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="red")
                self.limits_bg[self.file][str(self.bg_id)] = box_bg
                self.limits_bg[self.file]["ID"].append(self.bg_id)
                self.limits_bg[self.file]["type"].append("default")
                self.canvas.draw()
                self.indices_bg = helper_indices
                t_start = helper_indices[0]
                t_end = helper_indices[1]
                if self.file_type == "STD":
                    self.time_iw_std[self.file]["BG"].append([t_start, t_end])
                    self.positions_bg_std[self.file].append([helper_positions[0], helper_positions[1],
                                                             helper_indices[0], helper_indices[1], self.bg_id])
                elif self.file_type == "SMPL":
                    self.time_iw_smpl[self.file]["BG"].append([t_start, t_end])
                    self.positions_bg_smpl[self.file].append([helper_positions[0], helper_positions[1],
                                                             helper_indices[0], helper_indices[1], self.bg_id])
            #
            if self.var_entries_time["SIG"]["start"].get() != "Set start time":
                x_nearest_start = min(times, key=lambda x: abs(x-float(self.var_entries_time["SIG"]["start"].get())))
                x_nearest_end = min(times, key=lambda x: abs(x-float(self.var_entries_time["SIG"]["end"].get())))
                #
                helper_positions = [x_nearest_start, x_nearest_end]
                helper_indices = [times[times == x_nearest_start].index[0], times[times == x_nearest_end].index[0]]
                #
                self.sig_id += 1
                self.sig_idlist[self.file].append(self.sig_id)
                self.positions_sig.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
                # self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(helper_positions[0])+"-"
                #                    +str(helper_positions[1])+"]"+" ["+str(helper_indices[0]) + "-"
                #                    +str(helper_indices[1])+"]")
                self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(helper_positions[0])+"-"
                                   +str(helper_positions[1])+"]")
                box_sig = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="blue")
                self.limits_sig[self.file][str(self.sig_id)] = box_sig
                self.limits_sig[self.file]["ID"].append(self.sig_id)
                self.limits_sig[self.file]["type"].append("default")
                self.canvas.draw()
                self.indices_sig = helper_indices
                t_start = helper_indices[0]
                t_end = helper_indices[1]
                if self.file_type == "STD":
                    self.time_iw_std[self.file]["SIG"].append([t_start, t_end])
                    self.positions_sig_std[self.file].append([helper_positions[0], helper_positions[1],
                                                              helper_indices[0], helper_indices[1], self.sig_id])
                elif self.file_type == "SMPL":
                    self.time_iw_smpl[self.file]["SIG"].append([t_start, t_end])
                    self.positions_sig_smpl[self.file].append([helper_positions[0], helper_positions[1],
                                                              helper_indices[0], helper_indices[1], self.sig_id])
        elif len(keys_list_bg) == 3 and self.limits_bg[self.file]["type"][0] == "default":
            if self.var_entries_time["BG"]["start"].get() != "Set start time":
                x_nearest_start = min(times, key=lambda x: abs(x-float(self.var_entries_time["BG"]["start"].get())))
                x_nearest_end = min(times, key=lambda x: abs(x-float(self.var_entries_time["BG"]["end"].get())))
                #
                helper_positions = [x_nearest_start, x_nearest_end]
                helper_indices = [times[times == x_nearest_start].index[0], times[times == x_nearest_end].index[0]]
                #
                self.bg_id += self.limits_bg[self.file]["ID"][0]
                # self.bg_idlist.append(self.bg_id)
                self.positions_bg.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
                # self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(helper_positions[0])+"-"
                #                   +str(helper_positions[1])+"]"+" ["+str(helper_indices[0]) + "-"
                #                   +str(helper_indices[1])+"]")
                self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(helper_positions[0])+"-"
                                  +str(helper_positions[1])+"]")
                box_bg = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="red")
                self.limits_bg[self.file][str(self.bg_id)] = box_bg
                # self.limits_bg[self.file]["ID"].append(self.bg_id)
                # self.limits_bg[self.file]["type"].append("default")
                self.canvas.draw()
                # self.indices_bg = helper_indices
                # t_start = helper_indices[0]
                # t_end = helper_indices[1]
                # if self.file_type == "STD":
                #     self.time_iw_std[self.file]["BG"].append([t_start, t_end])
                #     self.positions_bg_std[self.file].append([helper_positions[0], helper_positions[1],
                #                                              helper_indices[0], helper_indices[1], self.bg_id])
                # elif self.file_type == "SMPL":
                #     self.time_iw_smpl[self.file]["BG"].append([t_start, t_end])
                #     self.positions_bg_smpl[self.file].append([helper_positions[0], helper_positions[1],
                #                                              helper_indices[0], helper_indices[1], self.bg_id])
            #
            if self.var_entries_time["SIG"]["start"].get() != "Set start time":
                x_nearest_start = min(times, key=lambda x: abs(x-float(self.var_entries_time["SIG"]["start"].get())))
                x_nearest_end = min(times, key=lambda x: abs(x-float(self.var_entries_time["SIG"]["end"].get())))
                #
                helper_positions = [x_nearest_start, x_nearest_end]
                helper_indices = [times[times == x_nearest_start].index[0], times[times == x_nearest_end].index[0]]
                #
                self.sig_id += 1
                self.sig_idlist[self.file].append(self.sig_id)
                self.positions_sig.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
                # self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(helper_positions[0])+"-"
                #                    +str(helper_positions[1])+"]"+" ["+str(helper_indices[0]) + "-"
                #                    +str(helper_indices[1])+"]")
                self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(helper_positions[0])+"-"
                                   +str(helper_positions[1])+"]")
                box_sig = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="blue")
                self.limits_sig[self.file][str(self.sig_id)] = box_sig
                self.limits_sig[self.file]["ID"].append(self.sig_id)
                self.limits_sig[self.file]["type"].append("default")
                self.canvas.draw()
                self.indices_sig = helper_indices
                t_start = helper_indices[0]
                t_end = helper_indices[1]
                if self.file_type == "STD":
                    self.time_iw_std[self.file]["SIG"].append([t_start, t_end])
                    self.positions_sig_std[self.file].append([helper_positions[0], helper_positions[1],
                                                              helper_indices[0], helper_indices[1], self.sig_id])
                elif self.file_type == "SMPL":
                    self.time_iw_smpl[self.file]["SIG"].append([t_start, t_end])
                    self.positions_sig_smpl[self.file].append([helper_positions[0], helper_positions[1],
                                                              helper_indices[0], helper_indices[1], self.sig_id])
        elif len(keys_list_bg) > 3 and self.limits_bg[self.file]["type"][0] == "default":
            if self.var_entries_time["BG"]["start"].get() != "Set start time":
                x_nearest_start = min(times, key=lambda x: abs(x-float(self.var_entries_time["BG"]["start"].get())))
                x_nearest_end = min(times, key=lambda x: abs(x-float(self.var_entries_time["BG"]["end"].get())))
                #
                helper_positions = [x_nearest_start, x_nearest_end]
                helper_indices = [times[times == x_nearest_start].index[0], times[times == x_nearest_end].index[0]]
                #
                self.bg_id += self.limits_bg[self.file]["ID"][0]
                self.positions_bg.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
                self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(helper_positions[0])+"-"
                                  +str(helper_positions[1])+"]")
                box_bg = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="red")
                self.limits_bg[self.file][str(self.bg_id)] = box_bg
                self.canvas.draw()
        #
        # for segment in ["BG", "SIG"]:
        #     if self.var_entries_time[segment]["start"].get() != "Set start time":
        #         x_nearest_start = min(times, key=lambda x: abs(x-float(self.var_entries_time[segment]["start"].get())))
        #         x_nearest_end = min(times, key=lambda x: abs(x-float(self.var_entries_time[segment]["end"].get())))
        #         #
        #         self.helper_positions.append(x_nearest_start)
        #         self.helper_indices.append(times[times == x_nearest_start].index[0])
        #         self.helper_positions.append(x_nearest_end)
        #         self.helper_indices.append(times[times == x_nearest_end].index[0])
        #         if segment == "BG":
        #             #
        #             self.bg_id += 1
        #             self.bg_idlist.append(self.bg_id)
        #             self.positions_bg.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
        #             self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(self.helper_positions[0])+"-"+
        #                                            str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
        #                                            str(self.helper_indices[1]) +"]")
        #             box_bg = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25, color="red")
        #             self.limits_bg[str(self.bg_id)] = box_bg
        #             self.canvas.draw()
        #             self.indices_bg = self.helper_indices
        #             t_start = self.helper_indices[0]
        #             t_end = self.helper_indices[1]
        #             if self.file_type == "STD":
        #                 self.time_iw_std[self.file]["BG"].append([t_start, t_end])
        #                 #
        #                 if len(self.positions_sig_std[self.file]) > 0:
        #                     for item in self.positions_sig_std[self.file]:
        #                         box_sig = self.ax.axvspan(item[0], item[1], alpha=0.25,
        #                                         color="blue")
        #                         self.canvas.draw()
        #                         self.lb_sig.insert(tk.END, "SIG"+str(item[4])+" ["+str(item[0])+"-"+
        #                                                                str(item[1])+"]"+" ["+str(item[2]) + "-"+
        #                                                                str(item[3]) +"]")
        #                         self.limits_sig[self.file][str(item[4])] = box_sig
        #                 #
        #             elif self.file_type == "SMPL":
        #                 self.time_iw_smpl[self.file]["BG"].append([t_start, t_end])
        #                 #
        #                 if len(self.positions_sig_smpl[self.file]) > 0:
        #                     for item in self.positions_sig_smpl[self.file]:
        #                         box_sig = self.ax.axvspan(item[0], item[1], alpha=0.25,
        #                                         color="blue")
        #                         self.canvas.draw()
        #                         self.lb_sig.insert(tk.END, "SIG"+str(item[4])+" ["+str(item[0])+"-"+
        #                                                                str(item[1])+"]"+" ["+str(item[2]) + "-"+
        #                                                                str(item[3]) +"]")
        #                         self.limits_sig[self.file][str(item[4])] = box_sig
        #         else:
        #             pass
        #     else:
        #         pass
    #
    def onclick(self, var, event, spikes=False):
        if spikes == False:
            if var.get() in [1, 2, 3]:
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
                        if self.file_type == "STD":
                            if len(self.positions_bg_std[self.file]) > 0:
                                self.bg_id = self.positions_bg_std[self.file][-1][4]
                        elif self.file_type == "SMPL":
                            if len(self.positions_bg_smpl[self.file]) > 0:
                                self.bg_id = self.positions_bg_smpl[self.file][-1][4]
                        #
                        self.bg_id += 1
                        self.bg_idlist.append(self.bg_id)
                        self.limits_bg[self.file]["ID"].append(self.bg_id)
                        self.limits_bg[self.file]["type"].append("custom")
                        self.positions_bg.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
                        # self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(self.helper_positions[0])+"-"+
                        #                                str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
                        #                                str(self.helper_indices[1]) +"]")
                        self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(self.helper_positions[0])+"-"+
                                                       str(self.helper_positions[1])+"]")
                        box_bg = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25, color="red")
                        self.limits_bg[self.file][str(self.bg_id)] = box_bg
                        self.canvas.draw()
                        self.indices_bg = self.helper_indices
                        t_start = self.helper_indices[0]
                        t_end = self.helper_indices[1]
                        if self.file_type == "STD":
                            self.time_iw_std[self.file]["BG"].append([t_start, t_end])
                            self.positions_bg_std[self.file].append([self.helper_positions[0], self.helper_positions[1],
                                                                     self.helper_indices[0], self.helper_indices[1],
                                                                     self.bg_id])
                        elif self.file_type == "SMPL":
                            self.time_iw_smpl[self.file]["BG"].append([t_start, t_end])
                            self.positions_bg_smpl[self.file].append([self.helper_positions[0], self.helper_positions[1],
                                                                     self.helper_indices[0], self.helper_indices[1],
                                                                     self.bg_id])
                    elif var.get() == 2:
                        if self.file_type == "STD":
                            if len(self.positions_sig_std[self.file]) > 0:
                                self.sig_id = self.positions_sig_std[self.file][-1][4]
                        elif self.file_type == "SMPL":
                            if len(self.positions_sig_smpl[self.file]) > 0:
                                self.sig_id = self.positions_sig_smpl[self.file][-1][4]
                        self.sig_id += 1
                        self.limits_sig[self.file]["ID"].append(self.sig_id)
                        self.limits_sig[self.file]["type"].append("custom")
                        # self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(self.helper_positions[0])+"-"+
                        #                                str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
                        #                                str(self.helper_indices[1]) +"]")
                        self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(self.helper_positions[0])+"-"+
                                                       str(self.helper_positions[1])+"]")
                        box_sig = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25, color="blue")
                        self.limits_sig[self.file][str(self.sig_id)] = box_sig
                        self.canvas.draw()
                        self.indices_sig = self.helper_indices
                        t_start = self.helper_indices[0]
                        t_end = self.helper_indices[1]
                        if self.file_type == "STD":
                            self.time_iw_std[self.file]["SIG"].append([t_start, t_end])
                            self.positions_sig_std[self.file].append([self.helper_positions[0], self.helper_positions[1],
                                                                      self.helper_indices[0], self.helper_indices[1],
                                                                      self.sig_id])
                        elif self.file_type == "SMPL":
                            self.time_iw_smpl[self.file]["SIG"].append([t_start, t_end])
                            self.positions_sig_smpl[self.file].append([self.helper_positions[0], self.helper_positions[1],
                                                                      self.helper_indices[0], self.helper_indices[1],
                                                                      self.sig_id])
                    elif var.get() == 3:
                        isotope_list = []
                        for isotope in self.measured_isotopes:
                            if self.var_cb_spikes[isotope].get() == 1:
                                isotope_list.append(isotope)
                        self.se_id += 1
                        self.se_idlist.append(self.se_id)
                        self.positions_se.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
                        self.indices_se_alt.append([self.helper_indices[0], self.helper_indices[1]])
                        self.lb_se.insert(tk.END, "["+", ".join(isotope_list)+"] #"+str(self.se_id)+" ["+str(self.helper_positions[0])+"-"+
                                                       str(self.helper_positions[1])+"]")
                        box_se = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.50, color="khaki")
                        self.limits_se[str(self.se_id)] = box_se
                        self.canvas.draw()
                        for isotope in isotope_list:
                            if isotope not in self.spikes_isotopes:
                                self.spikes_isotopes[isotope] = []
                                self.spikes_isotopes[isotope].append([self.helper_indices[0], self.helper_indices[1]])
                            else:
                                self.spikes_isotopes[isotope].append([self.helper_indices[0], self.helper_indices[1]])
                    elif var.get() == 0:
                        pass
            else:
                pass
            #
        else:
            if var.get() == 1:
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
                        self.se_id += 1
                        self.se_idlist.append(self.se_id)
                        self.positions_se.append([round(self.helper_positions[0], 4), round(self.helper_positions[1], 4)])
                        self.lb_se.insert(tk.END, "Spikes"+str(self.se_id)+" ["+str(self.helper_positions[0])+"-"+
                                                       str(self.helper_positions[1])+"]"+" ["+str(self.helper_indices[0]) + "-"+
                                                       str(self.helper_indices[1]) +"]")
                        box_se = self.ax.axvspan(self.helper_positions[0], self.helper_positions[1], alpha=0.25,
                                                 color="#fff6a4")
                        self.limits_se[str(self.se_id)] = box_se
                        self.canvas_se.draw()
                    elif var.get() == 0:
                        pass
            else:
                pass
    #
    def deselect_all_isotopes(self):
        for isotope in self.measured_isotopes:
            self.lines[isotope][0].set_visible(False)
            self.var_cb[isotope].set(0)
        self.canvas.draw()
    #
    def select_all_isotopes(self):
        for isotope in self.measured_isotopes:
            self.lines[isotope][0].set_visible(True)
            self.var_cb[isotope].set(1)
        self.canvas.draw()
    #
    def delete_csv(self, var):
        if var.get() == 1:
            item = self.lb_bg.curselection()
            index = self.limits_bg[self.file]["ID"][item[0]]
            self.lb_bg.delete(tk.ANCHOR)
            self.limits_bg[self.file][str(self.limits_bg[self.file]["ID"][item[0]])].set_visible(False)
            del self.limits_bg[self.file][str(index)]
            self.limits_bg[self.file]["ID"].remove(index)
            if self.file_type == "STD":
                self.positions_bg_std[self.file].pop(item[0])
            elif self.file_type == "SMPL":
                self.positions_bg_smpl[self.file].pop(item[0])
            self.canvas.draw()
        elif var.get() == 2:
            item = self.lb_sig.curselection()
            index = self.limits_sig[self.file]["ID"][item[0]]
            self.lb_sig.delete(tk.ANCHOR)
            self.limits_sig[self.file][str(self.limits_sig[self.file]["ID"][item[0]])].set_visible(False)
            del self.limits_sig[self.file][str(index)]
            self.limits_sig[self.file]["ID"].remove(index)
            if self.file_type == "STD":
                self.positions_sig_std[self.file].pop(item[0])
            elif self.file_type == "SMPL":
                self.positions_sig_smpl[self.file].pop(item[0])
            self.canvas.draw()
        elif var.get() == 3:
            item = self.lb_se.curselection()
            self.positions_se.remove(self.positions_se[item[0]])
            self.indices_se_alt.remove(self.indices_se_alt[item[0]])
            self.lb_se.delete(tk.ANCHOR)
            self.limits_se[str(self.se_idlist[item[0]])].set_visible(False)
            self.canvas.draw()
            del self.se_idlist[item[0]]
        #
        if self.file_type == "STD":
            if var.get() == 1:
                self.time_iw_std[self.file]["BG"].pop(item[0])
            elif var.get() == 2:
                self.time_iw_std[self.file]["SIG"].pop(item[0])
        elif self.file_type == "SMPL":
            if var.get() == 1:
                self.time_iw_smpl[self.file]["BG"].pop(item[0])
            elif var.get() == 2:
                self.time_iw_smpl[self.file]["SIG"].pop(item[0])
        #
        return self.positions_bg, self.positions_se #self.positions_sig, self.positions_se
    #
    def calculate_signal_ratios(self, var_is):
        if var_is != None:
            var_is = var_is.get()
            self.results_ir = {}
            #
            intensities_is = self.df_file[var_is]
            intensities_is = intensities_is.replace(0, np.NaN)
            for isotope in self.measured_isotopes:
                intensities_i = self.df_file[isotope]
                intensities_i = intensities_i.replace(0, np.NaN)
                ir = intensities_i/intensities_is
                ir_mu = round(ir.mean(), 4)
                ir_sigma = round(ir.std(), 4)
                self.results_ir[isotope] = ir.mean()
                self.tv_ir.insert("", tk.END, values=[str(isotope)+"/"+str(var_is), ir_mu, ir_sigma])
        else:
            pass
    #
    def make_treeview_ir(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        # General Settings
        ttk.Style().configure("Treeview", background=self.color_bg, foreground="black",
                              fieldbackground=self.color_bg)
        my_font = font.Font(size="11", weight="normal")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=my_font, background=self.color_bg, pressed_color=self.color_bg,
                        highlight_color=self.color_bg, foreground=self.color_fg)
        style.map("Treeview.Heading", background = [("pressed", "!focus", "gray"),
                                                    ("active", "gray"), ("disabled", self.color_bg)])
        #
        columns = ("#1", "#2", "#3")
        treeview = ttk.Treeview(parent, columns=columns, show="headings")
        treeview.heading("#1", text="Ratio")
        treeview.column("#1", minwidth=0, width=90, stretch=tk.NO)
        treeview.heading("#2", text="\u03BC")
        treeview.column("#2", minwidth=0, width=80, stretch=tk.NO)
        treeview.heading("#3", text="\u03C3")
        treeview.column("#3", minwidth=0, width=80, stretch=tk.NO)
        treeview.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        #
        return treeview
    #
    def do_spike_elimination(self, index):
        #
        dataset = data.Data(filename=self.file)
        df_file = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        isotopes_spiked_list = [*self.spikes_isotopes]
        corrected_isotopes = []
        not_corrected_isotopes = []
        #
        for isotope in self.measured_isotopes:
            if bool(self.spikes_isotopes) == True:
                for isotope_spiked, intervals in self.spikes_isotopes.items():
                    if isotope in isotopes_spiked_list:
                        if isotope not in corrected_isotopes:
                            corrected_isotopes.append(isotope)
                            spike_intervals = np.array(intervals)
                            merged_intervals = Essentials(variable=spike_intervals).merge_times()
                            for interval in merged_intervals:
                                data_smoothed, indices_outl = Essentials(variable=df_file[isotope][interval[0]:interval[1]]).find_outlier(limit=float(self.spike_settings["deviation"].get()),
                                                                                                                                          threshold=float(self.spike_settings["threshold"].get()),
                                                                                                                                          interval=interval, data_total=df_file, isotope=isotope)
                                self.signal_cleaned[self.file][isotope] = data_smoothed
                        else:
                            pass
                    else:
                        if isotope not in not_corrected_isotopes:
                            not_corrected_isotopes.append(isotope)
                            self.signal_cleaned[self.file][isotope] = df_file[isotope]
                        else:
                            pass
            else:
                if isotope not in not_corrected_isotopes:
                    not_corrected_isotopes.append(isotope)
                    self.signal_cleaned[self.file][isotope] = df_file[isotope]
                else:
                    pass
        #
        if self.n_isotopes >= 22:
            row_id_btn_helper = self.n_isotopes
        else:
            row_id_btn_helper = 22
        SE(parent=self.plot_ts_window, row_id=int(row_id_btn_helper+5), column_id=8, n_columns=2, fg=self.color_fg,
            bg=self.color_bg).create_label(text="Settings saved!", relief=tk.FLAT)
        if self.file_type == "STD":
            SE(parent=self.settings_window, row_id=1+index, column_id=3, fg=self.color_fg,
                bg="green").create_frame()
        else:
            SE(parent=self.settings_window, row_id=1+index, column_id=9, fg=self.color_fg,
                bg="green").create_frame()
    #
    def place_intenstities(self, eliminated=False):
        self.intensities_helper = {}
        for isotope in self.measured_isotopes:
            self.intensities_helper[isotope] = {}
            results_helper = []
            for srm in self.srm_found:
                for file_smpl in self.files_smpl:
                    results_indiv_helper = []
                    if self.srm_isotopes[isotope] == srm:
                        #
                        bg_intervals = np.array(self.time_iw_smpl[file_smpl]["BG"])
                        sig_intervals = np.array(self.time_iw_smpl[file_smpl]["SIG"])
                        bg_merged = Essentials(variable=bg_intervals).merge_times()
                        sig_merged = Essentials(variable=sig_intervals).merge_times()
                        #
                        for interval_bg in bg_merged:
                            for interval_sig in sig_merged:
                                bg_start = interval_bg[0]
                                bg_end = interval_bg[1]
                                sig_start = interval_sig[0]
                                sig_end = interval_sig[1]
                                #
                                if len(self.smpl_eliminated[file_smpl]) > 0:
                                    eliminated = True
                                if eliminated == False:
                                    df_smpl = self.signal_cleaned[file_smpl]

                                    intensity_i_bg = df_smpl[isotope][bg_start:bg_end+1].mean()
                                    intensity_i = df_smpl[isotope][sig_start:sig_end+1].mean() - intensity_i_bg
                                    intensity_is_bg = df_smpl[self.var_is_conc.get()][bg_start:bg_end+1].mean()
                                    intensity_is = df_smpl[self.var_is_conc.get()][sig_start:sig_end+1].mean() \
                                                   - intensity_is_bg
                                    self.intensities_helper[isotope][file_smpl] = intensity_i
                                    #
                                    intensity_i_all = df_smpl[isotope][sig_start:sig_end+1] - intensity_i_bg
                                    intensity_is_all = df_smpl[self.var_is_conc.get()][sig_start:sig_end+1] \
                                                       - intensity_is_bg
                                    ratio_all = intensity_i_all/intensity_is_all
                                    ratio = intensity_i/intensity_is
                                    #
                                    if intensity_is != 0.0:
                                        results_helper.append(ratio)
                                    else:
                                        results_helper.append(0.0)
                                else:
                                    intensity_i = np.mean(self.smpl_eliminated[file_smpl][isotope])
                                    intensity_is = np.mean(self.smpl_eliminated[file_smpl][self.var_is_conc.get()])
                                    results_helper.append(intensity_i/intensity_is)
                                #
                                results_indiv_helper.append([np.mean(ratio_all), np.std(ratio_all, ddof=1)])
                        results_indiv_helper = np.array(results_indiv_helper)
                        self.results_intensity_ratios_indiv[file_smpl][isotope] = [np.mean(results_indiv_helper[:, 0]), np.mean(results_indiv_helper[:, 1])]
                    else:
                        pass
            #
            result_mu = np.mean(results_helper)
            self.intensity_container_mu[isotope][2].delete(0, tk.END)
            self.intensity_container_mu[isotope][2].insert(0, round(result_mu, 6))
            if len(results_helper) > 1:
                result_sigma = np.std(results_helper, ddof=1)
                self.intensity_container_sigma[isotope][2].delete(0, tk.END)
                self.intensity_container_sigma[isotope][2].insert(0, round(result_sigma, 6))
            else:
                result_sigma = 0.0
                self.intensity_container_sigma[isotope][2].delete(0, tk.END)
                self.intensity_container_sigma[isotope][2].insert(0, result_sigma)
            self.results_intensity_ratios_final[isotope] = [result_mu, result_sigma]
    #
    def place_sensitivities(self, eliminated=False):
        self.concentrations_helper = {}
        self.sensitivities_helper = {}
        self.time_delta_to_start = []
        self.time_delta_to_start_smpl = []
        self.times_delta_files = {}
        self.sensitivities_regression = {}
        dates_0, times_0 = data.Data(filename=self.files_std[0]).import_as_list()
        t_start_0 = datetime.timedelta(hours=int(times_0[0][0]), minutes=int(times_0[0][1]), seconds=int(times_0[0][2]))
        #
        xi_std_timed = {}
        xi_smpl = {}
        for isotope in self.measured_isotopes:
            self.concentrations_helper[isotope] = {}
            self.sensitivities_helper[isotope] = {}
            self.sensitivities_regression[isotope] = {}
            key_i = re.search("(\D+)(\d+)", isotope)
            key_is = re.search("(\D+)(\d+)", self.var_is_conc.get())
            element_i = key_i.group(1)
            element_is = key_is.group(1)
            xi_smpl[isotope] = []
            xi_std = []
            xi_std_timed[isotope] = []
            i = 0
            for file_std in self.files_std:
                self.sensitivities_regression[isotope][file_std] = {}
                #
                bg_intervals = np.array(self.time_iw_std[file_std]["BG"])
                sig_intervals = np.array(self.time_iw_std[file_std]["SIG"])
                bg_merged = Essentials(variable=bg_intervals).merge_times()
                sig_merged = Essentials(variable=sig_intervals).merge_times()
                #
                for interval_bg in bg_merged:
                    for interval_sig in sig_merged:
                        bg_start = interval_bg[0]
                        bg_end = interval_bg[1]
                        sig_start = interval_sig[0]
                        sig_end = interval_sig[1]
                        #
                        ## This part calculates the times for the sensitivity drift
                        dates, times = data.Data(filename=file_std).import_as_list()
                        t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
                        t_delta_0 = (t_start - t_start_0).total_seconds()
                        self.time_delta_to_start.append([self.srm_files_indiv[i][0], float(t_delta_0)])
                        self.times_delta_files[file_std] = float(t_delta_0)
                        self.sensitivities_regression[isotope][file_std]["time"] = float(t_delta_0)
                        #
                        if len(self.std_eliminated[file_std]) > 0:
                            eliminated = True
                        if eliminated == False:
                            #dataset_std = data.Data(filename=file_std)
                            #df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                            df_std = self.signal_cleaned[file_std]
                            endpoint = 1
                            intensity_i_bg = df_std[isotope][bg_start:bg_end+endpoint].mean()
                            intensity_i = df_std[isotope][sig_start:sig_end+endpoint].mean() - intensity_i_bg
                            intensity_i_all = df_std[isotope][sig_start:sig_end+endpoint] - intensity_i_bg
                            intensity_is_bg = df_std[self.var_is_conc.get()][bg_start:bg_end+endpoint].mean()
                            intensity_is = df_std[self.var_is_conc.get()][sig_start:sig_end+endpoint].mean() - intensity_is_bg
                            intensity_is_all = df_std[self.var_is_conc.get()][sig_start:sig_end+endpoint] - intensity_is_bg
                            #
                            try:
                                concentration_i = self.srm_values[self.srm_isotopes[isotope]][element_i]
                            except:
                                concentration_i = 0.0
                            concentration_is = self.srm_values[self.srm_isotopes[isotope]][element_is]
                            if concentration_i > 0:
                                xi = (intensity_i/intensity_is) * (concentration_is/concentration_i)
                                xi_all = (intensity_i_all/intensity_is_all) * (concentration_is/concentration_i)
                            else:
                                xi = 0.0
                                xi_all = np.zeros(len(intensity_i_all))
                            xi_std.append(xi_all.mean())
                            self.sensitivities_regression[isotope][file_std]["mu"] = xi_all.mean()
                            self.sensitivities_regression[isotope][file_std]["sigma"] = xi_all.std()
                            self.intensities_helper[isotope][file_std] = intensity_i
                            self.concentrations_helper[isotope][file_std] = concentration_i
                            #self.sensitivities_helper[isotope][file_std] = xi
                            self.sensitivities_helper[isotope][file_std] = [xi_all.mean(), xi_all.std()]
                            #
                        #
                        for item_times in self.time_delta_to_start:
                            if file_std in item_times:
                                xi_std_timed[isotope].append([item_times[1], xi_all.mean()])
                i += 1
            #
            Essentials(variable=None).calculate_sensitivity_regression(xi_time=xi_std_timed, var_i=isotope,
                                                                       xi_opt=self.xi_opt)
            self.sensitivities_regression[isotope][file_std]["opt"] = self.xi_opt[isotope]
            #
            for file_smpl in self.files_smpl:
                self.sensitivities_regression[isotope][file_smpl] = {}
                results_indiv_helper = []
                dataset_smpl = data.Data(filename=file_smpl)
                df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                #
                ## This part calculates the times for the sensitivity drift
                dates, times = data.Data(filename=file_smpl).import_as_list()
                t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
                t_delta_0 = (t_start - t_start_0).total_seconds()
                self.times_delta_files[file_smpl] = float(t_delta_0)
                self.sensitivities_regression[isotope][file_smpl]["time"] = float(t_delta_0)
                #
                if isotope == self.var_is_conc.get():
                    xi_drifted = 1.0
                else:
                    xi_drifted = self.xi_opt[isotope][0]*t_delta_0 + self.xi_opt[isotope][1]
                xi_smpl[isotope].append(xi_drifted)
                self.sensitivities_helper[isotope][file_smpl] = xi_drifted
                #
                sig_intervals = np.array(self.time_iw_smpl[file_smpl]["SIG"])
                sig_merged = Essentials(variable=sig_intervals).merge_times()
                for interval_sig in sig_merged:
                    sig_start = interval_sig[0]
                    sig_end = interval_sig[1]
                    #
                    if isotope == self.var_is_conc.get():
                        results_indiv_helper.append([1.0, 0.0])
                    else:
                        xi_drifted_indiv = self.xi_opt[isotope][0]*(df_smpl.iloc[:, 0][sig_start:sig_end+1] + t_delta_0) \
                                           + self.xi_opt[isotope][1]
                        results_indiv_helper.append([np.mean(xi_drifted_indiv), np.std(xi_drifted_indiv, ddof=1)])
                results_indiv_helper = np.array(results_indiv_helper)
                self.results_sensitivities_indiv[file_smpl][isotope] = [np.mean(results_indiv_helper[:, 0]),
                                                                        np.mean(results_indiv_helper[:, 1])]
                # self.sensitivities_regression[isotope][file_std]["mu"] = self.results_sensitivities_indiv[file_smpl][isotope][0]
                # self.sensitivities_regression[isotope][file_std]["sigma"] = self.results_sensitivities_indiv[file_smpl][isotope][1]
                self.sensitivities_regression[isotope][file_smpl]["mu"] = self.xi_opt[isotope][0]*t_delta_0 + self.xi_opt[isotope][1]
                self.sensitivities_regression[isotope][file_smpl]["sigma"] = 0.0
            #
            result_mean = np.mean(xi_smpl[isotope])
            self.sensitivity_container_mu[isotope][2].delete(0, tk.END)
            self.sensitivity_container_mu[isotope][2].insert(0, round(result_mean, 6))
            if len(xi_smpl[isotope]) > 1:
                result_std = np.std(xi_smpl[isotope], ddof=1)
                self.sensitivity_container_sigma[isotope][2].delete(0, tk.END)
                self.sensitivity_container_sigma[isotope][2].insert(0, round(result_std, 6))
            else:
                result_std = 0.0
                self.sensitivity_container_sigma[isotope][2].delete(0, tk.END)
                self.sensitivity_container_sigma[isotope][2].insert(0, result_std)
            self.results_sensitivities_final[isotope] = [result_mean, result_std]
    #
    def place_concentrations(self, eliminated=False):
        for isotope in self.measured_isotopes:
            results_helper = []
            for file_smpl in self.files_smpl:
                if len(self.smpl_eliminated[file_smpl]) > 0:
                    eliminated = True
                if eliminated == False:
                    intensity_i = self.intensities_helper[isotope][file_smpl]
                    intensity_is = self.intensities_helper[self.var_is_conc.get()][file_smpl]
                    concentration_is = self.is_smpl[file_smpl][1]
                    sensitivity_i = self.sensitivities_helper[isotope][file_smpl]
                    #
                    if intensity_is > 0 and sensitivity_i > 0:
                        concentration_i = (intensity_i/intensity_is) * (concentration_is/sensitivity_i)
                    else:
                        concentration_i = 0.0
                    results_helper.append(concentration_i)
                    self.concentrations_helper[isotope][file_smpl] = concentration_i
            #
            result_mean = np.mean(results_helper)
            self.concentration_container_mu[isotope][2].delete(0, tk.END)
            self.concentration_container_mu[isotope][2].insert(0, round(result_mean, 6))
            if len(results_helper) > 1:
                result_std = np.std(results_helper, ddof=1)
                self.concentration_container_sigma[isotope][2].delete(0, tk.END)
                self.concentration_container_sigma[isotope][2].insert(0, round(result_std, 8))
            else:
                result_std = 0.0
                self.concentration_container_sigma[isotope][2].delete(0, tk.END)
                self.concentration_container_sigma[isotope][2].insert(0, result_std)
            self.results_concentrations_final[isotope] = [result_mean, result_std]
        #
        for file_smpl in self.files_smpl:
            self.results_concentrations_indiv[file_smpl] = {}
            bg_intervals = np.array(self.time_iw_smpl[file_smpl]["BG"])
            sig_intervals = np.array(self.time_iw_smpl[file_smpl]["SIG"])
            bg_merged = Essentials(variable=bg_intervals).merge_times()
            sig_merged = Essentials(variable=sig_intervals).merge_times()
            #
            for interval_bg in bg_merged:
                for interval_sig in sig_merged:
                    bg_start = interval_bg[0]
                    bg_end = interval_bg[1]
                    sig_start = interval_sig[0]
                    sig_end = interval_sig[1]
                    #
                    # dataset_smpl = data.Data(filename=file_smpl)
                    # df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    df_smpl = self.signal_cleaned[file_smpl]
                    #
                    for isotope in self.measured_isotopes:
                        results_indiv_helper = []
                        #
                        intensity_i_bg = df_smpl[isotope][bg_start:bg_end+1].mean()
                        intensity_is_bg = df_smpl[self.var_is_conc.get()][bg_start:bg_end+1].mean()
                        intensity_i_all = df_smpl[isotope][sig_start:sig_end+1] - intensity_i_bg
                        intensity_is_all = df_smpl[self.var_is_conc.get()][sig_start:sig_end+1] - intensity_is_bg
                        concentration_is = self.is_smpl[file_smpl][1]
                        sensitivity_i = self.sensitivities_helper[isotope][file_smpl]
                        #
                        if sensitivity_i > 0:
                            concentration_i = (intensity_i_all)/(intensity_is_all) * (concentration_is/sensitivity_i)
                        else:
                            concentration_i = np.zeros(len(intensity_i_all))
                        #
                        results_indiv_helper.append([np.mean(concentration_i), np.std(concentration_i, ddof=1)])
                        results_indiv_helper = np.array(results_indiv_helper)
                        self.results_concentrations_indiv[file_smpl][isotope] = [np.mean(results_indiv_helper[:, 0]),
                                                                                np.mean(results_indiv_helper[:, 1])]
    #
    def place_rsf(self, eliminated=False):
        self.rsf_helper = {}
        for file_smpl in self.files_smpl:
            for isotope in self.measured_isotopes:
                self.rsf_helper[isotope] = {}
                results_helper = []
                #
                for file_std in self.files_std:
                    if len(self.smpl_eliminated[file_smpl]) > 0:
                        eliminated = True
                    if eliminated == False:
                        concentration_is_std = self.concentrations_helper[self.var_is_conc.get()][file_std]
                        intensity_is_std = self.intensities_helper[self.var_is_conc.get()][file_std]
                        concentration_is_smpl = self.concentrations_helper[self.var_is_conc.get()][file_smpl]
                        intensity_is_smpl = self.intensities_helper[self.var_is_conc.get()][file_smpl]
                        #
                        rsf_i = (concentration_is_std/intensity_is_std) * (intensity_is_smpl/concentration_is_smpl)
                        results_helper.append(rsf_i)
                        self.rsf_helper[isotope][file_smpl] = rsf_i
                #
                result_mean = np.mean(results_helper)
                self.rsf_container_mu[isotope][2].delete(0, tk.END)
                self.rsf_container_mu[isotope][2].insert(0, round(result_mean, 6))
                if len(results_helper) > 1:
                    result_std = np.std(results_helper, ddof=1)
                    self.rsf_container_sigma[isotope][2].delete(0, tk.END)
                    self.rsf_container_sigma[isotope][2].insert(0, round(result_std, 8))
                else:
                    result_std = 0.0
                    self.rsf_container_sigma[isotope][2].delete(0, tk.END)
                    self.rsf_container_sigma[isotope][2].insert(0, 0.0)
                self.results_rsf_final[isotope] = [result_mean, result_std]
        #
        for file_smpl in self.files_smpl:
            self.results_rsf_indiv[file_smpl] = {}
            for isotope in self.measured_isotopes:
                results_indiv_helper = []
                #
                # dataset_smpl = data.Data(filename=file_smpl)
                # df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                df_smpl = self.signal_cleaned[file_smpl]
                #
                for file_std in self.files_std:
                    # dataset_std = data.Data(filename=file_std)
                    # df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    df_std = self.signal_cleaned[file_std]
                    #
                    bg_intervals_std = np.array(self.time_iw_std[file_std]["BG"])
                    sig_intervals_std = np.array(self.time_iw_std[file_std]["SIG"])
                    bg_merged_std = Essentials(variable=bg_intervals_std).merge_times()
                    sig_merged_std = Essentials(variable=sig_intervals_std).merge_times()
                    bg_intervals_smpl = np.array(self.time_iw_smpl[file_smpl]["BG"])
                    sig_intervals_smpl = np.array(self.time_iw_smpl[file_smpl]["SIG"])
                    bg_merged_smpl = Essentials(variable=bg_intervals_smpl).merge_times()
                    sig_merged_smpl = Essentials(variable=sig_intervals_smpl).merge_times()
                    #
                    for interval_bg_std in bg_merged_std:
                        bg_start_std = interval_bg_std[0]
                        bg_end_std = interval_bg_std[1]
                        for interval_sig_std in sig_merged_std:
                            sig_start_std = interval_sig_std[0]
                            sig_end_std = interval_sig_std[1]
                            for interval_bg_smpl in bg_merged_smpl:
                                bg_start_smpl = interval_bg_smpl[0]
                                bg_end_smpl = interval_bg_smpl[1]
                                for interval_sig_smpl in sig_merged_smpl:
                                    sig_start_smpl = interval_sig_smpl[0]
                                    sig_end_smpl = interval_sig_smpl[1]
                                    #
                                    intensity_is_bg_std = df_std[self.var_is_conc.get()][bg_start_std:bg_end_std+1].mean()
                                    intensity_is_sig_std = df_std[self.var_is_conc.get()][sig_start_std:sig_end_std+1] \
                                                           - intensity_is_bg_std
                                    intensity_is_bg_smpl = df_smpl[self.var_is_conc.get()][bg_start_smpl:bg_end_smpl+1].mean()
                                    intensity_is_sig_smpl = df_smpl[self.var_is_conc.get()][sig_start_smpl:sig_end_smpl+1] \
                                                            - intensity_is_bg_smpl
                                    #
                                    rsf_i = (concentration_is_std)/(intensity_is_sig_std.mean()) \
                                            * (intensity_is_sig_smpl)/(concentration_is_smpl)
                    results_indiv_helper.append([np.mean(rsf_i), np.std(rsf_i, ddof=1)])
                results_indiv_helper = np.array(results_indiv_helper)
                self.results_rsf_indiv[file_smpl][isotope] = [np.mean(results_indiv_helper[:, 0]),
                                                              np.mean(results_indiv_helper[:, 1])]
    #
    def place_lod(self, eliminated=False):
        self.lod_helper = {}
        results_container = {}
        for isotope in self.measured_isotopes:
            results_container[isotope] = []
        for file_smpl in self.files_smpl:
            self.results_lod_indiv[file_smpl] = {}
            for isotope in self.measured_isotopes:
                self.lod_helper[isotope] = {}
                results_helper = []
                results_indiv_helper = []
                #
                bg_intervals = np.array(self.time_iw_smpl[file_smpl]["BG"])
                sig_intervals = np.array(self.time_iw_smpl[file_smpl]["SIG"])
                bg_merged = Essentials(variable=bg_intervals).merge_times()
                sig_merged = Essentials(variable=sig_intervals).merge_times()
                #
                for interval_bg in bg_merged:
                    for interval_sig in sig_merged:
                        bg_start = interval_bg[0]
                        bg_end = interval_bg[1]
                        sig_start = interval_sig[0]
                        sig_end = interval_sig[1]
                        #
                        if len(self.smpl_eliminated[file_smpl]) > 0:
                            eliminated = True
                        if eliminated == False:
                            # dataset_smpl = data.Data(filename=file_smpl)
                            # df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                            df_smpl = self.signal_cleaned[file_smpl]
                            #
                            sigma_i_bg = np.std(df_smpl[isotope][bg_start:bg_end+1], ddof=1)
                            n_bg = len(df_smpl[isotope][bg_start:bg_end+1])
                            n_sig = len(df_smpl[isotope][sig_start:sig_end+1])
                            sensitivity_is = self.sensitivities_helper[isotope][file_smpl]
                            concentration_is_smpl = self.concentrations_helper[self.var_is_conc.get()][file_smpl]
                            intensity_is_smpl = self.intensities_helper[self.var_is_conc.get()][file_smpl]
                            #
                            lod_i = 3 * sigma_i_bg * np.sqrt(1/n_bg + 1/n_sig) * 1/sensitivity_is \
                                    * (concentration_is_smpl)/(intensity_is_smpl)
                            results_helper.append(lod_i)
                            results_container[isotope].append(lod_i)
                            self.lod_helper[isotope][file_smpl] = lod_i
                            #
                            intensity_is_bg_smpl = df_smpl[self.var_is_conc.get()][bg_start:bg_end+1].mean()
                            intensity_is_sig_smpl = df_smpl[self.var_is_conc.get()][sig_start:sig_end+1] \
                                                    - intensity_is_bg_smpl
                            lod_i_indiv = 3 * sigma_i_bg * np.sqrt(1/n_bg + 1/n_sig) * 1/sensitivity_is \
                                          * (concentration_is_smpl)/(intensity_is_sig_smpl)
                            results_indiv_helper.append([np.mean(lod_i_indiv), np.std(lod_i_indiv, ddof=1)])
                results_indiv_helper = np.array(results_indiv_helper)
                self.results_lod_indiv[file_smpl][isotope] = [np.mean(results_indiv_helper[:, 0]),
                                                              np.mean(results_indiv_helper[:, 1])]
                #
                result_mean = np.mean(results_container[isotope])
                self.lod_container_mu[isotope][2].delete(0, tk.END)
                self.lod_container_mu[isotope][2].insert(0, round(np.mean(results_container[isotope]), 6))
                if len(results_container[isotope]) > 1:
                    result_std = np.std(results_container[isotope], ddof=1)
                    self.lod_container_sigma[isotope][2].delete(0, tk.END)
                    self.lod_container_sigma[isotope][2].insert(0, round(result_std, 8))
                else:
                    result_std = 0.0
                    self.lod_container_sigma[isotope][2].delete(0, tk.END)
                    self.lod_container_sigma[isotope][2].insert(0, result_std)
                self.results_lod_final[isotope] = [result_mean, result_std]
    #
    def check_variable(self, var, op):
        print(var.get())
    #
    def fill_entries_conc_window(self, op):
        self.place_intenstities()
        self.place_sensitivities()
        self.place_concentrations()
        self.place_rsf()
        self.place_lod()
    #
    def create_concentration_report(self):
        header = ["filename"]
        for isotope in self.measured_isotopes:
            header.append(isotope)
        #
        container_intensity_ratios_mu_total = {}
        container_intensity_ratios_sigma_total = {}
        container_sensitivity_mu_total = {}
        container_sensitivity_sigma_total = {}
        container_concentration_mu_total = {}
        container_concentration_sigma_total = {}
        container_rsf_mu_total = {}
        container_rsf_sigma_total = {}
        container_lod_mu_total = {}
        container_lod_sigma_total = {}
        container_intensity_ratios_mu = []
        container_intensity_ratios_sigma = []
        container_sensitivity_mu = []
        container_sensitivity_sigma = []
        container_concentration_mu = []
        container_concentration_sigma = []
        container_rsf_mu = []
        container_rsf_sigma = []
        container_lod_mu = []
        container_lod_sigma = []
        #
        container_intensity_ratios_mu_total["filename"] = "Total"
        container_intensity_ratios_sigma_total["filename"] = "Total"
        container_sensitivity_mu_total["filename"] = "Total"
        container_sensitivity_sigma_total["filename"] = "Total"
        container_concentration_mu_total["filename"] = "Total"
        container_concentration_sigma_total["filename"] = "Total"
        container_rsf_mu_total["filename"] = "Total"
        container_rsf_sigma_total["filename"] = "Total"
        container_lod_mu_total["filename"] = "Total"
        container_lod_sigma_total["filename"] = "Total"
        #
        i = 0
        for file_std in self.files_std:
            parts = file_std.split("/")
            #
            container_sensitivity_mu.append({})
            container_sensitivity_sigma.append({})
            #
            container_sensitivity_mu[i]["filename"] = parts[-1]
            container_sensitivity_sigma[i]["filename"] = parts[-1]
            #
            for isotope in self.measured_isotopes:
                container_sensitivity_mu[i][isotope] = self.sensitivities_helper[isotope][file_std][0]
                container_sensitivity_sigma[i][isotope] = self.sensitivities_helper[isotope][file_std][1]
            #
            i += 1
        #
        i = 0
        j = len(container_sensitivity_mu)
        for file_smpl in self.files_smpl:
            parts = file_smpl.split("/")
            container_intensity_ratios_mu.append({})
            container_intensity_ratios_sigma.append({})
            container_sensitivity_mu.append({})
            container_sensitivity_sigma.append({})
            container_concentration_mu.append({})
            container_concentration_sigma.append({})
            container_rsf_mu.append({})
            container_rsf_sigma.append({})
            container_lod_mu.append({})
            container_lod_sigma.append({})
            #
            container_intensity_ratios_mu[i]["filename"] = parts[-1]
            container_intensity_ratios_sigma[i]["filename"] = parts[-1]
            container_sensitivity_mu[j]["filename"] = parts[-1]
            container_sensitivity_sigma[j]["filename"] = parts[-1]
            container_concentration_mu[i]["filename"] = parts[-1]
            container_concentration_sigma[i]["filename"] = parts[-1]
            container_rsf_mu[i]["filename"] = parts[-1]
            container_rsf_sigma[i]["filename"] = parts[-1]
            container_lod_mu[i]["filename"] = parts[-1]
            container_lod_sigma[i]["filename"] = parts[-1]
            #
            for isotope in self.measured_isotopes:
                container_intensity_ratios_mu_total[isotope] = self.results_intensity_ratios_final[isotope][0]
                container_intensity_ratios_sigma_total[isotope] = self.results_intensity_ratios_final[isotope][1]
                container_sensitivity_mu_total[isotope] = self.results_sensitivities_final[isotope][0]
                container_sensitivity_sigma_total[isotope] = self.results_sensitivities_final[isotope][1]
                container_concentration_mu_total[isotope] = self.results_concentrations_final[isotope][0]
                container_concentration_sigma_total[isotope] = self.results_concentrations_final[isotope][1]
                container_rsf_mu_total[isotope] = self.results_rsf_final[isotope][0]
                container_rsf_sigma_total[isotope] = self.results_rsf_final[isotope][1]
                container_lod_mu_total[isotope] = self.results_lod_final[isotope][0]
                container_lod_sigma_total[isotope] = self.results_lod_final[isotope][1]
                #
                container_intensity_ratios_mu[i][isotope] = self.results_intensity_ratios_indiv[file_smpl][isotope][0]
                container_intensity_ratios_sigma[i][isotope] = self.results_intensity_ratios_indiv[file_smpl][isotope][1]
                container_sensitivity_mu[j][isotope] = self.results_sensitivities_indiv[file_smpl][isotope][0]
                container_sensitivity_sigma[j][isotope] = self.results_sensitivities_indiv[file_smpl][isotope][1]
                container_concentration_mu[i][isotope] = self.results_concentrations_indiv[file_smpl][isotope][0]
                container_concentration_sigma[i][isotope] = self.results_concentrations_indiv[file_smpl][isotope][1]
                container_rsf_mu[i][isotope] = self.results_rsf_indiv[file_smpl][isotope][0]
                container_rsf_sigma[i][isotope] = self.results_rsf_indiv[file_smpl][isotope][1]
                container_lod_mu[i][isotope] = self.results_lod_indiv[file_smpl][isotope][0]
                container_lod_sigma[i][isotope] = self.results_lod_indiv[file_smpl][isotope][1]
                #
            i += 1
            j += 1
        #
        with open(str(self.general_information["origin"].get())+"_calculation_report.csv", "w") as report_file:
            writer = csv.DictWriter(report_file, fieldnames=header)
            report_file.write("CALCULATION REPORT\n")
            report_file.write("\n")
            report_file.write("AUTHOR: "+str(self.general_information["author"].get())+"\n")
            report_file.write("SOURCE ID: "+str(self.general_information["origin"].get())+"\n")
            report_file.write("\n")
            report_file.write("Signal Intensity Ratios (arithmetic mean)\n")
            writer.writeheader()
            for item in container_intensity_ratios_mu:
                writer.writerow(item)
            writer.writerow(container_intensity_ratios_mu_total)
            #
            report_file.write("\n")
            report_file.write("Signal Intensity Ratios (standard deviation)\n")
            writer.writeheader()
            for item in container_intensity_ratios_sigma:
                writer.writerow(item)
            writer.writerow(container_intensity_ratios_sigma_total)
            #
            report_file.write("\n")
            report_file.write("Sensitivity (arithmetic mean)\n")
            writer.writeheader()
            for item in container_sensitivity_mu:
                writer.writerow(item)
            writer.writerow(container_sensitivity_mu_total)
            #
            report_file.write("\n")
            report_file.write("Sensitivity (standard deviation)\n")
            writer.writeheader()
            for item in container_sensitivity_sigma:
                writer.writerow(item)
            writer.writerow(container_sensitivity_sigma_total)
            #
            report_file.write("\n")
            report_file.write("Concentration (arithmetic mean)\n")
            writer.writeheader()
            for item in container_concentration_mu:
                writer.writerow(item)
            writer.writerow(container_concentration_mu_total)
            #
            report_file.write("\n")
            report_file.write("Concentration (standard deviation)\n")
            writer.writeheader()
            for item in container_concentration_sigma:
                writer.writerow(item)
            writer.writerow(container_concentration_sigma_total)
            #
            report_file.write("\n")
            report_file.write("Relative Sensitivity Factor (arithmetic mean)\n")
            writer.writeheader()
            for item in container_rsf_mu:
                writer.writerow(item)
            writer.writerow(container_rsf_mu_total)
            #
            report_file.write("\n")
            report_file.write("Relative Sensitivity Factor (standard deviation)\n")
            writer.writeheader()
            for item in container_rsf_sigma:
                writer.writerow(item)
            writer.writerow(container_rsf_sigma_total)
            #
            report_file.write("\n")
            report_file.write("Limit of Detection (arithmetic mean)\n")
            writer.writeheader()
            for item in container_lod_mu:
                writer.writerow(item)
            writer.writerow(container_lod_mu_total)
            #
            report_file.write("\n")
            report_file.write("Limit of Detection (standard deviation)\n")
            writer.writeheader()
            for item in container_lod_sigma:
                writer.writerow(item)
            writer.writerow(container_lod_sigma_total)
    #
    def create_simple_entries(self, parent, row_id, column_id, pos, segment, n_rows=1, n_columns=1, command=False):
        if command == False:
            var = tk.StringVar()
            var.set(0.0)
            entr = tk.Entry(parent, textvariable=var)
        else:
            if segment == "BG":
                if pos == "start":
                    if self.var_entries_time[segment][pos].get() == "":
                        self.var_entries_time[segment][pos].set("Set start time")
                    else:
                        self.var_entries_time[segment][pos].set(self.var_entries_time[segment][pos].get())
                    self.entr_t_start = tk.Entry(parent, textvariable=self.var_entries_time[segment][pos])
                    self.entr_t_start.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns,
                               sticky="nesw")
                    self.entr_t_start.bind("<Return>", lambda event, var=self.var_entries_time[segment][pos],
                                                              entr=self.entr_t_start: self.set_default_time_window(var, entr, event))
                elif pos == "end":
                    if self.var_entries_time[segment][pos].get() == "":
                        self.var_entries_time[segment][pos].set("Set end time")
                    else:
                        self.var_entries_time[segment][pos].set(self.var_entries_time[segment][pos].get())
                    self.entr_t_end = tk.Entry(parent, textvariable=self.var_entries_time[segment][pos])
                    self.entr_t_end.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns,
                               sticky="nesw")
                    self.entr_t_end.bind("<Return>", lambda event, var=self.var_entries_time[segment][pos],
                                                            entr=self.entr_t_end: self.set_default_time_window(var,
                                                                                                               entr, event))
            elif segment == "SIG":
                if pos == "start":
                    if self.var_entries_time[segment][pos].get() == "":
                        self.var_entries_time[segment][pos].set("Set start time")
                    else:
                        self.var_entries_time[segment][pos].set(self.var_entries_time[segment][pos].get())
                    self.entr_t_start = tk.Entry(parent, textvariable=self.var_entries_time[segment][pos])
                    self.entr_t_start.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns,
                               sticky="nesw")
                    self.entr_t_start.bind("<Return>", lambda event, var=self.var_entries_time[segment][pos],
                                                              entr=self.entr_t_start: self.set_default_time_window(var, entr, event))
                elif pos == "end":
                    if self.var_entries_time[segment][pos].get() == "":
                        self.var_entries_time[segment][pos].set("Set end time")
                    else:
                        self.var_entries_time[segment][pos].set(self.var_entries_time[segment][pos].get())
                    self.entr_t_end = tk.Entry(parent, textvariable=self.var_entries_time[segment][pos])
                    self.entr_t_end.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns,
                               sticky="nesw")
                    self.entr_t_end.bind("<Return>", lambda event, var=self.var_entries_time[segment][pos],
                                                            entr=self.entr_t_end: self.set_default_time_window(var,
                                                                                                               entr, event))
    #
    def create_time_entries(self, parent, row_id, column_id, var_rb, times, n_rows=1, n_columns=1):
        # Start
        SE(parent=parent, row_id=row_id, column_id=column_id, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Start")
        self.var_entry_start = tk.StringVar()
        self.var_entry_start.set("Set start time")
        self.entry_start = tk.Entry(parent, textvariable=self.var_entry_start)
        self.entry_start.grid(row=row_id, column=column_id+1, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        self.entry_start.bind("<Return>", lambda event, var=self.var_entry_start,
                                                 entr=self.entry_start, var_rb=var_rb,
                                                 times=times: self.set_time_window_indiv(var, entr, var_rb, times,
                                                                                         event))
        # End
        SE(parent=parent, row_id=row_id+1, column_id=column_id, fg=self.color_fg,
           bg=self.color_bg).create_label(text="End")
        self.var_entry_end = tk.StringVar()
        self.var_entry_end.set("Set end time")
        self.entry_end = tk.Entry(parent, textvariable=self.var_entry_end)
        self.entry_end.grid(row=row_id+1, column=column_id+1, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        self.entry_end.bind("<Return>", lambda event, var=self.var_entry_end,
                                               entr=self.entry_end, var_rb=var_rb,
                                               times=times: self.set_time_window_indiv(var, entr, var_rb, times,
                                                                                       event))
    #
    def create_entry_with_label(self, parent, row_id, column_id, var, labeltext, key, n_rows=1, n_columns=1):
        if key == "deviation":
            SE(parent=parent, row_id=row_id, column_id=column_id, fg=self.color_fg,
               bg=self.color_bg).create_label(text="Deviation")
        elif key == "threshold":
            SE(parent=parent, row_id=row_id, column_id=column_id, fg=self.color_fg,
               bg=self.color_bg).create_label(text="Threshold")
        if key in ["deviation", "threshold"]:
            var.set(labeltext)
            entry = tk.Entry(parent, textvariable=var)
            entry.grid(row=row_id, column=column_id+1, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
            entry.bind("<Return>", lambda event, var=var, key=key: self.set_spike_settings(var, key, event))
        elif key in ["author", "origin"]:
            var.set(labeltext)
            entry = tk.Entry(parent, textvariable=var)
            entry.grid(row=row_id, column=column_id+1, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
            entry.bind("<Return>", lambda event, var=var, key=key: self.set_spike_settings(var, key, event))
    #
    def set_spike_settings(self, var, key, event):
        pass
    #
    def set_time_window_indiv(self, var, entr, var_rb, times, event):
        time = var.get()
        time = time.replace(',', '.')
        if var == self.var_entry_start:
            x_nearest_start = min(times, key=lambda x: abs(x-float(time)))
            entr.delete(0, tk.END)
            entr.insert(0, round(x_nearest_start, 8))
            self.values_time_helper["start"] = x_nearest_start
        elif var == self.var_entry_end:
            x_nearest_end = min(times, key=lambda x: abs(x-float(time)))
            entr.delete(0, tk.END)
            entr.insert(0, round(x_nearest_end, 8))
            self.values_time_helper["end"] = x_nearest_end
        #
        if var_rb.get() == 1 and self.values_time_helper["end"] != 0:
            helper_positions = [self.values_time_helper["start"], self.values_time_helper["end"]]
            helper_indices = [times[times == self.values_time_helper["start"]].index[0],
                              times[times == self.values_time_helper["end"]].index[0]]
            #
            self.bg_id += 1
            self.bg_idlist.append(self.bg_id)
            self.positions_bg.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
            self.lb_bg.insert(tk.END, "BG"+str(self.bg_id)+" ["+str(helper_positions[0])+"-"
                              +str(helper_positions[1])+"]")
            box_bg = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="red")
            self.limits_bg[self.file][str(self.bg_id)] = box_bg
            self.limits_bg[self.file]["ID"].append(self.bg_id)
            self.canvas.draw()
            self.indices_bg = helper_indices
            t_start = helper_indices[0]
            t_end = helper_indices[1]
            if self.file_type == "STD":
                self.time_iw_std[self.file]["BG"].append([t_start, t_end])
                self.positions_bg_std[self.file].append([helper_positions[0], helper_positions[1],
                                                         helper_indices[0], helper_indices[1], self.bg_id])
            elif self.file_type == "SMPL":
                self.time_iw_smpl[self.file]["BG"].append([t_start, t_end])
                self.positions_bg_smpl[self.file].append([helper_positions[0], helper_positions[1],
                                                         helper_indices[0], helper_indices[1], self.bg_id])
            self.values_time_helper["start"] = 0
            self.values_time_helper["end"] = 0
        elif var_rb.get() == 2 and self.values_time_helper["end"] != 0:
            helper_positions = [self.values_time_helper["start"], self.values_time_helper["end"]]
            helper_indices = [times[times == self.values_time_helper["start"]].index[0],
                              times[times == self.values_time_helper["end"]].index[0]]
            #
            self.sig_id += 1
            self.sig_idlist[self.file].append(self.sig_id)
            self.positions_sig.append([round(helper_positions[0], 4), round(helper_positions[1], 4)])
            self.lb_sig.insert(tk.END, "SIG"+str(self.sig_id)+" ["+str(helper_positions[0])+"-"
                              +str(helper_positions[1])+"]")
            box_sig = self.ax.axvspan(helper_positions[0], helper_positions[1], alpha=0.25, color="blue")
            self.limits_sig[self.file][str(self.sig_id)] = box_sig
            self.limits_sig[self.file]["ID"].append(self.sig_id)
            self.canvas.draw()
            self.indices_sig = helper_indices
            t_start = helper_indices[0]
            t_end = helper_indices[1]
            if self.file_type == "STD":
                self.time_iw_std[self.file]["SIG"].append([t_start, t_end])
                self.positions_sig_std[self.file].append([helper_positions[0], helper_positions[1],
                                                         helper_indices[0], helper_indices[1], self.sig_id])
            elif self.file_type == "SMPL":
                self.time_iw_smpl[self.file]["SIG"].append([t_start, t_end])
                self.positions_sig_smpl[self.file].append([helper_positions[0], helper_positions[1],
                                                         helper_indices[0], helper_indices[1], self.sig_id])
            self.values_time_helper["start"] = 0
            self.values_time_helper["end"] = 0
    #
    ####################################################################################################################
    # WINDOW - PLOT (Spike Elimination) ################################################################################
    ####################################################################################################################
    #
    def make_simple_signals_window_plot_spikes(self, index, file_type):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.file_type = file_type
        helper_isotopes = {}
        helper_indices_outlier = {}
        signal_cleaned = {}
        self.lines_spikes = {}
        self.var_rb = tk.IntVar()
        self.var_rb.set(1)
        #
        if self.file_type == "STD":
            self.file = self.files_std[index]
        elif self.file_type == "SMPL":
            self.file = self.files_smpl[index]
        #
        dataset = data.Data(filename=self.file)
        df_file = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        #
        isotopes_spiked_list = [*self.spikes_isotopes]
        corrected_isotopes = []
        not_corrected_isotopes = []
        #
        for isotope in self.measured_isotopes:
            for isotope_spiked, intervals in self.spikes_isotopes.items():
                if isotope in isotopes_spiked_list:
                    if isotope not in corrected_isotopes:
                        corrected_isotopes.append(isotope)
                        spike_intervals = np.array(intervals)
                        merged_intervals = Essentials(variable=spike_intervals).merge_times()
                        for interval in merged_intervals:
                            data_smoothed, indices_outl = Essentials(variable=self.df_file[isotope][interval[0]:interval[1]]).find_outlier(limit=float(self.spike_settings["deviation"].get()), interval=interval,
                                                                                                                                                  data_total=self.df_file, isotope=isotope, threshold=float(self.spike_settings["threshold"].get()))
                            helper_indices_outlier[isotope] = indices_outl
                            signal_cleaned[isotope] = data_smoothed
                    else:
                        pass
                else:
                    if isotope not in not_corrected_isotopes:
                        not_corrected_isotopes.append(isotope)
                        signal_cleaned[isotope] = self.df_file[isotope]
                    else:
                        pass
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(8*90 + 2*60 + 15)
        height = int((len(self.spikes_isotopes)+1)*30 + (20 - (len(self.spikes_isotopes)+1) - 1)*45 + 15)
        self.plot_spikes_window = tk.Toplevel(self.parent)
        self.plot_spikes_window.geometry(str(width)+"x"+str(height))
        self.plot_spikes_window.title("Simple Signals: Spike Elimination")
        #
        for y in range(20):
            tk.Grid.rowconfigure(self.plot_spikes_window, y, weight=1)
        for x in range(11):
            tk.Grid.columnconfigure(self.plot_spikes_window, x, weight=1)
        #
        # Rows
        for i in range(0, len(self.spikes_isotopes)+1):
            self.plot_spikes_window.grid_rowconfigure(i, minsize=30)
        for i in range(len(self.spikes_isotopes)+1, 19):
            self.plot_spikes_window.grid_rowconfigure(i, minsize=45)
        self.plot_spikes_window.grid_rowconfigure(19, minsize=15)
        # Columns
        for i in range(0, 8):
            self.plot_spikes_window.grid_columnconfigure(i, minsize=30)
        for i in range(8, 10):
            self.plot_spikes_window.grid_columnconfigure(i, minsize=60)
        self.plot_spikes_window.grid_columnconfigure(10, minsize=15)
        #
        ################################################################################################################
        ## Labels + Radio Buttons ######################################################################################
        #
        SE(parent=self.plot_spikes_window, row_id=0, column_id=8, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Corrected Signals")
        i = 0
        for isotope, intervals in self.spikes_isotopes.items():
            SE(parent=self.plot_spikes_window, row_id=1+i, column_id=8, fg=self.color_fg,
            bg=self.color_bg).create_label(text=isotope)
            SE(parent=self.plot_spikes_window, row_id=i+1, column_id=9, fg=self.color_fg,
                bg=self.color_bg).create_radiobutton(var_rb=self.var_rb, value_rb=1+i, relief=tk.GROOVE,
                                                     color_bg=self.colors_lines[isotope],
                                                     command=lambda var=self.var_rb, isotope_selected=isotope:
                                                     self.select_rb_spikes(var, isotope_selected))
            helper_isotopes[isotope] = df_file[isotope]
            i += 1
        #
        ################################################################################################################
        ## Plot ########################################################################################################
        #
        times = df_file.iloc[:, 0]
        x_max = np.amax(times)
        y_max = df_file.max().max()
        #
        self.fig = Figure(figsize=(9, 6), facecolor=self.color_bg)
        self.ax_t = self.fig.add_subplot(211)
        self.ax_b = self.fig.add_subplot(212)
        i = 0
        for isotope, values in helper_isotopes.items():
            self.lines_spikes[isotope] = []
            if i == 0:
                ln_raw = self.ax_t.plot(times, values, visible=True, color=self.colors_lines[isotope])
                dots_outl = self.ax_t.scatter(times[helper_indices_outlier[isotope]],
                                            values[helper_indices_outlier[isotope]], visible=True,
                                            color=self.colors_lines[isotope])
                ln_edited = self.ax_t.plot(times, signal_cleaned[isotope], visible=True,
                                         color="black", linestyle="dashed")
                res = values-signal_cleaned[isotope]
                ln_res = self.ax_b.plot(times, res, visible=True, color=self.colors_lines[isotope])
                #
                self.lines_spikes[isotope].append(ln_raw)
                self.lines_spikes[isotope].append(dots_outl)
                self.lines_spikes[isotope].append(ln_edited)
                self.lines_spikes[isotope].append(ln_res)
            else:
                ln_raw = self.ax_t.plot(times, values, visible=False, color=self.colors_lines[isotope])
                dots_outl = self.ax_t.scatter(times[helper_indices_outlier[isotope]],
                                            values[helper_indices_outlier[isotope]], visible=False,
                                            color=self.colors_lines[isotope])
                ln_edited = self.ax_t.plot(times, signal_cleaned[isotope], visible=False,
                                         color="black", linestyle="dashed")
                res = values-signal_cleaned[isotope]
                ln_res = self.ax_b.plot(times, res, visible=False, color=self.colors_lines[isotope])
                #
                self.lines_spikes[isotope].append(ln_raw)
                self.lines_spikes[isotope].append(dots_outl)
                self.lines_spikes[isotope].append(ln_edited)
                self.lines_spikes[isotope].append(ln_res)
            i += 1
        self.ax_t.grid(True)
        self.ax_b.grid(True)
        self.ax_t.set_yscale("log")
        self.ax_b.set_yscale("log")
        self.ax_t.set_xlim(left=0, right=x_max)
        self.ax_t.set_xticks(np.arange(0, x_max, 10))
        self.ax_t.set_ylim(bottom=1.0, top=1.5*y_max)
        self.ax_b.set_ylim(auto=True)
        self.ax_t.set_axisbelow(True)
        self.ax_b.set_axisbelow(True)
        self.ax_t.set_xlabel("Time (s)", labelpad=0.5)
        self.ax_b.set_xlabel("Time (s)", labelpad=0.8)
        self.ax_t.set_ylabel("Signal Intensity (cps)", labelpad=0.5)
        self.ax_b.set_ylabel("Residual (cps)", labelpad=0.8)
        #
        self.fig.subplots_adjust(bottom=0.125, top=0.975, left=0.125, right=0.975)
        #
        self.plotting_area = tk.Frame(self.plot_spikes_window, bg=self.color_bg)
        self.plotting_area.grid(row=0, column=0, rowspan=20, columnspan=7, sticky="nesw")
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotting_area)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plotting_area)
        self.toolbar.config(background=self.color_bg)
        self.toolbar._message_label.config(background=self.color_bg)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #
    def select_rb_spikes(self, var, isotope_selected):
        for isotope, lines in self.lines_spikes.items():
            if isotope_selected == isotope:
                lines[0][0].set_visible(True)
                lines[1].set_visible(True)
                lines[2][0].set_visible(True)
                lines[3][0].set_visible(True)
                self.ax_b.relim()
            else:
                lines[0][0].set_visible(False)
                lines[1].set_visible(False)
                lines[2][0].set_visible(False)
                lines[3][0].set_visible(False)
                self.ax_b.relim()
        self.canvas.draw()
    #
    ####################################################################################################################
    # WINDOW - PLOT (Spike Elimination) ################################################################################
    ####################################################################################################################
    #
    def data_exploration_signal_ratios(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.intensity_container_mu = {}
        self.intensity_container_sigma = {}
        self.intensity_ratio_container_mu = {}
        self.intensity_ratio_container_sigma = {}
        self.var_file_std = tk.StringVar()
        self.var_file_smpl = tk.StringVar()
        self.var_is = []
        for file_smpl in self.files_smpl:
            if self.is_smpl[file_smpl][0] not in self.var_is:
                self.var_is.append(self.is_smpl[file_smpl][0])
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(5*90 + 2*175 + 3*60 + 15)
        height = int(2*20 + (self.n_isotopes)*30 + 15)
        self.data_expl_sig_ratios = tk.Toplevel(self.parent)
        self.data_expl_sig_ratios.geometry(str(width)+"x"+str(height))
        self.data_expl_sig_ratios.title("Simple Signals: Isotopic Ratios")
        #
        for y in range(int(2 + (self.n_isotopes + 1) + 1)):
            tk.Grid.rowconfigure(self.data_expl_sig_ratios, y, weight=1)
        for x in range(11):
            tk.Grid.columnconfigure(self.data_expl_sig_ratios, x, weight=1)
        #
        # Rows
        for i in range(0, 2):
            self.data_expl_sig_ratios.grid_rowconfigure(i, minsize=20)
        for i in range(2, int(2 + self.n_isotopes)):
            self.data_expl_sig_ratios.grid_rowconfigure(i, minsize=30)
        self.data_expl_sig_ratios.grid_rowconfigure(int(2 + self.n_isotopes), minsize=15)
        # Columns
        for i in range(0, 5):
            self.data_expl_sig_ratios.grid_columnconfigure(i, minsize=90)
        for i in range(5, 7):
            self.data_expl_sig_ratios.grid_columnconfigure(i, minsize=175)
        for i in range(7, 10):
            self.data_expl_sig_ratios.grid_columnconfigure(i, minsize=60)
        self.data_expl_sig_ratios.grid_columnconfigure(10, minsize=15)
        #
        ################################################################################################################
        ## Labels ######################################################################################################
        #
        SE(parent=self.data_expl_sig_ratios, row_id=0, column_id=0, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Isotopes")
        SE(parent=self.data_expl_sig_ratios, row_id=0, column_id=1, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Intensity")
        SE(parent=self.data_expl_sig_ratios, row_id=1, column_id=1, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.data_expl_sig_ratios, row_id=1, column_id=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.data_expl_sig_ratios, row_id=0, column_id=3, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Intensity Ratio")
        SE(parent=self.data_expl_sig_ratios, row_id=1, column_id=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.data_expl_sig_ratios, row_id=1, column_id=4, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        i = 0
        for isotope in self.measured_isotopes:
            SE(parent=self.data_expl_sig_ratios, row_id=2+i, column_id=0, fg=self.color_fg,
            bg=self.color_bg).create_label(text=isotope)
            i += 1
        #
        ################################################################################################################
        ## Entries #####################################################################################################
        #
        self.create_entries(parent=self.data_expl_sig_ratios, row_id=2, column_id=1,
                            entries_container=self.intensity_container_mu)
        self.create_entries(parent=self.data_expl_sig_ratios, row_id=2, column_id=2,
                            entries_container=self.intensity_container_sigma)
        self.create_entries(parent=self.data_expl_sig_ratios, row_id=2, column_id=3,
                            entries_container=self.intensity_ratio_container_mu)
        self.create_entries(parent=self.data_expl_sig_ratios, row_id=2, column_id=4,
                            entries_container=self.intensity_ratio_container_sigma)
        #
        ################################################################################################################
        ## Option Menus ################################################################################################
        #
        SE(parent=self.data_expl_sig_ratios, row_id=0, column_id=5, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_option_file(found_files=self.files_std, var_file=self.var_file_std,
                                                command=lambda file=self.var_file_std.get(),
                                                               file_type="STD":
                                                self.change_file_ratio(file, file_type))
        SE(parent=self.data_expl_sig_ratios, row_id=0, column_id=6, n_rows=2, fg=self.color_fg,
           bg=self.color_bg).create_option_file(found_files=self.files_smpl, var_file=self.var_file_smpl,
                                                command=lambda file=self.var_file_smpl.get(),
                                                               file_type="SMPL":
                                                self.change_file_ratio(file, file_type))
    #
    def change_file_ratio(self, file, file_type):
        file = file[0]
        #
        SE(parent=self.data_expl_sig_ratios, row_id=0, column_id=7, n_columns=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Last File:", relief=tk.FLAT)
        SE(parent=self.data_expl_sig_ratios, row_id=1, column_id=7, n_columns=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text=file, relief=tk.FLAT)
        #
        time_iw = None
        if file_type == "STD":
            for file_std in self.files_std:
                if file in file_std:
                    file = file_std
                    time_iw = self.time_iw_std[file_std]
        else:
            for file_smpl in self.files_smpl:
                if file in file_smpl:
                    file = file_smpl
                    time_iw = self.time_iw_smpl[file_smpl]
        #
        if file in self.files_smpl:
            var_is = self.is_smpl[file][0]
        else:
            var_is = self.var_is[0]
        #
        dataset = data.Data(filename=file)
        df_file = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        #
        bg_start = time_iw["BG"][0][0]
        bg_end = time_iw["BG"][0][1]
        sig_start = time_iw["SIG"][0][0]
        sig_end = time_iw["SIG"][0][1]
        #
        var_is_mu = df_file[var_is][sig_start:sig_end+1].mean() - df_file[var_is][bg_start:bg_end+1].mean()
        var_is_sigma = df_file[var_is][sig_start:sig_end+1] - df_file[var_is][bg_start:bg_end+1].mean()
        #
        data_ratio = []
        #
        for isotope in self.measured_isotopes:
            result_mu = df_file[isotope][sig_start:sig_end+1].mean() - df_file[isotope][bg_start:bg_end+1].mean()
            self.intensity_container_mu[isotope][2].delete(0, tk.END)
            self.intensity_container_mu[isotope][2].insert(0, round(result_mu, 6))
            #
            result_sigma = df_file[isotope][sig_start:sig_end+1] - df_file[isotope][bg_start:bg_end+1].mean()
            self.intensity_container_sigma[isotope][2].delete(0, tk.END)
            self.intensity_container_sigma[isotope][2].insert(0, round(result_sigma.std(), 6))
            #
            var_i_mu = df_file[isotope][sig_start:sig_end+1].mean() - df_file[isotope][bg_start:bg_end+1].mean()
            result_ratio_mu = var_i_mu/var_is_mu
            data_ratio.append(result_ratio_mu)
            self.intensity_ratio_container_mu[isotope][2].delete(0, tk.END)
            self.intensity_ratio_container_mu[isotope][2].insert(0, round(result_ratio_mu, 6))
            #
            var_i_sigma = df_file[isotope][sig_start:sig_end+1] - df_file[isotope][bg_start:bg_end+1].mean()
            result_ratio_sigma = var_i_sigma/var_is_sigma
            self.intensity_ratio_container_sigma[isotope][2].delete(0, tk.END)
            self.intensity_ratio_container_sigma[isotope][2].insert(0, round(result_ratio_sigma.std(), 6))
        #
        try:
            self.fig_bar.clf()
            self.ax_bar.cla()
            self.canvas_bar.get_tk_widget().pack_forget()
        except AttributeError:
            pass

        try:
            if self.canvas_bar:
                self.canvas_bar.destroy()
        except AttributeError:
            pass
        #
        self.canvas_bar = None
        #
        self.fig_bar = Figure(figsize=(12, 8), facecolor=self.color_bg)
        self.ax_bar = self.fig_bar.add_subplot()
        #
        self.ax_bar.axhline(1.0, color="tomato", linestyle="dashed")
        self.ax_bar.bar(self.measured_isotopes, data_ratio, edgecolor="black")
        self.ax_bar.set_xticklabels(self.measured_isotopes, rotation=90)
        self.ax_bar.grid(True)
        self.ax_bar.set_yscale("log")
        self.ax_bar.set_axisbelow(True)
        self.ax_bar.set_ylabel("Isotope ratio (*/"+str(var_is)+")", labelpad=0.5)
        self.fig_bar.subplots_adjust(bottom=0.15)
        #
        self.plotting_area_bar = tk.Frame(self.data_expl_sig_ratios, bg=self.color_bg)
        self.plotting_area_bar.grid(row=2, column=5, rowspan=self.n_isotopes, columnspan=5, sticky="nesw")
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=self.plotting_area_bar)
        self.canvas_bar.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #
    def smooth_all_isotopes(self, times):
        start = times.iloc[0]
        end = times.iloc[-1]
        helper_indices = []
        helper_indices.append(times[times == start].index[0])
        helper_indices.append(times[times == end].index[0])
        for isotope in self.measured_isotopes:
            self.se_id += 1
            self.se_idlist.append(self.se_id)
            self.positions_se.append([round(start, 4), round(end, 4)])
            self.indices_se_alt.append([helper_indices[0], helper_indices[1]])
            self.lb_se.insert(tk.END, "["+str(isotope)+"] #"+str(self.se_id)+" ["+str(start)+"-"+str(end)+"]")
            box_se = self.ax.axvspan(start, end, alpha=0.01, facecolor="khaki", edgecolor=self.colors_lines[isotope])
            self.limits_se[str(self.se_id)] = box_se
            self.canvas.draw()
            #
            if isotope not in self.spikes_isotopes:
                self.spikes_isotopes[isotope] = []
                self.spikes_isotopes[isotope].append([helper_indices[0], helper_indices[1]])
            else:
                self.spikes_isotopes[isotope].append([helper_indices[0], helper_indices[1]])
    #
    ####################################################################################################################
    # WINDOW - DRIFT CORRECTION ########################################################################################
    ####################################################################################################################
    #
    def drift_correction_window(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        option_list_i = self.measured_isotopes
        option_list_is = self.is_found
        self.var_opt_i = tk.StringVar()
        self.var_opt_i.set("Set Isotope")
        self.var_opt_is = tk.StringVar()
        self.var_opt_is.set(option_list_is[0])
        #
        self.analytical_sensitivity = {}
        self.relative_sensitivity = {}
        self.entries_container = {}
        for file_std in self.files_std:
            self.entries_container[file_std] = {}
            for key_xi in ["sensitivity"]:
                self.entries_container[file_std][key_xi] = {}
                for key_param in ["mu", "sigma"]:
                    self.entries_container[file_std][key_xi][key_param] = None
        for file_smpl in self.files_smpl:
            self.entries_container[file_smpl] = {}
            for key_xi in ["sensitivity"]:
                self.entries_container[file_smpl][key_xi] = {}
                for key_param in ["mu", "sigma"]:
                    self.entries_container[file_smpl][key_xi][key_param] = None
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(150 + 4*90 + 5*100 + 15)
        if int(len(self.files_std) + len(self.files_smpl)) > 17:
            height = int(2*30 + (len(self.files_std) + len(self.files_smpl))*30 + 15)
        else:
            height = int(2*30 + 17*30 + 15)
        #
        self.drift_window = tk.Toplevel(self.parent)
        self.drift_window.geometry(str(width)+"x"+str(height))
        self.drift_window.title("Simple Signals: Drift Correction")
        #
        if int(len(self.files_std) + len(self.files_smpl)) > 17:
            for y in range(int(2+len(self.files_std)+len(self.files_smpl)+1)):
                tk.Grid.rowconfigure(self.drift_window, y, weight=1)
        else:
            for y in range(20):
                tk.Grid.rowconfigure(self.drift_window, y, weight=1)
        for x in range(11):
            tk.Grid.columnconfigure(self.drift_window, x, weight=1)
        #
        # Rows
        for i in range(0, 2):
            self.drift_window.grid_rowconfigure(i, minsize=30)
        if int(len(self.files_std) + len(self.files_smpl)) > 17:
            for i in range(2, int(2+len(self.files_std)+len(self.files_smpl))):
                self.drift_window.grid_rowconfigure(i, minsize=30)
            self.drift_window.grid_rowconfigure(int(len(self.files_std)+len(self.files_smpl)+3), minsize=15)
        else:
            for i in range(2, 19):
                self.drift_window.grid_rowconfigure(i, minsize=30)
            self.drift_window.grid_rowconfigure(19, minsize=15)
        # Columns
        self.drift_window.grid_columnconfigure(0, minsize=150)
        for i in range(1, 5):
            self.drift_window.grid_columnconfigure(i, minsize=90)
        for i in range(5, 10):
            self.drift_window.grid_columnconfigure(i, minsize=100)
        self.drift_window.grid_columnconfigure(10, minsize=15)
        #
        ################################################################################################################
        ## Labels ######################################################################################################
        #
        i = 0
        for file in self.files_std:
            parts = file.split("/")
            self.analytical_sensitivity[file] = {"mu": tk.StringVar(), "sigma": tk.StringVar()}
            self.relative_sensitivity[file] = {"mu": tk.StringVar(), "sigma": tk.StringVar()}
            SE(parent=self.drift_window, row_id=2+i, column_id=0, fg=self.color_fg,
               bg=self.color_bg).create_label(text=parts[-1])
            i += 1
        #
        i = int(2+len(self.files_std))
        for file in self.files_smpl:
            parts = file.split("/")
            self.analytical_sensitivity[file] = {"mu": tk.StringVar(), "sigma": tk.StringVar()}
            self.relative_sensitivity[file] = {"mu": tk.StringVar(), "sigma": tk.StringVar()}
            SE(parent=self.drift_window, row_id=i, column_id=0, fg=self.color_fg,
               bg=self.color_bg).create_label(text=parts[-1])
            i += 1
        #
        SE(parent=self.drift_window, row_id=0, column_id=1, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Sensitivity \u03BE (cps/ppm)")
        SE(parent=self.drift_window, row_id=1, column_id=1, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.drift_window, row_id=1, column_id=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="\u03C3")
        #
        ################################################################################################################
        ## Entries #++++################################################################################################
        #
        self.create_entries_drift(parent=self.drift_window, row_id=2, column_id=1, key_xi="sensitivity", key_param="mu")
        self.create_entries_drift(parent=self.drift_window, row_id=2, column_id=2, key_xi="sensitivity", key_param="sigma")
        #
        ################################################################################################################
        ## Option Menus ################################################################################################
        #
        opt_menu_i = tk.OptionMenu(self.drift_window, self.var_opt_i, *option_list_i,
                                   command=lambda op, var_i=self.var_opt_i, var_is=self.var_opt_is:
                                   self.select_isotope_drift(var_i, var_is, op))
        opt_menu_i.grid(row=0, column=0, sticky="nesw")
        #
        opt_menu_is = tk.OptionMenu(self.drift_window, self.var_opt_is, *option_list_is)
        opt_menu_is.grid(row=1, column=0, sticky="nesw")
        #
    #
    def create_entries_drift(self, parent, row_id, column_id, key_xi, key_param):
        i = 0
        for file in self.files_std:
            if key_xi == "sensitivity":
                if key_param == "mu":
                    variable = self.analytical_sensitivity[file]["mu"]
                else:
                    variable = self.analytical_sensitivity[file]["sigma"]
                variable.set(0.0)
                entr = tk.Entry(parent, textvariable=variable)
                entr.grid(row=row_id+i, column=column_id, sticky="nesw")
                self.entries_container[file][key_xi][key_param] = entr
            i += 1
        #
        j = len(self.files_std)
        for file in self.files_smpl:
            if key_xi == "sensitivity":
                if key_param == "mu":
                    variable = self.analytical_sensitivity[file]["mu"]
                else:
                    variable = self.analytical_sensitivity[file]["sigma"]
                variable.set(0.0)
                entr = tk.Entry(parent, textvariable=variable)
                entr.grid(row=row_id+j, column=column_id, sticky="nesw")
                self.entries_container[file][key_xi][key_param] = entr
            j += 1
    #
    def select_isotope_drift(self, var_i, var_is, op):
        isotope = str(var_i.get())
        internal_standard = var_is.get()
        sensitivity_helper = {}
        #
        for file_std in self.files_std:
            # mu_i = float(self.sensitivities_helper[isotope][file_std][0])
            # sigma_i = float(self.sensitivities_helper[isotope][file_std][1])
            mu_i = self.sensitivities_regression[isotope][file_std]["mu"]
            sigma_i = self.sensitivities_regression[isotope][file_std]["sigma"]
            sensitivity_helper[file_std] = [mu_i, sigma_i, self.times_delta_files[file_std]]
            self.entries_container[file_std]["sensitivity"]["mu"].delete(0, tk.END)
            self.entries_container[file_std]["sensitivity"]["mu"].insert(0, round(mu_i, 6))
            self.entries_container[file_std]["sensitivity"]["sigma"].delete(0, tk.END)
            self.entries_container[file_std]["sensitivity"]["sigma"].insert(0, round(sigma_i, 6))
        for file_smpl in self.files_smpl:
            # mu_i = float(self.results_sensitivities_indiv[file_smpl][isotope][0])
            # sigma_i = float(self.results_sensitivities_indiv[file_smpl][isotope][1])
            mu_i = self.sensitivities_regression[isotope][file_smpl]["mu"]
            sigma_i = self.sensitivities_regression[isotope][file_smpl]["sigma"]
            sensitivity_helper[file_smpl] = [mu_i, sigma_i, self.times_delta_files[file_smpl]]
            self.entries_container[file_smpl]["sensitivity"]["mu"].delete(0, tk.END)
            self.entries_container[file_smpl]["sensitivity"]["mu"].insert(0, round(mu_i, 6))
            self.entries_container[file_smpl]["sensitivity"]["sigma"].delete(0, tk.END)
            self.entries_container[file_smpl]["sensitivity"]["sigma"].insert(0, round(sigma_i, 6))
        #
        x_srm = []
        x_smpl = []
        y_srm = []
        y_smpl = []
        first_xi_smpl = []
        last_xi_smpl = []
        for file, values in sensitivity_helper.items():
            if file in self.files_std:
                x_srm.append(values[2])
                y_srm.append(values[0])
            elif file in self.files_smpl:
                x_smpl.append(values[2])
                y_smpl.append(values[0])
                if len(first_xi_smpl) == 0 and len(last_xi_smpl) == 0:
                    first_xi_smpl.extend([values[2], values[0]])
                    last_xi_smpl.extend([values[2], values[0]])
                else:
                    if values[2] < first_xi_smpl[0]:
                        first_xi_smpl.clear()
                        first_xi_smpl.extend([values[2], values[0]])
                    elif values[2] > last_xi_smpl[0]:
                        last_xi_smpl.clear()
                        last_xi_smpl.extend([values[2], values[0]])
        #
        self.canvas_drift = None
        self.fig_drift = Figure(facecolor=self.color_bg)
        # self.ax_drift = self.fig_drift.add_subplot(211)
        # self.ax_drift_change = self.fig_drift.add_subplot(212)
        self.ax_drift = self.fig_drift.add_subplot()
        #
        x_regr = np.arange(min(x_srm), max(x_srm))
        y_regr = self.xi_opt[isotope][0]*x_regr + self.xi_opt[isotope][1]
        #
        self.ax_drift.scatter(x_srm, y_srm, label="SRM", edgecolor="black")
        self.ax_drift.scatter(x_smpl, y_smpl, label="SMPL", color="tomato", edgecolor="black")
        self.ax_drift.plot(x_regr, y_regr, linestyle="dashed", color="tomato",)
        self.ax_drift.grid(True)
        self.ax_drift.set_title("Sensitivity drift of "+str(isotope), fontsize=11)
        self.ax_drift.set_ylabel("Sensitivity $\\xi$ (cps/ppm)", labelpad=0.5)
        self.ax_drift.set_xlabel("Time (s)", labelpad=0.5)
        self.ax_drift.set_axisbelow(True)
        self.ax_drift.legend(fontsize="x-small", framealpha=1.0, loc="best")
        plt.tight_layout()
        #
        # self.fig_drift.subplots_adjust(left=0.2, hspace=0.4)

        self.plotting_area_drift = tk.Frame(self.drift_window, bg=self.color_bg)
        self.plotting_area_drift.grid(row=0, column=5, rowspan=19, columnspan=5, sticky="nesw")
        self.canvas_drift = FigureCanvasTkAgg(self.fig_drift, master=self.plotting_area_drift)
        self.canvas_drift.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)