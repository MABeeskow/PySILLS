#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		fi_method_matrix_only_tracer.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		22.08.2022

#-----------------------------------------------

## MODULES
import numpy as np
import re

class Name:
    #
    def __init__(self):
        name = "Matrix-only Tracer"

class Method:
    #
    def __init__(self, container_measurements, container_lists, container_files, var_is, var_datatype,
                 concentration_host_hostonly, concentration_host_is, host_isotope):
        self.container_measurements = container_measurements
        self.container_lists = container_lists
        self.container_files = container_files
        self.var_is = var_is
        self.var_datatype = var_datatype
        self.concentration_host_hostonly = concentration_host_hostonly
        self.concentration_host_is = concentration_host_is
        self.host_isotope = host_isotope
    #
    def calculate_ratio_R(self, intensity, host_isotope):
        helper = []
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_mix_hostonly = np.mean(intensity["MIX"][file_smpl][host_isotope])
            intensity_host_hostonly = np.mean(intensity["MATRIX CORRECTED"][file_smpl][host_isotope])
            #
            value = intensity_mix_hostonly/intensity_host_hostonly
            #
            helper.append(value)
            #
        ## TESTING
        # print("Testing: Ratio R")
        # print("Mean:", np.mean(helper), "Error:", np.std(helper, ddof=1))
        #
        return helper
    #
    def calculate_ratio_a(self, intensity, sensitivity, host_isotope):
        helper = []
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_mix_hostonly = np.mean(intensity["MIX"][file_smpl][host_isotope])
            intensity_mix_is = np.mean(intensity["MIX"][file_smpl][self.var_is])
            sensitivity_hostonly = np.mean(sensitivity[host_isotope])
            #
            value = (intensity_mix_hostonly)/(sensitivity_hostonly*intensity_mix_is)
            #
            helper.append(value)
        #
        ## TESTING
        # print("Testing: Ratio a")
        # print("Mean:", np.mean(helper), "Error:", np.std(helper, ddof=1))
        #
        return helper
    #
    def calculate_ratio_x(self, ratio_a, sensitivity, intensity, calculation_via_a=True):
        helper = []
        #
        concentration_host_hostonly = self.concentration_host_hostonly
        concentration_host_is = self.concentration_host_is
        file_smpl = self.container_lists["SMPL"]["Short"][0]
        concentration_incl_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
        #
        if calculation_via_a == True:
            for a in ratio_a:
                value = (concentration_host_hostonly - a*concentration_host_is)/(
                        concentration_host_hostonly - a*(concentration_host_is - concentration_incl_is))
                #
                helper.append(value)
        else:
            helper_2 = {}
            helper_2["I(M,IS)"] = []
            helper_2["I(M,HO)"] = []
            sensitivity_ho = np.mean(sensitivity[self.host_isotope])
            for file_smpl in self.container_lists["SMPL"]["Short"]:
                intensity_mix_is = np.mean(intensity["MIX"][file_smpl][self.var_is])
                intensity_mix_ho = np.mean(intensity["MIX"][file_smpl][self.host_isotope])
                #
                helper_2["I(M,IS)"].append(intensity_mix_is)
                helper_2["I(M,HO)"].append(intensity_mix_ho)
            #
            intensity_mix_is = np.mean(helper_2["I(M,IS)"])
            intensity_mix_ho = np.mean(helper_2["I(M,HO)"])
            #
            value = (sensitivity_ho*intensity_mix_is*concentration_host_hostonly
                     - intensity_mix_ho*concentration_host_is)/(
                    sensitivity_ho*intensity_mix_is*concentration_host_hostonly - intensity_mix_ho*(
                    concentration_host_is - concentration_incl_is))
            #
            helper.append(value)
        #
        ## TESTING
        # print("Testing: Ratio x")
        # print("Mean:", np.mean(helper), "Error:", np.std(helper, ddof=1))
        #
        return helper
    #
    def calculate_intensity_smpl(self, intensity_mat, intensity_mixed, host_isotope):
        #
        intensity_ratio_ri = {}
        intensity_sample = {}
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_ratio_ri[file_smpl] = np.mean(intensity_mixed[file_smpl][host_isotope])\
                                            /np.mean(intensity_mat[file_smpl][host_isotope])
            intensity_sample[file_smpl] = {}
            for isotope in self.container_lists["ISOTOPES"]:
                intensity_sample[file_smpl][isotope] = intensity_mixed[file_smpl][isotope] \
                                                       - intensity_ratio_ri[file_smpl]\
                                                       *np.mean(intensity_mat[file_smpl][isotope])
        #
        ## TESTING
        # print("RI:", intensity_ratio_ri)
        # print("Intensity (SMPL):", intensity_sample)
        #
        return intensity_sample
    #
    def calculate_concentration_smpl(self, intensity_sample, sensitivity):
        #
        concentration_smpl = {}
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            concentration_smpl[file_smpl] = {}
            concentration_is_smpl = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in concentration_smpl:
                    concentration_smpl[isotope] = []
                concentration_smpl[file_smpl][isotope] = np.mean((intensity_sample[file_smpl][isotope]))\
                                                         /(np.mean(intensity_sample[file_smpl][self.var_is]))\
                                                         *(concentration_is_smpl)/(np.mean(sensitivity[isotope]))
                value = round(concentration_smpl[file_smpl][isotope], 6)
                if value >= 0:
                    concentration_smpl[isotope].append(abs(value))
                else:
                    concentration_smpl[isotope].append(0.0)
        #
        ## TESTING
        # print("Concentration (IS SMPL):", concentration_is_smpl)
        # print("Concentration (SMPL):", concentration_smpl)
        #
        return concentration_smpl
    #
    def calculate_intensity_inclusion_heinrich_2(self, intensity):
        helper = {}
        helper["Result"] = {}
        helper["I(M,HO)"] = []
        helper["I(H,IS)"] = []
        helper["I(M,i)"] = {}
        helper["I(H,i)"] = {}
        #
        internal_standard = self.var_is
        host_isotope = self.host_isotope
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_mix_ho = np.mean(intensity["MIX"][file_smpl][host_isotope])
            intensity_host_is = np.mean(intensity["MATRIX CORRECTED"][file_smpl][internal_standard])
            #
            helper["I(M,HO)"].append(intensity_mix_ho)
            helper["I(H,IS)"].append(intensity_host_is)
            #
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper["Result"]:
                    helper["Result"][isotope] = []
                    helper["I(M,i)"][isotope] = []
                    helper["I(H,i)"][isotope] = []
                #
                intensity_mix_i = np.mean(intensity["MIX"][file_smpl][isotope])
                intensity_host_i = np.mean(intensity["MATRIX CORRECTED"][file_smpl][isotope])
                #
                helper["I(M,i)"][isotope].append(intensity_mix_i)
                helper["I(H,i)"][isotope].append(intensity_host_i)
        #
        intensity_mix_ho = np.mean(helper["I(M,HO)"])
        intensity_host_is = np.mean(helper["I(H,IS)"])
        #
        for isotope in self.container_lists["ISOTOPES"]:
            intensity_mix_i = np.mean(helper["I(M,i)"][isotope])
            intensity_host_i = np.mean(helper["I(H,i)"][isotope])
            #
            value = intensity_mix_i - intensity_mix_ho*(intensity_host_i/intensity_host_is)
            #
            helper["Result"][isotope].append(value)
        #
        ## TESTING
        # print("Testing: Inclusion Intensity (Heinrich)")
        # for key, value in helper["Result"].items():
        #     print("Isotope:", key)
        #     print("Mean:", np.mean(value), "Error:", np.std(value, ddof=1))
        #
        return helper["Result"]
    #
    def calculate_concentration_inclusion_heinrich_2(self, intensity_incl, sensitivity):
        helper = {}
        helper["Results"] = {}
        helper["Xi(i)"] = {}
        helper["I(INCL,i)"] = {}
        #
        internal_standard = self.var_is
        file_smpl = self.container_lists["SMPL"]["Short"][0]
        concentration_incl_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
        intensity_incl_is = np.mean(intensity_incl[internal_standard])
        #
        for isotope in self.container_lists["ISOTOPES"]:
            if isotope not in helper["Results"]:
                helper["Results"][isotope] = []
                helper["Xi(i)"][isotope] = []
                helper["I(INCL,i)"][isotope] = []
            #
            sensitivity_i = np.mean(sensitivity[isotope])
            intensity_incl_i = np.mean(intensity_incl[isotope])
            #
            helper["Xi(i)"][isotope].append(sensitivity_i)
            helper["I(INCL,i)"][isotope].append(intensity_incl_i)
        #
        for isotope in self.container_lists["ISOTOPES"]:
            sensitivity_i = np.mean(helper["Xi(i)"][isotope])
            intensity_incl_i = np.mean(helper["I(INCL,i)"][isotope])
            #
            value = (intensity_incl_i/intensity_incl_is)*(concentration_incl_is/sensitivity_i)
            #
            helper["Results"][isotope].append(value)
        #
        ## TESTING
        # print("Testing: Inclusion Concentration (Heinrich)")
        # for key, value in helper["Results"].items():
        #     print("Isotope:", key)
        #     print("Mean:", np.mean(value), "Error:", np.std(value, ddof=1))
        #
        return helper["Results"]
    #
    def calculate_intensity_inclusion(self, host_isotope, intensity_mixed, intensity_mat):
        helper = {}
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_mixed_t = np.mean(intensity_mixed[file_smpl][host_isotope])
            intensity_mat_t = np.mean(intensity_mat[file_smpl][host_isotope])
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = []
                intensity_mixed_i = np.mean(intensity_mixed[file_smpl][isotope])
                intensity_mat_i = np.mean(intensity_mat[file_smpl][isotope])
                value = intensity_mixed_i - intensity_mixed_t*intensity_mat_i/intensity_mat_t
                helper[isotope].append(value)
        #
        return helper
    #
    def calculate_concentration_inclusion(self, intensity_incl, intensity_mat):
        helper = {}
        key_element_is = re.search("(\D+)(\d+)", self.var_is)
        var_is_element = key_element_is.group(1)
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            concentration_incl_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
            intensity_incl_is = np.mean(intensity_incl[self.var_is])
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                concentration_std_is = self.container_lists["SRM Data"][var_srm][var_is_element]
                intensity_std_is = np.mean(intensity_mat[file_std][self.var_is])
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    key_element_i = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element_i.group(1)
                    concentration_std_i = self.container_lists["SRM Data"][var_srm][var_i_element]
                    intensity_std_i = np.mean(intensity_mat[file_std][isotope])
                    intensity_incl_i = np.mean(intensity_incl[isotope])
                    #
                    value = concentration_incl_is*concentration_std_i/concentration_std_is*intensity_std_is/\
                            intensity_std_i*intensity_incl_i/intensity_incl_is
                    helper[isotope].append(value)
        #
        return helper
    #
    def calculate_intensity_ratio(self, intensity_smpl, var_is):
        helper = {}
        #
        for isotope in self.container_lists["ISOTOPES"]:
            if isotope not in helper:
                helper[isotope] = []
            #
            value = np.mean(intensity_smpl[isotope])/np.mean(intensity_smpl[var_is])
            helper[isotope].append(value)
        #
        return helper
    #
    def calculate_intensity_inclusion_heinrich(self, host_isotope, intensity):
        helper = {}
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_mix_hostonly = np.mean(intensity["MIX"][file_smpl][host_isotope])
            intensity_host_hostonly = np.mean(intensity["MATRIX CORRECTED"][file_smpl][host_isotope])
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper:
                    helper[isotope] = []
                intensity_mix_i = np.mean(intensity["MIX"][file_smpl][isotope])
                intensity_host_i = np.mean(intensity["MATRIX CORRECTED"][file_smpl][isotope])
                #
                if np.mean(intensity_mix_i) >= np.mean(intensity_mix_hostonly*(intensity_host_i/intensity_host_hostonly)):
                    value = intensity_mix_i - intensity_mix_hostonly*(intensity_host_i/intensity_host_hostonly)
                else:
                    value = intensity_mix_hostonly*(intensity_host_i/intensity_host_hostonly) - intensity_mix_i
                #
                helper[isotope].append(np.mean(value))
        #
        ## TESTING
        # print("TESTING: Intensity Inclusion")
        # for key, value in helper.items():
        #     print(key)
        #     print("Mean:", np.mean(value), "Error:", np.std(value, ddof=1))
        #
        return helper
    #
    def calculate_concentration_heinrich(self, intensity_incl):
        helper = {}
        key_element_is = re.search("(\D+)(\d+)", self.var_is)
        var_is_element = key_element_is.group(1)
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            concentration_incl_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
            intensity_incl_is = np.mean(intensity_incl[self.var_is])
            for file_std in self.container_lists["STD"]["Short"]:
                var_srm = self.container_files["STD"][file_std]["SRM"].get()
                concentration_std_is = self.container_lists["SRM Data"][var_srm][var_is_element]
                #
                intensity_std_is_bg = np.mean(
                    self.container_measurements["SELECTED"][file_std][self.var_datatype][self.var_is]["BG"])
                intensity_std_is_mat = np.mean(
                    self.container_measurements["SELECTED"][file_std][self.var_datatype][self.var_is]["MAT"])
                #
                if np.mean(intensity_std_is_mat) >= np.mean(intensity_std_is_bg):
                    intensity_std_is = np.mean(intensity_std_is_mat - np.mean(intensity_std_is_bg))
                else:
                    intensity_std_is = np.mean(intensity_std_is_bg - np.mean(intensity_std_is_mat))
                #
                for isotope in self.container_lists["ISOTOPES"]:
                    if isotope not in helper:
                        helper[isotope] = []
                    #
                    key_element_i = re.search("(\D+)(\d+)", isotope)
                    var_i_element = key_element_i.group(1)
                    concentration_std_i = self.container_lists["SRM Data"][var_srm][var_i_element]
                    #
                    intensity_std_i_bg = np.mean(
                        self.container_measurements["SELECTED"][file_std][self.var_datatype][isotope]["BG"])
                    intensity_std_i_mat = np.mean(
                        self.container_measurements["SELECTED"][file_std][self.var_datatype][isotope]["MAT"])
                    #
                    if np.mean(intensity_std_i_mat) >= np.mean(intensity_std_i_bg):
                        intensity_std_i = np.mean(intensity_std_i_mat - np.mean(intensity_std_i_bg))
                    else:
                        intensity_std_i = np.mean(intensity_std_i_bg - np.mean(intensity_std_i_mat))
                    #
                    intensity_incl_i = np.mean(intensity_incl[isotope])
                    #
                    value = concentration_incl_is*(concentration_std_i/concentration_std_is)*(
                            intensity_incl_i*intensity_std_is)/(intensity_incl_is*intensity_std_i)
                    #
                    helper[isotope].append(value)
        #
        ## TESTING
        # print("TESTING: Concentration Inclusion")
        # for key, value in helper.items():
        #     print(key)
        #     print("Mean:", np.mean(value), "Error:", np.std(value, ddof=1))
        #
        return helper
    #
    def calculate_concentration_mixed_is(self, ratio_x, intensity, host_isotope):
        helper = {}
        helper["Host IS"] = []
        helper["Host Host Only"] = []
        helper["Mix IS"] = []
        helper["Mix Host Only"] = []
        helper["Result"] = []
        #
        concentration_host_is = self.concentration_host_is
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_host_is = np.mean(intensity["MATRIX CORRECTED"][file_smpl][self.var_is])
            intensity_host_hostonly = np.mean(intensity["MATRIX CORRECTED"][file_smpl][host_isotope])
            intensity_mix_is = np.mean(intensity["MIX"][file_smpl][self.var_is])
            intensity_mix_hostonly = np.mean(intensity["MIX"][file_smpl][host_isotope])
            #
            helper["Host IS"].append(intensity_host_is)
            helper["Host Host Only"].append(intensity_host_hostonly)
            helper["Mix IS"].append(intensity_mix_is)
            helper["Mix Host Only"].append(intensity_mix_hostonly)
        #
        intensity_host_is = np.mean(helper["Host IS"])
        intensity_host_hostonly = np.mean(helper["Host Host Only"])
        intensity_mix_is = np.mean(helper["Mix IS"])
        intensity_mix_hostonly = np.mean(helper["Mix Host Only"])
        #
        for x in ratio_x:
            value = (1 - x)*concentration_host_is*(intensity_mix_is*intensity_host_hostonly)/(
                    intensity_host_is*intensity_mix_hostonly)
            #
            helper["Result"].append(value)
        #
        ## TESTING
        # print("Testing: Concentration C(IS,MIX)")
        # print("Mean:", np.mean(helper["Result"]), "Error:", np.std(helper["Result"], ddof=1))
        #
        return helper["Result"]
    #
    def calculate_concentration_mixed_hostonly(self, ratio_x):
        helper = []
        concentration_host_hostonly = self.concentration_host_hostonly
        #
        for x in ratio_x:
            value = (1 - x)*concentration_host_hostonly
            #
            helper.append(value)
        #
        ## TESTING
        # print("Testing: Concentration C(HO,MIX)")
        # print("Mean:", np.mean(helper), "Error:", np.std(helper, ddof=1))
        #
        return helper
    #
    def calculate_rsf_mix(self, ratio_x, intensity, host_isotope):
        helper = {}
        helper["Result"] = {}
        helper["Result"]["HOST"] = []
        helper["Result"]["MIX"] = []
        helper["C(IS,STD)"] = []
        helper["I(IS,STD)"] = []
        helper["Host IS"] = []
        helper["Host Host Only"] = []
        helper["Mix Host Only"] = []
        #
        key_element_is = re.search("(\D+)(\d+)", self.var_is)
        var_is_element = key_element_is.group(1)
        concentration_host_is = self.concentration_host_is
        #
        for file_std in self.container_lists["STD"]["Short"]:
            var_srm = self.container_files["STD"][file_std]["SRM"].get()
            concentration_std_is = self.container_lists["SRM Data"][var_srm][var_is_element]
            helper["C(IS,STD)"].append(concentration_std_is)
            #
            intensity_std_is_bg = np.mean(
                self.container_measurements["SELECTED"][file_std][self.var_datatype][self.var_is]["BG"])
            intensity_std_is_mat = np.mean(
                self.container_measurements["SELECTED"][file_std][self.var_datatype][self.var_is]["MAT"])
            #
            if np.mean(intensity_std_is_mat) >= np.mean(intensity_std_is_bg):
                intensity_std_is = np.mean(intensity_std_is_mat - np.mean(intensity_std_is_bg))
            else:
                intensity_std_is = np.mean(intensity_std_is_bg - np.mean(intensity_std_is_mat))
            #
            helper["I(IS,STD)"].append(intensity_std_is)
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_host_is = np.mean(intensity["MATRIX CORRECTED"][file_smpl][self.var_is])
            intensity_host_hostonly = np.mean(intensity["MATRIX CORRECTED"][file_smpl][host_isotope])
            intensity_mix_hostonly = np.mean(intensity["MIX"][file_smpl][host_isotope])
            #
            helper["Host IS"].append(intensity_host_is)
            helper["Host Host Only"].append(intensity_host_hostonly)
            helper["Mix Host Only"].append(intensity_mix_hostonly)
        #
        concentration_std_is = np.mean(helper["C(IS,STD)"])
        intensity_std_is = np.mean(helper["I(IS,STD)"])
        intensity_host_is = np.mean(helper["Host IS"])
        intensity_host_hostonly = np.mean(helper["Host Host Only"])
        intensity_mix_hostonly = np.mean(helper["Mix Host Only"])
        #
        for x in ratio_x:
            if intensity_std_is > 0 and intensity_host_hostonly > 0:
                value_mix = (concentration_std_is/intensity_std_is)*(1/((1 - x)*concentration_host_is))*(
                        (intensity_host_is*intensity_mix_hostonly)/intensity_host_hostonly)
            else:
                value_mix = 0.0
            #
            helper["Result"]["MIX"].append(value_mix)
            #
            if intensity_std_is > 0:
                value_host = (intensity_host_is*concentration_std_is)/(intensity_std_is*concentration_host_is)
            else:
                value_host = 0.0
            #
            helper["Result"]["HOST"].append(value_host)
        #
        ## TESTING
        # print("Testing: RSF Mix")
        # print("Mean:", np.mean(helper["Result"]["MIX"]), "Error:", np.std(helper["Result"]["MIX"], ddof=1))
        # print("Testing: RSF Host")
        # print("Mean:", np.mean(helper["Result"]["HOST"]), "Error:", np.std(helper["Result"]["HOST"], ddof=1))
        #
        return helper["Result"]
    #
    def calculate_concentration_host_sills(self, sensitivity, intensity):
        helper = {}
        helper["Result"] = {}
        helper["I(H,IS)"] = []
        helper["I(H,i)"] = {}
        helper["Xi(i)"] = {}
        concentration_host_is = self.concentration_host_is
        internal_standard = self.var_is
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_host_is = np.mean(intensity["MATRIX CORRECTED"][file_smpl][internal_standard])
            #
            helper["I(H,IS)"].append(intensity_host_is)
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper["Result"]:
                    helper["Result"][isotope] = []
                    helper["I(H,i)"][isotope] = []
                    helper["Xi(i)"][isotope] = []
                #
                sensitivity_i = np.mean(sensitivity[isotope])
                intensity_host_i = np.mean(intensity["MATRIX CORRECTED"][file_smpl][isotope])
                #
                helper["Xi(i)"][isotope].append(sensitivity_i)
                helper["I(H,i)"][isotope].append(intensity_host_i)
        #
        intensity_host_is = np.mean(helper["I(H,IS)"])
        #
        for isotope in self.container_lists["ISOTOPES"]:
            sensitivity_i = np.mean(helper["Xi(i)"][isotope])
            intensity_host_i = np.mean(helper["I(H,i)"][isotope])
            value = (1/sensitivity_i)*(intensity_host_i/intensity_host_is)*concentration_host_is
            #
            helper["Result"][isotope].append(value)
        #
        ## TESTING
        # print("Testing: Host Concentration")
        # for isotope, result in helper["Result"].items():
        #     print("Isotope:", isotope)
        #     print("Mean:", round(np.mean(result), 6), "Error:", round(np.std(result, ddof=1), 6))
        #
        return helper["Result"]
    #
    def calculate_concentration_mix_sills(self, sensitivity, intensity, ratio_x):
        helper = {}
        helper["Result"] = {}
        helper["I(H,IS)"] = []
        helper["I(H,HO)"] = []
        helper["I(M,HO)"] = []
        helper["I(M,i)"] = {}
        helper["Xi(i)"] = {}
        internal_standard = self.var_is
        host_isotope = self.host_isotope
        #
        concentration_host_is = self.concentration_host_is
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_host_is = np.mean(intensity["MATRIX CORRECTED"][file_smpl][internal_standard])
            intensity_host_ho = np.mean(intensity["MATRIX CORRECTED"][file_smpl][host_isotope])
            intensity_mix_ho = np.mean(intensity["MIX"][file_smpl][host_isotope])
            #
            helper["I(H,IS)"].append(intensity_host_is)
            helper["I(H,HO)"].append(intensity_host_ho)
            helper["I(M,HO)"].append(intensity_mix_ho)
            #
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper["Result"]:
                    helper["Result"][isotope] = []
                    helper["I(M,i)"][isotope] = []
                    helper["Xi(i)"][isotope] = []
                #
                intensity_mix_i = np.mean(intensity["MIX"][file_smpl][isotope])
                sensitivity_i = np.mean(sensitivity[isotope])
                #
                helper["I(M,i)"][isotope].append(intensity_mix_i)
                helper["Xi(i)"][isotope].append(sensitivity_i)
        #
        intensity_host_is = np.mean(helper["I(H,IS)"])
        intensity_host_ho = np.mean(helper["I(H,HO)"])
        intensity_mix_ho = np.mean(helper["I(M,HO)"])
        #
        for x in ratio_x:
            for isotope in self.container_lists["ISOTOPES"]:
                sensitivity_i = np.mean(helper["Xi(i)"][isotope])
                intensity_mix_i = np.mean(helper["I(M,i)"][isotope])
                #
                value = np.mean((1/sensitivity_i)*(intensity_mix_i/intensity_mix_ho)*(
                        intensity_host_ho/intensity_host_is)*(1 - x)*concentration_host_is)
                #
                helper["Result"][isotope].append(value)
        #
        ## TESTING
        # print("Testing: Mix Concentration")
        # for isotope, result in helper["Result"].items():
        #     print("Isotope:", isotope)
        #     print("Mean:", round(np.mean(result), 6), "Error:", round(np.std(result, ddof=1), 6))
        #
        return helper["Result"]
    #
    def calculate_concentration_inclusion_sills(self, ratio_x, intensity, sensitivity):
        helper = {}
        helper["Result"] = {}
        helper["I(H,IS)"] = []
        helper["I(H,HO)"] = []
        helper["I(M,HO)"] = []
        helper["Xi(i)"] = {}
        helper["I(M,i)"] = {}
        helper["I(H,i)"] = {}
        #
        internal_standard = self.var_is
        host_isotope = self.host_isotope
        concentration_host_is = self.concentration_host_is
        #
        for file_smpl in self.container_lists["SMPL"]["Short"]:
            intensity_host_is = np.mean(intensity["MATRIX CORRECTED"][file_smpl][internal_standard])
            intensity_host_ho = np.mean(intensity["MATRIX CORRECTED"][file_smpl][host_isotope])
            intensity_mix_ho = np.mean(intensity["MIX"][file_smpl][host_isotope])
            #
            helper["I(H,IS)"].append(intensity_host_is)
            helper["I(H,HO)"].append(intensity_host_ho)
            helper["I(M,HO)"].append(intensity_mix_ho)
            #
            for isotope in self.container_lists["ISOTOPES"]:
                if isotope not in helper["Result"]:
                    helper["Result"][isotope] = []
                    helper["Xi(i)"][isotope] = []
                    helper["I(M,i)"][isotope] = []
                    helper["I(H,i)"][isotope] = []
                #
                sensitivity_i = np.mean(sensitivity[isotope])
                intensity_mix_i = np.mean(intensity["MIX"][file_smpl][isotope])
                intensity_host_i = np.mean(intensity["MATRIX CORRECTED"][file_smpl][isotope])
                #
                helper["Xi(i)"][isotope].append(sensitivity_i)
                helper["I(M,i)"][isotope].append(intensity_mix_i)
                helper["I(H,i)"][isotope].append(intensity_host_i)
        #
        intensity_host_is = np.mean(helper["I(H,IS)"])
        intensity_mix_ho = np.mean(helper["I(M,HO)"])
        intensity_host_ho = np.mean(helper["I(H,HO)"])
        x = np.mean(ratio_x)
        #
        for isotope in self.container_lists["ISOTOPES"]:
            sensitivity_i = np.mean(helper["Xi(i)"][isotope])
            intensity_mix_i = np.mean(helper["I(M,i)"][isotope])
            intensity_host_i = np.mean(helper["I(H,i)"][isotope])
            #
            value = ((1 - x)/x)*(concentration_host_is/intensity_host_is)*(1/sensitivity_i)*(
                    (intensity_mix_i/intensity_mix_ho)*intensity_host_ho - intensity_host_i)
            #
            helper["Result"][isotope].append(value)
        #
        ## TESTING
        # print("Testing: Inclusion Concentration")
        # for key, value in helper["Result"].items():
        #     print("Isotope:", key)
        #     print("Mean:", round(np.mean(value), 6), "Error:", round(np.std(value, ddof=1), 6))
        #
        return helper["Result"]
    #
    def calculate_concentration_inclusion_sills_alternative(self, ratio_x, concentration_host, concentration_mix):
        helper = {}
        #
        x = np.mean(ratio_x)
        # file_smpl = self.container_lists["SMPL"]["Short"][0]
        # concentration_incl_is = float(self.container_files["SMPL"][file_smpl]["IS Concentration"].get())
        # x_calib = (np.mean(concentration_mix[self.var_is]) - np.mean(concentration_host[self.var_is]))/(concentration_incl_is - np.mean(concentration_host[self.var_is]))
        # x = x_calib
        #
        for isotope in self.container_lists["ISOTOPES"]:
            if isotope not in helper:
                helper[isotope] = []
            #
            concentration_host_i = np.mean(concentration_host[isotope])
            concentration_mix_i = np.mean(concentration_mix[isotope])
            #
            value = (1 - 1/x)*concentration_host_i + (1/x)*concentration_mix_i
            #
            helper[isotope].append(value)
        #
        ## TESTING
        # print("Testing: Inclusion Concentration (Alternative)")
        # for key, value in helper.items():
        #     print("Isotope:", key)
        #     print("Mean:", round(np.mean(value), 6), "Error:", round(np.std(value, ddof=1), 6))
        #
        return helper
    #
    def do_quantification(self, intensity_mat, intensity_mixed, intensity_incl, host_isotope, sensitivity, intensity):
        #
        ## PREREQUISITES
        # print("Intensity (MAT):", intensity_mat)
        # print("Intensity (MIXED):", intensity_mixed)
        # print("Host Isotope:", host_isotope)
        # print("Sensitivity:", sensitivity)
        #
        ## Calculation: Intensity INCL
        intensity_incl = self.calculate_intensity_inclusion_heinrich(host_isotope=host_isotope, intensity=intensity)
        intensity_incl_heinrich = self.calculate_intensity_inclusion_heinrich_2(intensity=intensity)
        #
        ## Calculation: Ratio R
        ratio_R = self.calculate_ratio_R(intensity=intensity, host_isotope=host_isotope)
        #
        ## Calculation: Ratio a
        ratio_a = self.calculate_ratio_a(intensity=intensity, sensitivity=sensitivity, host_isotope=host_isotope)
        #
        ## Calculation: Ratio x
        ratio_x = self.calculate_ratio_x(ratio_a=ratio_a, intensity=intensity, sensitivity=sensitivity,
                                         calculation_via_a=False)
        #
        ###################
        ## CONCENTRATION ##
        ###################
        #
        ## Host Concentration:
        concentration_host = self.calculate_concentration_host_sills(sensitivity=sensitivity, intensity=intensity)
        #
        ## Mix Concentration:
        concentration_mix = self.calculate_concentration_mix_sills(
            sensitivity=sensitivity, intensity=intensity, ratio_x=ratio_x)
        #
        ## Calculation: C(IS,MIX)
        concentration_mix_is = self.calculate_concentration_mixed_is(ratio_x=ratio_x, intensity=intensity,
                                                                     host_isotope=host_isotope)
        #
        ## Calculation: C(HO,MIX)
        concentration_mix_ho = self.calculate_concentration_mixed_hostonly(ratio_x=ratio_x)
        #
        ## Calculation: RSF(MIX)
        rsf_mix = self.calculate_rsf_mix(ratio_x=ratio_x, intensity=intensity, host_isotope=host_isotope)
        #
        # Calculation: Intensity SMPL
        intensity_smpl = self.calculate_intensity_smpl(intensity_mat=intensity_mat, intensity_mixed=intensity_mixed,
                                                       host_isotope=host_isotope)
        intensity_smpl_2 = self.calculate_intensity_inclusion(
            host_isotope=host_isotope, intensity_mixed=intensity_mixed, intensity_mat=intensity_mat)
        #
        ## Calculation: Intensity Ratio SMPL
        intensity_ratio = self.calculate_intensity_ratio(intensity_smpl=intensity_incl, var_is=self.var_is)
        #
        ## Calculation: Concentration SMPL
        concentration_smpl = self.calculate_concentration_smpl(intensity_sample=intensity_smpl, sensitivity=sensitivity)
        concentration_smpl2 = self.calculate_concentration_inclusion(
            intensity_incl=intensity_smpl_2, intensity_mat=intensity_mat)
        concentration_heinrich = self.calculate_concentration_heinrich(intensity_incl=intensity_incl)
        concentration_heinrich_2 = self.calculate_concentration_inclusion_heinrich_2(
            intensity_incl=intensity_incl_heinrich, sensitivity=sensitivity)
        concentration_sills = self.calculate_concentration_inclusion_sills(
            ratio_x=ratio_x, intensity=intensity, sensitivity=sensitivity)
        concentration_sills_alternative = self.calculate_concentration_inclusion_sills_alternative(
            ratio_x=ratio_x, concentration_host=concentration_host, concentration_mix=concentration_mix)
        #
        ## TESTING
        # print("Intensity (SMPL):", intensity_smpl)
        # print("Intensity (INCL):", intensity_smpl_2)
        # print("Concentration (SMPL):", concentration_smpl)
        # print("Concentration (INCL):", concentration_smpl2)
        #
        return intensity_ratio, concentration_heinrich
