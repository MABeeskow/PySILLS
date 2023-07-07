#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# results.py
# Maximilian Beeskow
# 16.08.2021
# ----------------------
#
## MODULES
import numpy as np
import os
from modules import data
from modules.chemistry import PeriodicSystemOfElements as PSE
from modules.standard import StandardReferenceMaterials as SRM
import re
import matplotlib.colors as mplcol
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy import stats
import pandas as pd
import tkinter as tk
from tkinter import ttk, font
import tkinter.filedialog as fd
#
## CLASSES
class Sensitivities:
    #
    def __int__(self, signal, concentration, internal_std, isotopes, limits):
        self.signal = signal
        self.concentration = concentration
        self.internal_std = internal_std
        self.isotopes = isotopes
        self.limits = limits
    #
    def calculate_xi(self):
        xi = []
        for isotope in self.isotopes:
            signal_i = np.mean(self.signal[isotope][self.limits[0]:self.limits[1]])
            signal_is = np.mean(self.signal[self.internal_std][self.limits[0]:self.limits[1]])
            concentration_i = self.concentration[isotope]
            concentration_is = self.concentration[self.internal_std]
            xi.append([isotope, (signal_i)/(signal_is)*(concentration_is)/(concentration_i)])
        #
        return xi
#
class IsotopeRatios:
    #
    def __init__(self, parent, color_bg, signal, isotopes):
        # Input
        self.parent = parent
        self.color_bg = color_bg
        self.signal = signal
        self.isotopes = isotopes
        self.color_fg = "black"
        #
        padx_value = 0
        pady_value = 0
        ipadx_value = 1
        ipady_value = 1
        #
        self.ir_window = tk.Toplevel(self.parent)
        self.ir_window.geometry("900x700")
        self.ir_window.title("Isotope Ratios")
        #
        for x in range(12):
            tk.Grid.columnconfigure(self.ir_window, x, weight=1)
        for y in range(27):
            tk.Grid.rowconfigure(self.ir_window, y, weight=1)
        #
        self.ir_window.grid_columnconfigure(0, minsize=80)
        self.ir_window.grid_columnconfigure(1, minsize=65)
        self.ir_window.grid_columnconfigure(2, minsize=80)
        self.ir_window.grid_columnconfigure(3, minsize=60)
        for i in range(4, 12):
            self.ir_window.grid_columnconfigure(i, minsize=75)
        for i in range(0, 2):
            self.ir_window.grid_rowconfigure(i, minsize=35)
        self.ir_window.grid_rowconfigure(2, minsize=15)
        for i in range(3, 26):
            self.ir_window.grid_rowconfigure(i, minsize=25)
        self.ir_window.grid_rowconfigure(26, minsize=40)
        #
        # Labels
        lbl_01 = tk.Label(self.ir_window, text="Select Isotope")
        lbl_01.grid(row=0, column=0, columnspan=2, padx=padx_value, pady=pady_value,
                    ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        #
        # Options menus
        option_list = self.isotopes
        self.var_srm = tk.StringVar()
        self.var_srm.set(option_list[0])
        opt_menu = tk.OptionMenu(self.ir_window, self.var_srm, *option_list, command=self.option_changed)
        opt_menu.grid(row=1, column=0, columnspan=2, padx=padx_value, pady=pady_value,
                      ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        #
    def option_changed(self, op):
        #
        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().pack_forget()
            self.fig_histo.clf()
            self.ax_histo.cla()
            self.canvas_histo.get_tk_widget().pack_forget()
        except AttributeError:
            pass

        try:
            if self.canvas:
                self.canvas.destroy()
            if self.canvas_histo:
                self.canvas.destroy()
        except AttributeError:
            pass

        self.canvas = None
        self.canvas_histo = None
        #
        ioi = self.var_srm.get() # ioi = isotope-of-interest
        mean_ioi = np.mean(self.signal[ioi])
        n_isotopes = len(self.isotopes)
        n_left = int(n_isotopes/2)
        self.ratios = []
        variables = []
        entries = []
        for i in range(n_left): # left column
            tk.Label(self.ir_window, text=str(self.isotopes[i][0])+"/"+str(ioi)).grid(row=i+3, column=0, sticky="nesw")
            value = round(np.mean(self.signal[self.isotopes[i][0]])/mean_ioi, 4)
            self.ratios.append(value)
            variables.append(tk.StringVar())
            entries.append(tk.Entry(self.ir_window, textvariable=variables[-1]))
            entries[-1].grid(row=i+3, column=1, sticky="nesw")
            entries[-1].insert(0, value)
        for i in range(n_left, n_isotopes): # right column
            tk.Label(self.ir_window, text=str(self.isotopes[i][0])+"/"+str(ioi)).grid(row=i-8, column=2, sticky="nesw")
            value = round(np.mean(self.signal[self.isotopes[i][0]])/mean_ioi, 4)
            self.ratios.append(value)
            variables.append(tk.StringVar())
            entries.append(tk.Entry(self.ir_window, textvariable=variables[-1]))
            entries[-1].grid(row=i-8, column=3, sticky="nesw")
            entries[-1].insert(0, value)
        #
        X = self.isotopes[:, 0]
        Y = self.ratios
        #
        self.fig = Figure(figsize=(10, 5), facecolor=self.color_bg)
        self.ax = self.fig.add_subplot()
        #
        self.ax.axhline(1.0, color="tomato", linestyle="dashed")
        self.ax.bar(X, Y)
        self.ax.set_xticklabels(X, rotation=90)
        self.ax.grid(True)
        self.ax.set_yscale("log")
        self.ax.set_axisbelow(True)
        self.ax.set_ylabel("Isotope ratio (*/"+str(ioi)+")", labelpad=0.5)

        self.plotting_area = tk.Frame(self.ir_window, bg=self.color_bg)
        self.plotting_area.grid(row=0, column=4, rowspan=26, columnspan=8, sticky="nesw")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotting_area)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
        self.plotting_histo = tk.Frame(self.ir_window, bg=self.color_bg)
        self.plotting_histo.grid(row=n_left+3, column=0, rowspan=int(26-n_left), columnspan=4, sticky="nesw")
        self.fig_histo = Figure(figsize=(10, 5), facecolor=self.color_bg, tight_layout=True)
        self.ax_histo = self.fig_histo.add_subplot()
        #
        self.ax_histo.hist(Y, bins=75)
        self.ax_histo.grid(True)
        self.ax_histo.set_axisbelow(True)
        self.ax_histo.set_xlabel("Isotope ratio (*/"+str(ioi)+")", labelpad=0.5)
        self.ax_histo.set_ylabel("Frequency", labelpad=0.5)

        self.canvas_histo = FigureCanvasTkAgg(self.fig_histo, master=self.plotting_histo)
        self.canvas_histo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
class SimpleSignals:
    #
    def __init__(self, parent, color_bg, signal, isotopes, times, times_def, times_def_bg, files_std, files_smpl, file_actual):
        self.parent = parent
        self.color_bg = color_bg
        self.color_fg = "black"
        self.signal = signal
        self.isotopes = isotopes
        self.times = times
        self.times_def = times_def
        self.times_def_bg = times_def_bg
        self.files_std = files_std
        self.files_smpl = files_smpl
        self.file_actual = file_actual
        #
        self.n_isotopes = len(self.isotopes[:, 0])
        #
        self.index_start_sig = 0
        self.index_end_sig = len(self.times)-1
        self.indices_sig = [self.index_start_sig, self.index_end_sig]
        self.index_start_bg = 0
        self.index_end_bg = len(self.times)-1
        self.indices_bg = [self.index_start_bg, self.index_end_bg]
        #
    #
    def calculate_sensitivities(self):
        self.xi_window = tk.Toplevel(self.parent)
        self.xi_window.geometry("900x800")
        self.xi_window.title("Sensitivities")
        #
        self.xi_values = []
        #
        self.pse_list = PSE().get_element_names()
        #
        for x in range(12):
            tk.Grid.columnconfigure(self.xi_window, x, weight=1)
        for y in range(26):
            tk.Grid.rowconfigure(self.xi_window, y, weight=1)
        #
        self.xi_window.grid_columnconfigure(0, minsize=90)
        self.xi_window.grid_columnconfigure(1, minsize=80)
        self.xi_window.grid_columnconfigure(2, minsize=90)
        self.xi_window.grid_columnconfigure(3, minsize=80)
        for i in range(4, 12):
            self.xi_window.grid_columnconfigure(i, minsize=70)
        for i in range(0, 4):
            self.xi_window.grid_rowconfigure(i, minsize=35)
        for i in range(4, 26):
            self.xi_window.grid_rowconfigure(i, minsize=30)
        #
        # Labels
        lbl_01 = tk.Label(self.xi_window, text="Internal Standard")
        lbl_01.grid(row=0, column=0, columnspan=2, sticky="nesw")
        lbl_02 = tk.Label(self.xi_window, text="Time Interval")
        lbl_02.grid(row=0, column=2, columnspan=2, sticky="nesw")
        lbl_03 = tk.Label(self.xi_window, text="Start")
        lbl_03.grid(row=1, column=2, sticky="nesw")
        lbl_04 = tk.Label(self.xi_window, text="End")
        lbl_04.grid(row=2, column=2, sticky="nesw")
        #
        self.srm_values = []
        option_list_srm = np.array([["NIST 606"], ["NIST 610"], ["NIST 610 (GeoReM)"], ["NIST 610 (Spandler)"],
                                     ["NIST 611"], ["NIST 611 (GeoReM)"], ["NIST 612"], ["NIST 612 (GeoReM)"],
                                     ["NIST 613"], ["NIST 613 (GeoReM)"], ["NIST 614"], ["NIST 614 (GeoReM)"],
                                     ["NIST 615"], ["NIST 615 (GeoReM)"], ["NIST 616"], ["NIST 616 (GeoReM)"],
                                     ["NIST 617"], ["NIST 617 (GeoReM)"], ["USGS BCR-2G (GeoReM)"],
                                     ["USGS GSD-1G (GeoReM)"], ["USGS GSE-1G (GeoReM)"]])[:, 0]
        self.var_srm = tk.StringVar()
        self.var_srm.set("Select SRM")
        opt_menu_srm = tk.OptionMenu(self.xi_window, self.var_srm, *option_list_srm, command=self.option_changed_srm)
        opt_menu_srm.grid(row=2, column=0, columnspan=2, sticky="nesw")
        #
        # Options menus (Integration window)
        option_list_iw = []
        if len(self.times_def) == 0:
            option_list_iw.append(["No Time Intervals"])
        else:
            for i in range(len(self.times_def)):
                option_list_iw.append([str(self.times_def[i][0])+" - "+str(self.times_def[i][1])])
        option_list_iw = np.array(option_list_iw)[:, 0]
        self.var_iw = tk.StringVar()
        self.var_iw.set("Select Time Interval")
        opt_menu_iw = tk.OptionMenu(self.xi_window, self.var_iw, *option_list_iw,
                                    command=lambda op, parent_plot=self.xi_window:
                                    self.selected_integration_window(parent_plot, op))
        opt_menu_iw.grid(row=3, column=2, columnspan=2, sticky="nesw")
        #
        # Treeviews
        self.xi_treeview = self.make_treeview_xi(parent=self.xi_window)
        self.srm_treeview = self.make_treeview_srm(parent=self.xi_window)
        #
        # Entries Time Interval
        self.index_start = 0
        self.index_end = len(self.times)-1
        self.indices_sig = [self.index_start, self.index_end]

        self.t_start = tk.StringVar()
        self.t_start.set(self.times.iloc[0])
        self.entr_t_start = tk.Entry(self.xi_window, textvariable=self.t_start)
        self.entr_t_start.grid(row=1, column=3, sticky="nesw")
        self.entr_t_start.bind("<Return>", lambda event, entr=self.entr_t_start, var=self.t_start, t_id=self.indices_sig[0],
                                                  pos="start", parent_treeview=self.xi_treeview,
                                                  parent_plot=self.xi_window, key_plot=True: self.find_nearest_time(entr, var, t_id,
                                                                                                     pos, parent_treeview,
                                                                                                     parent_plot, key_plot, event))
        self.t_end = tk.StringVar()
        self.t_end.set(self.times.iloc[-1])
        self.entr_t_end = tk.Entry(self.xi_window, textvariable=self.t_end)
        self.entr_t_end.grid(row=2, column=3, sticky="nesw")
        self.entr_t_end.bind("<Return>", lambda event, entr=self.entr_t_end, var=self.t_end, t_id=self.indices_sig[1],
                                                pos="end", parent_treeview=self.xi_treeview,
                                                parent_plot=self.xi_window, key_plot=True: self.find_nearest_time(entr, var, t_id,
                                                                                                     pos, parent_treeview,
                                                                                                     parent_plot, key_plot, event))
        #
        # Options menus (SRM)
        option_list = self.isotopes[:, 0]
        self.var_is = tk.StringVar()
        self.var_is.set("Select Isotope")
        opt_menu = tk.OptionMenu(self.xi_window, self.var_is, *option_list,
                                 command=lambda op, parent_treeview=self.xi_treeview, parent_plot=self.xi_window:
                                 self.option_changed(parent_treeview, parent_plot, op))
        opt_menu.grid(row=1, column=0, columnspan=2, sticky="nesw")
        #
        # Buttons
        btn_01 = tk.Button(self.xi_window, text="Load SRM", fg=self.color_fg, bg=self.color_bg,
                           command=lambda parent=self.xi_window: self.load_srm_from_csv(parent))
        btn_01.grid(row=3, column=0, columnspan=2, sticky="nesw")
    #
    def make_treeview_xi(self, parent):
        # General Settings
        ttk.Style().configure("Treeview", background=self.color_bg, foreground="black",
                              fieldbackground=self.color_bg)
        my_font = font.Font(size="11", weight="normal")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=my_font, background="gray", pressed_color="gray",
                        highlight_color="gray", foreground=self.color_fg)
        style.map("Treeview.Heading", background = [("pressed", "!focus", "gray"),
                                                    ("active", "gray"), ("disabled", self.color_bg)])
        #
        columns = ("#1", "#2", "#3")
        treeview = ttk.Treeview(parent, columns=columns, show="headings")
        treeview.heading("#1", text="Isotope")
        treeview.column("#1", minwidth=0, width=90, stretch=tk.NO)
        treeview.heading("#2", text="Sensitivity")
        treeview.column("#2", minwidth=0, width=85, stretch=tk.NO)
        treeview.heading("#3", text="Error")
        treeview.column("#3", minwidth=0, width=85, stretch=tk.NO)
        treeview.grid(row=5, column=0, rowspan=10, columnspan=3, sticky="nesw")
        #
        return treeview
    #
    def make_treeview_srm(self, parent, row_id=16, column_id=0, n_rows=10, n_columns=3):
        # General Settings
        ttk.Style().configure("Treeview", background=self.color_bg, foreground="black",
                              fieldbackground=self.color_bg)
        my_font = font.Font(size="11", weight="normal")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=my_font, background="gray", pressed_color="gray",
                        highlight_color="gray", foreground=self.color_fg)
        style.map("Treeview.Heading", background = [("pressed", "!focus", "gray"),
                                                    ("active", "gray"), ("disabled", self.color_bg)])
        #
        columns = ("#1", "#2")
        treeview = ttk.Treeview(parent, columns=columns, show="headings")
        treeview.heading("#1", text="Element")
        treeview.column("#1", minwidth=0, width=90, stretch=tk.NO)
        treeview.heading("#2", text="Concentration")
        treeview.column("#2", minwidth=0, width=170, stretch=tk.NO)
        treeview.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        #
        return treeview
    #
    def selected_integration_window(self, parent_plot, op, mode_xi=True, key_plot=True, mode="SIG"):
        #
        if mode_xi == True:
            for i in self.xi_treeview.get_children():
                self.xi_treeview.delete(i)
            #
            if self.var_iw.get() != "No Time Intervals":
                key = re.search("(\d+\.\d+)"+" - "+"(\d+\.\d+)", self.var_iw.get())
                t_start = float(key.group(1))
                t_end = float(key.group(2))
                #
                t_id_start = self.times[self.times == t_start].index[0]
                t_id_end = self.times[self.times == t_end].index[0]
                self.indices_sig[0] = t_id_start
                self.indices_sig[1] = t_id_end
                self.entr_t_start.delete(0, tk.END)
                self.entr_t_start.insert(0, t_start)
                self.entr_t_end.delete(0, tk.END)
                self.entr_t_end.insert(0, t_end)
                #
                xi_results = self.calculate_xi(id_start=self.indices_sig[0], id_end=self.indices_sig[1])
                for isotopes, xi_mean, xi_std in xi_results:
                    self.xi_treeview.insert("", tk.END, values=[isotopes, round(xi_mean, 4), round(xi_std, 4)])
                #
                if key_plot == True:
                    X = self.isotopes[:, 0]
                    xi_results = np.array(xi_results, dtype=object)
                    Y = np.array(xi_results)[:, 1]
                    #
                    self.make_bar_plot(X=X, Y=Y, parent=parent_plot)
                    self.make_histo_plot(X=X, Y=Y, parent=parent_plot)
            else:
                pass
        else:
            #
            if mode == "SIG":
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
                    for i in range(self.n_isotopes):
                        self.calculate_xi_2(var_file=self.var_file_std_default.get(), var_i=self.isotopes[:, 0][i],
                                            var_is=self.var_is_default.get(), index=i)
                        self.calculate_ci(var_file_std=self.var_file_std_default.get(),
                                          var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                                          var_i=self.isotopes[:, 0][i], index=i)
                        self.calculate_rsf(var_file_std=self.var_file_std_default.get(),
                                           var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                                           var_i=self.isotopes[:, 0][i], index=i)
                        self.calculate_lod(var_file_std=self.var_file_std_default.get(), var_file_smpl=self.var_file_smpl_default.get(),
                               var_is=self.var_is_default.get(), var_i=self.isotopes[:, 0][i], index=i)
                else:
                    pass
            else:
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
                    for i in range(self.n_isotopes):
                        self.calculate_xi_2(var_file=self.var_file_std_default.get(), var_i=self.isotopes[:, 0][i],
                                            var_is=self.var_is_default.get(), index=i)
                        self.calculate_ci(var_file_std=self.var_file_std_default.get(),
                                          var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                                          var_i=self.isotopes[:, 0][i], index=i)
                        self.calculate_rsf(var_file_std=self.var_file_std_default.get(),
                                           var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                                           var_i=self.isotopes[:, 0][i], index=i)
                        self.calculate_lod(var_file_std=self.var_file_std_default.get(), var_file_smpl=self.var_file_smpl_default.get(),
                               var_is=self.var_is_default.get(), var_i=self.isotopes[:, 0][i], index=i)
                else:
                    pass
    #
    def find_nearest_time(self, entr, var, t_id, pos, parent_treeview, parent_plot, key_plot, event, t_iw=None):
        #
        if t_iw == None:
            t_nearest = min(self.times, key=lambda x: abs(x - float(var.get())))
            entr.delete(0, tk.END)
            entr.insert(0, t_nearest)
            t_id = self.times[self.times == t_nearest].index[0]
            #
            for i in parent_treeview.get_children():
                parent_treeview.delete(i)
            #
            if pos == "start":
                self.indices_sig[0] = t_id
            else:
                self.indices_sig[1] = t_id
        else:
            t_id_start = self.times[self.times == t_iw[0]].index[0]
            t_id_end = self.times[self.times == t_iw[1]].index[0]
            self.indices_sig[0] = t_id_start
            self.indices_sig[1] = t_id_end
            self.entr_t_start.delete(0, tk.END)
            entr.insert(0, t_iw[0])
            self.entr_t_end.delete(0, tk.END)
            entr.insert(0, t_iw[1])
        #
        xi_results = self.calculate_xi(id_start=self.indices_sig[0], id_end=self.indices_sig[1])
        for isotopes, xi_mean, xi_std in xi_results:
            parent_treeview.insert("", tk.END, values=[isotopes, round(xi_mean, 4), round(xi_std, 4)])
        #
        if key_plot == True:
            X = self.isotopes[:, 0]
            xi_results = np.array(xi_results, dtype=object)
            Y = np.array(xi_results)[:, 1]
            #
            self.make_bar_plot(X=X, Y=Y, parent=parent_plot)
            self.make_histo_plot(X=X, Y=Y, parent=parent_plot)
    #
    def calculate_xi(self, id_start, id_end, var=False):
        isotopes = self.isotopes[:, 0]
        if var == False:
            internal_standard = self.var_is.get()
        else:
            internal_standard = var.get()
        key_is = re.search("(\D+)(\d+)", internal_standard)
        index_is = self.pse_list.index(key_is.group(1))
        #
        xi_helper = []
        xi_results = []
        for isotope in isotopes:
            xi_helper.clear()
            key = re.search("(\D+)(\d+)", isotope)
            index_i = self.pse_list.index(key.group(1))
            for i in range(id_start, id_end+1):
                if self.signal[isotope][i] > 0 and self.signal[internal_standard][i] > 0 and self.srm_values[index_i] > 0:
                    signal_i = self.signal[isotope][i]
                    signal_is = self.signal[internal_standard][i]
                    conc_ratio = self.srm_values[index_is]/self.srm_values[index_i]
                    xi = signal_i/signal_is * conc_ratio
                    xi_helper.append(xi)
                elif self.srm_values[index_i] == 0:
                    xi_helper.append(0.0)
            xi_results.append([isotope, np.mean(xi_helper), np.std(xi_helper, ddof=1)])
        #
        return xi_results
    #
    def option_changed(self, parent_treeview, parent_plot, op, category="sensitivity", key_plot=True):
        xi_results = self.calculate_xi(id_start=self.indices_sig[0], id_end=self.indices_sig[1])
        #
        for i in parent_treeview.get_children():
            parent_treeview.delete(i)
        #
        i = 0
        for isotopes, xi_mean, xi_std in xi_results:
            if category == "sensitivity":
                parent_treeview.insert("", tk.END, values=[isotopes, round(xi_mean, 4), round(xi_std, 4)])
            else:
                #parent_treeview.insert("", tk.END, values=[isotopes, 0.0, 0.0, round(xi_mean, 4), round(xi_std, 4)])
                self.entries_xi_mu[i][2].delete(0, tk.END)
                self.entries_xi_mu[i][2].insert(0, round(xi_mean, 4))
                self.entries_xi_std[i][2].delete(0, tk.END)
                self.entries_xi_std[i][2].insert(0, round(xi_std, 4))
                #
                i += 1
        #
        if key_plot == True:
            X = self.isotopes[:, 0]
            xi_results = np.array(xi_results, dtype=object)
            Y = np.array(xi_results)[:, 1]
            #
            self.make_bar_plot(X=X, Y=Y, parent=parent_plot)
            self.make_histo_plot(X=X, Y=Y, parent=parent_plot)
    #
    def option_changed_srm(self, op):
        #
        for i in self.srm_treeview.get_children():
            self.srm_treeview.delete(i)
        if len(self.srm_values) > 0:
            self.srm_values.clear()
        #
        path = os.getcwd()
        parent = os.path.dirname(path)
        if self.var_srm.get() == "NIST 606":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_606.csv"))
        elif self.var_srm.get() == "NIST 610":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610.csv"))
        elif self.var_srm.get() == "NIST 610 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 610 (Spandler)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_Spandler.csv"))
        elif self.var_srm.get() == "NIST 611":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611.csv"))
        elif self.var_srm.get() == "NIST 611 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 612":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612.csv"))
        elif self.var_srm.get() == "NIST 612 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 613":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613.csv"))
        elif self.var_srm.get() == "NIST 613 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 614":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614.csv"))
        elif self.var_srm.get() == "NIST 614 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 615":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615.csv"))
        elif self.var_srm.get() == "NIST 615 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 616":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616.csv"))
        elif self.var_srm.get() == "NIST 616 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616_GeoReM.csv"))
        elif self.var_srm.get() == "NIST 617":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617.csv"))
        elif self.var_srm.get() == "NIST 617 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617_GeoReM.csv"))
        elif self.var_srm.get() == "USGS BCR-2G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_BCR2G_GeoReM.csv"))
        elif self.var_srm.get() == "USGS GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSD1G_GeoReM.csv"))
        elif self.var_srm.get() == "USGS GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSE1G_GeoReM.csv"))

        self.isotopes_measured = np.array(data_srm)[:, 0]
        for element in self.pse_list:
            if element in self.isotopes_measured:
                for name, conc in data_srm:
                    if name == element:
                        self.srm_treeview.insert("", tk.END, values=[element, conc])
                        self.srm_values.append(float(conc))
            else:
                self.srm_treeview.insert("", tk.END, values=[element, 0.0])
                self.srm_values.append(0.0)
    #
    def load_srm_from_csv(self, parent):
        #
        for i in self.srm_treeview.get_children():
            self.srm_treeview.delete(i)
        if len(self.srm_values) > 0:
            self.srm_values.clear()
        #
        filename = fd.askopenfilenames(parent=parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        data_srm = data.general().importSRM(filename=filename[0])
        #
        self.isotopes_measured = np.array(data_srm)[:, 0]
        for element in self.pse_list:
            if element in self.isotopes_measured:
                for name, conc in data_srm:
                    if name == element:
                        self.srm_treeview.insert("", tk.END, values=[element, conc])
                        self.srm_values.append(float(conc))
            else:
                self.srm_treeview.insert("", tk.END, values=[element, 0.0])
                self.srm_values.append(0.0)
    #
    def load_conc_from_csv(self, parent, parent_tv, values_list):
        #
        for i in parent_tv.get_children():
            parent_tv.delete(i)
        if len(values_list) > 0:
            values_list.clear()
        #
        filename = fd.askopenfilenames(parent=parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        data_conc = data.general().importSRM(filename=filename[0])
        #
        self.isotopes_measured = np.array(data_conc)[:, 0]
        for element in self.pse_list:
            if element in self.isotopes_measured:
                for name, conc in data_conc:
                    if name == element:
                        parent_tv.insert("", tk.END, values=[element, conc])
                        values_list.append(float(conc))
            else:
                parent_tv.insert("", tk.END, values=[element, 0.0])
                values_list.append(0.0)
    #
    def make_bar_plot(self, X, Y, parent):
        #
        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass

        try:
            if self.canvas:
                self.canvas.destroy()
        except AttributeError:
            pass
        #
        self.canvas = None
        self.fig = Figure(figsize=(10, 5), facecolor=self.color_bg)
        self.ax = self.fig.add_subplot()
        #
        self.ax.axhline(1.0, color="tomato", linestyle="dashed")
        self.ax.bar(X, Y)
        self.ax.set_xticklabels(X, rotation=90)
        self.ax.grid(True)
        self.ax.set_yscale("log")
        self.ax.set_axisbelow(True)
        self.ax.set_ylabel("Sensitivity $\\xi$", labelpad=0.5)

        self.plotting_area = tk.Frame(parent, bg=self.color_bg)
        self.plotting_area.grid(row=0, column=4, rowspan=14, columnspan=8, sticky="nesw")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotting_area)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #
    def make_histo_plot(self, X, Y, parent):
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
        self.fig_histo = Figure(figsize=(10, 5), facecolor=self.color_bg)
        self.ax_histo = self.fig_histo.add_subplot()
        #
        self.ax_histo.axhline(1.0, color="tomato", linestyle="dashed")
        self.ax_histo.hist(Y, bins=50)
        self.ax_histo.grid(True)
        self.ax_histo.set_yscale("log")
        self.ax_histo.set_axisbelow(True)
        self.ax_histo.set_ylabel("Sensitivity $\\xi$", labelpad=0.5)

        self.plotting_area_histo = tk.Frame(parent, bg=self.color_bg)
        self.plotting_area_histo.grid(row=14, column=4, rowspan=12, columnspan=8, sticky="nesw")
        self.canvas_histo = FigureCanvasTkAgg(self.fig_histo, master=self.plotting_area_histo)
        self.canvas_histo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #
    def calculate_concentrations(self):
        # GEOMETRY
        width = int(4*85 + 15 + 9*90 + 140 + 2*150 + 15)
        height = int(2*20 + (self.n_isotopes+3)*30 + 15)
        self.ci_window = tk.Toplevel(self.parent)
        self.ci_window.geometry(str(width)+"x"+str(height))
        self.ci_window.title("Sample Concentrations")
        #
        self.ci_values = []
        #
        self.pse_list = PSE().get_element_names()
        #
        for y in range(int(2 + self.n_isotopes + 4)):
            tk.Grid.rowconfigure(self.ci_window, y, weight=1)
        for x in range(18):
            tk.Grid.columnconfigure(self.ci_window, x, weight=1)
        #
        # Rows
        for i in range(0, 2):
            self.ci_window.grid_rowconfigure(i, minsize=20)
        for i in range(2, int(2+self.n_isotopes+4)):
            self.ci_window.grid_rowconfigure(i, minsize=30)
        self.ci_window.grid_rowconfigure(int(2+self.n_isotopes+4), minsize=15)
        # Columns
        for i in range(0, 4):
            self.ci_window.grid_columnconfigure(i, minsize=85)
        self.ci_window.grid_columnconfigure(4, minsize=15)
        for i in range(5, 14):
            self.ci_window.grid_columnconfigure(i, minsize=90)
        self.ci_window.grid_columnconfigure(14, minsize=140)
        self.ci_window.grid_columnconfigure(15, minsize=150)
        self.ci_window.grid_columnconfigure(16, minsize=150)
        self.ci_window.grid_columnconfigure(17, minsize=15)
        #
        # VARIABLES
        self.conc_smpl_is = []
        self.var_is_default = tk.StringVar()
        self.var_file_std_default = tk.StringVar()
        self.var_file_smpl_default = tk.StringVar()
        self.make_variable_file_std()
        self.make_variable_file_smpl()

        isotope_names = self.isotopes[:, 0]
        self.results_concentration = [[item] for item in isotope_names]
        #
        # Labels
        lbl_03 = tk.Label(self.ci_window, text="Isotope")
        lbl_03.grid(row=0, column=5, rowspan=2, sticky="nesw")
        lbl_04_a = tk.Label(self.ci_window, text="Concentration")
        lbl_04_a.grid(row=0, column=6, columnspan=2, sticky="nesw")
        lbl_04_b = tk.Label(self.ci_window, text="\u03BC")  # Concentration Mean
        lbl_04_b.grid(row=1, column=6, sticky="nesw")
        lbl_04_c = tk.Label(self.ci_window, text="\u03C3")  # Concentration Standard Deviation
        lbl_04_c.grid(row=1, column=7, sticky="nesw")
        lbl_05_a = tk.Label(self.ci_window, text="Sensitivity")
        lbl_05_a.grid(row=0, column=8, columnspan=2, sticky="nesw")
        lbl_05_b = tk.Label(self.ci_window, text="\u03BC")  # Sensitivity Mean
        lbl_05_b.grid(row=1, column=8, sticky="nesw")
        lbl_05_c = tk.Label(self.ci_window, text="\u03C3")  # Sensitivity Standard Deviation
        lbl_05_c.grid(row=1, column=9, sticky="nesw")
        lbl_06 = tk.Label(self.ci_window, text="Standard Reference Material")
        lbl_06.grid(row=11, column=0, columnspan=3, sticky="nesw")
        lbl_07 = tk.Label(self.ci_window, text="Sample Concentration IS")
        lbl_07.grid(row=19, column=0, columnspan=3, sticky="nesw")
        lbl_08_a = tk.Label(self.ci_window, text="Internal")
        lbl_08_a.grid(row=0, column=14, sticky="nesw")
        lbl_08_b = tk.Label(self.ci_window, text="Standard")
        lbl_08_b.grid(row=1, column=14, sticky="nesw")
        lbl_09_a = tk.Label(self.ci_window, text="Input file")
        lbl_09_a.grid(row=0, column=15, columnspan=2, sticky="nesw")
        lbl_09_b = tk.Label(self.ci_window, text="Standard")
        lbl_09_b.grid(row=1, column=15, sticky="nesw")
        lbl_09_c = tk.Label(self.ci_window, text="Sample")
        lbl_09_c.grid(row=1, column=16, sticky="nesw")

        lbl_10 = tk.Label(self.ci_window, text="General Settings")
        lbl_10.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="nesw")
        lbl_bg = tk.Label(self.ci_window, text="Integration Window (BG)")
        lbl_bg.grid(row=2, column=2, columnspan=2, sticky="nesw")
        lbl_sig = tk.Label(self.ci_window, text="Integration Window (SIG)")
        lbl_sig.grid(row=6, column=2, columnspan=2, sticky="nesw")
        lbl_11_a = tk.Label(self.ci_window, text="Relative Sensitivity Factor")
        lbl_11_a.grid(row=0, column=10, columnspan=2, sticky="nesw")
        lbl_11_b = tk.Label(self.ci_window, text="\u03BC")  # RSF Mean
        lbl_11_b.grid(row=1, column=10, sticky="nesw")
        lbl_11_c = tk.Label(self.ci_window, text="\u03C3")  # RSF Standard Deviation
        lbl_11_c.grid(row=1, column=11, sticky="nesw")
        lbl_12_a = tk.Label(self.ci_window, text="Limit of Detection")
        lbl_12_a.grid(row=0, column=12, columnspan=2, sticky="nesw")
        lbl_12_b = tk.Label(self.ci_window, text="\u03BC")  # RSF Mean
        lbl_12_b.grid(row=1, column=12, sticky="nesw")
        lbl_12_c = tk.Label(self.ci_window, text="\u03C3")  # RSF Standard Deviation
        lbl_12_c.grid(row=1, column=13, sticky="nesw")
        #
        # Treeviews
        self.srm_treeview = self.make_treeview_srm(parent=self.ci_window, row_id=12, n_rows=7)
        self.conc_is_treeview = self.make_treeview_srm(parent=self.ci_window, row_id=20, n_rows=7)
        #
        # Options menus
        self.make_option_srm(parent=self.ci_window, row_id=2, column_id=0, n_columns=2) # Select SRM data
        self.make_option_is(parent=self.ci_window, row_id=int(2+self.n_isotopes), column_id=14)  # Select default internal standard
        self.make_option_file_std(parent=self.ci_window, row_id=int(2+self.n_isotopes), column_id=15)   # Select default standard file
        self.make_option_file_smpl(parent=self.ci_window, row_id=int(2+self.n_isotopes), column_id=16)   # Select default sample file
        self.make_option_iw_bg(parent=self.ci_window, row_id=3, column_id=2, n_columns=2)  # Select time integration window (background)
        self.make_option_iw(parent=self.ci_window, row_id=7, column_id=2, n_columns=2)  # Select time integration window
        #
        # Buttons
        self.make_button_srm(parent=self.ci_window, row_id=3, column_id=0, n_columns=2)
        self.make_button_smpl_conc(parent=self.ci_window, row_id=4, column_id=0, n_columns=2)
        self.make_button_advstat(parent=self.ci_window, row_id=5, column_id=0, n_columns=2)
        self.make_button_export(parent=self.ci_window, row_id=6, column_id=0, n_rows=2, n_columns=2)
        #
        # Entries Time Interval
        self.make_time_window_bg_entries(parent=self.ci_window, row_id=4, column_id=2)
        self.make_time_window_sig_entries(parent=self.ci_window, row_id=8, column_id=2)
        #
        self.var_file_indiv = []
        self.make_isotope_column(parent=self.ci_window, row_id=2, column_id=5)
        self.make_concentration_entries(parent=self.ci_window, row_id=2, column_id=6)
        self.make_sensitivity_entries(parent=self.ci_window, row_id=2, column_id=8)
        self.make_rsf_entries(parent=self.ci_window, row_id=2, column_id=10)
        self.make_lod_entries(parent=self.ci_window, row_id=2, column_id=12)
        self.make_option_is_column(parent=self.ci_window, row_id=2, column_id=14)
        self.make_option_file_column_std(parent=self.ci_window, row_id=2, column_id=15)
        self.make_option_file_column_smpl(parent=self.ci_window, row_id=2, column_id=16)
    #
    def make_option_srm(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        #
        self.srm_values = []
        option_list_srm = np.array([["NIST 606"], ["NIST 610"], ["NIST 610 (GeoReM)"], ["NIST 610 (Spandler)"],
                                     ["NIST 611"], ["NIST 611 (GeoReM)"], ["NIST 612"], ["NIST 612 (GeoReM)"],
                                     ["NIST 613"], ["NIST 613 (GeoReM)"], ["NIST 614"], ["NIST 614 (GeoReM)"],
                                     ["NIST 615"], ["NIST 615 (GeoReM)"], ["NIST 616"], ["NIST 616 (GeoReM)"],
                                     ["NIST 617"], ["NIST 617 (GeoReM)"], ["USGS BCR-2G (GeoReM)"],
                                     ["USGS GSD-1G (GeoReM)"], ["USGS GSE-1G (GeoReM)"]])[:, 0]
        self.var_srm = tk.StringVar()
        self.var_srm.set("Select SRM")
        opt_menu_srm = tk.OptionMenu(parent, self.var_srm, *option_list_srm, command=self.option_changed_srm)
        opt_menu_srm.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_option_is(self, parent, row_id, column_id, n_rows=1, n_columns=1, default_is=True, var_is=None):
        option_list_is = self.isotopes[:, 0]
        self.var_is = tk.StringVar()
        if default_is == True:
            self.var_is_default.set("Select Isotope")
            opt_menu_is = tk.OptionMenu(parent, self.var_is_default, *option_list_is, command=lambda op, var=self.var_is_default, is_default=True: self.option_changed_conc(var, is_default, op))
            opt_menu_is.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        else:
            var_is.set("Select Isotope")
            opt_menu_is = tk.OptionMenu(parent, var_is, *option_list_is, command=lambda op, var=var_is: self.option_changed_conc(var, op))
            self.entr_is_indiv.append(opt_menu_is)
            opt_menu_is.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_option_iw(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        option_list_iw = []
        if len(self.times_def) == 0:
            option_list_iw.append(["No Time Intervals"])
        else:
            for i in range(len(self.times_def)):
                option_list_iw.append([str(self.times_def[i][0])+" - "+str(self.times_def[i][1])])
        option_list_iw = np.array(option_list_iw)[:, 0]
        self.var_iw_sig = tk.StringVar()
        self.var_iw_sig.set("Select Time Interval")
        opt_menu_iw = tk.OptionMenu(parent, self.var_iw_sig, *option_list_iw,
                                    command=lambda op, parent_plot=parent, key_plot=False, mode_xi=False:
                                    self.selected_integration_window(parent_plot, key_plot, mode_xi, op))
        opt_menu_iw.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_option_iw_bg(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        option_list_iw_bg = []
        if len(self.times_def_bg) == 0:
            option_list_iw_bg.append(["No Time Intervals"])
        else:
            for i in range(len(self.times_def_bg)):
                option_list_iw_bg.append([str(self.times_def_bg[i][0])+" - "+str(self.times_def_bg[i][1])])
        option_list_iw_bg = np.array(option_list_iw_bg)[:, 0]
        self.var_iw_bg = tk.StringVar()
        self.var_iw_bg.set("Select Time Interval")
        opt_menu_iw_bg = tk.OptionMenu(parent, self.var_iw_bg, *option_list_iw_bg,
                                    command=lambda op, parent_plot=parent, key_plot=False, mode_xi=False, mode="BG":
                                    self.selected_integration_window(parent_plot, key_plot, mode_xi, mode, op))
        opt_menu_iw_bg.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_button_srm(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        btn_srm = tk.Button(parent, text="Load SRM", fg=self.color_fg, bg=self.color_bg,
                           command=lambda parent=self.ci_window: self.load_srm_from_csv(parent))
        btn_srm.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_button_advstat(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        btn = tk.Button(parent, text="Advanced Statistics", fg=self.color_fg, bg=self.color_bg)
        btn.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_button_export(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        btn = tk.Button(parent, text="Export Results", fg=self.color_fg, bg=self.color_bg, command=self.export_results_as_csv)
        btn.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_button_smpl_conc(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        btn_smpl_conc = tk.Button(parent, text="Load IS Concentration", fg=self.color_fg, bg=self.color_bg,
                           command=lambda parent=self.ci_window, parent_tv=self.conc_is_treeview,
                                          values_list=self.conc_smpl_is: self.load_conc_from_csv(parent, parent_tv,
                                                                                                 values_list))
        btn_smpl_conc.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_time_window_sig_entries(self, parent, row_id, column_id):
        #
        lbl_01 = tk.Label(parent, text="Time Start")
        lbl_01.grid(row=row_id, column=column_id, sticky="nesw")
        lbl_02 = tk.Label(parent, text="Time End")
        lbl_02.grid(row=row_id+1, column=column_id, sticky="nesw")
        #
        self.t_start_sig = tk.StringVar()
        self.t_start_sig.set(self.times.iloc[0])
        self.entr_t_start_sig = tk.Entry(parent, textvariable=self.t_start_sig)
        self.entr_t_start_sig.grid(row=row_id, column=column_id+1, sticky="nesw")
        self.entr_t_start_sig.bind("<Return>", lambda event, entr=self.entr_t_start_sig, var=self.t_start_sig,
                                                 pos="start": self.find_nearest_time_conc(entr, var, pos, event))
        self.t_end_sig = tk.StringVar()
        self.t_end_sig.set(self.times.iloc[-1])
        self.entr_t_end_sig = tk.Entry(parent, textvariable=self.t_end_sig)
        self.entr_t_end_sig.grid(row=row_id+1, column=column_id+1, sticky="nesw")
        self.entr_t_end_sig.bind("<Return>", lambda event, entr=self.entr_t_end_sig, var=self.t_end_sig,
                                                pos="end": self.find_nearest_time_conc(entr, var, pos, event))
    #
    def make_time_window_bg_entries(self, parent, row_id, column_id):
        #
        lbl_01 = tk.Label(parent, text="Time Start")
        lbl_01.grid(row=row_id, column=column_id, sticky="nesw")
        lbl_02 = tk.Label(parent, text="Time End")
        lbl_02.grid(row=row_id+1, column=column_id, sticky="nesw")
        #
        self.t_start_bg = tk.StringVar()
        self.t_start_bg.set(self.times.iloc[0])
        self.entr_t_start_bg = tk.Entry(parent, textvariable=self.t_start_bg)
        self.entr_t_start_bg.grid(row=row_id, column=column_id+1, sticky="nesw")
        self.entr_t_start_bg.bind("<Return>", lambda event, entr=self.entr_t_start_bg, var=self.t_start_bg,
                                                  pos="start", mode="BG": self.find_nearest_time_conc(entr, var, pos, mode, event))
        self.t_end_bg = tk.StringVar()
        self.t_end_bg.set(self.times.iloc[-1])
        self.entr_t_end_bg = tk.Entry(parent, textvariable=self.t_end_bg)
        self.entr_t_end_bg.grid(row=row_id+1, column=column_id+1, sticky="nesw")
        self.entr_t_end_bg.bind("<Return>", lambda event, entr=self.entr_t_end_bg, var=self.t_end_bg,
                                                pos="end", mode="BG": self.find_nearest_time_conc(entr, var, pos, mode, event))
    #
    def make_treeview_conc(self, parent, row_id=0, column_id=5, n_rows=20, n_columns=5):
        # General Settings
        ttk.Style().configure("Treeview", background=self.color_bg, foreground="black",
                              fieldbackground=self.color_bg)
        my_font = font.Font(size="11", weight="normal")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=my_font, background="gray", pressed_color="gray",
                        highlight_color="gray", foreground=self.color_fg)
        style.map("Treeview.Heading", background = [("pressed", "!focus", "gray"),
                                                    ("active", "gray"), ("disabled", self.color_bg)])
        #
        columns = ("#1", "#2", "#3", "#4", "#5")
        treeview = ttk.Treeview(parent, columns=columns, show="headings")
        treeview.heading("#1", text="Isotope")
        treeview.column("#1", minwidth=0, width=70, stretch=tk.NO)
        treeview.heading("#2", text="Concentration")
        treeview.column("#2", minwidth=0, width=130, stretch=tk.NO)
        treeview.heading("#3", text="Error")
        treeview.column("#3", minwidth=0, width=80, stretch=tk.NO)
        treeview.heading("#4", text="Sensitivity")
        treeview.column("#4", minwidth=0, width=90, stretch=tk.NO)
        treeview.heading("#5", text="Error")
        treeview.column("#5", minwidth=0, width=80, stretch=tk.NO)
        treeview.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
        #
        return treeview
    #
    def option_changed_conc(self, var, op, is_default=False):
        if is_default == True:
            for i in range(self.n_isotopes):
                self.var_is_indiv[i].set(var.get())
        else:
            for i in range(self.n_isotopes):
                self.var_is_indiv[i].set(var.get())
        #
        for i in range(self.n_isotopes):
            self.calculate_xi_2(var_file=self.var_file_std_default.get(), var_i=self.isotopes[:, 0][i],
                                var_is=self.var_is_default.get(), index=i)
            self.calculate_ci(var_file_std=self.var_file_std_default.get(),
                              var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                              var_i=self.isotopes[:, 0][i], index=i)
        for i in range(self.n_isotopes):
            self.calculate_rsf(var_file_std=self.var_file_std_default.get(),
                               var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                               var_i=self.isotopes[:, 0][i], index=i)
            self.calculate_lod(var_file_std=self.var_file_std_default.get(),
                               var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                               var_i=self.isotopes[:, 0][i], index=i)
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
        for i in range(self.n_isotopes):
            self.calculate_xi_2(var_file=self.var_file_std_default.get(), var_i=self.isotopes[:, 0][i],
                                var_is=self.var_is_default.get(), index=i)
            self.calculate_ci(var_file_std=self.var_file_std_default.get(),
                              var_file_smpl=self.var_file_smpl_default.get(), var_is=self.var_is_default.get(),
                              var_i=self.isotopes[:, 0][i], index=i)
            self.calculate_rsf(var_file_std=self.var_file_std_default.get(), var_file_smpl=self.var_file_smpl_default.get(),
                           var_is=self.var_is_default.get(), var_i=self.isotopes[:, 0][i], index=i)
            self.calculate_lod(var_file_std=self.var_file_std_default.get(), var_file_smpl=self.var_file_smpl_default.get(),
                           var_is=self.var_is_default.get(), var_i=self.isotopes[:, 0][i], index=i)
    #
    def make_isotope_column(self, parent, row_id, column_id):
        i = 0
        for isotope in self.isotopes[:, 0]:
            lbl_isotope = tk.Label(parent, text=isotope)
            lbl_isotope.grid(row=row_id+i, column=column_id, sticky="nesw")
            i += 1
    #
    def make_concentration_entries(self, parent, row_id, column_id):
        i = 0
        self.variables_conc_mu = []
        self.entries_conc_mu = []
        self.variables_conc_std = []
        self.entries_conc_std = []
        for isotope in self.isotopes[:, 0]:
            self.variables_conc_mu.append([isotope, tk.StringVar()])
            self.variables_conc_mu[i][1].set(0.0)
            self.entries_conc_mu.append([isotope, self.variables_conc_mu[i][1],
                                      tk.Entry(parent, textvariable=self.variables_conc_mu[i][1])])
            self.entries_conc_mu[i][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            #
            self.variables_conc_std.append([isotope, tk.StringVar()])
            self.variables_conc_std[i][1].set(0.0)
            self.entries_conc_std.append([isotope, self.variables_conc_std[i][1],
                                      tk.Entry(parent, textvariable=self.variables_conc_std[i][1])])
            self.entries_conc_std[i][2].grid(row=row_id+i, column=column_id+1, sticky="nesw")
            #
            i += 1
    #
    def make_sensitivity_entries(self, parent, row_id, column_id):
        i = 0
        self.variables_xi_mu = []
        self.entries_xi_mu = []
        self.variables_xi_std = []
        self.entries_xi_std = []
        for isotope in self.isotopes[:, 0]:
            self.variables_xi_mu.append([isotope, tk.StringVar()])
            self.variables_xi_mu[i][1].set(0.0)
            self.entries_xi_mu.append([isotope, self.variables_xi_mu[i][1],
                                      tk.Entry(parent, textvariable=self.variables_xi_mu[i][1])])
            self.entries_xi_mu[i][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            #
            self.variables_xi_std.append([isotope, tk.StringVar()])
            self.variables_xi_std[i][1].set(0.0)
            self.entries_xi_std.append([isotope, self.variables_xi_std[i][1],
                                      tk.Entry(parent, textvariable=self.variables_xi_std[i][1])])
            self.entries_xi_std[i][2].grid(row=row_id+i, column=column_id+1, sticky="nesw")
            #
            i += 1
    #
    def make_rsf_entries(self, parent, row_id, column_id):
        i = 0
        self.variables_rsf_mu = []
        self.entries_rsf_mu = []
        self.variables_rsf_std = []
        self.entries_rsf_std = []
        for isotope in self.isotopes[:, 0]:
            self.variables_rsf_mu.append([isotope, tk.StringVar()])
            self.variables_rsf_mu[i][1].set(0.0)
            self.entries_rsf_mu.append([isotope, self.variables_rsf_mu[i][1],
                                      tk.Entry(parent, textvariable=self.variables_rsf_mu[i][1])])
            self.entries_rsf_mu[i][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            #
            self.variables_rsf_std.append([isotope, tk.StringVar()])
            self.variables_rsf_std[i][1].set(0.0)
            self.entries_rsf_std.append([isotope, self.variables_rsf_std[i][1],
                                      tk.Entry(parent, textvariable=self.variables_rsf_std[i][1])])
            self.entries_rsf_std[i][2].grid(row=row_id+i, column=column_id+1, sticky="nesw")
            #
            i += 1
    #
    def make_lod_entries(self, parent, row_id, column_id):
        i = 0
        self.variables_lod_mu = []
        self.entries_lod_mu = []
        self.variables_lod_std = []
        self.entries_lod_std = []
        for isotope in self.isotopes[:, 0]:
            self.variables_lod_mu.append([isotope, tk.StringVar()])
            self.variables_lod_mu[i][1].set(0.0)
            self.entries_lod_mu.append([isotope, self.variables_lod_mu[i][1],
                                      tk.Entry(parent, textvariable=self.variables_lod_mu[i][1])])
            self.entries_lod_mu[i][2].grid(row=row_id+i, column=column_id, sticky="nesw")
            #
            self.variables_lod_std.append([isotope, tk.StringVar()])
            self.variables_lod_std[i][1].set(0.0)
            self.entries_lod_std.append([isotope, self.variables_lod_std[i][1],
                                      tk.Entry(parent, textvariable=self.variables_lod_std[i][1])])
            self.entries_lod_std[i][2].grid(row=row_id+i, column=column_id+1, sticky="nesw")
            #
            i += 1
    #
    def make_option_is_column(self, parent, row_id=2, column_id=10):
        self.var_is_indiv = []
        option_list_is = self.isotopes[:, 0]
        for i in range(self.n_isotopes):
            self.var_is_indiv.append(tk.StringVar())
            self.var_is_indiv[i].set("Select isotope")
            opt_menu_is = tk.OptionMenu(parent, self.var_is_indiv[i], *option_list_is,
                                        command=lambda op, var_file_std=self.var_file_std_indiv[i],
                                                       var_file_smpl=self.var_file_smpl_indiv[i], index=i,
                                                       var_is=self.var_is_indiv[i]: self.option_changed_is(var_file_std,
                                                                                                           var_file_smpl,
                                                                                                           index, var_is,
                                                                                                           op))
            opt_menu_is.grid(row=row_id+i, column=column_id, rowspan=1, columnspan=1, sticky="nesw")
    #
    def make_variable_file_std(self):
        self.var_file_std_indiv = []
        file_helper = ["All Standards"]
        for file in self.files_std:
            parts = file.split("/")
            file_helper.append(parts[-1])
        parts_actual = self.file_actual.split("/")
        self.option_list_files_std = np.array(file_helper)
        for i in range(self.n_isotopes):
            self.var_file_std_indiv.append(tk.StringVar())
            if self.file_actual in self.files_std:
                self.var_file_std_indiv[i].set(parts_actual[-1])
            else:
                self.var_file_std_indiv[i].set(self.option_list_files_std[1])
    #
    def make_variable_file_smpl(self):
        self.var_file_smpl_indiv = []
        file_helper = ["All Samples"]
        for file in self.files_smpl:
            parts = file.split("/")
            file_helper.append(parts[-1])
        parts_actual = self.file_actual.split("/")
        self.option_list_files_smpl = np.array(file_helper)
        for i in range(self.n_isotopes):
            self.var_file_smpl_indiv.append(tk.StringVar())
            if self.file_actual in self.files_smpl:
                self.var_file_smpl_indiv[i].set(parts_actual[-1])
            else:
                self.var_file_smpl_indiv[i].set(self.option_list_files_smpl[1])
    #
    def make_option_file_std(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        parts_actual = self.file_actual.split("/")
        if self.file_actual in self.files_std:
                self.var_file_std_default.set(parts_actual[-1])
        else:
            self.var_file_std_default.set(self.option_list_files_std[1])
        opt_menu_file_std = tk.OptionMenu(parent, self.var_file_std_default, *self.option_list_files_std,
                                          command=lambda op, var_default=self.var_file_std_default,
                                                         var_indiv=self.var_file_std_indiv, key="standard": self.option_changed_file_default(var_default, var_indiv, key, op))
        opt_menu_file_std.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def make_option_file_smpl(self, parent, row_id, column_id, n_rows=1, n_columns=1):
        parts_actual = self.file_actual.split("/")
        if self.file_actual in self.files_smpl:
                self.var_file_smpl_default.set(parts_actual[-1])
        else:
            self.var_file_smpl_default.set(self.option_list_files_smpl[1])
        opt_menu_file_smpl = tk.OptionMenu(parent, self.var_file_smpl_default, *self.option_list_files_smpl,
                                          command=lambda op, var_default=self.var_file_smpl_default,
                                                         var_indiv=self.var_file_smpl_indiv, key="sample": self.option_changed_file_default(var_default, var_indiv, key, op))
        opt_menu_file_smpl.grid(row=row_id, column=column_id, rowspan=n_rows, columnspan=n_columns, sticky="nesw")
    #
    def option_changed_file_default(self, var_default, var_indiv, key, op):
        if key == "standard":
            for i in range(self.n_isotopes):
                var_indiv[i].set(var_default.get())
                self.calculate_xi_2(var_file=var_indiv[i].get(), var_i=self.isotopes[:, 0][i], var_is=self.var_is_indiv[i].get(), index=i)
                self.calculate_ci(var_file_std=self.var_file_std_indiv[i].get(), var_file_smpl=self.var_file_smpl_indiv[i].get(), var_is=self.var_is_indiv[i].get(),
                                  var_i=self.isotopes[:, 0][i], index=i)
                self.calculate_rsf(var_file_std=self.var_file_std_indiv[i].get(), var_file_smpl=self.var_file_smpl_indiv[i].get(),
                           var_is=self.var_is_indiv[i].get(), var_i=self.isotopes[:, 0][i], index=i)
                self.calculate_lod(var_file_std=self.var_file_std_indiv[i].get(), var_file_smpl=self.var_file_smpl_indiv[i].get(),
                           var_is=self.var_is_indiv[i].get(), var_i=self.isotopes[:, 0][i], index=i)
        elif key == "sample":
            for i in range(self.n_isotopes):
                var_indiv[i].set(var_default.get())
                self.calculate_ci(var_file_std=self.var_file_std_indiv[i].get(), var_file_smpl=self.var_file_smpl_indiv[i].get(), var_is=self.var_is_indiv[i].get(),
                                      var_i=self.isotopes[:, 0][i], index=i)
                self.calculate_rsf(var_file_std=self.var_file_std_indiv[i].get(), var_file_smpl=self.var_file_smpl_indiv[i].get(),
                           var_is=self.var_is_indiv[i].get(), var_i=self.isotopes[:, 0][i], index=i)
                self.calculate_lod(var_file_std=self.var_file_std_indiv[i].get(), var_file_smpl=self.var_file_smpl_indiv[i].get(),
                           var_is=self.var_is_indiv[i].get(), var_i=self.isotopes[:, 0][i], index=i)
    #
    def make_option_file_column_std(self, parent, row_id=2, column_id=11):
        for i in range(self.n_isotopes):
            opt_menu_file = tk.OptionMenu(parent, self.var_file_std_indiv[i], *self.option_list_files_std,
                                          command=lambda op, var_file_std=self.var_file_std_indiv[i],
                                                         var_file_smpl=self.var_file_smpl_indiv[i], index=i,
                                                         var_is=self.var_is_indiv[i], key="standard": self.option_changed_file(var_file_std, var_file_smpl,
                                                                                                               index,
                                                                                                               var_is, key,
                                                                                                               op))
            opt_menu_file.grid(row=row_id+i, column=column_id, rowspan=1, columnspan=1, sticky="nesw")
    #
    def make_option_file_column_smpl(self, parent, row_id=2, column_id=12):
        for i in range(self.n_isotopes):
            opt_menu_file = tk.OptionMenu(parent, self.var_file_smpl_indiv[i], *self.option_list_files_smpl,
                                          command=lambda op, var_file_std=self.var_file_std_indiv[i],
                                                         var_file_smpl=self.var_file_smpl_indiv[i], index=i,
                                                         var_is=self.var_is_indiv[i], key="sample": self.option_changed_file(var_file_std, var_file_smpl,
                                                                                                               index,
                                                                                                               var_is, key,
                                                                                                               op))
            opt_menu_file.grid(row=row_id+i, column=column_id, rowspan=1, columnspan=1, sticky="nesw")
    #
    def calculate_xi_2(self, var_file, var_i, var_is, index):
        #
        key_i = re.search("(\D+)(\d+)", var_i)
        key_is = re.search("(\D+)(\d+)", var_is)
        index_i = self.pse_list.index(key_i.group(1))
        index_is = self.pse_list.index(key_is.group(1))
        #
        concentration_i = self.srm_values[index_i]
        concentration_is = self.srm_values[index_is]
        #
        if var_file not in ["All Standards", "All Samples"]:
            for item in self.files_std:
                    if var_file in item:
                        var_file = item
            #
            dataset_std = data.Data(filename=var_file)
            df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            #
            intensity_i = df_std[var_i][self.indices_sig[0]:self.indices_sig[1]+1].mean()
            intensity_is = df_std[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
            #
            if concentration_i == 0:
                self.entries_xi_mu[index][2].delete(0, tk.END)
                self.entries_xi_mu[index][2].insert(0, round(0.0, 8))
                self.entries_xi_std[index][2].delete(0, tk.END)
                self.entries_xi_std[index][2].insert(0, round(0.0, 8))
            else:
                xi = intensity_i/intensity_is * concentration_is/concentration_i
                self.entries_xi_mu[index][2].delete(0, tk.END)
                self.entries_xi_mu[index][2].insert(0, round(xi.mean(), 8))
                self.entries_xi_std[index][2].delete(0, tk.END)
                self.entries_xi_std[index][2].insert(0, round(0.0, 8))
        else:
            files_helper = []
            results_helper = [[], []]
            if var_file == "All Standards":
                var_file = self.option_list_files_std[1:]
                for item_1 in self.files_std:
                    for item_2 in var_file:
                        if item_2 in item_1:
                            files_helper.append(item_1)
            elif var_file == "All Samples":
                var_file = self.option_list_files_smpl[1:]
                for item_1 in self.files_smpl:
                    for item_2 in var_file:
                        if item_2 in item_1:
                            files_helper.append(item_1)
            #
            for item in files_helper:
                dataset_std_j = data.Data(filename=item)
                df_std_j = dataset_std_j.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                #
                intensity_i_j = df_std_j[var_i][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                intensity_is_j = df_std_j[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                #
                if concentration_i > 0:
                    xi_j = intensity_i_j/intensity_is_j * concentration_is/concentration_i
                    results_helper[0].append(xi_j)
                    results_helper[1].append(xi_j)
                #
            if concentration_i == 0:
                self.entries_xi_mu[index][2].delete(0, tk.END)
                self.entries_xi_mu[index][2].insert(0, round(0.0, 8))
                self.entries_xi_std[index][2].delete(0, tk.END)
                self.entries_xi_std[index][2].insert(0, round(0.0, 8))
            else:
                self.entries_xi_mu[index][2].delete(0, tk.END)
                self.entries_xi_mu[index][2].insert(0, round(np.mean(results_helper[0]), 8))
                if len(files_helper) == 1:
                    self.entries_xi_std[index][2].delete(0, tk.END)
                    self.entries_xi_std[index][2].insert(0, 0.0)
                else:
                    self.entries_xi_std[index][2].delete(0, tk.END)
                    self.entries_xi_std[index][2].insert(0, round(np.std(results_helper[1], ddof=1), 8))
    #
    def option_changed_file(self, var_file_std, var_file_smpl, index, var_is, key, op):
        if key == "standard":
            self.calculate_xi_2(var_file=var_file_std.get(), var_i=self.isotopes[:, 0][index], var_is=var_is.get(), index=index)
            self.calculate_ci(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                              var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
            self.calculate_rsf(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                           var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
            self.calculate_lod(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                           var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
        elif key == "sample":
            self.calculate_ci(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                              var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
            self.calculate_rsf(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                           var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
            self.calculate_lod(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                           var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
    #
    def option_changed_is(self, var_file_std, var_file_smpl, index, var_is, op):
        self.calculate_xi_2(var_file=var_file_std.get(), var_i=self.isotopes[:, 0][index], var_is=var_is.get(),
                            index=index)
        self.calculate_ci(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                          var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
        self.calculate_rsf(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                           var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
        self.calculate_lod(var_file_std=var_file_std.get(), var_file_smpl=var_file_smpl.get(),
                           var_is=var_is.get(), var_i=self.isotopes[:, 0][index], index=index)
    #
    def calculate_ci(self, var_file_std, var_file_smpl, var_is, var_i, index):
        files_helper_std = []
        files_helper_smpl = []
        #
        results_helper = []
        if var_file_smpl == "All Samples":
            if var_file_smpl == "All Samples":
                var_file_smpl = self.option_list_files_smpl[1:]
                for item_1 in self.files_smpl:
                    for item_2 in var_file_smpl:
                        if item_2 in item_1:
                            files_helper_smpl.append(item_1)
        else:
            for item in self.files_smpl:
                if var_file_smpl in item:
                    var_file_smpl = item
                    files_helper_smpl.append(item)
        #
        if var_file_std == "All Standards":
            if var_file_std == "All Standards":
                var_file_std = self.option_list_files_std[1:]
                for item_1 in self.files_std:
                    for item_2 in var_file_std:
                        if item_2 in item_1:
                            files_helper_std.append(item_1)
        else:
            for item in self.files_std:
                if var_file_std in item:
                    var_file_std = item
                    files_helper_std.append(item)
        #
        if len(self.results_concentration[index]) > 1:
            self.results_concentration[index] = self.results_concentration[index][:1]
        self.results_concentration[index].append(var_is)
        #
        key_i = re.search("(\D+)(\d+)", var_i)
        key_is = re.search("(\D+)(\d+)", var_is)
        index_i = self.pse_list.index(key_i.group(1))
        index_is = self.pse_list.index(key_is.group(1))
        #
        concentration_i = self.srm_values[index_i]
        concentration_is = self.srm_values[index_is]
        concentration_is_smpl = self.conc_smpl_is[index_is]
        #
        for item_std in files_helper_std:
            for item in files_helper_smpl:
                dataset_std_k = data.Data(filename=item_std)
                df_std_k = dataset_std_k.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                dataset_smpl_j = data.Data(filename=item)
                df_smpl_j = dataset_smpl_j.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                #
                intensity_i_k = df_std_k[var_i][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                intensity_is_k = df_std_k[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                intensity_i_j = df_smpl_j[var_i][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                intensity_is_j = df_smpl_j[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                if concentration_i > 0:
                    xi_self = (intensity_i_k/intensity_is_k) * (concentration_is/concentration_i)
                else:
                    xi_self = 0.0
                xi_j = float(self.entries_xi_mu[index][2].get())
                #
                if xi_j > 0 and xi_self > 0:
                    #ci_j = (intensity_i_j/intensity_is_j)*(concentration_is_smpl/xi_j)
                    ci_jk = (intensity_i_j/intensity_is_j)*(concentration_is_smpl/xi_j) * (intensity_i_k/intensity_is_k) * (concentration_is/concentration_i)
                    results_helper.append(ci_jk)
                else:
                    pass
        #
        if concentration_i > 0:
            conc_mu = np.mean(results_helper)
            self.entries_conc_mu[index][2].delete(0, tk.END)
            self.entries_conc_mu[index][2].insert(0, round(conc_mu, 8))
            self.results_concentration[index].append(conc_mu)
            if len(files_helper_smpl)*len(files_helper_std) == 1:
                cond_std = 0.0
                self.entries_conc_std[index][2].delete(0, tk.END)
                self.entries_conc_std[index][2].insert(0, cond_std)
                self.results_concentration[index].append(cond_std)
            else:
                conc_std = np.std(results_helper, ddof=1)
                self.entries_conc_std[index][2].delete(0, tk.END)
                self.entries_conc_std[index][2].insert(0, round(conc_std, 8))
                self.results_concentration[index].append(conc_std)
        else:
            self.results_concentration[index].append(0.0)
            self.results_concentration[index].append(0.0)
    #
    def calculate_rsf(self, var_file_std, var_file_smpl, var_is, var_i, index):
        files_helper_std = []
        files_helper_smpl = []
        results_helper = []
        #
        if var_file_smpl == "All Samples":
            if var_file_smpl == "All Samples":
                var_file_smpl = self.option_list_files_smpl[1:]
                for item_1 in self.files_smpl:
                    for item_2 in var_file_smpl:
                        if item_2 in item_1:
                            files_helper_smpl.append(item_1)
        else:
            for item in self.files_smpl:
                if var_file_smpl in item:
                    var_file_smpl = item
                    files_helper_smpl.append(item)
        #
        if var_file_std == "All Standards":
            if var_file_std == "All Standards":
                var_file_std = self.option_list_files_std[1:]
                for item_1 in self.files_std:
                    for item_2 in var_file_std:
                        if item_2 in item_1:
                            files_helper_std.append(item_1)
        else:
            for item in self.files_std:
                if var_file_std in item:
                    var_file_std = item
                    files_helper_std.append(item)
        #
        if len(files_helper_smpl) == 0 and len(files_helper_std) == 0:
            dataset_std = data.Data(filename=var_file_std)
            df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            dataset_smpl = data.Data(filename=var_file_smpl)
            df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            #
            key_is = re.search("(\D+)(\d+)", var_is)
            index_is = self.isotopes[:, 0].tolist().index(key_is.group(0))
            key_is_std = re.search("(\D+)(\d+)", var_is)
            index_is_std = self.pse_list.index(key_is_std.group(1))
            #
            intensity_is_std = df_std[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
            intensity_is_smpl = df_smpl[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
            c_is_std = self.srm_values[index_is_std]
            c_is_smpl = float(self.entries_conc_mu[index_is][2].get())
            #
            if c_is_smpl > 0:
                rsf_i = (c_is_std/c_is_smpl) * (intensity_is_smpl/intensity_is_std)
                self.entries_rsf_mu[index][2].delete(0, tk.END)
                self.entries_rsf_mu[index][2].insert(0, round(rsf_i, 8))
                self.entries_rsf_std[index][2].delete(0, tk.END)
                self.entries_rsf_std[index][2].insert(0, round(0.0, 8))
            else:
                pass
        else:
            key_is = re.search("(\D+)(\d+)", var_is)
            index_is = self.isotopes[:, 0].tolist().index(key_is.group(0))
            key_is_std = re.search("(\D+)(\d+)", var_is)
            index_is_std = self.pse_list.index(key_is_std.group(1))
            #
            c_is_std = self.srm_values[index_is_std]
            c_is_smpl = float(self.entries_conc_mu[index_is][2].get())
            #
            for item_std in files_helper_std:
                for item_smpl in files_helper_smpl:
                    dataset_std_j = data.Data(filename=item_std)
                    df_std_j = dataset_std_j.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    dataset_smpl_j = data.Data(filename=item_smpl)
                    df_smpl_j = dataset_smpl_j.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    #
                    intensity_is_std_j = df_std_j[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                    intensity_is_smpl_j = df_smpl_j[var_is][self.indices_sig[0]:self.indices_sig[1]+1].mean()
                    #
                    if c_is_smpl > 0:
                        rsf_j = (c_is_std/c_is_smpl) * (intensity_is_smpl_j/intensity_is_std_j)
                        results_helper.append(rsf_j)
                #
                if c_is_smpl > 0:
                    self.entries_rsf_mu[index][2].delete(0, tk.END)
                    self.entries_rsf_mu[index][2].insert(0, round(np.mean(results_helper), 8))
                    if len(results_helper) == 1:
                        self.entries_rsf_std[index][2].delete(0, tk.END)
                        self.entries_rsf_std[index][2].insert(0, 0.0)
                    else:
                        self.entries_rsf_std[index][2].delete(0, tk.END)
                        self.entries_rsf_std[index][2].insert(0, round(np.std(results_helper, ddof=1), 8))
                else:
                    pass
    #
    def calculate_lod(self, var_file_std, var_file_smpl, var_is, var_i, index):
        files_helper_std = []
        files_helper_smpl = []
        results_helper = []
        #
        if var_file_smpl == "All Samples":
            if var_file_smpl == "All Samples":
                var_file_smpl = self.option_list_files_smpl[1:]
                for item_1 in self.files_smpl:
                    for item_2 in var_file_smpl:
                        if item_2 in item_1:
                            files_helper_smpl.append(item_1)
        else:
            for item in self.files_smpl:
                if var_file_smpl in item:
                    var_file_smpl = item
                    files_helper_smpl.append(item)
        #
        if var_file_std == "All Standards":
            if var_file_std == "All Standards":
                var_file_std = self.option_list_files_std[1:]
                for item_1 in self.files_std:
                    for item_2 in var_file_std:
                        if item_2 in item_1:
                            files_helper_std.append(item_1)
        else:
            for item in self.files_std:
                if var_file_std in item:
                    var_file_std = item
                    files_helper_std.append(item)
        #
        key_i_std = re.search("(\D+)(\d+)", var_i)
        index_i_std = self.pse_list.index(key_i_std.group(1))
        #
        c_i_std = self.srm_values[index_i_std]
        #
        n_bg = len(self.times[self.indices_bg[0]:self.indices_bg[1]+1])
        n_sig = len(self.times[self.indices_sig[0]:self.indices_sig[1]+1])
        #
        rsf_i = float(self.entries_rsf_mu[index][2].get())
        #
        for item_std in files_helper_std:
            dataset_std_j = data.Data(filename=item_std)
            df_std_j = dataset_std_j.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
            #
            intensity_i_std_j = df_std_j[var_i][self.indices_sig[0]:self.indices_sig[1]+1].mean()
            sigma_i_j = df_std_j[var_i][self.indices_bg[0]:self.indices_bg[1]+1].std()
            #
            if rsf_i > 0:
                lod_j = (3*sigma_i_j)/rsf_i * np.sqrt((1/n_bg) + (1/n_sig)) * (c_i_std/intensity_i_std_j)
                results_helper.append(lod_j)
        #
        if rsf_i > 0:
            self.entries_lod_mu[index][2].delete(0, tk.END)
            self.entries_lod_mu[index][2].insert(0, round(np.mean(results_helper), 8))
            if len(files_helper_std) == 1:
                self.entries_lod_std[index][2].delete(0, tk.END)
                self.entries_lod_std[index][2].insert(0, 0.0)
            else:
                self.entries_lod_std[index][2].delete(0, tk.END)
                self.entries_lod_std[index][2].insert(0, round(np.std(results_helper, ddof=1), 8))
        else:
            pass
    #
    def export_results_as_csv(self):
        print(self.results_concentration)
       # results_csv = open("results.csv", "w")
       # results_csv.write("C_mu"+";"+"C_std")