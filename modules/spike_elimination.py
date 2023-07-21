#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		spike_elimination.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		21.07.2023

#-----------------------------------------------

## MODULES
import numpy as np
import scipy.stats as stats
from math import sqrt
from collections import defaultdict
import pandas as pd
import tkinter as tk
#from modules.gui_elements import SimpleElements as SE
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

## CLASSES
# class SpikeElimination:
#     #
#     def __init__(self, container_lists, gui_elements, container_spikes):
#         self.container_lists = container_lists
#         self.gui_elements = gui_elements
#         self.container_spikes = container_spikes
#         #
#         self.green_light = self.container_lists["Colors PySILLS"]["Light"]["Green"]
#         self.green_medium = self.container_lists["Colors PySILLS"]["Medium"]["Green"]
#         self.green_dark = self.container_lists["Colors PySILLS"]["Dark"]["Green"]
#         self.red_dark = self.container_lists["Colors PySILLS"]["Dark"]["Red"]
#         #
#         self.container_gui = {}
#         self.container_var_spk = {}
#         categories = ["Frame", "Label", "Radiobutton", "Checkbox", "Canvas"]
#         subcategories = ["Specific", "Temporary"]
#         for category in categories:
#             self.container_gui[category] = {}
#             self.container_var_spk[category] = {}
#             for subcategory in subcategories:
#                 if subcategory == "Temporary":
#                     self.container_gui[category][subcategory] = []
#                 else:
#                     self.container_gui[category][subcategory] = {}
#         #
#         self.outlier_isotopes = {}
#         #
#         for var_filetype in ["STD", "SMPL"]:
#             for var_file in self.container_lists[var_filetype]["Short"]:
#                 if var_file not in self.outlier_isotopes:
#                     self.outlier_isotopes[var_file] = {}
#                     for isotope in self.container_lists["ISOTOPES"]:
#                         if var_file in self.container_spikes:
#                             if len(self.container_spikes[var_file][isotope]["Indices"]) > 0:
#                                 self.outlier_isotopes[var_file][isotope] = {}
#         #
#         self.last_isotope = None
#     #
#     def spike_elimination_check(self, filetype):
#         ## Window Geometry
#         self.new_window = tk.Toplevel()
#         self.new_window.geometry("1200x900")
#         self.new_window["bg"] = self.green_light
#         #
#         window_width = 1200
#         window_heigth = 900
#         row_min = 15
#         n_rows = int(window_heigth/row_min)
#         column_min = 15
#         n_columns = int(window_width/column_min)
#         #
#         for x in range(n_columns):
#             tk.Grid.columnconfigure(self.new_window, x, weight=1)
#         for y in range(n_rows):
#             tk.Grid.rowconfigure(self.new_window, y, weight=1)
#         #
#         # Rows
#         for i in range(0, n_rows):
#             self.new_window.grid_rowconfigure(i, minsize=row_min)
#         # Columns
#         for i in range(0, n_columns):
#             self.new_window.grid_columnconfigure(i, minsize=column_min)
#         #
#         ## Label
#         lb_file = SE(
#             parent=self.new_window, row_id=4, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
#             bg=self.green_dark).create_simple_label(text="Select File", relief=tk.GROOVE, fontsize="sans 10 bold")
#         lb_isotope = SE(
#             parent=self.new_window, row_id=8, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
#             bg=self.green_dark).create_simple_label(text="Select Isotope", relief=tk.GROOVE, fontsize="sans 10 bold")
#         lb_fast = SE(
#             parent=self.new_window, row_id=0, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
#             bg=self.green_dark).create_simple_label(text="Quick Check", relief=tk.GROOVE, fontsize="sans 10 bold")
#         lb_outlier = SE(
#             parent=self.new_window, row_id=12, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
#             bg=self.green_dark).create_simple_label(text="Found Outlier", relief=tk.GROOVE, fontsize="sans 10 bold")
#         lb_outlier2 = SE(
#             parent=self.new_window, row_id=14, column_id=0, n_rows=2, n_columns=6, fg=self.green_light,
#             bg=self.green_medium).create_simple_label(text="Isotope", relief=tk.GROOVE, fontsize="sans 10 bold")
#         lb_outlier3 = SE(
#             parent=self.new_window, row_id=14, column_id=6, n_rows=2, n_columns=4, fg=self.green_light,
#             bg=self.green_medium).create_simple_label(text="Accept", relief=tk.GROOVE, fontsize="sans 10 bold")
#         #
#         ## Option Menu
#         self.var_opt_file = tk.StringVar()
#         self.var_opt_file.set(self.container_lists[filetype]["Short"][0])
#         var_file = self.container_lists[filetype]["Short"][0]
#         self.opt_file = SE(
#             parent=self.new_window, row_id=6, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
#             bg=self.green_medium).create_option_menu(
#             var_opt=self.var_opt_file, text_set=self.var_opt_file.get(), fg_active=self.green_dark,
#             bg_active=self.red_dark, option_list=self.container_lists[filetype]["Short"],
#             command=lambda event: self.change_file_spikes(event))
#         #
#         self.var_opt_isotope = tk.StringVar()
#         self.var_opt_isotope.set(self.container_lists["ISOTOPES"][0])
#         if len(list(self.outlier_isotopes[var_file].keys())) > 0:
#             self.opt_isotope = SE(
#                 parent=self.new_window, row_id=10, column_id=0, n_rows=2, n_columns=10, fg=self.green_light,
#                 bg=self.green_medium).create_option_menu(
#                 var_opt=self.var_opt_isotope, text_set=self.var_opt_isotope.get(), fg_active=self.green_dark,
#                 bg_active=self.red_dark, option_list=list(self.outlier_isotopes[var_file].keys()),
#                 command=lambda var_iso=self.var_opt_isotope: self.change_isotope_spikes(var_iso))
#         #
#         ## Button
#         btn_fast = SE(
#             parent=self.new_window, row_id=2, column_id=0, n_rows=2, n_columns=10, fg=self.green_dark,
#             bg=self.red_dark).create_simple_button(
#             text="Confirm All Spikes", bg_active=self.green_dark, fg_active=self.green_light,
#             command=lambda var_filetype=filetype: self.confirm_all_spikes(var_filetype))
#     #
#     def confirm_all_spikes(self, var_filetype):
#         if var_filetype == "STD":
#             frm_item = self.gui_elements["ma_setting"]["Frame"]["Specific"][0]
#         elif var_filetype == "SMPL":
#             frm_item = self.gui_elements["ma_setting"]["Frame"]["Specific"][1]
#         #
#         frm_item.configure(background=self.container_lists["Colors PySILLS"]["Sign"]["Green"])
#     #
#     def change_file_spikes(self, event):
#         var_file = self.var_opt_file.get()
#         #
#         ## Cleaning
#         for category in ["Radiobutton", "Checkbox"]:
#             if len(self.container_gui[category]["Temporary"]) > 0:
#                 for gui_item in self.container_gui[category]["Temporary"]:
#                     gui_item.grid_remove()
#                 #
#                 self.container_gui[category]["Temporary"].clear()
#         #
#         ## Reset
#         self.var_opt_isotope.set(list(self.outlier_isotopes[var_file].keys())[0])
#         self.opt_isotope["menu"].delete(0, "end")
#         for isotope in list(self.outlier_isotopes[var_file].keys()):
#             self.opt_isotope["menu"].add_command(
#                 label=isotope, command=lambda var_iso=isotope: self.change_isotope_spikes(var_iso))
#     #
#     def change_isotope_spikes(self, var_iso):
#         var_isotope = var_iso
#         self.var_opt_isotope.set(var_isotope)
#         var_file = self.var_opt_file.get()
#         var_indices = self.container_spikes[var_file][var_isotope]["Indices"]
#         #
#         # if var_file not in self.outlier_isotopes:
#         #     self.outlier_isotopes[var_file] = []
#         #     for isotope in self.container_lists["ISOTOPES"]:
#         #         if len(self.container_spikes[var_file][isotope]["Indices"]) > 0:
#         #             self.outlier_isotopes[var_file].append(isotope)
#         #
#         ## Cleaning
#         for category in ["Radiobutton", "Checkbox"]:
#             if len(self.container_gui[category]["Temporary"]) > 0:
#                 for gui_item in self.container_gui[category]["Temporary"]:
#                     gui_item.grid_remove()
#                 #
#                 self.container_gui[category]["Temporary"].clear()
#         #
#         if self.last_isotope != var_isotope and len(var_indices) > 0:
#             ## GUI
#             if var_file not in self.container_gui["Radiobutton"]["Specific"]:
#                 self.container_gui["Radiobutton"]["Specific"][var_file] = {}
#                 self.container_gui["Checkbox"]["Specific"][var_file] = {}
#             if var_isotope not in self.container_gui["Radiobutton"]["Specific"][var_file]:
#                 self.container_gui["Radiobutton"]["Specific"][var_file][var_isotope] = []
#                 self.container_gui["Checkbox"]["Specific"][var_file][var_isotope] = []
#             # if len(var_indices) > 0:
#             #     self.outlier_isotopes[var_file].append(var_isotope)
#             #
#             ## Reconstruction
#             for category in ["Radiobutton", "Checkbox"]:
#                 if var_file in self.container_gui[category]["Specific"]:
#                     if var_isotope in self.container_gui[category]["Specific"][var_file]:
#                         if len(self.container_gui[category]["Specific"][var_file][var_isotope]) > 0:
#                             for gui_item in self.container_gui[category]["Specific"][var_file][var_isotope]:
#                                 gui_item.grid()
#                                 self.container_gui[category]["Temporary"].append(gui_item)
#             #
#             ## Variables
#             if var_file not in self.container_var_spk["Radiobutton"]:
#                 self.container_var_spk["Radiobutton"][var_file] = {}
#             if var_isotope not in self.container_var_spk["Radiobutton"][var_file]:
#                 self.container_var_spk["Radiobutton"][var_file][var_isotope] = tk.IntVar()
#                 self.container_var_spk["Radiobutton"][var_file][var_isotope].set(0)
#             #
#             if var_file not in self.container_var_spk["Checkbox"]:
#                 self.container_var_spk["Checkbox"][var_file] = {}
#             if var_isotope not in self.container_var_spk["Checkbox"][var_file]:
#                 self.container_var_spk["Checkbox"][var_file][var_isotope] = {}
#             #
#             frm_spikes = SE(
#                 parent=self.new_window, row_id=16, column_id=0, n_rows=20, n_columns=10,
#                 fg=self.green_light, bg=self.green_light).create_frame()
#             self.vsb = tk.Scrollbar(master=frm_spikes, orient="vertical")
#             self.text = tk.Text(master=frm_spikes, width=30, height=15, yscrollcommand=self.vsb.set, bg=self.green_light)
#             self.vsb.config(command=self.text.yview)
#             self.vsb.pack(side="right", fill="y")
#             self.text.pack(side="left", fill="both", expand=True)
#             #
#             var_indices = np.sort(var_indices)
#             if len(self.container_gui["Radiobutton"]["Specific"][var_file][var_isotope]) == 0:
#                 for index, var_index in enumerate(var_indices):
#                     if var_index not in self.container_var_spk["Checkbox"][var_file][var_isotope]:
#                         self.container_var_spk["Checkbox"][var_file][var_isotope][var_index] = tk.IntVar()
#                         self.container_var_spk["Checkbox"][var_file][var_isotope][var_index].set(1)
#                     #
#                     cb_i = tk.Checkbutton(
#                         master=frm_spikes, text="#"+str(var_index), fg=self.green_dark, bg=self.green_light,
#                         variable=self.container_var_spk["Checkbox"][var_file][var_isotope][var_index],
#                         command=lambda var_cb=self.container_var_spk["Checkbox"][var_file][var_isotope][var_index],
#                                        var_file=var_file, var_isotope=var_isotope, var_index=var_index:
#                         self.change_cb_state(var_cb, var_file, var_isotope, var_index))
#                     self.text.window_create("end", window=cb_i)
#                     self.text.insert("end", "\n")
#         #
#         self.last_isotope = var_isotope
#         #
#         self.show_diagram(var_file=var_file, var_indices=var_indices)
#     #
#     def show_outliers(self, event):
#         var_file = self.var_opt_file.get()
#         if var_file not in self.container_gui["Radiobutton"]["Specific"]:
#             self.container_gui["Radiobutton"]["Specific"][var_file] = []
#             self.container_gui["Label"]["Specific"][var_file] = []
#             self.container_gui["Checkbox"]["Specific"][var_file] = []
#             self.outlier_isotopes[var_file] = []
#         #
#         ## Cleaning
#         for category in ["Frame", "Label", "Radiobutton", "Checkbox"]:
#             if len(self.container_gui[category]["Temporary"]) > 0:
#                 for gui_item in self.container_gui[category]["Temporary"]:
#                     gui_item.grid_remove()
#                 #
#                 self.container_gui[category]["Temporary"].clear()
#         #
#         ## Reconstruction
#         for category in ["Frame", "Label", "Radiobutton", "Checkbox"]:
#             if var_file in self.container_gui[category]["Specific"]:
#                 if len(self.container_gui[category]["Specific"][var_file]) > 0:
#                     for gui_item in self.container_gui[category]["Specific"][var_file]:
#                         gui_item.grid()
#         #
#         if len(self.container_gui["Label"]["Specific"][var_file]) == 0:
#             index = 0
#             for key, value in self.container_spikes[var_file].items():
#                 if len(value["Indices"]) > 0:
#                     self.outlier_isotopes[var_file].append(key)
#                     #
#                     ## Radiobutton
#                     if var_file not in self.container_var_spk["Radiobutton"]:
#                         self.container_var_spk["Radiobutton"][var_file] = tk.IntVar()
#                         self.container_var_spk["Radiobutton"][var_file].set(0)
#                     #
#                     rb_isotope = SE(
#                         parent=self.new_window, row_id=16 + 2*index, column_id=0, n_rows=2, n_columns=2,
#                         fg=self.green_light, bg=self.green_medium).create_radiobutton(
#                         var_rb=self.container_var_spk["Radiobutton"][var_file], value_rb=index, color_bg=self.green_medium,
#                         fg=self.green_light, text="", sticky="nesw", relief=tk.GROOVE,
#                         command=lambda var_rb=self.container_var_spk["Radiobutton"][var_file], var_file=var_file:
#                         self.change_rb_isotope(var_rb, var_file))
#                     #
#                     ## Labels
#                     lbl_isotope = SE(
#                         parent=self.new_window, row_id=16 + 2*index, column_id=2, n_rows=2, n_columns=4,
#                         fg=self.green_light, bg=self.green_medium).create_simple_label(
#                         text=key, relief=tk.GROOVE, fontsize="sans 10 bold")
#                     #
#                     ## Checkboxes
#                     if var_file not in self.container_var_spk["Checkbox"]:
#                         self.container_var_spk["Checkbox"][var_file] = {}
#                     #
#                     if key not in self.container_var_spk["Checkbox"][var_file]:
#                         self.container_var_spk["Checkbox"][var_file][key] = tk.IntVar()
#                         self.container_var_spk["Checkbox"][var_file][key].set(1)
#                     #
#                     cb_isotope = SE(
#                         parent=self.new_window, row_id=16 + 2*index, column_id=6, fg=self.green_light, n_rows=2,
#                         n_columns=4, bg=self.green_medium).create_checkbox(
#                         var_cb=self.container_var_spk["Checkbox"][var_file][key], text="")
#                     #
#                     index += 1
#                     #
#                     self.container_gui["Radiobutton"]["Temporary"].append(rb_isotope)
#                     self.container_gui["Label"]["Temporary"].append(lbl_isotope)
#                     self.container_gui["Checkbox"]["Temporary"].append(cb_isotope)
#                     #
#                     self.container_gui["Radiobutton"]["Specific"][var_file].append(rb_isotope)
#                     self.container_gui["Label"]["Specific"][var_file].append(lbl_isotope)
#                     self.container_gui["Checkbox"]["Specific"][var_file].append(cb_isotope)
#     #
#     def show_diagram(self, var_file, var_indices):
#         var_isotope = self.var_opt_isotope.get()
#         var_times = self.container_spikes[var_file][var_isotope]["Times"]
#         self.var_raw = self.container_spikes[var_file][var_isotope]["Data RAW"]
#         self.var_smoothed = self.container_spikes[var_file][var_isotope]["Data SMOOTHED"]
#         # for index, value in enumerate(self.var_raw):
#         #     if value != self.var_smoothed[index]:
#         #         print(index, value, self.var_smoothed[index])
#         x_min = min(var_times)
#         x_max = max(var_times)
#         #
#         ## Diagram
#         fig = Figure(figsize=(10, 5), facecolor=self.green_light)
#         self.ax = fig.add_subplot()
#         #
#         self.ax.plot(var_times, self.var_raw, color=self.container_lists["Isotope Colors"][var_isotope], linestyle="--")
#         self.ax.plot(var_times, self.var_smoothed, color=self.container_lists["Isotope Colors"][var_isotope],
#                      linestyle="-")
#         #
#         for var_index in var_indices:
#             outlier_raw = self.ax.scatter(
#                 var_times[var_index], self.var_raw[var_index],
#                 color=self.container_lists["Isotope Colors"][var_isotope], marker="o", s=30, edgecolor="black")
#             outlier_smoothed = self.ax.scatter(
#                 var_times[var_index], self.var_smoothed[var_index],
#                 color=self.container_lists["Isotope Colors"][var_isotope], marker="s", s=30, edgecolor="black")
#         #
#         self.ax.set_xlim(x_min, x_max)
#         self.ax.set_yscale("log")
#         self.ax.grid()
#         #
#         self.canvas = FigureCanvasTkAgg(fig, master=self.new_window)
#         self.canvas.get_tk_widget().grid(row=0, column=12, rowspan=45, columnspan=60, sticky="nesw")
#         toolbarFrame = tk.Frame(master=self.new_window)
#         toolbarFrame.grid(row=45, column=12, rowspan=2, columnspan=60, sticky="w")
#         toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
#         toolbar.config(background=self.green_light)
#         toolbar._message_label.config(background=self.green_light)
#         toolbar.winfo_children()[-2].config(background=self.green_light)
#     #
#     def change_rb_isotope(self, var_index):
#         var_file = self.var_opt_file.get()
#         var_isotope = self.var_opt_isotope.get()
#         #
#         ## Cleaning
#         try:
#             self.outlier_isotopes[var_file][var_isotope][self.last_index].set_visible(False)
#             self.canvas.draw()
#         except:
#             pass
#         #
#         var_times = self.container_spikes[var_file][var_isotope]["Times"]
#         var_raw = self.container_spikes[var_file][var_isotope]["Data RAW"]
#         #
#         outlier_time = self.ax.axvline(
#             x=var_times[var_index], ymin=0, ymax=2*max(var_raw), color="black", linestyle="--")
#         self.outlier_isotopes[var_file][var_isotope][var_index] = outlier_time
#         #
#         self.canvas.draw()
#         #
#         self.last_index = var_index
#     #
#     def change_cb_state(self, var_cb, var_file, var_isotope, var_index):
#         if var_file not in self.container_spikes["Selection"]:
#             self.container_spikes["Selection"][var_file] = {}
#         #
#         if var_isotope not in self.container_spikes["Selection"][var_file]:
#             self.container_spikes["Selection"][var_file][var_isotope] = {}
#         #
#         if var_cb.get() == 0:
#             self.container_spikes["Selection"][var_file][var_isotope][var_index] = self.var_raw[var_index]
#         else:
#             self.container_spikes["Selection"][var_file][var_isotope][var_index] = self.var_smoothed[var_index]

class GrubbsTestSILLS:
    def __init__(self, raw_data, alpha, threshold, start_index, dataset_complete):
        self.raw_data = raw_data
        self.alpha = alpha
        self.threshold = threshold
        #self.val_check_3 = 2.097
        #self.val_check_4 = 2.323
        self.smoothed_data = []
        self.spike_indices = []
        self.start_index = start_index
        self.dataset_complete = dataset_complete

    def determine_outlier(self):
        helper_data = {}
        for index, value in enumerate(self.raw_data):
            if value >= self.threshold:
                surrounding_3 = self.determine_surrounded_values(index=index, stepsize=3)
                surrounding_4 = self.determine_surrounded_values(index=index, stepsize=4)

                mean_3 = np.mean(surrounding_3["All"])
                std_3 = np.std(surrounding_3["All"], ddof=1)
                mean_4 = np.mean(surrounding_4["All"])
                std_4 = np.std(surrounding_4["All"], ddof=1)

                val_poi_3 = round(abs(value - mean_3)/std_3, 3)
                val_poi_4 = round(abs(value - mean_4)/std_4, 3)

                val_crit_3 = round(self.calculate_grubbs_critical_value(size=len(surrounding_3["All"])), 3)
                val_crit_4 = round(self.calculate_grubbs_critical_value(size=len(surrounding_4["All"])), 3)

                if val_poi_3 > val_crit_3 and val_poi_4 > val_crit_4:
                    val_corr = np.mean(surrounding_3["SP"])
                    self.spike_indices.append(index + self.start_index)
                    helper_data[index + self.start_index] = val_corr

        for index, value in enumerate(self.dataset_complete):
            if index in self.spike_indices:
                self.smoothed_data.append(helper_data[index])
            else:
                self.smoothed_data.append(value)

        return self.smoothed_data, self.spike_indices

    def determine_surrounded_values(self, index, stepsize=4):
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.raw_data[index]
        helper_values["POI"] = val_poi
        helper_values["All"].append(val_poi)

        for step in range(1, stepsize):
            step_before = index - step
            step_after = index + step
            if step_before >= 0:
                helper_values["SP"].append(self.raw_data[step_before])
                helper_values["All"].append(self.raw_data[step_before])
            if step_after < len(self.raw_data):
                helper_values["SP"].append(self.raw_data[step_after])
                helper_values["All"].append(self.raw_data[step_after])

        return helper_values

    def calculate_grubbs_critical_value(self, size):
        t_dist = stats.t.ppf(1 - self.alpha/(2*size), size - 2)
        numerator = (size - 1)*np.sqrt(np.square(t_dist))
        denominator = np.sqrt(size)*np.sqrt(size - 2 + np.square(t_dist))
        critical_value = numerator/denominator

        return critical_value

class GrubbsTest:
    def __init__(self, raw_data, alpha, threshold, start_index, dataset_complete):
        self.raw_data = raw_data
        self.alpha = alpha
        self.threshold = threshold
        self.smoothed_data = []
        self.spike_indices = []
        self.start_index = start_index
        self.dataset_complete = dataset_complete

    def determine_outlier(self):
        helper_data = {}
        for index, value in enumerate(self.raw_data):
            if value >= self.threshold:
                surrounding_3 = self.determine_surrounded_values(index=index, stepsize=3)
                surrounding_4 = self.determine_surrounded_values(index=index, stepsize=4)
                val_poi_3, index_poi_3 = self.calculate_grubbs_value()
                val_poi_3 = round(val_poi_3, 3)
                val_crit_3 = round(self.calculate_grubbs_critical_value(size=len(surrounding_3["All"])), 3)
                val_poi_4, index_poi_4 = self.calculate_grubbs_value()
                val_poi_4 = round(val_poi_4, 3)
                val_crit_4 = round(self.calculate_grubbs_critical_value(size=len(surrounding_4["All"])), 3)

                if val_poi_3 > val_crit_3 and val_poi_4 > val_crit_4:
                    val_corr = np.mean(surrounding_3["SP"])
                    self.spike_indices.append(index + self.start_index)
                    helper_data[index + self.start_index] = val_corr

        for index, value in enumerate(self.dataset_complete):
            if index in self.spike_indices:
                self.smoothed_data.append(helper_data[index])
            else:
                self.smoothed_data.append(value)

        return self.smoothed_data, self.spike_indices

    def determine_surrounded_values(self, index, stepsize=4):
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.raw_data[index]
        helper_values["POI"] = val_poi
        helper_values["All"].append(val_poi)

        for step in range(1, stepsize):
            step_before = index - step
            step_after = index + step
            if step_before >= 0:
                helper_values["SP"].append(self.raw_data[step_before])
                helper_values["All"].append(self.raw_data[step_before])
            if step_after < len(self.raw_data):
                helper_values["SP"].append(self.raw_data[step_after])
                helper_values["All"].append(self.raw_data[step_after])

        return helper_values

    def calculate_grubbs_critical_value(self, size):
        t_dist = stats.t.ppf(1 - self.alpha/(2*size), size - 2)
        numerator = (size - 1)*np.sqrt(np.square(t_dist))
        denominator = np.sqrt(size)*np.sqrt(size - 2 + np.square(t_dist))
        critical_value = numerator/denominator

        return critical_value

    def calculate_grubbs_value(self):
        std_dev = np.std(self.raw_data, ddof=1)
        avg_y = np.mean(self.raw_data)
        abs_val_minus_avg = abs(np.array(self.raw_data) - avg_y)
        max_of_deviations = max(abs_val_minus_avg)
        max_ind = np.argmax(abs_val_minus_avg)
        Gcal = max_of_deviations/std_dev

        return Gcal, max_ind


__all__ = ['two_sided_test_indices',
           'two_sided_test_outliers',
           'TwoSidedGrubbsTest',
           'OutputType']


DEFAULT_ALPHA = 0.95


# Test output types
class OutputType:
    DATA = 0  # Output data without outliers
    OUTLIERS = 1  # Output outliers
    INDICES = 2  # Output outlier indices


class GrubbsTestAlternative(object):
    def __init__(self, data):
        self.original_data = data

    def _copy_data(self):
        if isinstance(self.original_data, np.ndarray):
            return self.original_data
        elif pd is not None and isinstance(self.original_data, pd.Series):
            return self.original_data
        elif isinstance(self.original_data, list):
            return np.array(self.original_data)
        else:
            raise TypeError('Unsupported data format')

    def _delete_item(self, data, index):
        if pd is not None and isinstance(data, pd.Series):
            return data.drop(index)
        elif isinstance(data, np.ndarray):
            return np.delete(data, index)
        else:
            raise TypeError('Unsupported data format')

    def _get_indices(self, values):
        last_seen = defaultdict(lambda: 0)
        data = list(self.original_data)
        indices = list()
        for value in values:
            start = last_seen[value]
            index = data.index(value, start)
            indices.append(index)
            last_seen[value] = index + 1
        return indices

    def _get_g_test(self, data, alpha):
        """Compute a significant value score following these steps, being alpha
        the requested significance level:

        1. Find the upper critical value of the t-distribution with n-2
           degrees of freedom and a significance level of alpha/2n
           (for two-sided tests) or alpha/n (for one-sided tests).

        2. Use this t value to find the score with the following formula:
           ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))

        :param numpy.array data: data set
        :param float alpha: significance level
        :return: G_test score
        """
        n = len(data)
        significance_level = self._get_t_significance_level(alpha, n)
        t = stats.t.isf(significance_level, n-2)
        return ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))

    def _test_once(self, data, alpha):
        """Perform one iteration of the Smirnov-Grubbs test.

        :param numpy.array data: data set
        :param float alpha: significance level
        :return: the index of the outlier if one if found; None otherwise
        """
        target_index, value = self._target(data)

        g = value / data.std()
        g_test = self._get_g_test(data, alpha)
        return target_index if g > g_test else None

    def run(self, alpha=DEFAULT_ALPHA, output_type=OutputType.DATA):
        """Run the Smirnov-Grubbs test to remove outliers in the given data set.

        :param float alpha: significance level
        :param int output_type: test output type (from OutputType class values)
        :return: depending on the value of output_type, the data set without
        outliers (DATA), the outliers themselves (OUTLIERS) or the indices of
        the outliers in the original data set (INDICES)
        """
        data = self._copy_data()
        outliers = list()

        while True:
            outlier_index = self._test_once(data, alpha)
            if outlier_index is None:
                break
            outlier = data[outlier_index]
            outliers.append(outlier)
            data = self._delete_item(data, outlier_index)

        return_value = data
        if output_type == OutputType.OUTLIERS:
            return_value = outliers
        elif output_type == OutputType.INDICES:
            return_value = self._get_indices(outliers)
        return return_value

    def _target(self, data):
        raise NotImplementedError

    def _get_t_significance_level(self, alpha):
        raise NotImplementedError

class TwoSidedGrubbsTest(GrubbsTestAlternative):
    def _target(self, data):
        """Compute the index of the farthest value from the sample mean and its
        distance.

        :param numpy.array data: data set
        :return int, float: the index of the element and its distance to the
        mean
        """
        relative_values = abs(data - data.mean())
        index = relative_values.argmax()
        value = relative_values[index]
        return index, value

    def _get_t_significance_level(self, alpha, n):
        return alpha/(2*n)

def _test(test_class, data, alpha, output_type):
    return test_class(data).run(alpha, output_type=output_type)

def _two_sided_test(data, alpha, output_type):
    return _test(TwoSidedGrubbsTest, data, alpha, output_type)

def two_sided_test_indices(data, alpha=DEFAULT_ALPHA):
    #alpha = 1 - alpha
    return _two_sided_test(data, alpha, OutputType.INDICES)

def two_sided_test_outliers(data, alpha=DEFAULT_ALPHA):
    return _two_sided_test(data, alpha, OutputType.OUTLIERS)