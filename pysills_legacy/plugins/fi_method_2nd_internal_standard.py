#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		fi_method_2nd_internal_standard.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		24.06.2022

#-----------------------------------------------

## MODULES
import numpy as np

class Method:
    #
    def __init__(self, container_measurements, container_lists, container_files, var_is1, var_is2, var_file,
                 var_datatype):
        self.container_measurements = container_measurements
        self.container_lists = container_lists
        self.container_files = container_files
        self.var_is1 = var_is1
        self.var_is2 = var_is2
        self.var_file = var_file
        self.var_datatype = var_datatype
    #
    def calculate_x(self, var_CHost_is1, var_CHost_is2, var_CIncl_is1, var_CIncl_is2, var_a):
        value = (var_CHost_is1 - var_a*var_CHost_is2)/(
                var_CHost_is1 - var_CIncl_is1 - var_a*(var_CHost_is2 - var_CIncl_is2))
        #
        return value
    #
    def calculate_concentration_mix_2nd_internal(self, var_x, var_CHost_is2, var_CIncl_is2):
        value = (1 - var_x)*var_CHost_is2 + var_x*var_CIncl_is2
        #
        return value
    #
    def calculate_concentration_mixed(self, var_CMix_is2, var_xi_is2):
        helper = {}
        #
        intensity_mix_is2 = np.mean(np.array(
            self.container_measurements["SELECTED"][self.var_file][self.var_datatype][self.var_is2]["INCL"]) - np.mean(
            self.container_measurements["SELECTED"][self.var_file][self.var_datatype][self.var_is2]["BG"]))
        for isotope in self.container_lists["ISOTOPES"]:
            if isotope not in helper:
                helper[isotope] = []
            intensity_mix_i = np.array(
                self.container_measurements["SELECTED"][self.var_file][self.var_datatype][isotope]["INCL"]) - np.mean(
                self.container_measurements["SELECTED"][self.var_file][self.var_datatype][isotope]["BG"])
            sensitivity_is2 = np.mean(var_xi_is2)
            concentration_mix_is2 = var_CMix_is2
            value = (intensity_mix_i*concentration_mix_is2)/(intensity_mix_is2*sensitivity_is2)
            helper[isotope].extend(value)
        #
        return helper
    #
    def calculate_concentration_inclusion(self, var_x, var_concentration_mix, var_concentration_host):
        helper = {}
        #
        for isotope in self.container_lists["ISOTOPES"]:
            if isotope not in helper:
                helper[isotope] = 0
            value = var_concentration_mix[isotope]/var_x - ((1 - var_x)/var_x)*var_concentration_host[isotope]
            helper[isotope] += value
        #
        return helper