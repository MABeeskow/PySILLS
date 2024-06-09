#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		fluid_inclusions.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		22.08.2022

#-----------------------------------------------

## MODULES
import re, datetime
import tkinter as tk
import numpy as np
from modules.data import Data
from modules.gui_elements import SimpleElements as SE
from modules.essential_functions import EssentialsSRM as ESRM
from plugins.fi_method_matrix_only_tracer import Method as MatrixOnlyTracer
#
class FluidInclusions:
    #
    def __init__(self, parent=None, filename=None, list_isotopes=None, srm_actual=None, container_var=None,
                 container_lists=None, container_measurements=None, container_files=None, xi_std_time=None,
                 container_results=None):
        #
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
        #
        self.parent = parent
        self.filename = filename
        self.list_isotopes = list_isotopes
        self.srm_actual = srm_actual
        self.container_var = container_var
        self.container_lists = container_lists
        self.container_measurements = container_measurements
        self.container_files = container_files
        self.xi_std_time = xi_std_time
        self.container_results = container_results
    #
    def create_salt_correction_window(self, gui_elements):
        ## Window Settings
        window_salt = tk.Toplevel(self.parent)
        window_salt.title("Salt Correction")
        window_salt.geometry("600x400+0+0")
        window_salt.resizable(False, False)
        window_salt["bg"] = self.green_light
        #
        window_width = 600
        window_heigth = 400
        row_min = 25
        n_rows = int(window_heigth / row_min)
        column_min = 20
        n_columns = int(window_width / column_min)
        #
        for x in range(n_columns):
            tk.Grid.columnconfigure(window_salt, x, weight=1)
        for y in range(n_rows):
            tk.Grid.rowconfigure(window_salt, y, weight=1)
        #
        # Rows
        for i in range(0, n_rows):
            window_salt.grid_rowconfigure(i, minsize=row_min)
        # Columns
        for i in range(0, n_columns):
            window_salt.grid_columnconfigure(i, minsize=column_min)
        #
        ## Labels
        lbl_01 = SE(
            parent=window_salt, row_id=0, column_id=0, n_rows=1, n_columns=10, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Major components: H2O + ...", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_02 = SE(
            parent=window_salt, row_id=1, column_id=0, n_rows=1, n_columns=6, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Salt", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_03 = SE(
            parent=window_salt, row_id=1, column_id=6, n_rows=1, n_columns=4, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Selection", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_04 = SE(
            parent=window_salt, row_id=1, column_id=6, n_rows=1, n_columns=4, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Selection", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_05 = SE(
            parent=window_salt, row_id=0, column_id=10, n_rows=1, n_columns=8, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="NaCl equivalents", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_06 = SE(
            parent=window_salt, row_id=1, column_id=10, n_rows=1, n_columns=4, fg=self.green_light,
            bg=self.green_medium).create_simple_label(
            text="Salinity", relief=tk.GROOVE, fontsize="sans 10 bold")
        #
        gui_elements["salt_correction"]["Label"]["General"].extend([lbl_01, lbl_02, lbl_03, lbl_04, lbl_05, lbl_06])
        #
        list_salts = ["NaCl", "KCl", "MgCl2", "CaCl2", "Na2SO4", "K2SO4", "MgSO4", "CaSO4"]
        for index, salt in enumerate(list_salts):
            lbl_salt = SE(
                parent=window_salt, row_id=2 + index, column_id=0, n_rows=1, n_columns=6, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text=salt, relief=tk.GROOVE, fontsize="sans 10 bold")
            #
            ## Checkboxes
            self.container_var["salt_correction"]["Checkboxes"][salt] = tk.IntVar()
            if salt == "NaCl":
                self.container_var["salt_correction"]["Checkboxes"][salt].set(1)
            cb_salt = SE(
                parent=window_salt, row_id=2 + index, column_id=6, n_rows=1, n_columns=4, fg=self.red_dark,
                bg=self.green_medium).create_simple_checkbox(
                var_cb=self.container_var["salt_correction"]["Checkboxes"][salt],
                text="", set_sticky="news", own_color=True)
            #
            gui_elements["salt_correction"]["Label"]["General"].append(lbl_salt)
            gui_elements["salt_correction"]["Checkbox"]["General"].append(cb_salt)
        #
        ## Treeview
        lb_results = SE(
            parent=window_salt, row_id=2, column_id=10, n_rows=8, n_columns=8, fg=self.green_dark,
            bg=self.red_light).create_treeview(text_1="Element", text_2="w (ppm)", width_1=75, width_2=75)
        #
        gui_elements["salt_correction"]["Listbox"]["General"].append(lb_results)
        #
        ## Entry
        if self.container_var["salt_correction"]["Salinity"].get() != "Set salinity":
            var_text = self.container_var["salt_correction"]["Salinity"].get()
        else:
            var_text = "Set salinity"
        entr_salinity = SE(
            parent=window_salt, row_id=1, column_id=14, n_rows=1, n_columns=4,
            fg=self.green_light, bg=self.green_dark).create_simple_entry(
            var=self.container_var["salt_correction"]["Salinity"], text_default=var_text,
            command=lambda event, var_sal=self.container_var["salt_correction"]["Salinity"], listbox=lb_results:
            self.calculate_salt_concentrations(var_sal, listbox, event))
        #
        gui_elements["salt_correction"]["Entry"]["General"].append(entr_salinity)
        #
    def create_method_settings_window(self, gui_elements, var_method):
        ## Window Settings
        window_method = tk.Toplevel(self.parent)
        window_method.title("Quantification Method Settings")
        window_method.geometry("400x400+0+0")
        window_method.resizable(False, False)
        window_method["bg"] = self.green_light
        #
        window_width = 400
        window_heigth = 400
        row_min = 25
        n_rows = int(window_heigth / row_min)
        column_min = 20
        n_columns = int(window_width / column_min)
        #
        for x in range(n_columns):
            tk.Grid.columnconfigure(window_method, x, weight=1)
        for y in range(n_rows):
            tk.Grid.rowconfigure(window_method, y, weight=1)
        #
        # Rows
        for i in range(0, n_rows):
            window_method.grid_rowconfigure(i, minsize=row_min)
        # Columns
        for i in range(0, n_columns):
            window_method.grid_columnconfigure(i, minsize=column_min)
        #
        ## Labels
        lbl_01 = SE(
            parent=window_method, row_id=0, column_id=0, n_rows=1, n_columns=14, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text=" Primary Internal Standard", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_02 = SE(
            parent=window_method, row_id=1, column_id=0, n_rows=1, n_columns=8, fg=self.green_light,
            bg=self.green_medium).create_simple_label(
            text="Standard Files", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_03 = SE(
            parent=window_method, row_id=2, column_id=0, n_rows=1, n_columns=8, fg=self.green_light,
            bg=self.green_medium).create_simple_label(
            text="Sample Files", relief=tk.GROOVE, fontsize="sans 10 bold")
        lbl_04 = SE(
            parent=window_method, row_id=3, column_id=0, n_rows=1, n_columns=14, fg=self.green_light,
            bg=self.green_dark).create_simple_label(
            text="Settings: " + str(var_method.get()), relief=tk.GROOVE, fontsize="sans 10 bold")
        #
        gui_elements["fi_method_setting"]["Label"]["General"].extend([lbl_01, lbl_02, lbl_03, lbl_04])
        #
        ## Option Menus
        if self.container_var["IS"]["Default STD"].get() != "Select IS":
            var_text = self.container_var["IS"]["Default STD"].get()
        else:
            var_text = "Select IS"
        #
        self.opt_is_std_def = SE(
            parent=window_method, row_id=1, column_id=8, n_rows=1, n_columns=6,
            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
            var_iso=self.container_var["IS"]["Default STD"],
            option_list=self.container_lists["ISOTOPES"], text_set=var_text,
            fg_active=self.green_dark, bg_active=self.red_dark,
            command=lambda var_is=self.container_var["IS"]["Default STD"], var_filetype="STD":
            self.change_is_def(var_is, var_filetype))
        #
        if self.container_var["IS"]["Default SMPL"].get() != "Select IS":
            var_text = self.container_var["IS"]["Default SMPL"].get()
        else:
            var_text = "Select IS"
        #
        self.opt_is_smpl_def = SE(
            parent=window_method, row_id=2, column_id=8, n_rows=1, n_columns=6,
            fg=self.green_dark, bg=self.green_medium).create_option_isotope(
            var_iso=self.container_var["IS"]["Default SMPL"],
            option_list=self.container_lists["ISOTOPES"], text_set=var_text,
            fg_active=self.green_dark, bg_active=self.red_dark,
            command=lambda var_is=self.container_var["IS"]["Default SMPL"], var_filetype="SMPL":
            self.change_is_def(var_is, var_filetype))
        #
        gui_elements["fi_method_setting"]["Option Menu"]["General"].extend([self.opt_is_std_def, self.opt_is_smpl_def])
        #
        if var_method.get() == "Matrix Only Tracer":
            lbl_05 = SE(
                parent=window_method, row_id=4, column_id=0, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="Host-Only Isotope", relief=tk.GROOVE, fontsize="sans 10 bold")
            self.opt_isotope = SE(
                parent=window_method, row_id=4, column_id=8, n_rows=1, n_columns=6,
                fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["fi_setting"]["Host Only"],
                option_list=self.container_lists["ISOTOPES"], text_set="Select Isotope",
                fg_active=self.green_dark, bg_active=self.red_dark)
        elif var_method.get() == "2nd Internal Standard":
            lbl_05 = SE(
                parent=window_method, row_id=4, column_id=0, n_rows=1, n_columns=8, fg=self.green_light,
                bg=self.green_medium).create_simple_label(
                text="2nd Internal Standard", relief=tk.GROOVE, fontsize="sans 10 bold")
            self.opt_isotope = SE(
                parent=window_method, row_id=4, column_id=8, n_rows=1, n_columns=6,
                fg=self.green_dark, bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["fi_setting"]["2nd Internal"],
                option_list=self.container_lists["ISOTOPES"], text_set="Select Isotope",
                fg_active=self.green_dark, bg_active=self.red_dark)
            entry_conc = SE(
                parent=window_method, row_id=5, column_id=8, n_rows=1, n_columns=6,
                fg=self.green_light, bg=self.green_dark).create_simple_entry(
                var=self.container_var["fi_setting"]["2nd Internal Concentration"], text_default="2nd IS Concentration",
                command=lambda event, var_entr=self.container_var["fi_setting"]["2nd Internal Concentration"]:
                self.set_entry_value(var_entr, event))
            gui_elements["fi_method_setting"]["Entry"]["General"].append(entry_conc)
        #
        gui_elements["fi_method_setting"]["Label"]["General"].append(lbl_05)
        gui_elements["fi_method_setting"]["Option Menu"]["General"].append(self.opt_isotope)
        #
    #
    def set_entry_value(self, var_entr, event):
        var_entr.set(var_entr.get())
    #
    def calculate_salt_concentrations(self, var_sal, listbox, event):
        concentration = float(var_sal.get())/100
        helper = {}
        list_elements = ["H", "O", "Na", "Cl"]
        water_chemistry = {"H": 0.1119, "O": 0.8881}
        halite_chemistry = {"Na": 0.3934, "Cl": 0.6066}
        for element in list_elements:
            if element not in helper:
                helper[element] = 0
            if element in water_chemistry:
                helper[element] += (1 - concentration)*water_chemistry[element]
            if element in halite_chemistry:
                helper[element] += concentration*halite_chemistry[element]
        #
        try:
            for row in listbox.get_children():
                listbox.delete(row)
        except:
            pass
        #
        for key, value in helper.items():
            listbox.insert("", tk.END, values=[str(key), int(value*1000000)])
            self.container_var["salt_correction"]["Concentration"][str(key)] = int(value*1000000)
        #
        ## TESTING
        # print("TESTING: Salt Concentration")
        # for key, value in helper.items():
        #     print(key, int(value*1000000), "ppm")
        #     print(key, round(value*100, 2), "%")
    #
    def create_datareduction_window(self, container_elements, gui_elements, list_srm):
        ## Cleaning
        categories = ["SRM", "ma_setting", "plotting", "PSE", "fi_setting"]
        for category in categories:
            if len(container_elements[category]["Label"]) > 0:
                for item in container_elements[category]["Label"]:
                    item.grid_remove()
            if len(container_elements[category]["Button"]) > 0:
                for item in container_elements[category]["Button"]:
                    item.grid_remove()
            if len(container_elements[category]["Option Menu"]) > 0:
                for item in container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(container_elements[category]["Entry"]) > 0:
                for item in container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(container_elements[category]["Frame"]) > 0:
                for item in container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(container_elements[category]["Radiobutton"]) > 0:
                for item in container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(container_elements[category]["Checkbox"]) > 0:
                for item in container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(container_elements[category]["Listbox"]) > 0:
                for item in container_elements[category]["Listbox"]:
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
            for lbl_item in container_elements["fi_datareduction"]["Label"]:
                lbl_item.grid()
            for btn_item in container_elements["fi_datareduction"]["Button"]:
                btn_item.grid()
            for optmen_item in container_elements["fi_datareduction"]["Option Menu"]:
                optmen_item.grid()
            for entr_item in container_elements["fi_datareduction"]["Entry"]:
                entr_item.grid()
            for entr_item in container_elements["fi_datareduction"]["Frame"]:
                entr_item.grid()
            for rb_item in container_elements["fi_datareduction"]["Radiobutton"]:
                rb_item.grid()
        except:
            print("Error! Reconstruction 'Data Reduction' failed!")
        #
        self.container_lists["SRM"].clear()
        self.container_lists["IS"].clear()
        self.container_lists["ID"].clear()
        self.container_lists["ID Files"].clear()
        list_files = ["All Standard Files", "All Sample Files"]
        list_methods = ["Matrix-only Tracer", "2nd Internal Standard"]
        #
        for key, value in self.container_files["SRM"].items():
            if value.get() not in self.container_lists["SRM"] and value.get() in list_srm:
                self.container_lists["SRM"].append(value.get())
                self.fill_srm_values(var_srm=value.get())
        #
        for file_std in self.container_lists["STD"]["Short"]:
            var_is = self.container_files["STD"][file_std]["IS"]
            if var_is.get() not in self.container_lists["IS"] and var_is.get() in self.container_lists["ISOTOPES"]:
                self.container_lists["IS"].append(var_is.get())
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            var_is = self.container_files["SMPL"][file_smpl]["IS"]
            if var_is.get() not in self.container_lists["IS"] and var_is.get() in self.container_lists["ISOTOPES"]:
                self.container_lists["IS"].append(var_is.get())
        #
        # for filename, item in self.container_files["STD"].items():
        #     if item["ID"].get() not in self.container_lists["ID"]:
        #         self.container_lists["ID"].append(item["ID"].get())
        #         self.container_lists["ID Files"][item["ID"].get()] = [filename]
        #         list_files.append(str(item["ID"].get()) + " Files")
        #     elif item["ID"].get() in self.container_lists["ID"] and item["ID"].get() in self.container_lists[
        #         "ID Files"]:
        #         self.container_lists["ID Files"][item["ID"].get()].append(filename)
        for filename, item in self.container_files["SMPL"].items():
            if item["ID"].get() not in self.container_lists["ID"]:
                self.container_lists["ID"].append(item["ID"].get())
                self.container_lists["ID Files"][item["ID"].get()] = [filename]
                list_files.append(str(item["ID"].get()) + " Files")
            elif item["ID"].get() in self.container_lists["ID"] and item["ID"].get() in self.container_lists[
                "ID Files"]:
                self.container_lists["ID Files"][item["ID"].get()].append(filename)
        #
        ## VARIABLES
        self.container_var["fi_datareduction"]["Radiobutton"] = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
        #
        ## LABELS
        if len(container_elements["fi_datareduction"]["Label"]) == 0:
            lbl_01 = SE(
                parent=self.parent, row_id=0, column_id=21, n_rows=2, n_columns=9, fg=self.green_light,
                bg=self.green_dark).create_simple_label(
                text="General Settings", relief=tk.GROOVE, fontsize="sans 10 bold")
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
            container_elements["fi_datareduction"]["Label"].extend(
                [lbl_01, lbl_02, lbl_03, lbl_03a, lbl_03b, lbl_04, lbl_04a, lbl_04b, lbl_05, lbl_05a, lbl_05b,
                 lbl_06,
                 lbl_06a, lbl_06b, lbl_07, lbl_07a, lbl_07b])
            gui_elements["fi_datareduction"]["Label"]["General"].append(lbl_01)
            gui_elements["fi_datareduction"]["Label"]["Specific"].extend(
                [lbl_02, lbl_03, lbl_03a, lbl_03b, lbl_04, lbl_04a, lbl_04b, lbl_05, lbl_05a, lbl_05b, lbl_06,
                 lbl_06a, lbl_06b, lbl_07, lbl_07a, lbl_07b])
            #
            for index, isotope in enumerate(self.list_isotopes):
                ## LABELS
                lbl_isotope = SE(
                    parent=self.parent, row_id=2 + index, column_id=31, n_rows=1, n_columns=3, fg=self.green_light,
                    bg=self.green_medium).create_simple_label(
                    text=isotope, relief=tk.GROOVE, fontsize="sans 10 bold")
                #
                container_elements["fi_datareduction"]["Label"].append(lbl_isotope)
                gui_elements["fi_datareduction"]["Label"]["Specific"].append(lbl_isotope)
                #
                ## ENTRIES
                self.container_var["fi_datareduction"][isotope] = [
                    tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(),
                    tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
                width_sum = 29
                for index_02, var_entr in enumerate(self.container_var["fi_datareduction"][isotope]):
                    if (index_02 % 2) == 0:
                        width = 5
                        width_col = 6
                    else:
                        width = 6
                        width_col = 5
                    width_sum += width
                    entr_iso = SE(
                        parent=self.parent, row_id=2 + index, column_id=width_sum, n_rows=1, n_columns=width_col,
                        fg=self.green_light, bg=self.green_dark).create_simple_entry(
                        var=var_entr, text_default="0.0")
                    #
                    container_elements["fi_datareduction"]["Entry"].append(entr_iso)
                    gui_elements["fi_datareduction"]["Entry"]["Specific"].append(entr_iso)
            #
            ## OPTION MENUS
            self.container_var["fi_datareduction"]["Option SRM"] = tk.StringVar()
            self.container_var["fi_datareduction"]["Option IS"] = tk.StringVar()
            self.container_var["fi_datareduction"]["Option File"] = tk.StringVar()
            #self.container_var["fi_datareduction"]["Quantification Method"] = tk.StringVar()
            opt_menu_srm = SE(
                parent=self.parent, row_id=2, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_srm(
                var_srm=self.container_var["fi_datareduction"]["Option SRM"], text_set=self.container_lists["SRM"][0],
                fg_active=self.green_dark, bg_active=self.red_dark, option_list=self.container_lists["SRM"])
            opt_menu_is = SE(
                parent=self.parent, row_id=3, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["fi_datareduction"]["Option IS"], option_list=self.container_lists["IS"],
                text_set=self.container_lists["IS"][0], fg_active=self.green_dark, bg_active=self.red_dark)
            opt_menu_file = SE(
                parent=self.parent, row_id=4, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_option_isotope(
                var_iso=self.container_var["fi_datareduction"]["Option File"],
                option_list=list_files, text_set="Select File Type", fg_active=self.green_dark,
                bg_active=self.red_dark,
                command=lambda filetype=self.container_var["fi_datareduction"]["Option File"],
                               datatype=self.container_var["fi_datareduction"]["Radiobutton"][0]:
                self.datareduction_fi(filetype, datatype))
            # opt_menu_method = SE(
            #     parent=self.parent, row_id=5, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
            #     bg=self.green_medium).create_option_isotope(
            #     var_iso=self.container_var["fi_datareduction"]["Quantification Method"],
            #     option_list=list_methods, text_set=self.container_var["fi_setting"]["Method"].get(),
            #     fg_active=self.green_dark, bg_active=self.red_dark,
            #     command=lambda var_opt=self.container_var["fi_datareduction"]["Quantification Method"]:
            #     self.select_method(var_opt))
            #
            container_elements["fi_datareduction"]["Option Menu"].extend(
                [opt_menu_srm, opt_menu_is, opt_menu_file])
            #
            ## RADIOBUTTONS
            rb_01 = SE(
                parent=self.parent, row_id=6, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["fi_datareduction"]["Radiobutton"][2], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Host Mineral", sticky="nesw", relief=tk.GROOVE)
            rb_02 = SE(
                parent=self.parent, row_id=7, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["fi_datareduction"]["Radiobutton"][2], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Fluid Inclusion", sticky="nesw", relief=tk.GROOVE)
            rb_03 = SE(
                parent=self.parent, row_id=8, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["fi_datareduction"]["Radiobutton"][0], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Raw Data", sticky="nesw", relief=tk.GROOVE)
            rb_04 = SE(
                parent=self.parent, row_id=9, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.yellow_dark).create_radiobutton(
                var_rb=self.container_var["fi_datareduction"]["Radiobutton"][0], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Smoothed Data", sticky="nesw", relief=tk.GROOVE)
            rb_05 = SE(
                parent=self.parent, row_id=10, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["fi_datareduction"]["Radiobutton"][1], value_rb=0, color_bg=self.green_medium,
                fg=self.green_light, text="Show Results", sticky="nesw", relief=tk.GROOVE)
            rb_06 = SE(
                parent=self.parent, row_id=11, column_id=21, n_rows=1, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_radiobutton(
                var_rb=self.container_var["fi_datareduction"]["Radiobutton"][1], value_rb=1, color_bg=self.green_medium,
                fg=self.green_light, text="Show Drift Correction", sticky="nesw", relief=tk.GROOVE)
            #
            container_elements["fi_datareduction"]["Radiobutton"].extend([rb_01, rb_02, rb_03, rb_04, rb_05, rb_06])
            #
            ## BUTTONS
            btn_01 = SE(
                parent=self.parent, row_id=12, column_id=21, n_rows=2, n_columns=9, fg=self.green_dark,
                bg=self.green_medium).create_simple_button(
                text="Quantification Method\n Settings", bg_active=self.green_dark, fg_active=self.green_light)
            btn_02 = SE(
                parent=self.parent, row_id=15, column_id=21, n_rows=2, n_columns=9, fg=self.green_dark,
                bg=self.red_dark).create_simple_button(
                text="Export Calculation Report", bg_active=self.green_dark, fg_active=self.green_light)
            #
            container_elements["fi_datareduction"]["Button"].extend([btn_01, btn_02])
            #
        return container_elements, gui_elements, self.container_var, self.container_lists, self.container_files
        #
    def create_dataexploration_window(self, container_elements):
        ## Cleaning
        categories = ["SRM", "ma_setting", "plotting", "PSE", "fi_setting", "fi_datareduction"]
        for category in categories:
            if len(container_elements[category]["Label"]) > 0:
                for item in container_elements[category]["Label"]:
                    item.grid_remove()
            if len(container_elements[category]["Button"]) > 0:
                for item in container_elements[category]["Button"]:
                    item.grid_remove()
            if len(container_elements[category]["Option Menu"]) > 0:
                for item in container_elements[category]["Option Menu"]:
                    item.grid_remove()
            if len(container_elements[category]["Entry"]) > 0:
                for item in container_elements[category]["Entry"]:
                    item.grid_remove()
            if len(container_elements[category]["Frame"]) > 0:
                for item in container_elements[category]["Frame"]:
                    item.grid_remove()
            if len(container_elements[category]["Radiobutton"]) > 0:
                for item in container_elements[category]["Radiobutton"]:
                    item.grid_remove()
            if len(container_elements[category]["Checkbox"]) > 0:
                for item in container_elements[category]["Checkbox"]:
                    item.grid_remove()
            if len(container_elements[category]["Listbox"]) > 0:
                for item in container_elements[category]["Listbox"]:
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
            for lbl_item in container_elements["fi_dataexploration"]["Label"]:
                lbl_item.grid()
            for btn_item in container_elements["fi_dataexploration"]["Button"]:
                btn_item.grid()
            for optmen_item in container_elements["fi_dataexploration"]["Option Menu"]:
                optmen_item.grid()
            for entr_item in container_elements["fi_dataexploration"]["Entry"]:
                entr_item.grid()
            for entr_item in container_elements["fi_dataexploration"]["Frame"]:
                entr_item.grid()
            for rb_item in container_elements["fi_dataexploration"]["Radiobutton"]:
                rb_item.grid()
        except:
            print("Error! Reconstruction 'Data Exploration' failed!")
        #
        return container_elements
    #
    def fill_srm_values(self, var_srm):
        if var_srm not in self.srm_actual:
            self.srm_actual[var_srm] = {}
            ESRM().place_srm_values(srm_name=var_srm, srm_dict=self.srm_actual)
    #
    def datareduction_fi(self, filetype, datatype=None):
        #
        if datatype == None:
            var_datatype = self.container_var["fi_datareduction"]["Radiobutton"][0].get()
        else:
            var_datatype = datatype
        #
        if self.container_var["fi_datareduction"]["Radiobutton"][0].get() == 0:
            var_datatype = "RAW"
        elif self.container_var["fi_datareduction"]["Radiobutton"][0].get() == 1:
            var_datatype = "SMOOTHED"
        #
        if self.container_var["fi_datareduction"]["Radiobutton"][2].get() == 0:
            var_mode = "Host Mineral"
            var_ho = self.container_var["fi_setting"]["Host Only"].get()
        elif self.container_var["fi_datareduction"]["Radiobutton"][2].get() == 1:
            var_mode = "Fluid Inclusion"
            var_ho = self.container_var["fi_setting"]["Host Only"].get()
        #
        var_is = self.container_var["fi_datareduction"]["Option IS"].get()
        key_element = re.search("(\D+)(\d+)", var_is)
        var_is_element = key_element.group(1)
        key_host_element = re.search("(\D+)(\d+)", var_ho)
        var_ho_element = key_host_element.group(1)
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
        elif filetype == "All Standard Files":
            var_filetype["STD"] += len(self.container_lists["STD"]["Short"])
            var_filetype["Result"] = "STD"
        elif filetype == "All Sample Files":
            var_filetype["SMPL"] += len(self.container_lists["SMPL"]["Short"])
            var_filetype["Result"] = "SMPL"
        #
        self.intensity_bg, self.intensity_mat, self.intensity_incl, self.intensity_mixed = self.calculate_mixed_signal(
            var_datatype=var_datatype)
        #
        if var_mode == "Host Mineral":
            ## Intensity Data
            intensity = self.get_intensity_data(
                var_filetype=var_filetype["Result"], var_datatype=var_datatype, var_mode=var_mode)
            intensity_host = intensity["MATRIX CORRECTED"]
            #
            ## Intensity Ratio Calculation
            intensity_ratio = self.calculate_intensity_ratio_host(var_is=var_is, intensity=intensity)
            #
            ## Sensitivity Calculation
            sensitivity = self.calculate_sensitivity_host(
                var_is=var_is, var_is_element=var_is_element, var_filetype=var_filetype["Result"],
                var_datatype=var_datatype)
            #
            if self.container_var["fi_setting"]["Host Setup Selection"].get() == 1:
                var_oxide = self.container_var["fi_setting"]["Oxide"].get()
                concentration_oxide = self.calculate_concentration_oxides(
                    var_oxide=var_oxide)
                self.concentration_ho_host = concentration_oxide[var_oxide][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host*np.mean(intensity_host[var_is])*np.mean(
                    sensitivity[var_ho]))/np.mean(intensity_host[var_ho])
            elif self.container_var["fi_setting"]["Host Setup Selection"].get() == 2:
                var_sulfide = self.container_var["fi_setting"]["Sulfide"].get()
                concentration_sulfide = self.calculate_concentration_sulfides(
                    var_sulfide=self.container_var["fi_setting"]["Sulfide"])
                self.concentration_ho_host = concentration_sulfide[var_sulfide][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_is])) / np.mean(intensity_host[var_ho])
            elif self.container_var["fi_setting"]["Host Setup Selection"].get() == 3:
                var_halide = self.container_var["fi_setting"]["Halide"].get()
                concentration_halide = self.calculate_concentration_halides(
                    var_halide=self.container_var["fi_setting"]["Halide"])
                self.concentration_ho_host = concentration_halide[var_halide][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_is])) / np.mean(intensity_host[var_ho])
            elif self.container_var["fi_setting"]["Host Setup Selection"].get() == 4:
                var_mineral = self.container_var["mineral"].get()
                concentration_mineral = self.calculate_concentration_mineral(
                    var_mineral=self.container_var["mineral"])
                self.concentration_ho_host = concentration_mineral[var_mineral][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_is])) / np.mean(intensity_host[var_ho])
            #
            ## Relative Sensitivity Factor Calculation
            relative_sensitivity_factor = self.calculate_rsf_host(
                var_is=var_is, var_is_element=var_is_element, concentration_is_host=self.concentration_is_host,
                sensitivity=sensitivity, var_filetype=var_filetype["Result"], var_datatype=var_datatype)
            #
            ## Limit of Detection Calculation
            # limit_of_detection = self.calculate_lod_host(
            #     var_is=var_is, sensitivity=sensitivity, var_filetype=var_filetype["Result"], var_datatype=var_datatype)
            limit_of_detection = self.calculate_lod(intensity=intensity, sensitivity=sensitivity,
                                                    var_filetype=var_filetype["Result"], var_datatype=var_datatype)
            #
            ## Concentration Calculation
            concentration = self.calculate_concentration_host_alternative(
                var_is=var_is, concentration_is_host=self.concentration_is_host, intensity=intensity,
                sensitivity=sensitivity, var_filetype=var_filetype["Result"])
            #
        elif var_mode == "Fluid Inclusion":
            ## Intensity Data
            intensity = self.get_intensity_data(
                var_filetype=var_filetype["Result"], var_datatype=var_datatype, var_mode=var_mode)
            intensity_host = intensity["MATRIX CORRECTED"]
            ## Mixing Ratio RI (Matrix-Only)
            mixing_ratio_ri = self.calculate_mixing_ratio_ri(
                only_host_isotope=var_ho, var_filetype=var_filetype["Result"], var_datatype=var_datatype)
            #
            ## Intensity Ratio (IR)
            intensity_ratio = self.calculate_intensity_ratio_inclusion(
                var_is=var_is, mixing_ratio=mixing_ratio_ri, var_filetype=var_filetype["Result"],
                var_datatype=var_datatype)
            #
            ## Sensitivity (Xi)
            sensitivity = self.calculate_sensitivity_inclusion(
                var_is=var_is, var_is_element=var_is_element, var_filetype=var_filetype["Result"],
                var_datatype=var_datatype)
            self.var_a = self.calculate_mixture_ratio_a(
                var_is=var_is, var_ho=var_ho, sensitivity=sensitivity, var_filetype=var_filetype["Result"],
                var_datatype=var_datatype)
            self.rsf_mix = self.calculate_rsf_mix(
                var_is=var_is, var_is_element=var_is_element, intensity=intensity, var_filetype="SMPL",
                var_datatype=var_datatype)
            self.rsf_host = self.calculate_rsf_host(
                var_is=var_is, var_is_element=var_is_element, concentration_is_host=self.concentration_is_host,
                sensitivity=sensitivity, var_filetype="SMPL", var_datatype=var_datatype)
            #
            if self.container_var["fi_setting"]["Host Setup Selection"].get() == 1:
                var_oxide = self.container_var["fi_setting"]["Oxide"].get()
                concentration_oxide = self.calculate_concentration_oxides(
                    var_oxide=var_oxide)
                self.concentration_ho_host = concentration_oxide[var_oxide][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_ho])) / np.mean(intensity_host[var_ho])
            elif self.container_var["fi_setting"]["Host Setup Selection"].get() == 2:
                var_sulfide = self.container_var["fi_setting"]["Sulfide"].get()
                concentration_sulfide = self.calculate_concentration_sulfides(
                    var_sulfide=self.container_var["fi_setting"]["Sulfide"])
                self.concentration_ho_host = concentration_sulfide[var_sulfide][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_is])) / np.mean(intensity_host[var_ho])
            elif self.container_var["fi_setting"]["Host Setup Selection"].get() == 3:
                var_halide = self.container_var["fi_setting"]["Halide"].get()
                concentration_halide = self.calculate_concentration_halides(
                    var_halide=self.container_var["fi_setting"]["Halide"])
                self.concentration_ho_host = concentration_halide[var_halide][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_is])) / np.mean(intensity_host[var_ho])
            elif self.container_var["fi_setting"]["Host Setup Selection"].get() == 4:
                var_mineral = self.container_var["mineral"].get()
                concentration_mineral = self.calculate_concentration_mineral(
                    var_mineral=self.container_var["mineral"])
                self.concentration_ho_host = concentration_mineral[var_mineral][var_ho_element]
                self.concentration_is_host = (self.concentration_ho_host * np.mean(intensity_host[var_is]) * np.mean(
                    sensitivity[var_is])) / np.mean(intensity_host[var_ho])
            #
            ## Relative Sensitivity Factor (RSF)
            #
            #
            ## Concentration (C)
            intensity_inclusion = self.calculate_intensity_inclusion(
                mixing_ratio=mixing_ratio_ri, var_ho=var_ho, var_filetype=var_filetype["Result"],
                var_datatype=var_datatype)
            # concentration = self.calculate_concentration_inclusion(
            #     var_is=var_is, intensity_inclusion=intensity_inclusion, sensitivity=sensitivity,
            #     var_filetype=var_filetype["Result"], var_datatype=var_datatype)
            #
            key = "matrix"
            plugin_title = "fi_method_matrix_only_tracer.py"
            if key in plugin_title:
                from plugins.fi_method_matrix_only_tracer import Method
                intensity_incl, concentration_incl = Method(
                    container_measurements=self.container_measurements, container_lists=self.container_lists,
                    container_files=self.container_files, var_is=var_is, var_datatype=var_datatype,
                    concentration_host_hostonly=self.concentration_ho_host,
                    concentration_host_is=self.concentration_is_host, host_isotope=var_ho).do_quantification(
                    intensity_mat=self.intensity_mat, intensity_mixed=self.intensity_mixed,
                    intensity_incl=self.intensity_incl, host_isotope=var_ho, sensitivity=sensitivity,
                    intensity=intensity)
                concentration = concentration_incl
                intensity_ratio = intensity_incl
                #self.calculate_intensity_ratio_incl(intensity_incl=intensity_incl)
            # if var_filetype["Result"] == "SMPL":
            #     concentration = {}
            #     for isotope in self.container_lists["ISOTOPES"]:
            #         concentration[isotope] = []
            #         for file_smpl in self.container_lists["SMPL"]["Short"]:
            #             concentration[isotope].append(np.mean(concentration_incl[file_smpl][isotope]))
            #
            ## Relative Sensitivity Factor (RSF)
            #
            ## Limit of Detection (LoD)
            #
            limit_of_detection = self.calculate_lod(intensity=intensity, sensitivity=sensitivity,
                                                    var_filetype=var_filetype["Result"], var_datatype=var_datatype)
        #
        ## FILLING THE TABLE
        for isotope in self.container_lists["ISOTOPES"]:
            # Intensity Ratio (IR)
            try:
                if type(intensity_ratio[isotope]) == dict:
                    self.container_var["fi_datareduction"][isotope][0].set(round(intensity_ratio[isotope]["Mean"], 8))
                    self.container_var["fi_datareduction"][isotope][1].set(round(intensity_ratio[isotope]["STD"], 8))
                else:
                    self.container_var["fi_datareduction"][isotope][0].set(round(np.mean(intensity_ratio[isotope]), 8))
                    self.container_var["fi_datareduction"][isotope][1].set(
                        round(np.std(intensity_ratio[isotope], ddof=1), 8))
            except:
                self.container_var["fi_datareduction"][isotope][0].set(0.0)
                self.container_var["fi_datareduction"][isotope][1].set(0.0)
            # Sensitivity (Xi)
            try:
                self.container_var["fi_datareduction"][isotope][2].set(round(np.mean(sensitivity[isotope]), 8))
                self.container_var["fi_datareduction"][isotope][3].set(round(np.std(sensitivity[isotope], ddof=1), 8))
            except:
                self.container_var["fi_datareduction"][isotope][2].set(0.0)
                self.container_var["fi_datareduction"][isotope][3].set(0.0)
            # Concentration (C)
            try:
                self.container_var["fi_datareduction"][isotope][4].set(round(np.mean(concentration[isotope]), 8))
                self.container_var["fi_datareduction"][isotope][5].set(round(np.std(concentration[isotope], ddof=1), 8))
            except:
                self.container_var["fi_datareduction"][isotope][4].set(0.0)
                self.container_var["fi_datareduction"][isotope][5].set(0.0)
            # Relative Sensitivity Factor (RSF)
            try:
                self.container_var["fi_datareduction"][isotope][6].set(
                    round(np.mean(relative_sensitivity_factor[var_is]), 8))
                self.container_var["fi_datareduction"][isotope][7].set(
                    round(np.std(relative_sensitivity_factor[var_is], ddof=1), 8))
            except:
                self.container_var["fi_datareduction"][isotope][6].set(0.0)
                self.container_var["fi_datareduction"][isotope][7].set(0.0)
            # Limit of Detection (LoD)
            try:
                self.container_var["fi_datareduction"][isotope][8].set(round(np.mean(limit_of_detection[isotope]), 8))
                self.container_var["fi_datareduction"][isotope][9].set(
                    round(np.std(limit_of_detection[isotope], ddof=1), 8))
            except:
                self.container_var["fi_datareduction"][isotope][8].set(0.0)
                self.container_var["fi_datareduction"][isotope][9].set(0.0)
    #
    ###################################
    ## DATA REDUCTION (HOST MINERAL) ##
    ###################################
    #
    def get_intensity_data(self, var_filetype, var_datatype, var_mode):
        helper = {}
        helper["BACKGROUND"] = {}
        helper["MATRIX"] = {}
        helper["MATRIX CORRECTED"] = {}
        helper["MIX"] = {}
        #
        if var_filetype == "STD":
            for file_std in self.container_lists["STD"]["Short"]:
                helper["BACKGROUND"][file_std] = {}
                helper["MATRIX"][file_std] = {}
                helper["MATRIX CORRECTED"][file_std] = {}
                for isotope in self.container_lists["ISOTOPES"]:
                    intensity_i_bg = np.mean(
                        self.container_measurements["SELECTED"][file_std][var_datatype][isotope]["BG"])
                    intensity_i_mat = np.mean(
                        self.container_measurements["SELECTED"][file_std][var_datatype][isotope]["MAT"])
                    #
                    if np.mean(intensity_i_mat) >= np.mean(intensity_i_bg):
                        intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                    else:
                        intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                    #
                    helper["BACKGROUND"][file_std][isotope] = intensity_i_bg
                    helper["MATRIX"][file_std][isotope] = intensity_i_mat
                    helper["MATRIX CORRECTED"][file_std][isotope] = intensity_i
                    #
                    if isotope not in helper["BACKGROUND"]:
                        helper["BACKGROUND"][isotope] = []
                        helper["MATRIX"][isotope] = []
                        helper["MATRIX CORRECTED"][isotope] = []
                    #
                    helper["BACKGROUND"][isotope].append(np.mean(intensity_i_bg))
                    helper["MATRIX"][isotope].append(np.mean(intensity_i_mat))
                    helper["MATRIX CORRECTED"][isotope].append(np.mean(intensity_i))
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                helper["BACKGROUND"][file_smpl] = {}
                helper["MATRIX"][file_smpl] = {}
                helper["MATRIX CORRECTED"][file_smpl] = {}
                helper["MIX"][file_smpl] = {}
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper["BACKGROUND"]:
                        helper["BACKGROUND"][isotope] = []
                        helper["MATRIX"][isotope] = []
                        helper["MATRIX CORRECTED"][isotope] = []
                        if var_mode == "Fluid Inclusion":
                            helper["MIX"][isotope] = []
                    #
                    intensity_i_bg = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"])
                    intensity_i_mat = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"])
                    #
                    if np.mean(intensity_i_mat) >= np.mean(intensity_i_bg):
                        intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                    else:
                        intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                    #
                    helper["BACKGROUND"][file_smpl][isotope] = intensity_i_bg
                    helper["MATRIX"][file_smpl][isotope] = intensity_i_mat
                    helper["MATRIX CORRECTED"][file_smpl][isotope] = intensity_i
                    #
                    helper["BACKGROUND"][isotope].append(np.mean(intensity_i_bg))
                    helper["MATRIX"][isotope].append(np.mean(intensity_i_mat))
                    helper["MATRIX CORRECTED"][isotope].append(np.mean(intensity_i))
                    #
                    if var_mode == "Fluid Inclusion":
                        intensity_i_incl = np.array(
                            self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["INCL"])
                        #
                        if np.mean(intensity_i_incl) >= np.mean(intensity_i_bg):
                            intensity_i_mix = intensity_i_incl - np.mean(intensity_i_bg)
                        else:
                            intensity_i_mix = intensity_i_bg - np.mean(intensity_i_incl)
                        #
                        helper["MIX"][file_smpl][isotope] = intensity_i_mix
                        helper["MIX"][isotope].append(np.mean(intensity_i_mix))
        #
        ## TESTING
        # print("TESTING: Intensity")
        # for isotope in self.container_lists["ISOTOPES"]:
        #     print(isotope)
        #     print("Mean:", np.mean(helper["BACKGROUND"][isotope]),
        #           np.std(helper["BACKGROUND"][isotope], ddof=1))
        #     print("Mean:", np.mean(helper["MATRIX"][isotope]),
        #           np.std(helper["MATRIX"][isotope], ddof=1))
        #     print("Mean:", np.mean(helper["MATRIX CORRECTED"][isotope]),
        #           np.std(helper["MATRIX CORRECTED"][isotope], ddof=1))
        #     try:
        #         print("Mean:", np.mean(helper["MIX"][isotope]),
        #               np.std(helper["MIX"][isotope], ddof=1))
        #     except:
        #         pass
        #
        return helper
    #
    def calculate_intensity_ratio_host(self, var_is, intensity):
        helper = {}
        intensity_is = np.mean(intensity["MATRIX CORRECTED"][var_is])
        #
        for isotope in self.container_lists["ISOTOPES"]:
            intensity_i = np.mean(intensity["MATRIX CORRECTED"][isotope])
            intensity_i_all = np.array(intensity["MATRIX CORRECTED"][isotope])
            #
            helper[isotope] = {"Mean": round(intensity_i/intensity_is, 8),
                               "STD": round(np.std(intensity_i_all/intensity_is, ddof=1), 8),}
        #
        ## TESTING
        # print("TESTING: Intensity Ratio Calculation")
        # for key, value in helper.items():
        #     print(key+"/"+var_is)
        #     print("Mean:", value["Mean"], "Error:", value["STD"])
        #
        return helper
    #
    def calculate_sensitivity_host_alternative(self, var_is, intensity, var_filetype):
        helper = {}
        #
        if var_filetype == "STD":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                key_element = re.search("(\D+)(\d+)", var_is)
                var_is_element = key_element.group(1)
                #
                concentration_is = self.srm_actual[var_srm][var_is_element]
                intensity_is = np.mean(intensity["MATRIX CORRECTED"][file_std][var_is])
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    #
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    #
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    intensity_i = np.mean(intensity["MATRIX CORRECTED"][file_std][isotope])
                    intensity_ratio = intensity_i/intensity_is
                    concentration_ratio = concentration_is/concentration_i
                    value = intensity_ratio*concentration_ratio
                    #
                    helper[isotope].append(value)
        #
        ## TESTING
        # print("TESTING: Sensitivity Calculation")
        # for key, value in helper.items():
        #     print(key)
        #     print(value, np.mean(value), np.std(value, ddof=1))
        #
        return helper
    #
    def calculate_sensitivity_host(self, var_is, var_is_element, var_filetype, var_datatype):
        helper = {}
        self.xi_opt = {}
        #
        if var_filetype == "STD":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                intensity_is_bg = np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"])
                intensity_is_mat = np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"])
                if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                    intensity_is = intensity_is_mat - np.mean(intensity_is_bg)
                else:
                    intensity_is = intensity_is_bg - np.mean(intensity_is_mat)
                concentration_is = self.srm_actual[var_srm][var_is_element]
                for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                    if isotope not in helper:
                        helper[isotope] = []
                    intensity_i_bg = np.mean(value["BG"])
                    intensity_i_mat = np.mean(value["MAT"])
                    if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                        intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                    else:
                        intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    value = (intensity_i*concentration_is)/(intensity_is*concentration_i)
                    #
                    helper[isotope].append(value)
        elif var_filetype == "SMPL":
            helper_sensitivity_std = {}
            self.extract_data_times()
            for file_std in self.container_lists["STD"]["Short"]:
                self.xi_std_time[file_std] = {}
                helper_sensitivity_std[file_std] = {}
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                intensity_is_bg = np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"])
                intensity_is_mat = np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"])
                if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                    intensity_is = intensity_is_mat - np.mean(intensity_is_bg)
                else:
                    intensity_is = intensity_is_bg - np.mean(intensity_is_mat)
                concentration_is = self.srm_actual[var_srm][var_is_element]
                for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                    if isotope not in helper_sensitivity_std:
                        self.xi_opt[isotope] = []
                        helper_sensitivity_std[isotope] = []
                        helper_sensitivity_std[file_std][isotope] = {}
                    intensity_i_bg = np.mean(value["BG"])
                    intensity_i_mat = np.mean(value["MAT"])
                    if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                        intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                    else:
                        intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    value = (intensity_i*concentration_is)/(intensity_is*concentration_i)
                    #
                    helper_sensitivity_std[isotope].append(value)
                    helper_sensitivity_std[file_std][isotope] = {
                        "Time": self.std_times[file_std]["Delta"],
                        "Sensitivity": value}
                    #
                    if isotope not in self.xi_std_time[file_std]:
                        self.xi_std_time[file_std][isotope] = [
                            self.std_times[file_std]["Delta"], np.mean(value.tolist())]
            for isotope in self.container_lists["ISOTOPES"]:
                self.xi_regr = self.calculate_regression(
                    data=self.xi_std_time, isotope=isotope, file_data=self.container_lists["STD"]["Short"])
                self.xi_opt[isotope].extend(self.xi_regr)
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    value = self.xi_opt[isotope][0]*self.smpl_times[file_smpl]["Delta"] + self.xi_opt[isotope][1]
                    if value >= 0:
                        helper[isotope].append(value)
                    else:
                        helper[isotope].append(0.0)
        #
        ## TESTING
        # print("TESTING: Sensitivity Calculation")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_concentration_host_alternative(self, var_is, concentration_is_host, intensity, sensitivity,
                                                 var_filetype):
        helper = {}
        if var_filetype == "STD":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    value = concentration_i
                    # helper[isotope].append(value)
                    if value >= 0:
                        helper[isotope].append(value)
                    else:
                        helper[isotope].append(0.0)
        elif var_filetype == "SMPL":
            intensity_is = np.mean(intensity["MATRIX CORRECTED"][var_is])
            concentration_is = concentration_is_host
            #
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = []
                #
                intensity_i = np.mean(intensity["MATRIX CORRECTED"][isotope])
                sensitivity_i = np.mean(sensitivity[isotope])
                #
                value = (intensity_i*concentration_is)/(intensity_is*sensitivity_i)
                #
                helper[isotope].append(value)
        #
        ## TESTING
        # print("TESTING: Concentration Calculation (Alternative)")
        # for key, value in helper.items():
        #     print(key)
        #     print("Mean:", np.mean(value), "STD:", np.std(value, ddof=1))
        #
        return helper
    #
    def calculate_concentration_host(self, var_is, var_ho, var_rsf, var_filetype, var_datatype):
        helper = {}
        helper_std = {}
        #
        if var_filetype == "STD":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    value = concentration_i
                    # helper[isotope].append(value)
                    if value >= 0:
                        helper[isotope].append(value)
                    else:
                        helper[isotope].append(0.0)
        elif var_filetype == "SMPL":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper_std:
                        helper_std[isotope] = 0
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i_std = self.srm_actual[var_srm][var_i_element]
                    intensity_i_std = np.mean(np.mean(
                        self.container_measurements["SELECTED"][file_std][var_datatype][isotope]["MAT"]) - np.mean(
                        self.container_measurements["SELECTED"][file_std][var_datatype][isotope]["BG"]))
                    value = concentration_i_std/intensity_i_std
                    helper_std[isotope] += value
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    #
                    intensity_i_bg = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"])
                    intensity_i_mat = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"])
                    if np.mean(intensity_i_mat) >= np.mean(intensity_i_bg):
                        intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                    else:
                        intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                    #
                    value = helper_std[isotope]*intensity_i/np.mean(var_rsf[var_is])
                    print("C("+str(isotope)+"):", round(np.mean(value), 4), "ppm")
                    # if isotope not in [var_is, var_ho]:
                    #     intensity_i = np.array(
                    #         self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"]) - np.mean(
                    #         self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"])
                    #     value = helper_std[isotope]*intensity_i/np.mean(var_rsf[var_is])
                    # else:
                    #     if isotope == var_is:
                    #         value = self.concentration_is_host*np.ones(10)
                    #     elif isotope == var_ho:
                    #         value = self.concentration_ho_host*np.ones(10)
                    helper[isotope].append(value)
                    # list_pre = value.tolist()
                    # list_checked = [item for item in list_pre if item >= 0]
                    # helper[isotope].extend(list_checked)
        #
        ## TESTING
        # print("TESTING: Concentration Calculation")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_rsf_host(self, var_is, var_is_element, concentration_is_host, sensitivity, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            if var_is not in helper:
                # helper[var_is] = np.ones(len(self.container_lists["ISOTOPES"]))
                helper[var_is] = []
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                concentration_is_std = self.srm_actual[var_srm][var_is_element]
                intensity_is_std = np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"]) - np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"])
                value = concentration_is_std/intensity_is_std
                #
                helper[var_is].append(value)
                # list_pre = value.tolist()
                # list_checked = [item for item in list_pre if item >= 0]
                # helper[var_is].extend(list_checked)
        elif var_filetype == "SMPL":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                concentration_is_std = self.srm_actual[var_srm][var_is_element]
                intensity_is_std = np.mean(np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"]) - np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"]))
                for file_smpl in self.container_lists["SMPL"]["Short"]:
                    if var_is not in helper:
                        helper[var_is] = []
                    concentration_is_smpl = concentration_is_host
                    intensity_is_bg = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"])
                    intensity_is_mat = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["MAT"])
                    if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                        intensity_is_smpl = intensity_is_mat - np.mean(intensity_is_bg)
                    else:
                        intensity_is_smpl = intensity_is_bg - np.mean(intensity_is_mat)
                    value = (concentration_is_std*intensity_is_smpl)/(intensity_is_std*concentration_is_smpl)
                    #
                    helper[var_is].append(value)
        #
        ## TESTING
        # print("TESTING: Relative Sensitivity Factor (RSF) Calculation")
        # for key, value in helper.items():
        #     print(key)
        #     print(round(np.mean(value), 4), round(np.std(value, ddof=1), 4))
        #
        return helper
    #
    def calculate_lod_host(self, var_is, sensitivity, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = np.zeros(len(self.container_lists["ISOTOPES"]))
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                concentration_is_smpl = self.concentration_is_host
                #
                intensity_is_bg = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"])
                intensity_is_mat = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["MAT"])
                #
                if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                    intensity_is_smpl = intensity_is_mat - np.mean(intensity_is_bg)
                else:
                    intensity_is_smpl = intensity_is_bg - np.mean(intensity_is_mat)
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    n_smpl_bg = len(self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"])
                    n_smpl_mat = len(self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"])
                    sigma_smpl_bg = np.std(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"], ddof=1)
                    sensitivity_i = np.mean(sensitivity[isotope])
                    value = 3*sigma_smpl_bg*np.sqrt(1/n_smpl_bg + 1/n_smpl_mat)\
                            *(concentration_is_smpl)/(sensitivity_i*intensity_is_smpl)
                    #
                    helper[isotope].append(value)
        #
        ## TESTING
        # print("TESTING: Limit of Detection (LoD) Calculation")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    ######################################
    ## DATA REDUCTION (FLUID INCLUSION) ##
    ######################################
    #
    def calculate_mixing_ratio_ri(self, only_host_isotope, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = np.zeros(len(self.container_lists["ISOTOPES"]))
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                if file_smpl not in helper:
                    helper[file_smpl] = []
                intensity_only_incl = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][only_host_isotope]["INCL"]) \
                                      - np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][only_host_isotope]["BG"])
                intensity_only_mat = np.mean(np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][only_host_isotope]["MAT"]) \
                                      - np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][only_host_isotope]["BG"]))
                value = intensity_only_incl/intensity_only_mat
                #
                helper[file_smpl].append(value)
        #
        ## TESTING
        # print("TESTING: Mixing Ratio RI Calculation")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_intensity_ratio_incl(self, intensity_incl):
        print(intensity_incl)
    #
    def calculate_intensity_ratio_inclusion(self, var_is, mixing_ratio, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = np.zeros(len(self.container_lists["ISOTOPES"]))
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                intensity_is_incl = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["INCL"]) \
                                    - np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"]) \
                                    - np.mean(np.mean(mixing_ratio[file_smpl])\
                                    *(np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["MAT"]) - np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"])))
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    intensity_i_incl = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["INCL"]) \
                                        - np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"]) \
                                        - np.mean(np.mean(mixing_ratio[file_smpl]) \
                                                  * (np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"]) - np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"])))
                    value = intensity_i_incl/intensity_is_incl
                    #
                    helper[isotope].append(value)
        #
        ## TESTING
        # print("TESTING: Intensity Ratio")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_sensitivity_inclusion(self, var_is, var_is_element, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            if "SRM Data" not in self.container_lists:
                self.container_lists["SRM Data"] = {}
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                self.container_lists["SRM Data"][var_srm] = self.srm_actual[var_srm]
                intensity_is = np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"]) \
                               - np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"])
                concentration_is = self.srm_actual[var_srm][var_is_element]
                for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                    if isotope not in helper:
                        helper[isotope] = []
                    intensity_i = np.mean(value["MAT"]) - np.mean(value["BG"])
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    value = (intensity_i*concentration_is)/(intensity_is*concentration_i)
                    #
                    helper[isotope].append(value)
                    # list_pre = value.tolist()
                    # list_checked = [item for item in list_pre if item >= 0]
                    # helper[isotope].extend(list_checked)
        elif var_filetype == "SMPL":
            helper_sensitivity_std = {}
            self.extract_data_times()
            if "SRM Data" not in self.container_lists:
                self.container_lists["SRM Data"] = {}
            for file_std in self.container_lists["STD"]["Short"]:
                self.xi_std_time[file_std] = {}
                helper_sensitivity_std[file_std] = {}
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                self.container_lists["SRM Data"][var_srm] = self.srm_actual[var_srm]
                intensity_is = np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"]) \
                               - np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"])
                concentration_is = self.srm_actual[var_srm][var_is_element]
                for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                    if isotope not in helper_sensitivity_std:
                        self.xi_opt[isotope] = []
                        helper_sensitivity_std[isotope] = []
                        helper_sensitivity_std[file_std][isotope] = {}
                    intensity_i = np.mean(value["MAT"]) - np.mean(value["BG"])
                    key_element = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element.group(1)
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    value = (intensity_i * concentration_is) / (intensity_is * concentration_i)
                    #
                    helper_sensitivity_std[isotope].append(value)
                    helper_sensitivity_std[file_std][isotope] = {"Time": self.std_times[file_std]["Delta"],
                                                                 "Sensitivity": value}
                    # helper_sensitivity_std[isotope].extend(value.tolist())
                    # helper_sensitivity_std[file_std][isotope] = {
                    #     "Time": self.std_times[file_std]["Delta"],
                    #     "Sensitivity": np.mean(value.tolist())}
                    #
                    if isotope not in self.xi_std_time[file_std]:
                        self.xi_std_time[file_std][isotope] = [
                            self.std_times[file_std]["Delta"], np.mean(value.tolist())]
            for isotope in self.container_lists["ISOTOPES"]:
                self.xi_regr = self.calculate_regression(
                    data=self.xi_std_time, isotope=isotope, file_data=self.container_lists["STD"]["Short"])
                self.xi_opt[isotope].extend(self.xi_regr)
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    value = self.xi_opt[isotope][0] * self.smpl_times[file_smpl]["Delta"] + self.xi_opt[isotope][1]
                    if value >= 0:
                        helper[isotope].append(value)
                    else:
                        helper[isotope].append(0.0)
        #
        ## TESTING
        # print("TESTING: Sensitivity")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_intensity_inclusion(self, mixing_ratio, var_ho, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = np.zeros(len(self.container_lists["ISOTOPES"]))
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                ri_factor = np.mean(mixing_ratio[file_smpl])
                intensity_mix_ho = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_ho]["INCL"]) - np.mean(
                    np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][var_ho]["BG"]))
                intensity_mat_ho = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_ho]["MAT"]) - np.mean(
                    np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][var_ho]["BG"]))
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    intensity_mix_i = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["INCL"]) - np.mean(
                        np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"]))
                    intensity_mat_i = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"]) - np.mean(
                        np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"]))
                    # value = intensity_mix_i - ri_factor*np.mean(intensity_mat_i)
                    value = intensity_mix_i - np.mean(intensity_mix_ho)*np.mean(intensity_mat_i)/np.mean(intensity_mat_ho)
                    if value >= 0:
                        value = abs(value)
                    helper[isotope].append(value)
                    # list_pre = value.tolist()
                    # list_checked = []
                    # for item in list_pre:
                    #     if item >= 0:
                    #         list_checked.append(abs(item))
                    #     # else:
                    #     #     list_checked.append(0.0)
                    # helper[isotope].extend(list_checked)
        #
        ## TESTING
        # print("TESTING: Intensity Inclusion (only)")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_concentration_inclusion(self, var_is, intensity_inclusion, sensitivity, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = np.zeros(len(self.container_lists["ISOTOPES"]))
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                intensity_is_incl = np.mean(np.mean(intensity_inclusion[var_is]))
                concentration_is_incl = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    intensity_i_incl = np.mean(intensity_inclusion[isotope])
                    xi_i = np.mean(sensitivity[isotope])
                    value = intensity_i_incl/intensity_is_incl*concentration_is_incl/xi_i
                    helper[isotope].append(value)
                    # list_pre = value.tolist()
                    # list_checked = [abs(item) for item in list_pre if item >= 0]
                    # helper[isotope].extend(list_checked)
        #
        ## TESTING
        # print("TESTING: Concentration")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_mixture_ratio_a(self, var_is, var_ho, sensitivity, var_filetype, var_datatype):
        # """
        # Parameters:
        #     var_is (str):   the internal standard
        #     var_ho (str):   the isotope that occurs only in the host mineral
        #     sensitivity (dict): the sensitivity values for all isotopes considering the internal standard
        #     var_filetype (str): a key that refers if standard or sample files are analyzed
        #     var_datatype (str): a key that refers if raw or smoothed data are analyzed
        # """
        helper = {}
        #
        if var_filetype == "STD":
            pass
        elif var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                if file_smpl not in helper:
                    helper[file_smpl] = None
                intensity_mix_is = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["INCL"]) \
                               - np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"])
                intensity_mix_ho = np.mean(
                    self.container_measurements["SELECTED"][file_smpl][var_datatype][var_ho]["INCL"]) \
                               - np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][var_ho]["BG"])
                sensitivity_ho = np.mean(sensitivity[var_ho])
                value = np.mean(intensity_mix_ho)/(np.mean(intensity_mix_is)*sensitivity_ho)
                helper[file_smpl] = value
        #
        ## TESTING
        # print("TESTING: Mixture Ratio 'a'")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_rsf_mix(self, var_is, var_is_element, intensity, var_filetype, var_datatype):
        helper = {}
        #
        if var_filetype == "STD":
            if var_is not in helper:
                helper[var_is] = np.ones(len(self.container_lists["ISOTOPES"]))
        elif var_filetype == "SMPL":
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                concentration_is_std = self.srm_actual[var_srm][var_is_element]
                intensity_is_std = np.mean(np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"]) \
                                           - np.mean(
                    self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"]))
                for file_smpl in self.container_lists["SMPL"]["Short"]:
                    if var_is not in helper:
                        helper[var_is] = []
                    concentration_is_smpl = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
                    intensity_is_smpl = np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["MAT"]) \
                                        - np.mean(
                        self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"])
                    value = (concentration_is_std * intensity_is_smpl) / (intensity_is_std * concentration_is_smpl)
                    helper[var_is].append(value)
                    # list_pre = value.tolist()
                    # list_checked = [item for item in list_pre if item >= 0]
                    # helper[var_is].extend(list_checked)
        #
        ## TESTING
        # print("TESTING: Relative Sensitivity Factor (Mixed Signal)")
        # for key, value in helper.items():
        #     print(key)
        #     print(value)
        #
        return helper
    #
    def calculate_mixed_signal(self, var_datatype):
        #
        intensity_bg = {}
        intensity_mat = {}
        intensity_incl = {}
        intensity_mixed = {}
        #
        if self.container_var["fi_datareduction"]["Option File"].get() == "All Standard Files":
            for file_std in self.container_lists["STD"]["Short"]:
                intensity_bg[file_std] = {}
                intensity_mat[file_std] = {}
                intensity_incl[file_std] = {}
                intensity_mixed[file_std] = {}
                for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                    intensity_bg[file_std][isotope] = np.mean(value["BG"])
                    intensity_mat[file_std][isotope] = np.mean(value["MAT"]) - np.mean(value["BG"])
                    intensity_incl[file_std][isotope] = np.mean([0])
                    intensity_mixed[file_std][isotope] = np.mean([0])
        #
        elif self.container_var["fi_datareduction"]["Option File"].get() == "All Sample Files":
            for file_std in self.container_lists["STD"]["Short"]:
                intensity_bg[file_std] = {}
                intensity_mat[file_std] = {}
                intensity_incl[file_std] = {}
                intensity_mixed[file_std] = {}
                for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                    intensity_bg[file_std][isotope] = np.mean(value["BG"])
                    intensity_mat[file_std][isotope] = np.mean(value["MAT"]) - np.mean(value["BG"])
                    intensity_incl[file_std][isotope] = np.mean([0])
                    intensity_mixed[file_std][isotope] = np.mean([0])
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                intensity_bg[file_smpl] = {}
                intensity_mat[file_smpl] = {}
                intensity_incl[file_smpl] = {}
                intensity_mixed[file_smpl] = {}
                for isotope, value in self.container_measurements["SELECTED"][file_smpl][var_datatype].items():
                    intensity_bg[file_smpl][isotope] = np.mean(value["BG"])
                    intensity_mat[file_smpl][isotope] = np.mean(value["MAT"]) - np.mean(value["BG"])
                    intensity_incl[file_smpl][isotope] = np.mean(value["INCL"])
                    intensity_mixed[file_smpl][isotope] = np.mean(value["INCL"]) - np.mean(value["BG"])
                    #
                    # intensity_mat[file_smpl][isotope] = intensity_mat[file_smpl][isotope][
                    #     intensity_mat[file_smpl][isotope] >= 0]
                    # intensity_incl[file_smpl][isotope] = intensity_incl[file_smpl][isotope][
                    #     intensity_incl[file_smpl][isotope] >= 0]
                    # intensity_mixed[file_smpl][isotope] = intensity_mixed[file_smpl][isotope][
                    #     intensity_mixed[file_smpl][isotope] >= 0]
        #
        # for key, value in intensity_incl.items():
        #     print(key)
        #     for key2, value2 in value.items():
        #         print(key2, np.mean(value2))
        #
        return intensity_bg, intensity_mat, intensity_incl, intensity_mixed
    #
    def calculate_sensitivity(self, var_datatype, var_is, var_is_element):
        #
        sensitivity = {}
        #
        #if self.container_var["fi_datareduction"]["Option File"].get() == "All Standard Files":
        for file_std in self.container_lists["STD"]["Short"]:
            var_srm = self.container_files["STD"][file_std]["SRM"].get()
            sensitivity[file_std] = {}
            intensity_is = np.mean(
                np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"])
                - np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"]))
            concentration_is = self.srm_actual[var_srm][var_is_element]
            for isotope, value in self.container_measurements["SELECTED"][file_std][var_datatype].items():
                sensitivity[isotope] = []
                key_element = re.search("(\D+)(\d+)", isotope)
                var_i_element = key_element.group(1)
                if var_i_element in self.srm_actual[var_srm]:
                    intensity_i = np.mean(np.mean(value["MAT"]) - np.mean(value["BG"]))
                    concentration_i = self.srm_actual[var_srm][var_i_element]
                    xi = (concentration_is)/(concentration_i)*(intensity_i)/(intensity_is)
                    sensitivity[file_std][isotope] = xi
                    sensitivity[isotope].append(xi)
                else:
                    sensitivity[file_std][isotope] = 0.0
                    sensitivity[isotope].append(0.0)
        #
        if self.container_var["fi_datareduction"]["Option File"].get() == "All Sample Files":
            self.calculcate_sensitivity_drift(var_datatype=var_datatype)
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                sensitivity[file_smpl] = {}
                for isotope, value in self.container_measurements["SELECTED"][file_smpl][var_datatype].items():
                    print("Xi (opt):", self.xi_opt[isotope])
                    sensitivity[file_smpl][isotope] = np.mean(self.xi_opt[isotope])
        #
        return sensitivity
    #
    def calculate_relative_sensitivity_factor(self, var_datatype, var_is, var_is_element):
        #
        relative_sensitivity_factor = {}
        relative_sensitivity_factor[var_is] = []
        #
        for file_std in self.container_lists["STD"]["Short"]:
            var_srm = self.container_files["STD"][file_std]["SRM"].get()
            intensity_is_std = np.mean(
                np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["MAT"]) \
                - np.mean(self.container_measurements["SELECTED"][file_std][var_datatype][var_is]["BG"]))
            concentration_is_std = self.srm_actual[var_srm][var_is_element]
            relative_sensitivity_factor[file_std] = 0.0
            #
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                intensity_is_smpl = np.mean(
                    np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["MAT"])
                    - np.mean(self.container_measurements["SELECTED"][file_smpl][var_datatype][var_is]["BG"]))
                concentration_is_smpl = float(self.container_var["fi_setting"]["IS Concentration"].get())
                rsf = (concentration_is_std)/(concentration_is_smpl)*(intensity_is_smpl)/(intensity_is_std)
                relative_sensitivity_factor[file_smpl] = rsf
                relative_sensitivity_factor[var_is].append(rsf)
        #
        return relative_sensitivity_factor
    #
    def select_method(self, var_opt):
        if var_opt == "Matrix-only Tracer" and self.container_var["fi_datareduction"]["Radiobutton"][2].get() == 1:
            print("Hallo")
            MatrixOnlyTracer(
                container_measurements=self.container_measurements, container_lists=self.container_lists,
                container_files=self.container_files,
                var_is=self.container_var["fi_datareduction"]["Option IS"].get()).do_quantification(
                intensity_mat=self.intensity_mat, intensity_mixed=self.intensity_mixed,
                host_isotope=self.container_var["fi_datareduction"]["Option IS"].get(), sensitivity=self.sensitivity)
    #
    def calculcate_sensitivity_drift(self, var_datatype):
        #
        self.xi_opt = {}
        var_is = self.container_var["fi_datareduction"]["Option IS"].get()
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
                    var_is_mat_raw = np.mean(
                        self.container_measurements["SELECTED"][file]["RAW"][var_is]["MAT"])
                    var_is_mat_smoothed = np.mean(
                        self.container_measurements["SELECTED"][file]["SMOOTHED"][var_is]["MAT"])
                    var_i_mat_raw = np.mean(
                        self.container_measurements["SELECTED"][file]["RAW"][isotope]["MAT"])
                    var_i_mat_smoothed = np.mean(
                        self.container_measurements["SELECTED"][file]["SMOOTHED"][isotope]["MAT"])
                    #
                    var_is_corrected_raw = var_is_mat_raw - var_is_bg_raw
                    var_i_corrected_raw = var_i_mat_raw - var_i_bg_raw
                    var_is_corrected_smoothed = var_is_mat_smoothed - var_is_bg_smoothed
                    var_i_corrected_smoothed = var_i_mat_smoothed - var_i_bg_smoothed
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
                        if var_srm_std == self.container_var["fi_datareduction"]["Option SRM"].get() \
                                and var_srm == self.container_var["fi_datareduction"]["Option SRM"].get():
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
                        if var_srm_std == self.container_var["fi_datareduction"]["Option SRM"].get() \
                                and var_srm == self.container_var["fi_datareduction"]["Option SRM"].get():
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
    def extract_data_times(self):
        self.std_times = {}
        dates_0, times_0 = Data(filename=self.container_lists["STD"]["Long"][0]).import_as_list()
        t_start_0 = datetime.timedelta(hours=int(times_0[0][0]), minutes=int(times_0[0][1]),
                                       seconds=int(times_0[0][2]))
        for file in self.container_lists["STD"]["Long"]:
            parts = file.split("/")
            self.std_times[parts[-1]] = {}
            dates, times = Data(filename=file).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            t_delta_0 = (t_start - t_start_0).total_seconds()
            self.std_times[parts[-1]]["Start"] = t_start
            self.std_times[parts[-1]]["Delta"] = t_delta_0
        #
        self.smpl_times = {}
        for file in self.container_lists["SMPL"]["Long"]:
            parts = file.split("/")
            self.smpl_times[parts[-1]] = {}
            dates, times = Data(filename=file).import_as_list()
            t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
            t_delta_0 = (t_start - t_start_0).total_seconds()
            self.smpl_times[parts[-1]]["Start"] = t_start
            self.smpl_times[parts[-1]]["Delta"] = t_delta_0
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
    def change_is_def(self, var_is, var_filetype):
        key_is = re.search("(\D+)(\d+)", var_is)
        element_is = key_is.group(1)
        #
        for file in self.container_lists[var_filetype]["Long"]:
            self.container_var[var_filetype][file]["IS"].set(var_is)
            parts = file.split("/")
            self.container_files[var_filetype][parts[-1]]["IS"].set(var_is)
            self.container_files[var_filetype][parts[-1]]["IS Concentration"].set(
                self.container_var["salt_correction"]["Concentration"][element_is])
        #
        if var_filetype == "STD" and self.container_var["IS"]["Default SMPL"].get() == "Select IS":
            self.container_var["IS"]["Default SMPL"].set(var_is)
            for file in self.container_lists["SMPL"]["Long"]:
                self.container_var["SMPL"][file]["IS"].set(var_is)
                parts = file.split("/")
                self.container_files["SMPL"][parts[-1]]["IS"].set(var_is)
                self.container_files["SMPL"][parts[-1]]["IS Concentration"].set(
                    self.container_var["salt_correction"]["Concentration"][element_is])
        elif var_filetype == "SMPL" and self.container_var["IS"]["Default STD"].get() == "Select IS":
            self.container_var["IS"]["Default STD"].set(var_is)
            for file in self.container_lists["STD"]["Long"]:
                self.container_var["STD"][file]["IS"].set(var_is)
                parts = file.split("/")
                self.container_files["STD"][parts[-1]]["IS"].set(var_is)
                self.container_files["STD"][parts[-1]]["IS Concentration"].set(
                    self.container_var["salt_correction"]["Concentration"][element_is])
    #
    def calculate_lod(self, intensity, sensitivity, var_filetype, var_datatype):
        helper = {}
        helper["Results"] = {}
        helper["I(BG,i)"] = {}
        helper["Xi(i)"] = {}
        #
        if var_filetype == "SMPL":
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper["I(BG,i)"]:
                        helper["I(BG,i)"][isotope] = []
                        helper["Xi(i)"][isotope] = []
                        helper["Results"][isotope] = []
                    #
                    intensity_bg_i = np.mean(intensity["BACKGROUND"][file_smpl][isotope])
                    dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                    n_mat = len(self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["MAT"])
                    n_bg = len(self.container_measurements["SELECTED"][file_smpl][var_datatype][isotope]["BG"])
                    sensitivity_i = np.mean(sensitivity[isotope])
                    #
                    value = (3.29*(intensity_bg_i*dwell_time_i*n_mat*(1 + n_mat/n_bg))**(0.5) + 2.71)/(
                            n_mat*dwell_time_i*sensitivity_i)
                    #
                    helper["Results"][isotope].append(value)
        elif var_filetype == "STD":
            for file_std in self.container_lists["STD"]["Short"]:
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper["I(BG,i)"]:
                        helper["I(BG,i)"][isotope] = []
                        helper["Xi(i)"][isotope] = []
                        helper["Results"][isotope] = []
                    #
                    intensity_bg_i = np.mean(intensity["BACKGROUND"][file_std][isotope])
                    dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                    n_mat = len(self.container_measurements["SELECTED"][file_std][var_datatype][isotope]["MAT"])
                    n_bg = len(self.container_measurements["SELECTED"][file_std][var_datatype][isotope]["BG"])
                    sensitivity_i = np.mean(sensitivity[isotope])
                    #
                    value = (3.29*(intensity_bg_i*dwell_time_i*n_mat*(1 + n_mat/n_bg))**(0.5) + 2.71)/(
                            n_mat*dwell_time_i*sensitivity_i)
                    #
                    helper["Results"][isotope].append(value)
        #
        ## TESTING
        # print("Testing: Limit of Detection")
        # for key, value in helper["Results"].items():
        #     print(key)
        #     print(np.mean(value))
        #
        return helper["Results"]
    #
    def calculate_concentration_oxides(self, var_oxide):
        helper = {}
        #
        M_O = 15.999
        M_Na = 22.990
        M_Mg = 24.304
        M_Al = 26.982
        M_Si = 28.084
        M_P = 30.974
        M_K = 39.098
        M_Ca = 40.078
        M_Ti = 47.867
        M_Cr = 51.996
        M_Mn = 54.938
        M_Fe = 55.845
        M_Zr = 91.224
        M_Ba = 137.330
        #
        total_ppm = 1000000
        #
        if var_oxide == "SiO2":
            helper[var_oxide] = {}
            helper[var_oxide]["Si"] = round(M_Si/(M_Si + 2*M_O)*total_ppm, 2)
        elif var_oxide == "TiO2":
            helper[var_oxide] = {}
            helper[var_oxide]["Ti"] = round(M_Ti/(M_Ti + 2*M_O)*total_ppm, 2)
        elif var_oxide == "Al2O3":
            helper[var_oxide] = {}
            helper[var_oxide]["Al"] = round(2*M_Al/(2*M_Al + 3*M_O)*total_ppm, 2)
        elif var_oxide == "Fe2O3":
            helper[var_oxide] = {}
            helper[var_oxide]["Fe"] = round(2*M_Fe/(2*M_Fe + 3*M_O)*total_ppm, 2)
        elif var_oxide == "Fe3O4":
            helper[var_oxide] = {}
            helper[var_oxide]["Fe"] = round(3*M_Fe/(3*M_Fe + 4*M_O)*total_ppm, 2)
        elif var_oxide == "FeO":
            helper[var_oxide] = {}
            helper[var_oxide]["Fe"] = round(M_Fe/(M_Fe + M_O)*total_ppm, 2)
        elif var_oxide == "MgO":
            helper[var_oxide] = {}
            helper[var_oxide]["Mg"] = round(M_Mg/(M_Mg + M_O)*total_ppm, 2)
        elif var_oxide == "MnO":
            helper[var_oxide] = {}
            helper[var_oxide]["Mn"] = round(M_Mn/(M_Mn + M_O)*total_ppm, 2)
        elif var_oxide == "CaO":
            helper[var_oxide] = {}
            helper[var_oxide]["Ca"] = round(M_Ca/(M_Ca + M_O)*total_ppm, 2)
        elif var_oxide == "BaO":
            helper[var_oxide] = {}
            helper[var_oxide]["Ba"] = round(M_Ba/(M_Ba + M_O)*total_ppm, 2)
        elif var_oxide == "Na2O":
            helper[var_oxide] = {}
            helper[var_oxide]["Na"] = round(2*M_Na/(2*M_Na + M_O)*total_ppm, 2)
        elif var_oxide == "K2O":
            helper[var_oxide] = {}
            helper[var_oxide]["K"] = round(2*M_K/(2*M_K + M_O)*total_ppm, 2)
        elif var_oxide == "P2O5":
            helper[var_oxide] = {}
            helper[var_oxide]["P"] = round(2*M_P/(2*M_P + 5*M_O)*total_ppm, 2)
        elif var_oxide == "Cr2O3":
            helper[var_oxide] = {}
            helper[var_oxide]["Cr"] = round(2*M_Cr/(2*M_Cr + 3*M_O)*total_ppm, 2)
        elif var_oxide == "ZrO2":
            helper[var_oxide] = {}
            helper[var_oxide]["Zr"] = round(M_Zr/(M_Zr + 2*M_O)*total_ppm, 2)
        #
        return helper
    #
    def calculate_concentration_sulfides(self, var_sulfide):
        helper = {}
        #
        M_Be = 9.012
        M_Na = 22.990
        M_S = 32.059
        M_Mn = 54.938
        M_Fe = 55.845
        M_Co = 58.933
        M_Ni = 58.639
        M_Cu = 63.546
        M_Zn = 65.380
        M_Se = 78.971
        M_Mo = 95.950
        M_Ag = 107.870
        M_Cd = 112.41
        M_Sn = 118.710
        M_Ba = 137.330
        M_Hg = 200.590
        M_Tl = 204.380
        M_Pb = 207.200
        #
        total_ppm = 1000000
        #
        if var_sulfide == "FeS2":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(2*M_S/(M_Fe + 2*M_S)*total_ppm, 2)
            helper[var_sulfide]["Fe"] = round(M_Fe/(M_Fe + 2*M_S)*total_ppm, 2)
        elif var_sulfide == "ZnS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Zn + M_S)*total_ppm, 2)
            helper[var_sulfide]["Zn"] = round(M_Zn/(M_Zn + M_S)*total_ppm, 2)
        elif var_sulfide == "PbS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Pb + M_S)*total_ppm, 2)
            helper[var_sulfide]["Pb"] = round(M_Pb/(M_Pb + M_S)*total_ppm, 2)
        elif var_sulfide == "Ag2S":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(2*M_Ag + M_S)*total_ppm, 2)
            helper[var_sulfide]["Ag"] = round(2*M_Ag/(2*M_Ag + M_S)*total_ppm, 2)
        elif var_sulfide == "Na2S":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(2*M_Na + M_S)*total_ppm, 2)
            helper[var_sulfide]["Na"] = round(2*M_Na/(2*M_Na + M_S)*total_ppm, 2)
        elif var_sulfide == "MoS2":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Mo + 2*M_S)*total_ppm, 2)
            helper[var_sulfide]["Mo"] = round(M_Mo/(M_Mo + 2*M_S)*total_ppm, 2)
        elif var_sulfide == "CdS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Cd + M_S)*total_ppm, 2)
            helper[var_sulfide]["Cd"] = round(M_Cd/(M_Cd + M_S)*total_ppm, 2)
        elif var_sulfide == "SeS2":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Se + 2*M_S)*total_ppm, 2)
            helper[var_sulfide]["Se"] = round(M_Se/(M_Se + 2*M_S)*total_ppm, 2)
        elif var_sulfide == "BaS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Ba + M_S)*total_ppm, 2)
            helper[var_sulfide]["Ba"] = round(M_Ba/(M_Ba + M_S)*total_ppm, 2)
        elif var_sulfide == "BeS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Be + M_S)*total_ppm, 2)
            helper[var_sulfide]["Be"] = round(M_Be/(M_Be + M_S)*total_ppm, 2)
        elif var_sulfide == "CoS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Co + M_S)*total_ppm, 2)
            helper[var_sulfide]["Co"] = round(M_Co/(M_Co + M_S)*total_ppm, 2)
        elif var_sulfide == "Cu2S":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(2*M_Cu + M_S)*total_ppm, 2)
            helper[var_sulfide]["Cu"] = round(2*M_Cu/(2*M_Cu + M_S)*total_ppm, 2)
        elif var_sulfide == "CuS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Cu + M_S)*total_ppm, 2)
            helper[var_sulfide]["Cu"] = round(M_Cu/(M_Cu + M_S)*total_ppm, 2)
        elif var_sulfide == "FeS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Fe + M_S)*total_ppm, 2)
            helper[var_sulfide]["Fe"] = round(M_Fe/(M_Fe + M_S)*total_ppm, 2)
        elif var_sulfide == "Fe2S3":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(3*M_S/(2*M_Fe + 3*M_S)*total_ppm, 2)
            helper[var_sulfide]["Fe"] = round(2*M_Fe/(2*M_Fe + 3*M_S)*total_ppm, 2)
        elif var_sulfide == "Hg2S":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(2*M_Hg + M_S)*total_ppm, 2)
            helper[var_sulfide]["Hg"] = round(2*M_Hg/(2*M_Hg + M_S)*total_ppm, 2)
        elif var_sulfide == "HgS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Hg + M_S)*total_ppm, 2)
            helper[var_sulfide]["Hg"] = round(M_Hg/(M_Hg + M_S)*total_ppm, 2)
        elif var_sulfide == "MnS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Mn + M_S)*total_ppm, 2)
            helper[var_sulfide]["Mn"] = round(M_Mn/(M_Mn + M_S)*total_ppm, 2)
        elif var_sulfide == "NiS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Ni + M_S)*total_ppm, 2)
            helper[var_sulfide]["Ni"] = round(M_Ni/(M_Ni + M_S)*total_ppm, 2)
        elif var_sulfide == "Tl2S":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(2*M_Tl + M_S)*total_ppm, 2)
            helper[var_sulfide]["Tl"] = round(2*M_Tl/(2*M_Tl + M_S)*total_ppm, 2)
        elif var_sulfide == "SnS":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(M_S/(M_Sn + M_S)*total_ppm, 2)
            helper[var_sulfide]["Sn"] = round(M_Sn/(M_Sn + M_S)*total_ppm, 2)
        elif var_sulfide == "SnS2":
            helper[var_sulfide] = {}
            helper[var_sulfide]["S"] = round(2*M_S/(M_Sn + 2*M_S)*total_ppm, 2)
            helper[var_sulfide]["Sn"] = round(M_Sn/(M_Sn + 2*M_S)*total_ppm, 2)
        #
        return helper
    #
    def calculate_concentration_halides(self, var_halide):
        helper = {}
        #
        M_H = 1.008
        M_Li = 6.938
        M_C = 12.009
        M_F = 18.998
        M_Na = 22.990
        M_Cl = 35.446
        M_K = 39.098
        M_Ca = 40.078
        M_Cu = 63.546
        M_Br = 79.901
        M_Ag = 107.870
        M_I = 126.900
        #
        total_ppm = 1000000
        #
        if var_halide == "NaCl":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(M_Cl/(M_Na + M_Cl)*total_ppm, 2)
            helper[var_halide]["Na"] = round(M_Na/(M_Na + M_Cl)*total_ppm, 2)
        elif var_halide == "KCl":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(M_Cl/(M_K + M_Cl)*total_ppm, 2)
            helper[var_halide]["K"] = round(M_K/(M_K + M_Cl)*total_ppm, 2)
        elif var_halide == "KI":
            helper[var_halide] = {}
            helper[var_halide]["I"] = round(M_I/(M_K + M_I)*total_ppm, 2)
            helper[var_halide]["K"] = round(M_K/(M_K + M_I)*total_ppm, 2)
        elif var_halide == "LiCl":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(M_Cl/(M_Li + M_Cl)*total_ppm, 2)
            helper[var_halide]["Li"] = round(M_Li/(M_Li + M_Cl)*total_ppm, 2)
        elif var_halide == "CuCl2":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(2*M_Cl/(M_Cu + 2*M_Cl)*total_ppm, 2)
            helper[var_halide]["Cu"] = round(M_Cu/(M_Cu + 2*M_Cl)*total_ppm, 2)
        elif var_halide == "AgCl":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(M_Cl/(M_Ag + M_Cl)*total_ppm, 2)
            helper[var_halide]["Ag"] = round(M_Ag/(M_Ag + M_Cl)*total_ppm, 2)
        elif var_halide == "CaCl2":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(2*M_Cl/(M_Ca + 2*M_Cl)*total_ppm, 2)
            helper[var_halide]["Ca"] = round(M_Ca/(M_Ca + 2*M_Cl)*total_ppm, 2)
        elif var_halide == "ClF":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(M_Cl/(M_F + M_Cl)*total_ppm, 2)
            helper[var_halide]["F"] = round(M_F/(M_F + M_Cl)*total_ppm, 2)
        elif var_halide == "CH3Br":
            helper[var_halide] = {}
            helper[var_halide]["H"] = round(3*M_H/(M_C + 3*M_H + M_Br)*total_ppm, 2)
            helper[var_halide]["C"] = round(M_C/(M_C + 3*M_H + M_Br)*total_ppm, 2)
            helper[var_halide]["Br"] = round(M_Br/(M_C + 3*M_H + M_Br)*total_ppm, 2)
        elif var_halide == "CHI3":
            helper[var_halide] = {}
            helper[var_halide]["H"] = round(M_H/(M_C + M_H + 3*M_I)*total_ppm, 2)
            helper[var_halide]["C"] = round(M_C/(M_C + M_H + 3*M_I)*total_ppm, 2)
            helper[var_halide]["I"] = round(3*M_I/(M_C + M_H + 3*M_I)*total_ppm, 2)
        elif var_halide == "HCl":
            helper[var_halide] = {}
            helper[var_halide]["Cl"] = round(M_Cl/(M_H + M_Cl)*total_ppm, 2)
            helper[var_halide]["H"] = round(M_H/(M_H + M_Cl)*total_ppm, 2)
        elif var_halide == "HBr":
            helper[var_halide] = {}
            helper[var_halide]["H"] = round(M_H/(M_H + M_Br)*total_ppm, 2)
            helper[var_halide]["Br"] = round(M_Br/(M_H + M_Br)*total_ppm, 2)
        #
        return helper
    #
    def calculate_concentration_mineral(self, var_mineral):
        for mineral in self.container_lists["Minerals"]:
            if mineral == var_mineral:
                print(mineral, "and", var_mineral, "are the same!")