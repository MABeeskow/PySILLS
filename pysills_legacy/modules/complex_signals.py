#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# complex_signals.py
# Maximilian Beeskow
# 17.08.2021
# ----------------------
#
## MODULES
import tkinter as tk
from modules.gui_elements import SimpleElements as SE
from modules import data
import re
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

## CLASSES
class ComplexSignals:
    #
    def __init__(self, parent, color_bg, signal, isotopes, times, times_iw_bg, times_iw_sig, files_std, files_smpl,
                 file_actual, test_data):
        self.parent = parent
        self.color_bg = color_bg
        self.color_fg = "black"
        self.signal = signal
        self.isotopes = isotopes
        self.times = times
        self.times_iw_bg = times_iw_bg
        self.times_iw_sig = times_iw_sig
        self.files_std = files_std
        self.files_smpl = files_smpl
        self.file_actual = file_actual
        self.test_data = test_data
        #
        self.n_isotopes = len(self.isotopes[:, 0])
        self.measured_isotopes = self.isotopes[:, 0]
        #
        self.index_start_sig = 0
        self.index_end_sig = len(self.times)-1
        self.indices_sig = [self.index_start_sig, self.index_end_sig]
        self.index_start_bg = 0
        self.index_end_bg = len(self.times)-1
        self.indices_bg = [self.index_start_bg, self.index_end_bg]
        #
    def make_complex_signals_window(self):
        # GEOMETRY
        width = int(4*85 + 15 + 9*90 + 140 + 2*150 + 15)
        height = int(2*20 + (self.n_isotopes+3)*30 + 15)
        self.cs_window = tk.Toplevel(self.parent)
        self.cs_window.geometry(str(width)+"x"+str(height))
        self.cs_window.title("Complex Signals")
        print(self.test_data)
        #
    #
    def make_complex_signals_window_SIG1(self):
        #
        ################################################################################################################
        ## VARIABLES ###################################################################################################
        #
        self.var_sig_mu = []
        self.entr_sig_mu = []
        self.var_sig_std = []
        self.entr_sig_std = []
        self.var_file_std_default = tk.StringVar()
        self.var_file_smpl_default = tk.StringVar()
        self.var_file_std_indiv = []
        self.var_file_smpl_indiv = []
        self.option_list_files_std = []
        self.option_list_files_smpl = []
        self.var_rb = tk.IntVar()
        self.var_cb_std = tk.IntVar()
        self.var_cb_smpl = tk.IntVar()
        #
        ################################################################################################################
        ## GEOMETRY ####################################################################################################
        #
        width = int(7*90 + 2*100 + 2*150 + 15)
        height = int(3*20 + (self.n_isotopes+2)*30 + 15)
        self.cs_window = tk.Toplevel(self.parent)
        self.cs_window.geometry(str(width)+"x"+str(height))
        self.cs_window.title("Complex Signals - Segment 1 (Background)")
        #
        for y in range(int(self.n_isotopes + 5)):
            tk.Grid.rowconfigure(self.cs_window, y, weight=1)
        for x in range(12):
            tk.Grid.columnconfigure(self.cs_window, x, weight=1)
        #
        # Rows
        for i in range(0, 3):
            self.cs_window.grid_rowconfigure(i, minsize=20)
        for i in range(3, int(self.n_isotopes+5)):
            self.cs_window.grid_rowconfigure(i, minsize=30)
        self.cs_window.grid_rowconfigure(int(self.n_isotopes+5), minsize=15)
        # Columns
        for i in range(0, 6):
            self.cs_window.grid_columnconfigure(i, minsize=90)
        for i in range(6, 8):
            self.cs_window.grid_columnconfigure(i, minsize=100)
        for i in range(8, 10):
            self.cs_window.grid_columnconfigure(i, minsize=150)
        self.cs_window.grid_columnconfigure(10, minsize=90)
        self.cs_window.grid_columnconfigure(11, minsize=15)
        #
        ################################################################################################################
        ## LABELS ######################################################################################################
        #
        SE(parent=self.cs_window, row_id=0, column_id=0, n_rows=3, n_columns=4, fg=self.color_fg,
           bg=self.color_bg).create_label(text="General Settings")
        SE(parent=self.cs_window, row_id=3, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Time Settings (BG)")
        SE(parent=self.cs_window, row_id=0, column_id=5, n_rows=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Isotopes")
        SE(parent=self.cs_window, row_id=0, column_id=6, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Segment 1")
        SE(parent=self.cs_window, row_id=1, column_id=6, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Background BG")
        SE(parent=self.cs_window, row_id=2, column_id=6, fg=self.color_fg, bg=self.color_bg).create_label(text="\u03BC")
        SE(parent=self.cs_window, row_id=2, column_id=7, fg=self.color_fg, bg=self.color_bg).create_label(text="\u03C3")
        SE(parent=self.cs_window, row_id=0, column_id=8, n_rows=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Input File")
        SE(parent=self.cs_window, row_id=2, column_id=8, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Standard STD")
        SE(parent=self.cs_window, row_id=2, column_id=9, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Sample SMPL")
        SE(parent=self.cs_window, row_id=0, column_id=10, n_rows=3, fg=self.color_fg,
           bg=self.color_bg).create_label(text="Display")
        #
        SE(parent=self.cs_window, row_id=3, column_id=5, fg=self.color_fg,
           bg=self.color_bg).create_isotope_column(input_isotopes=self.isotopes)
        #
        ################################################################################################################
        ## Buttons #####################################################################################################
        #
        SE(parent=self.cs_window, row_id=3, column_id=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Advanced Statistics")
        SE(parent=self.cs_window, row_id=4, column_id=2, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_button(text="Export Results")
        #
        ################################################################################################################
        ## Time Windows ################################################################################################
        #
        self.entr_t_start_bg, self.entr_t_end_bg = SE(parent=self.cs_window, row_id=5, column_id=0, fg=self.color_fg,
           bg=self.color_bg).create_time_window_entries(times=self.times, part="BG")
        self.var_iw_bg = SE(parent=self.cs_window, row_id=4, column_id=0, n_columns=2, fg=self.color_fg,
           bg=self.color_bg).create_option_times(part="BG", times_seg=self.times_iw_bg,
                                                 command=lambda op, part="BG": self.select_time_window(part, op))
        #
        ################################################################################################################
        ## Segment 1 ###################################################################################################
        #
        SE(parent=self.cs_window, row_id=3, column_id=6, fg=self.color_fg,
           bg=self.color_bg).create_signal_entries(var_sig_mu=self.var_sig_mu, entr_sig_mu=self.entr_sig_mu,
                                                   var_sig_std=self.var_sig_std, entr_sig_std=self.entr_sig_std,
                                                   input_isotopes=self.isotopes)
        self.var_file_std_indiv, self.option_list_files_std = SE(parent=self.cs_window, row_id=int(3+self.n_isotopes), column_id=8, fg=self.color_fg,
           bg=self.color_bg).create_option_files(type_name="STD", file_selected=self.file_actual,
                                                 file_type=self.files_std, var_file_default=self.var_file_std_default,
                                                 n_isotopes=self.n_isotopes, command=lambda op, type_name="STD": self.select_option_file_default(type_name, op))
        self.var_file_smpl_indiv, self.option_list_files_smpl = SE(parent=self.cs_window, row_id=int(3+self.n_isotopes), column_id=9, fg=self.color_fg,
           bg=self.color_bg).create_option_files(type_name="SMPL", file_selected=self.file_actual,
                                                 file_type=self.files_smpl, var_file_default=self.var_file_smpl_default,
                                                 n_isotopes=self.n_isotopes, command=lambda op, type_name="SMPL": self.select_option_file_default(type_name, op))
        SE(parent=self.cs_window, row_id=3, column_id=8, fg=self.color_fg,
           bg=self.color_bg).create_option_files_column(var_file_indiv=self.var_file_std_indiv,
                                                        option_list=self.option_list_files_std,
                                                        n_isotopes=self.n_isotopes)
        SE(parent=self.cs_window, row_id=3, column_id=9, fg=self.color_fg,
           bg=self.color_bg).create_option_files_column(var_file_indiv=self.var_file_smpl_indiv,
                                                        option_list=self.option_list_files_smpl,
                                                        n_isotopes=self.n_isotopes)
        SE(parent=self.cs_window, row_id=3, column_id=10, fg=self.color_fg,
           bg=self.color_bg).create_radiobutton_column(var_rb=self.var_rb, isotopes=self.isotopes,
                                                       command=lambda var=self.var_rb: self.select_radiobutton(var))
        SE(parent=self.cs_window, row_id=int(3+self.n_isotopes+1), column_id=8, fg=self.color_fg,
           bg=self.color_bg).create_checkbox(var_cb=self.var_cb_std, text="only STD", type_name="STD",
                                             command=lambda var=self.var_cb_std: self.select_checkbox(var))
        SE(parent=self.cs_window, row_id=int(3+self.n_isotopes+1), column_id=9, fg=self.color_fg,
           bg=self.color_bg).create_checkbox(var_cb=self.var_cb_smpl, text="only SMPL", type_name="SMPL",
                                             command=lambda var=self.var_cb_smpl: self.select_checkbox(var))
        #
        ################################################################################################################
        ## Graphics ####################################################################################################
        #
        #
    #
    def select_radiobutton(self, var):
        print("Variable:", var.get(), "--> isotope", self.isotopes[:, 0][var.get()])
    #
    def select_checkbox(self, var):
        print("Variable:", var.get())
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
            for i in range(self.n_isotopes):
                self.fill_signal_entries(var_i=isotopes[i], var_file_std=self.var_file_std_indiv[i].get(),
                                         var_file_smpl=self.var_file_smpl_indiv[i].get(), part="BG", index=i)
        elif part == "MATR":
            if self.var_iw_matr.get() != "No Time Intervals":
                key = re.search("(\d+\.\d+)" + " - " + "(\d+\.\d+)", self.var_iw_matr.get())
                t_start = float(key.group(1))
                t_end = float(key.group(2))
                #
                t_id_start = self.times[self.times == t_start].index[0]
                t_id_end = self.times[self.times == t_end].index[0]
                #
                self.indices_matr[0] = t_id_start
                self.indices_matr[1] = t_id_end
                self.entr_t_start_matr.delete(0, tk.END)
                self.entr_t_start_matr.insert(0, t_start)
                self.entr_t_end_matr.delete(0, tk.END)
                self.entr_t_end_matr.insert(0, t_end)
        elif part == "INCL":
            if self.var_iw_incl.get() != "No Time Intervals":
                key = re.search("(\d+\.\d+)" + " - " + "(\d+\.\d+)", self.var_iw_incl.get())
                t_start = float(key.group(1))
                t_end = float(key.group(2))
                #
                t_id_start = self.times[self.times == t_start].index[0]
                t_id_end = self.times[self.times == t_end].index[0]
                #
                self.indices_incl[0] = t_id_start
                self.indices_incl[1] = t_id_end
                self.entr_t_start_incl.delete(0, tk.END)
                self.entr_t_start_incl.insert(0, t_start)
                self.entr_t_end_incl.delete(0, tk.END)
                self.entr_t_end_incl.insert(0, t_end)
    #
    def select_option_file_default(self, type_name, op):
        isotopes = self.isotopes[:, 0]
        if type_name == "STD":
            for i in range(self.n_isotopes):
                self.var_file_std_indiv[i].set(self.var_file_std_default.get())
                self.fill_signal_entries(var_i=isotopes[i], var_file_std=self.var_file_std_indiv[i].get(),
                                         var_file_smpl=self.var_file_smpl_indiv[i].get(), part="BG", index=i)
        elif type_name == "SMPL":
            for i in range(self.n_isotopes):
                self.var_file_smpl_indiv[i].set(self.var_file_smpl_default.get())
                self.fill_signal_entries(var_i=isotopes[i], var_file_std=self.var_file_std_indiv[i].get(),
                                         var_file_smpl=self.var_file_smpl_indiv[i].get(), part="BG", index=i)
    #
    def fill_signal_entries(self, var_i, var_file_std, var_file_smpl, part, index):
        files_helper_std = []
        files_helper_smpl = []
        results_helper = []
        all_data = []
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
        if part == "BG":
            if self.var_cb_std.get() == 1 and self.var_cb_smpl.get() == 0:
                for file_std in files_helper_std:
                    dataset_std = data.Data(filename=file_std)
                    df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    #
                    values_i_std = df_std[var_i][self.indices_bg[0]:self.indices_bg[1]+1]
                    if self.measured_isotopes[self.var_rb.get()] == var_i:
                        all_data.extend(values_i_std.values.tolist())
                        #self.make_histo_plot(input_data=all_data, isotope=var_i)
                    #
                    intensity_i_std = values_i_std.mean()
                    results_helper.append(intensity_i_std)
                    #
                self.entr_sig_mu[index][2].delete(0, tk.END)
                self.entr_sig_mu[index][2].insert(0, round(np.mean(results_helper), 8))
                if len(files_helper_std) == 1:
                    self.entr_sig_std[index][2].delete(0, tk.END)
                    self.entr_sig_std[index][2].insert(0, round(0.0, 8))
                else:
                    self.entr_sig_std[index][2].delete(0, tk.END)
                    self.entr_sig_std[index][2].insert(0, round(np.std(results_helper, ddof=1), 8))
            elif self.var_cb_std.get() == 1 and self.var_cb_smpl.get() == 1:
                for file_std in files_helper_std:
                    for file_smpl in files_helper_smpl:
                        dataset_std = data.Data(filename=file_std)
                        df_std = dataset_std.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                        dataset_smpl = data.Data(filename=file_smpl)
                        df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                        #
                        values_i_std = df_std[var_i][self.indices_bg[0]:self.indices_bg[1]+1]
                        values_i_smpl = df_smpl[var_i][self.indices_bg[0]:self.indices_bg[1]+1]
                        if self.measured_isotopes[self.var_rb.get()] == var_i:
                            all_data.extend(values_i_std.values.tolist())
                            all_data.extend(values_i_smpl.values.tolist())
                            #self.make_histo_plot(input_data=all_data, isotope=var_i)
                        #
                        intensity_i_std = values_i_std.mean()
                        intensity_i_smpl = values_i_smpl.mean()
                        results_helper.append(intensity_i_std)
                        results_helper.append(intensity_i_smpl)
                        #
                self.entr_sig_mu[index][2].delete(0, tk.END)
                self.entr_sig_mu[index][2].insert(0, round(np.mean(results_helper), 8))
                self.entr_sig_std[index][2].delete(0, tk.END)
                self.entr_sig_std[index][2].insert(0, round(np.std(results_helper, ddof=1), 8))
            elif self.var_cb_std.get() == 0 and self.var_cb_smpl.get() == 1:
                for file_smpl in files_helper_smpl:
                    dataset_smpl = data.Data(filename=file_smpl)
                    df_smpl = dataset_smpl.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
                    #
                    values_i_smpl = df_smpl[var_i][self.indices_bg[0]:self.indices_bg[1]+1]
                    if self.measured_isotopes[self.var_rb.get()] == var_i:
                        all_data.extend(values_i_smpl.values.tolist())
                    #
                    intensity_i_smpl = values_i_smpl.mean()
                    results_helper.append(intensity_i_smpl)
                    #
                self.entr_sig_mu[index][2].delete(0, tk.END)
                self.entr_sig_mu[index][2].insert(0, round(np.mean(results_helper), 8))
                if len(files_helper_smpl) == 1:
                    self.entr_sig_std[index][2].delete(0, tk.END)
                    self.entr_sig_std[index][2].insert(0, round(0.0, 8))
                else:
                    self.entr_sig_std[index][2].delete(0, tk.END)
                    self.entr_sig_std[index][2].insert(0, round(np.std(results_helper, ddof=1), 8))
        #
        if self.measured_isotopes[self.var_rb.get()] == var_i:
            self.make_histo_plot(input_data=all_data, isotope=var_i)
    #
    def make_histo_plot(self, input_data, isotope):
        #
        try:
            self.fig_histo.clf()
            self.ax_histo.cla()
            self.canvas_histo.get_tk_widget().forget_grid()
        except AttributeError:
            pass

        try:
            if self.canvas_histo:
                self.canvas_histo.destroy()
        except AttributeError:
            pass
        #
        self.canvas_histo = None
        self.fig_histo = Figure(facecolor=self.color_bg)
        self.ax_histo = self.fig_histo.add_subplot()
        #
        if self.var_cb_std.get() == 1 and self.var_cb_smpl.get() == 0:
            color = "tomato"
        elif self.var_cb_std.get() == 0 and self.var_cb_smpl.get() == 1:
            color = "forestgreen"
        elif self.var_cb_std.get() == 1 and self.var_cb_smpl.get() == 1:
            color = "slateblue"
        #
        self.ax_histo.axvline(x=np.mean(input_data), color="black", linestyle="dashed")
        self.ax_histo.hist(input_data, bins=15, color=color, edgecolor="black")
        self.ax_histo.grid(True)
        self.ax_histo.set_axisbelow(True)
        self.ax_histo.set_ylabel("Frequency", labelpad=0.5)
        self.ax_histo.set_title("Background intensities of "+str(isotope))
        #
        self.canvas_histo = FigureCanvasTkAgg(self.fig_histo, master=self.cs_window)
        self.canvas_histo.get_tk_widget().grid(row=7, column=0, rowspan=20, columnspan=5, sticky="nesw")
    #