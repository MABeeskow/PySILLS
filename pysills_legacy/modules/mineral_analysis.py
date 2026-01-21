#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		mineral_analysis.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		31.03.2023

#-----------------------------------------------

## MODULES
import math
import re, datetime
import numpy as np
from modules.data import Data

class MineralAnalysisCalculations:
    #
    def __init__(self, var_filetype, var_datatype, var_isotopes, var_results):
        pass

class MineralAnalysis:
    #
    def __init__(self, container_measurements, container_lists, container_files, container_var, srm_data, var_filetype,
                 var_datatype, var_is, xi_std_time):
        self.container_measurements = container_measurements
        self.container_lists = container_lists
        self.container_files = container_files
        self.container_var = container_var
        self.srm_data = srm_data
        self.var_filetype = var_filetype
        self.var_datatype = var_datatype
        self.var_is = var_is
        self.xi_std_time = xi_std_time
        #
        self.srm_isotopes = {}
        for isotope in self.container_lists["ISOTOPES"]:
            self.srm_isotopes[isotope] = {}
            var_srm = self.container_var["SRM"][isotope].get()
            key_element = re.search("(\D+)(\d+)", isotope)
            var_element = key_element.group(1)
            self.srm_isotopes[isotope]["SRM"] = var_srm
            if var_element in self.srm_data[var_srm]:
                self.srm_isotopes[isotope]["Concentration"] = self.srm_data[var_srm][var_element]
            else:
                self.srm_isotopes[isotope]["Concentration"] = 0.0
        #
        self.isotope_by_srm = {}
        for key, value in self.container_files["SRM"].items():
            var_srm = value.get()
            #
            if var_srm not in self.isotope_by_srm:
                self.isotope_by_srm[var_srm] = []
            #
            self.isotope_by_srm[var_srm].append(key)
        #
        category_results = ["Intensity BG", "Intensity SIG CORR", "Sensitivity", "Concentration", "RSF", "S", "LOD"]
        self.container_lists["Assemblages"] = {}
        for file_smpl in self.container_lists["SMPL"]["Long"]:
            parts = file_smpl.split("/")
            file_smpl_short = parts[-1]
            #
            var_id =self.container_var["SMPL"][file_smpl]["ID"].get()
            if var_id not in self.container_lists["Assemblages"]:
                self.container_lists["Assemblages"][var_id] = {}
                self.container_lists["Assemblages"][var_id][file_smpl_short] = {}
                for category in category_results:
                    self.container_lists["Assemblages"][var_id][file_smpl_short][category] = {}
                    for isotope in self.container_lists["ISOTOPES"]:
                        self.container_lists["Assemblages"][var_id][file_smpl_short][category][isotope] = 0
        #
        self.list_assemblages = list(self.container_lists["Assemblages"].keys())
        #
        self.container_results = {"STD": {"ALL": {}, "FILE": {}}, "SMPL": {"ALL": {}, "FILE": {}}}
        #
        for file_std in self.container_lists["STD"]["Short"]:
            self.container_results["STD"]["FILE"][file_std] = {}
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            self.container_results["SMPL"]["FILE"][file_smpl] = {}
        #
        for var_id, var_files in self.container_lists["ID Files"].items():
            self.container_results["SMPL"][var_id] = {"ALL": {}}
            for var_file in var_files:
                self.container_results["SMPL"][var_id][var_file] = {}

        # for key1, values in self.container_results.items():
        #     print(key1)
        #     for key2, value in values.items():
        #         print(key2, value)

    #
    def get_intensity_single(self):
        helper = {}
        #
        for isotope in self.container_lists["ISOTOPES"]:
            helper[isotope] = []
            #
            if self.data_section == "BG":
                intensity_i = np.nanmean(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["BG"])
            elif self.data_section == "SIG":
                intensity_i = np.nanmean(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["SIG"])
            elif self.data_section == "SIG CORR":
                intensity_i_bg = np.nanmean(
                    self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["BG"])
                intensity_i_mat = np.nanmean(
                    self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["SIG"])
                #
                if np.nanmean(intensity_i_mat) >= np.nanmean(intensity_i_bg):
                    intensity_i = intensity_i_mat - np.nanmean(intensity_i_bg)
                else:
                    intensity_i = 0.0
            #
            helper[isotope] = intensity_i
        #
        # print("TESTING: INTENSITY")
        # for key, value in helper.items():
        #     print(key, value)
        #
        return helper
    #
    def get_intensity_ratio_single(self):
        helper = {}
        #
        for isotope in self.container_lists["ISOTOPES"]:
            helper[isotope] = []
            #
            intensity_i = self.results_single["Intensity"][isotope]
            intensity_is = self.results_single["Intensity"][self.var_is]
            intensity_ratio_i = intensity_i/intensity_is
            #
            helper[isotope] = intensity_ratio_i
        #
        return helper
    #
    def get_sensitivity_single(self):
        helper = {}
        #
        if self.var_filetype == "STD":
            concentration_is = self.srm_isotopes[self.var_is]["Concentration"]
            #
            for isotope in self.container_lists["ISOTOPES"]:
                helper[isotope] = []
                #
                concentration_i = self.srm_isotopes[isotope]["Concentration"]
                #
                if concentration_i > 0:
                    sensitivity_i = self.results_single["Intensity Ratio"][isotope]*(concentration_is/concentration_i)
                else:
                    sensitivity_i = 0.0
                #
                helper[isotope] = sensitivity_i
        #
        elif self.var_filetype == "SMPL":
            self.extract_data_times()
            helper_sensitivity_std = {}
            xi_opt = {}
            #
            for index, file_std in enumerate(self.container_lists["STD"]["Short"]):
                self.xi_std_time[file_std] = {}
                #
                intensity_is_bg = np.mean(
                    self.container_measurements["SELECTED"][file_std][self.var_datatype][self.var_is]["BG"])
                intensity_is_mat = np.mean(
                    self.container_measurements["SELECTED"][file_std][self.var_datatype][self.var_is]["SIG"])
                #
                if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                    intensity_is = intensity_is_mat - np.mean(intensity_is_bg)
                else:
                    intensity_is = 0.0
                #
                concentration_is = self.srm_isotopes[self.var_is]["Concentration"]
                #
                for isotope, value in self.container_measurements["SELECTED"][file_std][self.var_datatype].items():
                    if isotope not in helper_sensitivity_std:
                        xi_opt[isotope] = []
                        helper_sensitivity_std[isotope] = []
                    intensity_i_bg = np.mean(value["BG"])
                    intensity_i_mat = np.mean(value["SIG"])
                    if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                        intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                    else:
                        intensity_i = 0.0
                        # intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                    #
                    concentration_i = self.srm_isotopes[isotope]["Concentration"]
                    value = (intensity_i*concentration_is)/(intensity_is*concentration_i)
                    #
                    helper_sensitivity_std[isotope].append(value)
                    #
                    if isotope not in self.xi_std_time[file_std]:
                        self.xi_std_time[file_std][isotope] = [
                            self.std_times[file_std]["Delta"], np.mean(value.tolist())]
            for isotope in self.container_lists["ISOTOPES"]:
                xi_regr = self.calculate_regression(
                    data=self.xi_std_time, isotope=isotope, file_data=self.container_lists["STD"]["Short"])
                xi_opt[isotope].extend(xi_regr)
            #
            for isotope in self.container_lists["ISOTOPES"]:
                helper[isotope] = []
                value = xi_opt[isotope][0]*self.smpl_times[self.filename_single]["Delta"] + xi_opt[isotope][1]
                if value >= 0:
                    helper[isotope] = value
                else:
                    helper[isotope] = 0.0
        #
        return helper
    #
    def get_concentration_single(self):
        helper = {}
        #
        if self.var_filetype == "STD":
            for isotope in self.container_lists["ISOTOPES"]:
                concentration_i = self.srm_isotopes[isotope]["Concentration"]
                #
                helper[isotope] = concentration_i
        elif self.var_filetype == "SMPL":
            # concentration_is = float(self.container_files["SMPL"][self.filename_single]["IS Concentration"].get())
            index_file = self.container_lists["SMPL"]["Short"].index(self.filename_single)
            file_long = self.container_lists["SMPL"]["Long"][index_file]
            concentration_is = float(self.container_var["SMPL"][file_long]["IS Data"]["Concentration"].get())
            for isotope in self.container_lists["ISOTOPES"]:
                intensity_ratio_i = self.results_single["Intensity Ratio"][isotope]
                sensitivity_i = self.results_single["Sensitivity"][isotope]
                #
                if sensitivity_i > 0:
                    concentration_i = intensity_ratio_i*(concentration_is/sensitivity_i)
                else:
                    concentration_i = 0.0
                #
                helper[isotope] = concentration_i
        #
        return helper
    #
    def get_lod_single(self):
        helper = {}
        #
        for isotope in self.container_lists["ISOTOPES"]:
            helper[isotope] = []
            #
            n_bg = len(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["BG"])
            n_sig = len(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["SIG"])
            sensitivity_i = self.results_single["Sensitivity"][isotope]
            dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
            mean_bg_i = np.mean(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["BG"])
            error_bg_i = np.std(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][isotope]["BG"], ddof=1)
            #
            if self.filename_single in self.container_lists["STD"]["Short"]:
                var_srm = self.srm_isotopes[isotope]["SRM"]
                var_is = self.container_files[self.var_filetype][self.filename_single]["IS"].get()
                key_element = re.search("(\D+)(\d+)", var_is)
                var_is_element = key_element.group(1)
                concentration_is = self.container_lists["SRM Data"][var_srm][var_is_element]
            else:
                index_file = self.container_lists["SMPL"]["Short"].index(self.filename_single)
                file_long = self.container_lists["SMPL"]["Long"][index_file]
                concentration_is = float(self.container_var["SMPL"][file_long]["IS Data"]["Concentration"].get())
                var_is = self.container_var["SMPL"][file_long]["IS Data"]["IS"].get()
            #
            intensity_is = np.mean(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][var_is]["SIG"]) - \
                           np.mean(
                self.container_measurements["SELECTED"][self.filename_single][self.var_datatype][var_is]["BG"])
            #
            if sensitivity_i > 0:
                if self.container_var["General Settings"]["LOD Selection"].get() == 0:
                    # Pettke et al. (2012)
                    lod_value = (3.29*(mean_bg_i*dwell_time_i*n_sig*(1 + n_sig/n_bg))**0.5 + 2.71)/(
                            n_sig*dwell_time_i*sensitivity_i)*(concentration_is/intensity_is)
                elif self.container_var["General Settings"]["LOD Selection"].get() == 1:
                    # Longerich et al. (1996)
                    lod_value = (3*error_bg_i)/(sensitivity_i)*(concentration_is/intensity_is)*(
                            1/n_bg + 1/n_sig)**0.5
                #
            else:
                lod_value = 0.0
            #
            helper[isotope] = lod_value
        #
        return helper
    #
    def get_intensity_data(self):
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        helper = {}
        filetypes = ["STD", "SMPL"]
        categories = ["BACKGROUND", "BACKGROUND ERROR", "SIGNAL", "SIGNAL CORRECTED"]
        n_digits = int(self.container_var["General Settings"]["Accuracy Intensity"].get())
        #
        for filetype in filetypes:
            helper[filetype] = {}
            for category in categories:
                helper[filetype][category] = {}
        #
        for filetype in filetypes:
            #
            if filetype == "STD":
                list_files = self.container_lists[filetype]["Short"]
            elif filetype == "SMPL":
                if var_id != "Select Assemblage":
                    list_files = list(self.container_results[filetype][var_id].keys())
                    list_files.remove("ALL")
                else:
                    list_files = self.container_lists[filetype]["Short"]
            #
            for index, filename in enumerate(list_files):
                cb_file = self.container_var[filetype][self.container_lists[filetype]["Long"][index]]["Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    helper[filetype]["BACKGROUND"][filename] = {}
                    helper[filetype]["BACKGROUND ERROR"][filename] = {}
                    helper[filetype]["SIGNAL"][filename] = {}
                    helper[filetype]["SIGNAL CORRECTED"][filename] = {}
                    for isotope in self.container_lists["ISOTOPES"]:
                        var_srm_isotope = self.srm_isotopes[isotope]["SRM"]
                        #
                        if filetype == "STD":
                            var_srm_file = self.container_files["STD"][filename]["SRM"].get()
                            var_is = self.container_files[filetype][filename]["IS"].get()
                            #
                            if var_srm_file == var_srm_isotope and filetype == "STD":
                                intensity_i_bg = np.mean(
                                    self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"])
                                intensity_i_bg_error = np.std(
                                    self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"],
                                    ddof=1)
                                intensity_i_mat = np.mean(
                                    self.container_measurements["SELECTED"][filename][self.var_datatype][isotope][
                                        "SIG"])
                                #
                                if np.mean(intensity_i_mat) >= np.mean(intensity_i_bg):
                                    intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                                else:
                                    intensity_i = 0.0
                                #
                            elif var_srm_file != var_srm_isotope and isotope == var_is:
                                intensity_i_bg = np.mean(
                                    self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"])
                                intensity_i_bg_error = np.std(
                                    self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"],
                                    ddof=1)
                                intensity_i_mat = np.mean(
                                    self.container_measurements["SELECTED"][filename][self.var_datatype][isotope][
                                        "SIG"])
                                #
                                if np.mean(intensity_i_mat) >= np.mean(intensity_i_bg):
                                    intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                                else:
                                    intensity_i = 0.0
                                #
                            else:
                                intensity_i_bg = np.nan
                                intensity_i_bg_error = np.nan
                                intensity_i_mat = np.nan
                                intensity_i = np.nan
                            #
                        else:   # SMPL
                            intensity_i_bg = np.mean(
                                self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"])
                            intensity_i_bg_error = np.std(
                                self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"],
                                ddof=1)
                            intensity_i_mat = np.mean(
                                self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["SIG"])
                            #
                            if np.mean(intensity_i_mat) >= np.mean(intensity_i_bg):
                                intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                            else:
                                intensity_i = 0.0
                        #
                        helper[filetype]["BACKGROUND"][filename][isotope] = round(intensity_i_bg, n_digits)
                        helper[filetype]["BACKGROUND ERROR"][filename][isotope] = round(intensity_i_bg_error, n_digits)
                        helper[filetype]["SIGNAL"][filename][isotope] = round(intensity_i_mat, n_digits)
                        helper[filetype]["SIGNAL CORRECTED"][filename][isotope] = round(intensity_i, n_digits)
                        #
                        if isotope not in helper[filetype]["BACKGROUND"]:
                            helper[filetype]["BACKGROUND"][isotope] = []
                            helper[filetype]["BACKGROUND ERROR"][isotope] = []
                            helper[filetype]["SIGNAL"][isotope] = []
                            helper[filetype]["SIGNAL CORRECTED"][isotope] = []
                        #
                        intensity_i_bg = round(intensity_i_bg, n_digits)
                        intensity_i_bg_error = round(intensity_i_bg_error, n_digits)
                        intensity_i_mat = round(intensity_i_mat, n_digits)
                        intensity_i = round(intensity_i, n_digits)
                        #
                        if filetype == "STD":
                            if var_srm_file == var_srm_isotope:
                                helper[filetype]["BACKGROUND"][isotope].append(intensity_i_bg)
                                helper[filetype]["BACKGROUND ERROR"][isotope].append(intensity_i_bg_error)
                                helper[filetype]["SIGNAL"][isotope].append(intensity_i_mat)
                                helper[filetype]["SIGNAL CORRECTED"][isotope].append(intensity_i)
                        else:
                            helper[filetype]["BACKGROUND"][isotope].append(intensity_i_bg)
                            helper[filetype]["BACKGROUND ERROR"][isotope].append(intensity_i_bg_error)
                            helper[filetype]["SIGNAL"][isotope].append(intensity_i_mat)
                            helper[filetype]["SIGNAL CORRECTED"][isotope].append(intensity_i)
        #
        ## TESTING
        # print("TESTING: Intensity")
        # print("Filetype: Standard")
        # for file_std in self.container_lists["STD"]["Short"]:
        #     print("File:", file_std)
        #     for isotope in self.container_lists["ISOTOPES"]:
        #         print("Isotope:", isotope)
        #         print("BACKGROUND:", round(helper["STD"]["BACKGROUND"][file_std][isotope], 9))
        #         print("SIGNAL:", round(helper["STD"]["SIGNAL"][file_std][isotope], 9))
        #         print("SIGNAL CORRECTED:", round(helper["STD"]["SIGNAL CORRECTED"][file_std][isotope], 9))
        # print("")
        # print("Filetype: Sample")
        # for file_smpl in self.container_lists["SMPL"]["Short"]:
        #     print("File:", file_smpl)
        #     for isotope in self.container_lists["ISOTOPES"]:
        #         print("Isotope:", isotope)
        #         print("BACKGROUND:", round(helper["SMPL"]["BACKGROUND"][file_smpl][isotope], 9))
        #         print("Data BG:", helper["SMPL"]["BACKGROUND"][file_smpl][isotope])
        #         print("SIGNAL:", round(helper["SMPL"]["SIGNAL"][file_smpl][isotope], 9))
        #         print("Data SIG:", helper["SMPL"]["SIGNAL"][file_smpl][isotope])
        #         print("SIGNAL CORRECTED:", round(helper["SMPL"]["SIGNAL CORRECTED"][file_smpl][isotope], 9))
        #         print("Data SIG CORR:", helper["SMPL"]["SIGNAL CORRECTED"][file_smpl][isotope])
        # for filetype in filetypes:
        #     print(filetype)
        #     for isotope in self.container_lists["ISOTOPES"]:
        #         print(isotope)
        #         print("Background:",
        #               "Mean:", np.nanmean(helper[filetype]["BACKGROUND"][isotope]),
        #               "Error:", np.nanstd(helper[filetype]["BACKGROUND"][isotope], ddof=1),
        #               "Size:", len(helper[filetype]["BACKGROUND"][isotope]))
        #         print("Data BG:", helper[filetype]["BACKGROUND"][isotope])
        #         print("Signal:",
        #               "Mean:", np.nanmean(helper[filetype]["SIGNAL"][isotope]),
        #               "Error:", np.nanstd(helper[filetype]["SIGNAL"][isotope], ddof=1),
        #               "Size:", len(helper[filetype]["SIGNAL"][isotope]))
        #         print("Data SIG:", helper[filetype]["SIGNAL"][isotope])
        #         print("Signal (BG corrected):",
        #               "Mean:", np.nanmean(helper[filetype]["SIGNAL CORRECTED"][isotope]),
        #               "Error:", np.nanstd(helper[filetype]["SIGNAL CORRECTED"][isotope], ddof=1),
        #               "Size:", len(helper[filetype]["SIGNAL CORRECTED"][isotope]))
        #         print("Data SIG CORRECTED:", helper[filetype]["SIGNAL CORRECTED"][isotope])
        #     print("")
        #
        return helper
    #
    def get_intensity_ratio_data(self, intensity):
        helper = {}
        helper["BACKGROUND"] = {}
        helper["SIGNAL"] = {}
        helper["SIGNAL CORRECTED"] = {}
        n_digits = int(self.container_var["General Settings"]["Accuracy Intensity"].get())
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        #
        if self.var_filetype == "STD":
            list_files = self.container_lists[self.var_filetype]["Short"]
        elif self.var_filetype == "SMPL":
            if var_id != "Select Assemblage":
                list_files = list(self.container_results[self.var_filetype][var_id].keys())
                list_files.remove("ALL")
            else:
                list_files = self.container_lists[self.var_filetype]["Short"]
        #
        for index, filename in enumerate(list_files):
            cb_file = self.container_var[self.var_filetype][self.container_lists[self.var_filetype]["Long"][index]][
                "Checkbox"].get()
            if isinstance(cb_file, str) == True:
                cb_file = int(cb_file)
            if cb_file == 1:
                helper["BACKGROUND"][filename] = {}
                helper["SIGNAL"][filename] = {}
                helper["SIGNAL CORRECTED"][filename] = {}
                var_is = self.container_files[self.var_filetype][filename]["IS"].get()
                #
                intensity_is_bg = intensity[self.var_filetype]["BACKGROUND"][filename][var_is]
                intensity_is_mat = intensity[self.var_filetype]["SIGNAL"][filename][var_is]
                intensity_is = intensity[self.var_filetype]["SIGNAL CORRECTED"][filename][var_is]
                #
                for isotope in self.container_lists["ISOTOPES"]:
                    #
                    if isotope not in helper["BACKGROUND"]:
                        helper["BACKGROUND"][isotope] = []
                        helper["SIGNAL"][isotope] = []
                        helper["SIGNAL CORRECTED"][isotope] = []
                    #
                    intensity_i_bg = intensity[self.var_filetype]["BACKGROUND"][filename][isotope]
                    intensity_i_mat = intensity[self.var_filetype]["SIGNAL"][filename][isotope]
                    intensity_i = intensity[self.var_filetype]["SIGNAL CORRECTED"][filename][isotope]
                    #
                    if math.isnan(intensity_i_bg) == False:
                        ratio_bg = round(intensity_i_bg/intensity_is_bg, int(1.5*n_digits))
                        ratio_sig = round(intensity_i_mat/intensity_is_mat, int(1.5*n_digits))
                        ratio_sigcorr = round(intensity_i/intensity_is, int(1.5*n_digits))
                    else:
                        ratio_bg = np.nan
                        ratio_sig = np.nan
                        ratio_sigcorr = np.nan
                    #
                    helper["BACKGROUND"][filename][isotope] = ratio_bg
                    helper["SIGNAL"][filename][isotope] = ratio_sig
                    helper["SIGNAL CORRECTED"][filename][isotope] = ratio_sigcorr
                    #
                    helper["BACKGROUND"][isotope].append(ratio_bg)
                    helper["SIGNAL"][isotope].append(ratio_sig)
                    helper["SIGNAL CORRECTED"][isotope].append(ratio_sigcorr)
        #
        ## TESTING
        # print("TESTING: Intensity Ratio")
        # for isotope in self.container_lists["ISOTOPES"]:
        #     print(isotope+"/"+self.var_is)
        #     print("Background:", "Mean:", np.mean(helper["BACKGROUND"][isotope]),
        #           np.std(helper["BACKGROUND"][isotope], ddof=1))
        #     print("Signal:", "Mean:", np.mean(helper["SIGNAL"][isotope]),
        #           np.std(helper["SIGNAL"][isotope], ddof=1))
        #     print("Signal (BG corrected):", "Mean:", np.mean(helper["SIGNAL CORRECTED"][isotope]),
        #           np.std(helper["SIGNAL CORRECTED"][isotope], ddof=1))
        #
        return helper
    #
    def get_sensitivity_data(self, intensity):
        helper = {}
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        #
        if self.var_filetype == "STD":
            list_files = self.container_lists[self.var_filetype]["Short"]
        elif self.var_filetype == "SMPL":
            if var_id != "Select Assemblage":
                list_files = list(self.container_results[self.var_filetype][var_id].keys())
                list_files.remove("ALL")
            else:
                list_files = self.container_lists[self.var_filetype]["Short"]
        #
        if self.var_filetype == "STD":
            #
            self.extract_data_times()
            #
            helper["Times"] = {}
            helper["Times"]["STD"] = self.std_times
            helper["Times"]["SMPL"] = self.smpl_times
            #
            for index, filename in enumerate(list_files):
                cb_file = self.container_var["STD"][self.container_lists["STD"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    helper[filename] = {}
                    #
                    var_srm = self.container_files["STD"][filename]["SRM"].get()
                    list_element_srm = list(self.container_lists["SRM Data"][var_srm].keys())
                    var_is = self.container_files["STD"][filename]["IS"].get()
                    var_srm_is = self.container_files["SRM"][var_is].get()
                    #
                    key_element = re.search("(\D+)(\d+)", var_is)
                    var_is_element = key_element.group(1)
                    #
                    concentration_is = self.srm_data[var_srm][var_is_element]
                    concentration_is = self.container_lists["SRM Data"][var_srm][var_is_element]
                    self.concentration_is_std = concentration_is
                    intensity_is = intensity["STD"]["SIGNAL CORRECTED"][filename][var_is]
                    #
                    for isotope in self.container_lists["ISOTOPES"]:
                        if isotope not in helper:
                                helper[isotope] = []
                        #
                        var_srm_i = self.container_files["SRM"][isotope].get()
                        #
                        if var_srm_i == var_srm:
                            key_element = re.search("(\D+)(\d+)", isotope)
                            var_i_element = key_element.group(1)
                            #
                            var_srm_is = self.container_files["SRM"][var_is].get()
                            #
                            concentration_is = self.container_lists["SRM Data"][var_srm_i][var_is_element]
                            #
                            if var_i_element in self.container_lists["SRM Data"][var_srm_i]:
                                concentration_i = self.container_lists["SRM Data"][var_srm_i][var_i_element]
                            else:
                                concentration_i = 0.0
                            #
                            intensity_i = intensity["STD"]["SIGNAL CORRECTED"][filename][isotope]
                            #
                            intensity_ratio = intensity_i/intensity_is
                            #
                            if var_i_element in self.container_lists["SRM Data"][var_srm_i]:
                                concentration_ratio = concentration_is/concentration_i
                            else:
                                concentration_ratio = 0.0
                            #
                            if math.isnan(intensity_i) == False:
                                sensitivity_i = intensity_ratio*concentration_ratio
                            else:
                                sensitivity_i = np.nan
                            #
                        else:
                            if isotope == var_is:
                                sensitivity_i = 1.0
                            else:
                                sensitivity_i = np.nan
                        #
                        helper[filename][isotope] = sensitivity_i
                        helper[isotope].append(sensitivity_i)
            #
        elif self.var_filetype == "SMPL":
            helper["Optimized"] = {}
            helper["Times"] = {}
            helper["Drift Change"] = {}
            helper_sensitivity_std = {}
            self.xi_opt = {}
            #
            self.extract_data_times()
            #
            helper["Times"]["STD"] = self.std_times
            helper["Times"]["SMPL"] = self.smpl_times
            list_valid_std = []
            list_valid_smpl = []
            #
            for index, file_std in enumerate(self.container_lists["STD"]["Short"]):
                cb_file = self.container_var["STD"][self.container_lists["STD"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    list_valid_std.append(file_std)
                    #
                    self.xi_std_time[file_std] = {}
                    helper_sensitivity_std[file_std] = {}
                    var_srm = self.container_files["STD"][file_std]["SRM"].get()
                    list_element_srm = list(self.container_lists["SRM Data"][var_srm].keys())
                    var_is = self.container_files["STD"][file_std]["IS"].get()
                    var_srm_is = self.container_files["SRM"][var_is].get()
                    #
                    key_element = re.search("(\D+)(\d+)", var_is)
                    var_is_element = key_element.group(1)
                    #
                    if var_is_element in self.container_lists["SRM Data"][var_srm]:
                        concentration_is = self.container_lists["SRM Data"][var_srm][var_is_element]
                    #
                    intensity_is_bg = np.mean(
                        self.container_measurements["SELECTED"][file_std][self.var_datatype][var_is]["BG"])
                    intensity_is_mat = np.mean(
                        self.container_measurements["SELECTED"][file_std][self.var_datatype][var_is]["SIG"])
                    #
                    if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                        intensity_is = intensity_is_mat - np.mean(intensity_is_bg)
                    else:
                        intensity_is = 0.0
                        # intensity_is = intensity_is_bg - np.mean(intensity_is_mat)
                    #
                    self.concentration_is_std = concentration_is
                    #
                    for isotope, value in self.container_measurements["SELECTED"][file_std][self.var_datatype].items():
                        if isotope in self.isotope_by_srm[var_srm]:
                            key_element = re.search("(\D+)(\d+)", isotope)
                            var_i_element = key_element.group(1)
                            #
                            if var_i_element in list_element_srm:
                                if isotope not in helper_sensitivity_std:
                                    self.xi_opt[isotope] = []
                                    helper_sensitivity_std[isotope] = []
                                    helper_sensitivity_std[file_std][isotope] = {}
                                #
                                intensity_i_bg = np.mean(value["BG"])
                                intensity_i_mat = np.mean(value["SIG"])
                                #
                                if np.mean(intensity_is_mat) >= np.mean(intensity_is_bg):
                                    intensity_i = intensity_i_mat - np.mean(intensity_i_bg)
                                else:
                                    intensity_i = 0.0
                                    # intensity_i = intensity_i_bg - np.mean(intensity_i_mat)
                                #
                                key_element = re.search("(\D+)(\d+)", isotope)
                                var_i_element = key_element.group(1)
                                #
                                var_srm_i = self.container_files["SRM"][isotope].get()
                                var_srm_is = self.container_files["SRM"][var_is].get()
                                #
                                if isotope in self.isotope_by_srm[var_srm_i]:
                                    if var_srm_i != var_srm_is:
                                        concentration_is = self.container_lists["SRM Data"][var_srm_i][var_is_element]
                                        concentration_i = self.container_lists["SRM Data"][var_srm_i][var_i_element]
                                    else:
                                        concentration_i = self.container_lists["SRM Data"][var_srm_is][var_i_element]
                                    #
                                    value = (intensity_i*concentration_is)/(intensity_is*concentration_i)
                                    #
                                    helper_sensitivity_std[isotope].append(value)
                                    helper_sensitivity_std[file_std][isotope] = {
                                        "Time": self.std_times[file_std]["Delta"],
                                        "Sensitivity": value}
                                    #
                                    if isotope not in self.xi_std_time[file_std]:
                                        if self.container_var["General Settings"]["Sensitivity Drift"].get() == 0:
                                            self.xi_std_time[file_std][isotope] = [
                                                self.std_times[file_std]["Delta"], np.mean(value.tolist())]
                                        else:
                                            self.xi_std_time[file_std][isotope] = [
                                                self.std_times[file_std]["Start"], np.mean(value.tolist())]
                            else:
                                if isotope not in helper_sensitivity_std:
                                    self.xi_opt[isotope] = []
                                    helper_sensitivity_std[isotope] = []
                                    helper_sensitivity_std[file_std][isotope] = {}
                                #
                                value = 0.0
                                #
                                helper_sensitivity_std[isotope].append(value)
                                helper_sensitivity_std[file_std][isotope] = {
                                    "Time": self.std_times[file_std]["Delta"],
                                    "Sensitivity": value}
                                #
                                if isotope not in self.xi_std_time[file_std]:
                                    if self.container_var["General Settings"]["Sensitivity Drift"].get() == 0:
                                        self.xi_std_time[file_std][isotope] = [self.std_times[file_std]["Delta"], value]
                                    else:
                                        self.xi_std_time[file_std][isotope] = [self.std_times[file_std]["Start"], value]
            #
            for isotope in self.container_lists["ISOTOPES"]:
                try:
                    helper["Drift Change"][isotope] = (helper_sensitivity_std[isotope][-1]/
                                                       helper_sensitivity_std[isotope][0] - 1)*100
                except:
                    helper["Drift Change"][isotope] = 0.0
            #
            # for key, value in self.xi_std_time.items():
            #     print(key, value)
            for isotope in self.container_lists["ISOTOPES"]:
                self.xi_regr = self.calculate_regression(
                    data=self.xi_std_time, isotope=isotope, file_data=list_valid_std)
                self.xi_opt[isotope].extend(self.xi_regr)
            #
            for index, file_smpl in enumerate(list_files):
                cb_file = self.container_var["SMPL"][self.container_lists["SMPL"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    list_valid_smpl.append(file_smpl)
                    #
                    helper[file_smpl] = {}
                    for isotope in self.container_lists["ISOTOPES"]:
                        if isotope not in helper:
                            helper[isotope] = []
                        #
                        if self.container_var["General Settings"]["Sensitivity Drift"].get() == 0:
                            value = self.xi_opt[isotope][0]*self.smpl_times[file_smpl]["Delta"] + self.xi_opt[isotope][1]
                        else:
                            value = self.xi_opt[isotope][0]*self.smpl_times[file_smpl]["Start"] + self.xi_opt[isotope][
                                1]
                        #
                        if value >= 0:
                            helper[file_smpl][isotope] = value
                            helper[isotope].append(value)
                            helper["Optimized"][isotope] = self.xi_opt[isotope]
                        else:
                            helper[file_smpl][isotope] = 0.0
                            helper[isotope].append(0.0)
                            helper["Optimized"] = self.xi_opt[isotope]
        #
        ## TESTING
        # print("TESTING: Sensitivity")
        # print("Filetype:", self.var_filetype)
        # for isotope in self.container_lists["ISOTOPES"]:
        #     print(isotope)
        #     print("Dataset size:", len(helper[isotope]))
        #     print("Mean:", np.mean(helper[isotope]), np.std(helper[isotope], ddof=1))
        # for key, value in helper["Times"].items():
        #     print(key, value)
        #
        return helper
    #
    def get_concentration_data(self, intensity, sensitivity):
        helper = {}
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        #
        if self.var_filetype == "STD":
            list_files = self.container_lists[self.var_filetype]["Short"]
        elif self.var_filetype == "SMPL":
            if var_id != "Select Assemblage":
                list_files = list(self.container_results[self.var_filetype][var_id].keys())
                list_files.remove("ALL")
            else:
                list_files = self.container_lists[self.var_filetype]["Short"]
        #
        if self.var_filetype == "STD":
            for index, file_std in enumerate(list_files):
                cb_file = self.container_var["STD"][self.container_lists["STD"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    helper[file_std] = {}
                    var_srm = self.container_files["STD"][file_std]["SRM"].get()
                    #
                    list_element_srm = list(self.container_lists["SRM Data"][var_srm].keys())
                    #
                    for isotope in self.container_lists["ISOTOPES"]:
                        if isotope not in helper:
                            helper[isotope] = []
                        #
                        key_element = re.search("(\D+)(\d+)", isotope)
                        var_i_element = key_element.group(1)
                        #
                        var_srm_i = self.container_files["SRM"][isotope].get()
                        #
                        if var_i_element in list(self.container_lists["SRM Data"][var_srm].keys()):
                            concentration_i = self.container_lists["SRM Data"][var_srm][var_i_element]
                        else:
                            concentration_i = np.nan
                        #
                        if concentration_i >= 0:
                            helper[file_std][isotope] = concentration_i
                            helper[isotope].append(concentration_i)
                        elif concentration_i < 0:
                            helper[file_std][isotope] = 0.0
                            helper[isotope].append(0.0)
                        else:
                            helper[file_std][isotope] = concentration_i
                            helper[isotope].append(concentration_i)
            #
        elif self.var_filetype == "SMPL":
            for index, file_smpl in enumerate(list_files):
                cb_file = self.container_var["SMPL"][self.container_lists["SMPL"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    helper[file_smpl] = {}
                    #
                    # concentration_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
                    concentration_is = float(self.container_var["SMPL"][self.container_lists["SMPL"]["Long"][index]][
                                                 "IS Data"]["Concentration"].get())
                    self.concentration_is_smpl = concentration_is
                    var_is = self.container_files["SMPL"][file_smpl]["IS"].get()
                    var_srm_is = self.container_files["SRM"][var_is].get()
                    intensity_is = intensity[self.var_filetype]["SIGNAL CORRECTED"][file_smpl][var_is]
                    #
                    for isotope in self.container_lists["ISOTOPES"]:
                        var_srm_i = self.container_files["SRM"][isotope].get()
                        if isotope not in helper:
                            helper[isotope] = []
                        #
                        intensity_i = intensity[self.var_filetype]["SIGNAL CORRECTED"][file_smpl][isotope]
                        sensitivity_i = sensitivity[file_smpl][isotope]
                        #
                        if sensitivity_i > 0:
                            concentration_i = (intensity_i/intensity_is)*(concentration_is/sensitivity_i)
                        else:
                            concentration_i = 0.0
                        #
                        if concentration_i >= 0:
                            helper[file_smpl][isotope] = concentration_i
                            helper[isotope].append(concentration_i)
                        else:
                            helper[file_smpl][isotope] = 0.0
                            helper[isotope].append(0.0)
        #
        ## TESTING
        # print("TESTING: Concentration")
        # for isotope in self.container_lists["ISOTOPES"]:
        #     print(isotope)
        #     print("Dataset size:", len(helper[isotope]))
        #     print("Mean:", np.mean(helper[isotope]), np.std(helper[isotope], ddof=1))
        #
        return helper
    #
    def get_rsf_data(self, intensity, sensitivity):
        helper = {}
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        #
        if self.var_filetype == "STD":
            list_files = self.container_lists[self.var_filetype]["Short"]
        elif self.var_filetype == "SMPL":
            if var_id != "Select Assemblage":
                list_files = list(self.container_results[self.var_filetype][var_id].keys())
                list_files.remove("ALL")
            else:
                list_files = self.container_lists[self.var_filetype]["Short"]
        #
        if self.var_filetype == "STD":
            for index, file_std in enumerate(list_files):
                cb_file = self.container_var["STD"][self.container_lists["STD"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    helper[file_std] = {}
                    for isotope in self.container_lists["ISOTOPES"]:
                        if isotope not in helper:
                            helper[isotope] = []
                        #
                        var_srm = self.container_files["STD"][file_std]["SRM"].get()
                        var_srm_isotope = self.srm_isotopes[isotope]["SRM"]
                        #
                        key_element = re.search("(\D+)(\d+)", isotope)
                        var_i_element = key_element.group(1)
                        #
                        key_element_is = re.search("(\D+)(\d+)", self.var_is)
                        var_is_element = key_element_is.group(1)
                        #
                        sensitivity_i = sensitivity[file_std][isotope]
                        intensity_i_std = intensity["STD"]["SIGNAL CORRECTED"][file_std][isotope]
                        intensity_is_std = intensity["STD"]["SIGNAL CORRECTED"][file_std][self.var_is]
                        #
                        if var_srm == var_srm_isotope:
                            if var_i_element in self.container_lists["SRM Data"][var_srm]:
                                concentration_i_std = self.container_lists["SRM Data"][var_srm][var_i_element]
                            else:
                                concentration_i_std = 0.0
                            #
                            concentration_is_std = self.container_lists["SRM Data"][var_srm][var_is_element]
                        else:
                            if var_i_element in self.container_lists["SRM Data"][var_srm_isotope]:
                                concentration_i_std = self.container_lists["SRM Data"][var_srm_isotope][var_i_element]
                            else:
                                concentration_i_std = 0.0
                            #
                            concentration_is_std = self.container_lists["SRM Data"][var_srm_isotope][var_is_element]
                        #
                        if math.isnan(sensitivity_i) == False:
                            try:
                                rsf_value = sensitivity_i*(concentration_i_std)/(intensity_i_std)*(
                                    intensity_is_std)/(concentration_is_std)
                            except:
                                rsf_value = np.nan
                        else:
                            rsf_value = np.nan
                        #
                        helper[file_std][isotope] = rsf_value
                        helper[isotope].append(rsf_value)
            #
        elif self.var_filetype == "SMPL":
            intensity_is_std = np.mean(intensity["STD"]["SIGNAL CORRECTED"][self.var_is])
            intensity_is_smpl = np.mean(intensity["SMPL"]["SIGNAL CORRECTED"][self.var_is])
            #
            for index, file_smpl in enumerate(list_files):
                concentration_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
                #
                cb_file = self.container_var["SMPL"][self.container_lists["SMPL"]["Long"][index]][
                    "Checkbox"].get()
                if isinstance(cb_file, str) == True:
                    cb_file = int(cb_file)
                if cb_file == 1:
                    helper[file_smpl] = {}
                    for isotope in self.container_lists["ISOTOPES"]:
                        if isotope not in helper:
                            helper[isotope] = []
                        #
                        intensity_i_std = np.mean(intensity["STD"]["SIGNAL CORRECTED"][isotope])
                        var_srm_isotope = self.srm_isotopes[isotope]["SRM"]
                        #
                        key_element = re.search("(\D+)(\d+)", isotope)
                        var_i_element = key_element.group(1)
                        #
                        if var_i_element in self.container_lists["SRM Data"][var_srm_isotope]:
                            concentration_i = self.container_lists["SRM Data"][var_srm_isotope][var_i_element]
                        else:
                            concentration_i = 0.0
                        #
                        sensitivity_i = sensitivity[file_smpl][isotope]
                        #
                        # rsf_value = (intensity_is_smpl/intensity_is_std)*(
                        #         self.concentration_is_std/self.concentration_is_smpl)
                        rsf_value = sensitivity_i*(concentration_i)/(intensity_i_std)*(intensity_is_smpl)/(concentration_is)
                        #
                        helper[file_smpl][isotope] = rsf_value
                        helper[isotope].append(rsf_value)
        #
        ## TESTING
        # print("TESTING: RSF")
        # for isotope in self.container_lists["ISOTOPES"]:
        #     print(isotope)
        #     print(isotope, helper[isotope])
        #     print("Mean:", np.nanmean(helper[isotope]), np.nanstd(helper[isotope], ddof=1))
        #
        return helper
    #
    def get_lod_data(self, intensity, sensitivity):
        helper = {}
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        #
        if self.var_filetype == "STD":
            list_files = self.container_lists[self.var_filetype]["Short"]
        elif self.var_filetype == "SMPL":
            if var_id != "Select Assemblage":
                list_files = list(self.container_results[self.var_filetype][var_id].keys())
                list_files.remove("ALL")
            else:
                list_files = self.container_lists[self.var_filetype]["Short"]
        #
        for index, filename in enumerate(list_files):
            cb_file = self.container_var[self.var_filetype][self.container_lists[self.var_filetype]["Long"][index]][
                "Checkbox"].get()
            if isinstance(cb_file, str) == True:
                cb_file = int(cb_file)
            if cb_file == 1:
                helper[filename] = {}
                #
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                            helper[isotope] = []
                    #
                    if isotope in sensitivity[filename]:
                        if self.var_filetype == "STD":  # STANDARD FILES
                            var_srm = self.container_files["STD"][filename]["SRM"].get()
                            key_element = re.search("(\D+)(\d+)", isotope)
                            var_i_element = key_element.group(1)
                            var_srm_i = self.container_files["SRM"][isotope].get()
                            var_is = self.container_files["STD"][filename]["IS"].get()
                            key_element = re.search("(\D+)(\d+)", var_is)
                            var_is_element = key_element.group(1)
                            concentration_is = self.container_lists["SRM Data"][var_srm][var_is_element]
                            intensity_is = intensity[self.var_filetype]["SIGNAL CORRECTED"][filename][var_is]
                            #
                            if var_srm_i == var_srm:
                                mean_bg_i = intensity[self.var_filetype]["BACKGROUND"][filename][isotope]
                                error_bg_i = intensity[self.var_filetype]["BACKGROUND ERROR"][filename][isotope]
                                n_bg = len(self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"])
                                n_sig = len(self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["SIG"])
                                sensitivity_i = sensitivity[filename][isotope]
                                dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                                #
                                if self.container_var["General Settings"]["LOD Selection"].get() == 0:
                                    # Pettke et al. (2012)
                                    if sensitivity_i > 0:
                                        lod_value = (3.29*(mean_bg_i*dwell_time_i*n_sig*(1 + n_sig/n_bg))**0.5 + 2.71)/(
                                                n_sig*dwell_time_i*sensitivity_i)*(concentration_is/intensity_is)
                                    else:
                                        lod_value = 0.0
                                elif self.container_var["General Settings"]["LOD Selection"].get() == 1:
                                    # Longerich et al. (1996)
                                    if sensitivity_i > 0:
                                        lod_value = (3*error_bg_i)/(sensitivity_i)*(concentration_is/intensity_is)*(
                                                1/n_bg + 1/n_sig)**0.5
                                    else:
                                        lod_value = 0.0
                                #
                            else:
                                lod_value = np.nan
                            #
                        else:   # SAMPLE FILES
                            var_is = self.container_files["SMPL"][filename]["IS"].get()
                            # concentration_is = float(self.container_files["SMPL"][filename]["IS Concentration"].get())
                            concentration_is = float(self.container_var["SMPL"][self.container_lists["SMPL"]["Long"][
                                index]]["IS Data"]["Concentration"].get())
                            intensity_is = intensity[self.var_filetype]["SIGNAL CORRECTED"][filename][var_is]
                            #
                            mean_bg_i = intensity[self.var_filetype]["BACKGROUND"][filename][isotope]
                            error_bg_i = intensity[self.var_filetype]["BACKGROUND ERROR"][filename][isotope]
                            n_bg = len(self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["BG"])
                            n_sig = len(self.container_measurements["SELECTED"][filename][self.var_datatype][isotope]["SIG"])
                            sensitivity_i = sensitivity[filename][isotope]
                            dwell_time_i = float(self.container_var["dwell_times"]["Entry"][isotope].get())
                            #
                            if self.container_var["General Settings"]["LOD Selection"].get() == 0:
                                # Pettke et al. (2012)
                                if sensitivity_i > 0:
                                    lod_value = (3.29*(mean_bg_i*dwell_time_i*n_sig*(1 + n_sig/n_bg))**0.5 + 2.71)/(
                                            n_sig*dwell_time_i*sensitivity_i)*(concentration_is/intensity_is)
                                else:
                                    lod_value = 0.0
                                #
                            elif self.container_var["General Settings"]["LOD Selection"].get() == 1:
                                # Longerich et al. (1996)
                                if sensitivity_i > 0:
                                    lod_value = (3*error_bg_i)/(sensitivity_i)*(concentration_is/intensity_is)*(
                                            1/n_bg + 1/n_sig)**0.5
                                else:
                                    lod_value = 0.0
                        #
                    else:
                        lod_value = np.nan
                    #
                    helper[filename][isotope] = lod_value
                    helper[isotope].append(lod_value)
                #
        ## TESTING
        # print("TESTING: LOD")
        # for isotope in self.container_lists["ISOTOPES"]:
        #     print(isotope)
        #     print("Mean:", np.mean(helper[isotope]), "Error:", np.std(helper[isotope], ddof=1))
        #
        return helper
    #
    def get_normalized_sensitivity(self, sensitivity, intensity, concentration):
        helper = {}
        var_id = self.container_var["ma_datareduction"]["Option ID"].get()
        #
        if self.var_filetype == "STD":
            list_files = self.container_lists[self.var_filetype]["Short"]
        elif self.var_filetype == "SMPL":
            if var_id != "Select Assemblage":
                list_files = list(self.container_results[self.var_filetype][var_id].keys())
                list_files.remove("ALL")
            else:
                list_files = self.container_lists[self.var_filetype]["Short"]
        #
        if self.var_filetype == "STD":
            for file_std in list_files:
                if file_std not in helper:
                    helper[file_std] = {}
                #
                var_is = self.container_files["STD"][file_std]["IS"].get()
                #
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                        helper[file_std][isotope] = 0
                    #
                    sensitivity_i = sensitivity[file_std][isotope]
                    intensity_i = intensity["STD"]["SIGNAL CORRECTED"][file_std][var_is]
                    concentration_i = concentration[file_std][var_is]
                    #
                    sensitivity_norm_i = sensitivity_i*(intensity_i/concentration_i)
                    #
                    helper[isotope].append(sensitivity_norm_i)
                    helper[file_std][isotope] = sensitivity_norm_i
        #
        elif self.var_filetype == "SMPL":
            for file_smpl in list_files:
                if file_smpl not in helper:
                    helper[file_smpl] = {}
                #
                var_is = self.container_files["SMPL"][file_smpl]["IS"].get()
                #
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                        helper[file_smpl][isotope] = 0
                    #
                    sensitivity_i = sensitivity[file_smpl][isotope]
                    intensity_i = intensity["SMPL"]["SIGNAL CORRECTED"][file_smpl][var_is]
                    concentration_i = concentration[file_smpl][var_is]
                    #
                    sensitivity_norm_i = sensitivity_i*(intensity_i/concentration_i)
                    #
                    helper[isotope].append(sensitivity_norm_i)
                    helper[file_smpl][isotope] = sensitivity_norm_i
        #
        return helper
    #
    def calculate_all_parameters(self):
        results = {}
        categories = ["intensity", "intensity ratio", "sensitivity", "concentration", "RSF", "LOD"]
        categories_data = ["RAW", "SMOOTHED"]
        for category in categories:
            results[category] = None
        #
        intensity = self.get_intensity_data()
        intensity_ratio = self.get_intensity_ratio_data(intensity=intensity)
        sensitivity = self.get_sensitivity_data(intensity=intensity)
        concentration = self.get_concentration_data(intensity=intensity, sensitivity=sensitivity)
        rsf = self.get_rsf_data(intensity=intensity, sensitivity=sensitivity)
        lod = self.get_lod_data(intensity=intensity, sensitivity=sensitivity)
        sensitivity_norm = self.get_normalized_sensitivity(sensitivity=sensitivity, intensity=intensity,
                                                           concentration=concentration)
        #
        results["intensity"] = intensity
        results["intensity ratio"] = intensity_ratio
        results["sensitivity"] = sensitivity
        results["concentration"] = concentration
        results["RSF"] = rsf
        results["LOD"] = lod
        results["sensitivity normalized"] = sensitivity_norm
        #
        # results_all = {}
        # results_all["STD"] = {}
        # results_all["SMPL"] = {}
        # for category in categories:
        #     results_all["STD"][category] = {}
        #     for category_data in categories_data:
        #         results_all["STD"][category][category_data] = {}
        #
        return results
    #
    def calculate_all_parameters_single(self, filename, data_section):
        self.filename_single = filename
        self.data_section = data_section
        self.results_single = {}
        categories = ["Intensity", "Intensity Ratio", "Sensitivity", "Concentration", "LOD"]
        #
        for category in categories:
            self.results_single[category] = None
        #
        intensity = self.get_intensity_single()
        self.results_single["Intensity"] = intensity
        intensity_ratio = self.get_intensity_ratio_single()
        self.results_single["Intensity Ratio"] = intensity_ratio
        sensitivity = self.get_sensitivity_single()
        self.results_single["Sensitivity"] = sensitivity
        concentration = self.get_concentration_single()
        self.results_single["Concentration"] = concentration
        lod = self.get_lod_single()
        self.results_single["LOD"] = lod
        #
        return self.results_single
    #
    def extract_data_times(self):
        self.std_times = {}
        dates_0, times_0 = Data(filename=self.container_lists["STD"]["Long"][0]).import_as_list()
        if self.container_var["General Settings"]["Sensitivity Drift"].get() == 0:
            t_start_0 = datetime.timedelta(
                hours=int(times_0[0][0]), minutes=int(times_0[0][1]), seconds=int(times_0[0][2]))
        else:
            t_start_0 = int(times_0[0][0]) + int(times_0[0][1])/60
        #
        for file in self.container_lists["STD"]["Long"]:
            parts = file.split("/")
            self.std_times[parts[-1]] = {}
            dates, times = Data(filename=file).import_as_list()
            if self.container_var["General Settings"]["Sensitivity Drift"].get() == 0:
                t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
                t_delta_0 = (t_start - t_start_0).total_seconds()
                self.std_times[parts[-1]]["Start"] = t_start.total_seconds()
                self.std_times[parts[-1]]["Delta"] = t_delta_0
            else:
                t_start = int(times[0][0]) + int(times[0][1])/60
                t_delta_0 = t_start - t_start_0
                self.std_times[parts[-1]]["Start"] = round(t_start, 4)
                self.std_times[parts[-1]]["Delta"] = round(t_delta_0, 4)
        #
        self.smpl_times = {}
        for file in self.container_lists["SMPL"]["Long"]:
            parts = file.split("/")
            self.smpl_times[parts[-1]] = {}
            dates, times = Data(filename=file).import_as_list()
            if self.container_var["General Settings"]["Sensitivity Drift"].get() == 0:
                t_start = datetime.timedelta(hours=int(times[0][0]), minutes=int(times[0][1]), seconds=int(times[0][2]))
                t_delta_0 = (t_start - t_start_0).total_seconds()
                self.smpl_times[parts[-1]]["Start"] = t_start.total_seconds()
                self.smpl_times[parts[-1]]["Delta"] = t_delta_0
            else:
                t_start = int(times[0][0]) + int(times[0][1])/60
                t_delta_0 = t_start - t_start_0
                self.smpl_times[parts[-1]]["Start"] = round(t_start, 4)
                self.smpl_times[parts[-1]]["Delta"] = round(t_delta_0, 4)
        #
    #
    def calculate_regression(self, data, isotope, file_data):
        x_data = []
        y_data = []
        for file in file_data:
            if file in data:
                if isotope in data[file]:
                    x_data.append(data[file][isotope][0])
                    y_data.append(data[file][isotope][1])
        #
        A = np.vstack([x_data, np.ones(len(x_data))]).T
        m, c = np.linalg.lstsq(A, y_data, rcond=None)[0]  # m*x + c
        results = [m, c]
        #
        return results