#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# gui_elements.py
# Maximilian Beeskow
# 14.03.2025
# ----------------------
#
## MODULES
# external
import tkinter as tk
from tkinter import ttk
import numpy as np
import colorsys
import matplotlib.colors
# internal
try:
    from pysills_legacy.modules.essential_functions import Essentials
except:
    from modules.essential_functions import Essentials

## CLASSES
class SimpleElements:
    #
    def __init__(self, parent, row_id, column_id, fg, bg, n_rows=1, n_columns=1):
        self.parent = parent
        self.row_id = row_id
        self.column_id = column_id
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.fg = fg
        self.bg = bg
    #
    def create_simple_label(self, text, fontsize=None, relief=tk.GROOVE, textvariable=False, anchor="center",
                            sticky="nesw", link=False):
        if fontsize != None:
            if textvariable == False:
                lbl = tk.Label(self.parent, text=text, relief=relief, bg=self.bg, fg=self.fg, font=(fontsize),
                               anchor=anchor)
            else:
                lbl = tk.Label(self.parent, textvariable=text, relief=relief, bg=self.bg, fg=self.fg, font=(fontsize),
                               anchor=anchor)
        else:
            if textvariable == False:
                lbl = tk.Label(self.parent, text=text, relief=relief, bg=self.bg, fg=self.fg, font=fontsize)
            else:
                lbl = tk.Label(self.parent, textvariable=text, relief=relief, bg=self.bg, fg=self.fg, font=fontsize)

        if link == True:
            lbl.configure(cursor="hand2")

        lbl.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky=sticky)
        #
        return lbl
    #
    def create_label(self, text, relief=tk.GROOVE):
        lbl = tk.Label(self.parent, text=text, relief=relief, bg=self.bg, fg=self.fg)
        lbl.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky="nesw")
    #
    def create_frame(self, relief=tk.GROOVE):
        frm = tk.Frame(self.parent, bg=self.bg, bd=1, relief=relief)
        frm.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky="nesw")
        return frm
    #
    def create_label_variable(self, label_container, relief=tk.SUNKEN):
        var_text = tk.IntVar()
        var_text.set(0)
        lbl = tk.Label(self.parent, text=var_text.get(), relief=relief)
        label_container.append(lbl)
        lbl.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky="nesw")
    #
    def create_button(self, text, command=None):
        if command == None:
            btn = tk.Button(self.parent, text=text, fg=self.fg, bg=self.bg)
        else:
            btn = tk.Button(self.parent, text=text, fg=self.fg, bg=self.bg, command=command)
        btn.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky="nesw")
    #
    def create_simple_button(self, text, bg_active="white", fg_active="black", command=None):
        if command == None:
            btn = tk.Button(self.parent, text=text, bg=self.bg, fg=self.fg, activebackground=bg_active,
                            activeforeground=fg_active, highlightbackground=self.bg, font="sans 10 bold")
        else:
            btn = tk.Button(self.parent, text=text, bg=self.bg, fg=self.fg, activebackground=bg_active,
                            activeforeground=fg_active, highlightbackground=self.bg,
                            highlightthickness=0, command=command, font="sans 10 bold")
        btn.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky="nesw")
        #
        return btn
    #
    def create_time_window_entries(self, times, part, command_start=None, command_end=None, relief=tk.GROOVE):
        #
        lbl_start = tk.Label(self.parent, text="Time Start", relief=relief)
        lbl_start.grid(row=self.row_id, column=self.column_id, sticky="nesw")
        lbl_end = tk.Label(self.parent, text="Time End", relief=relief)
        lbl_end.grid(row=self.row_id+1, column=self.column_id, sticky="nesw")
        #
        if part == "BG":
            self.t_start_bg = tk.StringVar()
            self.t_start_bg.set(times.iloc[0])
            self.entr_t_start_bg = tk.Entry(self.parent, textvariable=self.t_start_bg)
            self.entr_t_start_bg.grid(row=self.row_id, column=self.column_id+1, sticky="nesw")
            if command_start == None:
                pass
            else:
                self.entr_t_start_bg.bind("<Return>", command_start)
            self.t_end_bg = tk.StringVar()
            self.t_end_bg.set(times.iloc[-1])
            self.entr_t_end_bg = tk.Entry(self.parent, textvariable=self.t_end_bg)
            self.entr_t_end_bg.grid(row=self.row_id+1, column=self.column_id+1, sticky="nesw")
            if command_end == None:
                pass
            else:
                self.entr_t_end_bg.bind("<Return>", command_end)
            #
            return self.entr_t_start_bg, self.entr_t_end_bg
        elif part == "SIG":
            self.t_start_sig = tk.StringVar()
            self.t_start_sig.set(times.iloc[0])
            self.entr_t_start_sig = tk.Entry(self.parent, textvariable=self.t_start_sig)
            self.entr_t_start_sig.grid(row=self.row_id, column=self.column_id+1, sticky="nesw")
            if command_start == None:
                pass
            else:
                self.entr_t_start_sig.bind("<Return>", command_start)
            self.t_end_sig = tk.StringVar()
            self.t_end_sig.set(times.iloc[-1])
            self.entr_t_end_sig = tk.Entry(self.parent, textvariable=self.t_end_sig)
            self.entr_t_end_sig.grid(row=self.row_id+1, column=self.column_id+1, sticky="nesw")
            if command_end == None:
                pass
            else:
                self.entr_t_end_sig.bind("<Return>", command_end)
            #
            return self.entr_t_start_sig, self.entr_t_end_sig
        elif part == "MAT":
            self.t_start_mat = tk.StringVar()
            self.t_start_mat.set(times.iloc[0])
            self.entr_t_start_mat = tk.Entry(self.parent, textvariable=self.t_start_mat)
            self.entr_t_start_mat.grid(row=self.row_id, column=self.column_id+1, sticky="nesw")
            if command_start == None:
                pass
            else:
                self.entr_t_start_mat.bind("<Return>", command_start)
            self.t_end_mat = tk.StringVar()
            self.t_end_mat.set(times.iloc[-1])
            self.entr_t_end_mat = tk.Entry(self.parent, textvariable=self.t_end_mat)
            self.entr_t_end_mat.grid(row=self.row_id+1, column=self.column_id+1, sticky="nesw")
            if command_end == None:
                pass
            else:
                self.entr_t_end_mat.bind("<Return>", command_end)
            #
            return self.entr_t_start_mat, self.entr_t_end_mat
    #
    def create_option_times(self, part, times_seg, command=None):
        option_list = []
        if len(times_seg) == 0:
            option_list.append(["No Time Intervals"])
        else:
            for i in range(len(times_seg)):
                option_list.append([str(times_seg[i][0])+" - "+str(times_seg[i][1])])
        option_list = np.array(option_list)[:, 0]
        #
        if part == "BG":
            self.var_iw_bg = tk.StringVar()
            self.var_iw_bg.set("Select Time Interval")
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_bg, *option_list)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            else:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_bg, *option_list, command=command)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")
            #
            return self.var_iw_bg
        elif part == "MATR":
            self.var_iw_matr = tk.StringVar()
            self.var_iw_matr.set("Select Time Interval")
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_matr, *option_list)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            else:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_matr, *option_list, command=command)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")
            #
            return self.var_iw_matr
        elif part == "INCL":
            self.var_iw_incl = tk.StringVar()
            self.var_iw_incl.set("Select Time Interval")
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_incl, *option_list)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            else:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_incl, *option_list, command=command)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
            #
            return self.var_iw_incl
        elif part == "SIG":
            self.var_iw_sig = tk.StringVar()
            self.var_iw_sig.set("Select Time Interval")
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_sig, *option_list)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            else:
                opt_menu = tk.OptionMenu(self.parent, self.var_iw_sig, *option_list, command=command)
                opt_menu.config(bg=self.bg, activebackground=self.bg)
            opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
            #
            return self.var_iw_sig
    #
    def create_isotope_column(self, input_isotopes, relief=tk.GROOVE):
        i = 0
        try:
            for isotope in input_isotopes:
                lbl_isotope = tk.Label(self.parent, text=isotope, relief=relief)
                lbl_isotope.grid(row=self.row_id+i, column=self.column_id, sticky="nesw")
                i += 1
        except:
            for isotope in input_isotopes[:, 0]:
                lbl_isotope = tk.Label(self.parent, text=isotope, relief=relief)
                lbl_isotope.grid(row=self.row_id+i, column=self.column_id, sticky="nesw")
                i += 1
    #
    def create_signal_entries(self, var_sig_mu, entr_sig_mu, var_sig_std, entr_sig_std, input_isotopes):
        i = 0
        for isotope in input_isotopes[:, 0]:
            var_sig_mu.append([isotope, tk.StringVar()])
            var_sig_mu[i][1].set(0.0)
            entr_sig_mu.append([isotope, var_sig_mu[i][1],
                                      tk.Entry(self.parent, textvariable=var_sig_mu[i][1])])
            entr_sig_mu[i][2].grid(row=self.row_id+i, column=self.column_id, sticky="nesw")
            #
            var_sig_std.append([isotope, tk.StringVar()])
            var_sig_std[i][1].set(0.0)
            entr_sig_std.append([isotope, var_sig_std[i][1],
                                      tk.Entry(self.parent, textvariable=var_sig_std[i][1])])
            entr_sig_std[i][2].grid(row=self.row_id+i, column=self.column_id+1, sticky="nesw")
            #
            i += 1
    #
    def create_simple_entry(self, var, command=None, text_default=0.0):
        var.set(text_default)
        entry = tk.Entry(self.parent, textvariable=var, fg=self.fg, bg=self.bg, highlightthickness=0)
        entry.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                   sticky="nesw")
        if command != None:
            entry.bind("<Return>", command)
        #
        return entry
    #
    def create_simple_entries(self, command=None, text_default=0.0):
        var = tk.StringVar()
        var.set(text_default)
        entry = tk.Entry(self.parent, textvariable=var, fg=self.fg, bg=self.bg, highlightthickness=0)
        entry.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                   sticky="nesw")
        if command != None:
            entry.bind("<Return>", command)
        #
        return var, entry
    #
    def create_entries_column(self, var_mu, entr_mu, var_std, entr_std, input_isotopes):
        i = 0
        for isotope in input_isotopes[:, 0]:
            var_mu.append([isotope, tk.StringVar()])
            var_mu[i][1].set(0.0)
            entr_mu.append([isotope, var_mu[i][1],
                                      tk.Entry(self.parent, textvariable=var_mu[i][1])])
            entr_mu[i][2].grid(row=self.row_id+i, column=self.column_id, sticky="nesw")
            #
            var_std.append([isotope, tk.StringVar()])
            var_std[i][1].set(0.0)
            entr_std.append([isotope, var_std[i][1],
                                      tk.Entry(self.parent, textvariable=var_std[i][1])])
            entr_std[i][2].grid(row=self.row_id+i, column=self.column_id+1, sticky="nesw")
            #
            i += 1
    #
    def create_option_files(self, type_name, file_selected, file_type, var_file_default, n_isotopes, command=None):
        if type_name == "STD":
            var_file_std_indiv = []
            file_helper = ["All Standards"]
            for file in file_type:
                parts = file.split("/")
                file_helper.append(parts[-1])
            parts_actual = file_selected.split("/")
            option_list_files_std = np.array(file_helper)
            for i in range(n_isotopes):
                var_file_std_indiv.append(tk.StringVar())
                if file_selected in file_type:
                    var_file_std_indiv[i].set(parts_actual[-1])
                else:
                    var_file_std_indiv[i].set(option_list_files_std[1])
        elif type_name == "SMPL":
            var_file_smpl_indiv = []
            file_helper = ["All Samples"]
            for file in file_type:
                parts = file.split("/")
                file_helper.append(parts[-1])
            parts_actual = file_selected.split("/")
            option_list_files_smpl = np.array(file_helper)
            for i in range(n_isotopes):
                var_file_smpl_indiv.append(tk.StringVar())
                if file_selected in file_type:
                    var_file_smpl_indiv[i].set(parts_actual[-1])
                else:
                    var_file_smpl_indiv[i].set(option_list_files_smpl[1])
        #
        parts_actual = file_selected.split("/")
        if file_selected in file_type:
                var_file_default.set(parts_actual[-1])
        else:
            if type_name == "STD":
                var_file_default.set(option_list_files_std[1])
            elif type_name == "SMPL":
                var_file_default.set(option_list_files_smpl[1])
        #
        if type_name == "STD":
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, var_file_default, *option_list_files_std)
            else:
                opt_menu = tk.OptionMenu(self.parent, var_file_default, *option_list_files_std,
                                                  command=command)
            opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
            #
            return var_file_std_indiv, option_list_files_std
        elif type_name == "SMPL":
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, var_file_default, *option_list_files_smpl)
            else:
                opt_menu = tk.OptionMenu(self.parent, var_file_default, *option_list_files_smpl,
                                                  command=command)
            opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
            #
            return var_file_smpl_indiv, option_list_files_smpl
    #
    def create_option_files_column(self, var_file_indiv, option_list, n_isotopes, command=None):
        if command == None:
            for i in range(n_isotopes):
                opt_menu = tk.OptionMenu(self.parent, var_file_indiv[i], *option_list)
                opt_menu.grid(row=self.row_id+i, column=self.column_id, rowspan=1, columnspan=1, sticky="nesw")
        else:
            for i in range(n_isotopes):
                opt_menu = tk.OptionMenu(self.parent, var_file_indiv[i], *option_list, command=command)
                opt_menu.grid(row=self.row_id+i, column=self.column_id, rowspan=1, columnspan=1, sticky="nesw")
    #
    def create_radiobutton_column(self, var_rb, isotopes=None, list_data=None, command=None, relief=tk.FLAT):
        var_rb.set(0)
        try:
            n_isotopes = len(isotopes)
        except:
            n_isotopes = len(isotopes[:, 0])
        for i in range(n_isotopes):
            if command == None:
                if i == 0:
                    rb = tk.Radiobutton(self.parent, text="", variable=var_rb, value=0, relief=relief)
                else:
                    rb = tk.Radiobutton(self.parent, text="", variable=var_rb, value=i, relief=relief)
            else:
                rb = tk.Radiobutton(self.parent, text="", variable=var_rb, value=i, command=command, relief=relief)
            if self.n_rows == 1:
                rb.grid(row=self.row_id+i, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                        sticky="nesw")
            else:
                rb.grid(row=self.row_id+self.n_rows*i, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                        sticky="nesw")
    #
    def create_radiobutton(self, var_rb, value_rb, color_bg, relief=tk.FLAT, fg="black", command=None, text="",
                           font="sans 10 normal", sticky="nesw", anchor="w"):
        if value_rb == 0:
            var_rb.set(var_rb.get())
        if command == None:
            rb = tk.Radiobutton(
                self.parent, text=text, variable=var_rb, value=value_rb, bg=color_bg, fg=fg, activebackground=color_bg,
                relief=relief, selectcolor=color_bg, font=font, anchor=anchor)
        else:
            rb = tk.Radiobutton(
                self.parent, text=text, variable=var_rb, value=value_rb, bg=color_bg, fg=fg, activebackground=color_bg,
                relief=relief, selectcolor=color_bg, font=font, anchor=anchor, command=command)
        rb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                sticky=sticky)
        return rb
    #
    def create_simple_radiobutton(self, var_rb, value_rb, text, bg_active="white", fg_active="black", command=None,
                                  sticky="nesw", relief=tk.GROOVE, value_rb_default=0):
        if value_rb == value_rb_default:
            var_rb.set(value_rb_default)
        if command == None:
            rbtn = tk.Radiobutton(self.parent, text=text, variable=var_rb, value=value_rb, bg=self.bg, fg=self.fg,
                                activebackground=bg_active, activeforeground=fg_active, relief=relief,
                                  highlightthickness=0, font="sans 10 bold")
        else:
            rbtn = tk.Radiobutton(self.parent, text=text, variable=var_rb, value=value_rb, bg=self.bg, fg=self.fg,
                                activebackground=bg_active, activeforeground=fg_active, relief=relief,
                                  highlightthickness=0, command=command, font="sans 10 bold")
        rbtn.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                sticky=sticky)
        #
        return rbtn
    #
    def create_simple_checkbox(self, var_cb, text, command=None, set_sticky="nesw", own_color=False, var_anchor="w"):
        if own_color == False:
            color_rgb = matplotlib.colors.ColorConverter.to_rgb(self.bg)
            h, l, s = colorsys.rgb_to_hls(*color_rgb)
            color_light = matplotlib.colors.to_hex(colorsys.hls_to_rgb(h, min(1, l*1.5), s=s))
        else:
            color_light = self.fg
        if command == None:
            cb = tk.Checkbutton(self.parent, text=text, variable=var_cb, bg=self.bg, fg="black", anchor=var_anchor,
                                highlightthickness=0, bd=0, activebackground=self.bg, activeforeground=self.fg,
                                selectcolor="white")
        else:
            cb = tk.Checkbutton(self.parent, text=text, variable=var_cb, bg=self.bg, fg="black", anchor=var_anchor,
                                highlightthickness=0, bd=0, activebackground=self.bg, activeforeground=self.fg,
                                selectcolor="white", command=command)
        #
        if set_sticky == "":
            cb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns)
        else:
            cb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                    sticky=set_sticky)
        #
        return cb
    #
    def create_checkbox(self, var_cb, text, type_name="STD", relief=tk.GROOVE, command=None):
        if type_name == "STD":
            if command == None:
                cb = tk.Checkbutton(self.parent, text=text, variable=var_cb, bg=self.bg, relief=relief)
            else:
                cb = tk.Checkbutton(self.parent, text=text, variable=var_cb, bg=self.bg, relief=relief, command=command)
            cb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                    sticky="nesw")
        elif type_name == "SMPL":
            if command == None:
                cb = tk.Checkbutton(self.parent, text=text, variable=var_cb, bg=self.bg, relief=relief)
            else:
                cb = tk.Checkbutton(self.parent, text=text, variable=var_cb, bg=self.bg, relief=relief, command=command)
            cb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                    sticky="nesw")
        return cb
    #
    def create_option_srm(self, var_srm, text_set, command=None, option_list=None, fg_active="black", bg_active="white",
                          sort_list=True):
        #
        var_srm.set(text_set)
        if option_list == None:
            option_list_srm = np.array([
                ["NIST 606"], ["NIST 610"], ["NIST 610 (GeoReM)"], ["NIST 610 (Spandler)"], ["NIST 611"],
                ["NIST 611 (GeoReM)"], ["NIST 612"], ["NIST 612 (GeoReM)"], ["NIST 613"], ["NIST 613 (GeoReM)"],
                ["NIST 614"], ["NIST 614 (GeoReM)"], ["NIST 615"], ["NIST 615 (GeoReM)"], ["NIST 616"],
                ["NIST 616 (GeoReM)"], ["NIST 617"], ["NIST 617 (GeoReM)"], ["USGS BCR-2G (GeoReM)"],
                ["USGS GSD-1G (GeoReM)"], ["USGS GSE-1G (GeoReM)"], ["B6"], ["Durango Apatite"], ["Scapolite 17"],
                ["BAM-376"], ["BCR-2G"], ["BL-Q"], ["Br-Glass"], ["GSD-1G (GeoReM)"], ["GSE-1G (GeoReM)"], ["GSE-2G"],
                ["HAL-O"], ["K-Br"], ["MACS-3"], ["Po 724"], ["STDGL-2B2"]])[:, 0]
        else:
            option_list_srm = option_list

        if sort_list == True:
            option_list_srm.sort()
        #
        if command == None:
            opt_menu_srm = tk.OptionMenu(self.parent, var_srm, *option_list_srm)
        else:
            opt_menu_srm = tk.OptionMenu(self.parent, var_srm, *option_list_srm, command=command)
        opt_menu_srm.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
        opt_menu_srm.config(fg=self.fg, bg=self.bg, activebackground=self.bg, activeforeground=self.fg,
                            highlightthickness=0)
        opt_menu_srm["menu"].config(fg=self.fg, bg=self.bg, activeforeground=fg_active, activebackground=bg_active)
        #
        return opt_menu_srm
    #
    def create_option_mineral(self, var_min, text_set, command=None, option_list=None, fg_active="black", bg_active="white"):
        #
        var_min.set(text_set)
        if option_list == None:
            option_list_min = ["Quartz", "Calcite", "Fluorite", "Apatite-Cl", "Apatite-F", "Apatite-OH", "Forsterite",
                               "Fayalite", "Tephroite", "Albite", "Anorthite", "Orthoclase", "Microcline"]
        else:
            option_list_min = option_list
        option_list_min.sort()
        if command == None:
            opt_menu_min = tk.OptionMenu(self.parent, var_min, *option_list_min)
        else:
            opt_menu_min = tk.OptionMenu(self.parent, var_min, *option_list_min, command=command)
        opt_menu_min.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
        opt_menu_min.config(fg=self.fg, bg=self.bg, activebackground=self.bg, activeforeground=self.fg,
                            highlightthickness=0)
        opt_menu_min["menu"].config(fg=self.fg, bg=self.bg, activeforeground=fg_active, activebackground=bg_active)
        #
        return opt_menu_min
    #
    def create_option_isotope(self, var_iso, text_set, command=None, option_list=None, fg_active="black", bg_active="white"):
        var_iso.set(text_set)
        if option_list == None:
            option_list_iso = ["Si29"]
        else:
            option_list_iso = option_list
        if command == None:
            opt_menu_min = tk.OptionMenu(self.parent, var_iso, *option_list_iso)
        else:
            opt_menu_min = tk.OptionMenu(self.parent, var_iso, *option_list_iso, command=command)
        opt_menu_min.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")
        opt_menu_min.config(fg=self.fg, bg=self.bg, activebackground=self.bg, activeforeground=self.fg,
                            highlightthickness=0)
        opt_menu_min["menu"].config(fg=self.fg, bg=self.bg, activeforeground=fg_active, activebackground=bg_active)
        #
        return opt_menu_min
    #
    def create_option_menu(self, var_opt, text_set, command=None, option_list=None, fg_active="black", bg_active="white"):
        #
        var_opt.set(text_set)
        #
        if option_list == None:
            option_list_opt = ["Si29"]
        else:
            option_list_opt = option_list
        #
        if command == None:
            opt_menu = tk.OptionMenu(self.parent, var_opt, text_set, *option_list_opt)
        else:
            opt_menu = tk.OptionMenu(self.parent, var_opt, text_set, *option_list_opt, command=command)
        #
        opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")
        opt_menu.config(fg=self.fg, bg=self.bg, activebackground=self.bg, activeforeground=self.fg,
                        highlightthickness=0)
        opt_menu["menu"].config(fg=self.fg, bg=self.bg, activeforeground=fg_active, activebackground=bg_active)
        #
        return opt_menu
    #
    def create_option_is(self, var_is, var_is_default, isotopes, is_container=None, default_is=True, command=None):
        option_list_is = isotopes[:, 0]
        if default_is == True:
            var_is_default.set("Select Isotope")
            if command == None:
                opt_menu_is = tk.OptionMenu(self.parent, var_is_default, *option_list_is)
            else:
                opt_menu_is = tk.OptionMenu(self.parent, var_is_default, *option_list_is, command=command)
            opt_menu_is.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                             sticky="nesw")
        else:
            var_is.set("Select Isotope")
            if command == None:
                opt_menu_is = tk.OptionMenu(self.parent, var_is, *option_list_is)
            else:
                opt_menu_is = tk.OptionMenu(self.parent, var_is, *option_list_is, command=command)
            is_container.append(opt_menu_is)
            opt_menu_is.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                             sticky="nesw")
    #
    def create_option_is_column(self, is_container, isotopes, command=None):
        option_list_is = isotopes[:, 0]
        for i in range(len(isotopes[:, 0])):
            is_container.append(tk.StringVar())
            is_container[i].set("Select isotope")
            if command == None:
                opt_menu_is = tk.OptionMenu(self.parent, is_container[i], *option_list_is)
            else:
                opt_menu_is = tk.OptionMenu(self.parent, is_container[i], *option_list_is, command=lambda variable=is_container[i], index=i: Essentials(variable).change_option(index))
            opt_menu_is.grid(row=self.row_id+i, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                             sticky="nesw")
    #
    def create_option_srm_default(self, var_srm_default, found_srm, command=None, conc=False):
        option_list_srm = found_srm
        if conc == False:
            var_srm_default.set("Select SRM")
        else:
            var_srm_default.set(option_list_srm[0])
        if command == None:
            opt_menu_srm = tk.OptionMenu(self.parent, var_srm_default, *option_list_srm)
        else:
            opt_menu_srm = tk.OptionMenu(self.parent, var_srm_default, *option_list_srm, command=command)
        opt_menu_srm.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                         sticky="nesw")
    #
    def create_option_is_default(self, var_is_default, found_is, command=None):
        option_list_is = found_is
        var_is_default.set("Select SRM")
        if command == None:
            opt_menu_is = tk.OptionMenu(self.parent, var_is_default, *option_list_is)
        else:
            opt_menu_is = tk.OptionMenu(self.parent, var_is_default, *option_list_is, command=command)
        opt_menu_is.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                         sticky="nesw")
    #
    def create_option_srm_column(self, srm_container, found_srm, n_isotopes, command=None):
        option_list_srm = found_srm
        for i in range(n_isotopes):
            srm_container.append(tk.StringVar())
            srm_container[i].set("Select SRM")
            if command == None:
                opt_menu = tk.OptionMenu(self.parent, srm_container[i], *option_list_srm)
            else:
                opt_menu = tk.OptionMenu(self.parent, srm_container[i], *option_list_srm, command=lambda variable=srm_container[i], index=i: Essentials(variable).change_option(index))
            opt_menu.grid(row=self.row_id+i, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                             sticky="nesw")
    #
    def create_option_file(self, found_files, var_file, command=None):
        option_list = []
        for file in found_files:
            parts = file.split("/")
            option_list.append([parts[-1]])
        option_list_srm = option_list
        var_file.set("Select File")
        if command == None:
            opt_menu = tk.OptionMenu(self.parent, var_file, *option_list_srm)
        else:
            opt_menu = tk.OptionMenu(self.parent, var_file, *option_list_srm, command=command)
        opt_menu.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")
    #
    def create_simple_optionmenu(self, var_opt, var_default, var_list, fg_active=None, bg_active=None, command=None):
        var_opt.set(var_default)
        if command == None:
            opt_menu = tk.OptionMenu(self.parent, var_opt, *var_list)
        else:
            opt_menu = tk.OptionMenu(self.parent, var_opt, *var_list, command=command)
        #
        if fg_active == None:
            fg_active = self.fg
        if bg_active == None:
            bg_active == self.bg
        #
        opt_menu["menu"].config(fg=self.fg, bg=self.bg, activeforeground=fg_active, activebackground=bg_active)
        opt_menu.config(fg=self.fg, bg=self.bg, activeforeground=fg_active, activebackground=bg_active,
                        highlightthickness=0)
        #
        opt_menu.grid(
            row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns, sticky="nesw")
        #
        return opt_menu
    #
    def create_listbox(self, val_width, val_height):
        frame_lb = tk.Frame(self.parent, bg=self.bg)
        frame_lb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")
        #
        scrollbar_y = tk.Scrollbar(frame_lb, orient="vertical")
        scrollbar_x = tk.Scrollbar(frame_lb, orient="horizontal")
        listbox = tk.Listbox(frame_lb, bg=self.bg, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        #
        scrollbar_y.config(command=listbox.yview)
        scrollbar_x.config(command=listbox.xview)
        scrollbar_x.pack(side="bottom", fill="x", pady=0)
        listbox.pack(side="left", fill="both", padx=0, pady=0, expand=True)
        scrollbar_y.pack(side="right", fill="y", padx=0)
        frame_lb.columnconfigure(self.column_id, weight=1)
        frame_lb.rowconfigure(self.row_id, weight=1)
        #
        return listbox

    def create_simple_listbox2(self, include_scrb_x=True):
        frame_lb = tk.Frame(self.parent, bg=self.bg, relief=tk.FLAT)
        frame_lb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")

        scrollbar_y = tk.Scrollbar(frame_lb, orient="vertical")
        if include_scrb_x == True:
            scrollbar_x = tk.Scrollbar(frame_lb, orient="horizontal")
            listbox = tk.Listbox(
                frame_lb, fg=self.fg, bg=self.bg, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set,
                relief=tk.FLAT)
        else:
            listbox = tk.Listbox(frame_lb, fg=self.fg, bg=self.bg, yscrollcommand=scrollbar_y.set, relief=tk.FLAT)

        scrollbar_y.config(command=listbox.yview)
        if include_scrb_x == True:
            scrollbar_x.config(command=listbox.xview)
            scrollbar_x.pack(side="bottom", fill="x", pady=0)

        listbox.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        scrollbar_y.pack(side="right", fill="y", padx=0)
        frame_lb.columnconfigure(self.column_id, weight=1)
        frame_lb.rowconfigure(self.row_id, weight=1)

        return listbox

    def create_simple_listbox(self, include_scrb_x=True):
        frame_lb = tk.Frame(self.parent, bg=self.bg, relief=tk.FLAT)
        frame_lb.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                      sticky="nesw")

        frame_lb2 = tk.Label(self.parent, text="", bg=self.bg, relief=tk.RIDGE)
        frame_lb2.grid(row=self.row_id + self.n_rows - 1, column=self.column_id + self.n_columns - 1, rowspan=1,
                       columnspan=1, sticky="nesw")

        scrollbar_y = ttk.Scrollbar(self.parent, orient="vertical")

        #scrollbar_y = tk.Scrollbar(self.parent, orient="vertical")
        if include_scrb_x == True:
            scrollbar_x = ttk.Scrollbar(self.parent, orient="horizontal")
            listbox = tk.Listbox(
                self.parent, fg=self.fg, bg=self.bg, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set,
                relief=tk.FLAT, highlightthickness=0)
        else:
            listbox = tk.Listbox(self.parent, fg=self.fg, bg=self.bg, yscrollcommand=scrollbar_y.set, relief=tk.FLAT,
                                 highlightthickness=0)

        scrollbar_y.config(command=listbox.yview)

        if include_scrb_x == True:
            scrollbar_x.config(command=listbox.xview)
            #scrollbar_x.pack(side="bottom", fill="x", pady=0)

            scrollbar_x.grid(row=self.row_id + self.n_rows - 1, column=self.column_id, rowspan=1,
                             columnspan=self.n_columns - 1, sticky="ew")
        listbox.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows - 1, columnspan=self.n_columns - 1,
                     sticky="nesw", padx=10, pady=10)
        scrollbar_y.grid(row=self.row_id, column=self.column_id + self.n_columns - 1, rowspan=self.n_rows - 1,
                         columnspan=1, sticky="ns")
        #listbox.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        #scrollbar_y.pack(side="right", fill="y", padx=0)
        frame_lb.columnconfigure(self.column_id, weight=1)
        frame_lb.rowconfigure(self.row_id, weight=1)

        return listbox

    def create_simple_listbox_grid(self, include_scrb_x=True):
        scrollbar_y = tk.Scrollbar(self.parent, orient="vertical")
        if include_scrb_x == True:
            scrollbar_x = tk.Scrollbar(self.parent, orient="horizontal")
            listbox = tk.Listbox(
                self.parent, bg=self.bg, fg=self.fg, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        else:
            listbox = tk.Listbox(self.parent, bg=self.bg, fg=self.fg, yscrollcommand=scrollbar_y.set)
        #
        scrollbar_y.config(command=listbox.yview)
        if include_scrb_x == True:
            scrollbar_x.config(command=listbox.xview)
            scrollbar_x.grid(row=self.row_id+self.n_rows-1, column=self.column_id, rowspan=1, columnspan=self.n_columns,
                             sticky="ew")
            listbox.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows-1, columnspan=self.n_columns-1,
                         sticky="nesw")
        else:
            listbox.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns - 1,
                         sticky="nesw")
        scrollbar_y.grid(row=self.row_id, column=self.column_id+self.n_columns-1, rowspan=self.n_rows, columnspan=1,
                         sticky="ns")
        #
        if include_scrb_x == True:
            return listbox, scrollbar_x, scrollbar_y
        else:
            return listbox, scrollbar_y
    #
    def create_treeview(self, n_categories=2, text_1="Ratio", text_2="\u03BC", width_1 = 90, width_2 = 90, text_n=[],
                        width_n=[], individual=False):
        ttk.Style().configure("Treeview", background=self.bg, foreground=self.fg, fieldbackground=self.bg)
        style = ttk.Style()
        style.configure("Treeview.Heading", background=self.bg, pressed_color=self.bg,
                        highlight_color=self.bg, foreground=self.fg)

        if n_categories == 2 and individual == False:
            columns = ("#1", "#2")
            treeview = ttk.Treeview(self.parent, columns=columns, show="headings")
            treeview.heading("#1", text=text_1)
            treeview.column("#1", minwidth=0, width=width_1, stretch=tk.NO, anchor=tk.CENTER)
            treeview.heading("#2", text=text_2)
            treeview.column("#2", minwidth=0, width=width_2, stretch=tk.YES, anchor=tk.CENTER)
            treeview.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")

        if n_categories > 1 and individual == True:
            columns = []
            for n in range(n_categories):
                var_i = "#" + str(n + 1)
                columns.append(var_i)

            treeview = ttk.Treeview(self.parent, columns=columns, show="headings")

            for index, element in enumerate(columns):
                treeview.heading(element, text=text_n[index], anchor=tk.W)
                treeview.column(element, minwidth=0, width=width_n[index], stretch=tk.NO, anchor=tk.W)

            treeview.grid(row=self.row_id, column=self.column_id, rowspan=self.n_rows, columnspan=self.n_columns,
                          sticky="nesw")

        return treeview