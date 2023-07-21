#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# essential_functions.py
# Maximilian Beeskow
# 21.07.2023
# ----------------------
#
## MODULES
#
import re, os
import tkinter as tk
import numpy as np
from modules import data
import tkinter.filedialog as fd
from outliers import smirnov_grubbs
from modules.spike_elimination import two_sided_test_indices, two_sided_test_outliers
#
## CLASSES
#
class EssentialDataProcessing:
    #
    def __init__(self, parent):
        self.parent = parent
    #
    def open_csv(self, var_list, var_listbox):
        if "Default_STD_01.csv" in var_list or "Default_SMPL_01.csv" in var_list:
            var_list.clear()
        filename = fd.askopenfilenames(parent=self.parent, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        for i in filename:
            if i not in var_list:
                var_list.append(i)
                file_parts = i.split("/")
                var_listbox.insert(tk.END, file_parts[-1])
        #
        return filename
#
class Essentials:
    def __init__(self, variable):
        self.variable = variable
    #
    def open_txt_file(self):
        f = open(str(self.variable), "r")
        #
        return f
    #
    def find_nearest_time(self, var_t, times, event):
        try:
            time = var_t.get()
            time = time.replace(',', '.')

            x_nearest_start = min(times, key=lambda x: abs(x-float(time)))
            var_t.set(round(x_nearest_start, 8))
            #self.values_time_helper["start"] = x_nearest_start
        except:
            pass
    #
    def merge_times(self):
        sorted_times = sorted(self.variable, key=lambda x: x[0])
        time_index = 0
        #
        for i in sorted_times:
            if i[0] > sorted_times[time_index][1]:
                time_index += 1
                sorted_times[time_index] = i
            else:
                sorted_times[time_index] = [sorted_times[time_index][0], i[1]]
        #
        merged_times = np.array(sorted_times[:time_index+1])
        #
        return merged_times
    #
    def select_radiobutton(self):
        print("Variable:", self.variable.get())
    #
    def change_default_option(self, var_indiv, n_isotopes, lists=False):
        var_default = self.variable
        for i in range(n_isotopes):
            if lists == False:
                var_indiv[i].set(var_default)
            else:
                var_indiv[i][1].set(var_default)
    #
    def change_option(self, index):
        print(self.variable)
        print("Index:", index)
    #
    def select_time_window(self, op):
        part = self.variable
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
    def do_grubbs_test(self, dataset_complete, alpha=0.05, threshold=1000, n_range=3):
        dataset = self.variable
        #
        outlier_indices_pre = two_sided_test_indices(data=dataset, alpha=alpha)
        outlier_values_pre = two_sided_test_outliers(data=dataset, alpha=alpha)
        outlier_indices = []
        for index, value in enumerate(outlier_values_pre):
            if value > threshold:
                outlier_indices.append(outlier_indices_pre[index])
        outlier_indices.sort()
        #
        data_smoothed = []
        for index, value in enumerate(dataset_complete):
            if value > threshold:
                if index in outlier_indices:
                    if index >= 3:
                        lower_limit = index - 3
                    elif index == 2:
                        lower_limit = index - 2
                    elif index == 1:
                        lower_limit = index - 1
                    elif index == 0:
                        lower_limit = index

                    if index <= len(dataset_complete) - 4:
                        upper_limit = index + 3
                    elif index < len(dataset_complete) - 3:
                        upper_limit = index + 2
                    elif index < len(dataset_complete) - 2:
                        upper_limit = index + 1
                    elif index < len(dataset_complete) - 1:
                        upper_limit = index

                    average_dataset = dataset_complete[lower_limit:upper_limit]
                    var_index = average_dataset.index(value)
                    value_popped = average_dataset.pop(var_index)
                    value_corrected = np.mean(average_dataset)
                    data_smoothed.append(value_corrected)
                else:
                    data_smoothed.append(value)
            else:
                data_smoothed.append(value)
        #
        return data_smoothed, outlier_indices
    #
    def find_outlier(self, limit, interval, data_total, isotope, threshold=1000):
        data = self.variable
        n_outl = 0
        indices_outl = []
        data_corrected = []
        helper_interval = np.arange(interval[0], interval[1])
        for i in range(0, len(data)):
            if i == 0:
                data_ref = []
                data_ref.extend(data[1:3])
                data_ref = np.mean(data_ref)
            elif i == 1:
                data_ref = []
                data_ref.extend(data[0:1])
                data_ref.extend(data[2:4])
                data_ref = np.mean(data_ref)
            elif i >= 2 and i <= len(data)-3:
                data_ref = []
                data_ref.extend(data[i-2:i])
                data_ref.extend(data[i+1:i+3])
                data_ref = np.mean(data_ref)
            elif i == len(data)-2:
                data_ref = []
                data_ref.extend(data[i-2:i])
                data_ref.extend(data[i+1:i+2])
                data_ref = np.mean(data_ref)
            elif i == len(data)-1:
                data_ref = []
                data_ref.extend(data[i-2:i])
                data_ref = np.mean(data_ref)
            if isinstance(data, list):
                data_invest = data[i]
            else:
                data_invest = data.iloc[i]
            #if data.iloc[i] >= threshold:
            if data_invest >= threshold:
                if data_invest > data_ref*(1+limit/100) and data_invest > data_ref:
                    n_outl += 1
                    indices_outl.append(helper_interval[i])
                    if i == 0:
                        data_corrected.append(data_ref)
                    elif i == 1:
                        data_corrected.append(data_ref)
                    elif i >= 2 and i <= len(data)-3:
                        data_corrected.append(data_ref)
                    elif i == len(data)-2:
                        data_corrected.append(data_ref)
                    elif i == len(data)-1:
                        data_corrected.append(data_ref)
                elif data_invest < data_ref*(1-limit/100) and data_invest < data_ref:
                    n_outl += 1
                    indices_outl.append(helper_interval[i])
                    if i == 0:
                        data_corrected.append(data_ref)
                    elif i == 1:
                        data_corrected.append(data_ref)
                    elif i >= 2 and i <= len(data)-3:
                        data_corrected.append(data_ref)
                    elif i == len(data)-2:
                        data_corrected.append(data_ref)
                    elif i == len(data)-1:
                        data_corrected.append(data_ref)
                else:
                    #data_corrected.append(data.iloc[i])
                    data_corrected.append(data_invest)
            else:
                #data_corrected.append(data.iloc[i])
                data_corrected.append(data_invest)
        #
        data_smoothed = np.array(data_total[isotope])
        data_smoothed[interval[0]:interval[1]] = data_corrected
        data_smoothed.tolist()
        #data_smoothed = data_total[isotope].replace(
        #    data_total[isotope][interval[0]:interval[1]].tolist(), data_corrected)
        #
        return data_smoothed, indices_outl
    #
    def calculate_sensitivity_regression(self, xi_time, var_i, xi_opt):
        xi_time = np.array(xi_time[var_i])
        x = xi_time[:, 0]
        y = xi_time[:, 1]
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0] # m*x + c
        xi_opt[var_i] = [m, c]
#
class EssentialsSRM:
    #
    def __init__(self):
        pass
    #
    def place_srm_values(self, srm_name, srm_dict):
        path = os.getcwd()
        parent = os.path.dirname(path)
        #
        try:
            path_app = os.getcwd()
            path = os.path.dirname(path_app)
            data_srm = data.general().importSRM(filename=path + str("/lib/NIST_606.csv"))
        except:
            path = os.getcwd()
            data_srm = data.general().importSRM(filename=path + str("/lib/NIST_606.csv"))
        #
        if srm_name == "NIST 606":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_606.csv"))   # replaces parent with path
        elif srm_name == "NIST 610":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_610.csv"))
        elif srm_name == "NIST 610 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_610_GeoReM.csv"))
        elif srm_name == "NIST 610 (Spandler)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_610_Spandler.csv"))
        elif srm_name == "NIST 611":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_611.csv"))
        elif srm_name == "NIST 611 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_611_GeoReM.csv"))
        elif srm_name == "NIST 612":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_612.csv"))
        elif srm_name == "NIST 612 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_612_GeoReM.csv"))
        elif srm_name == "NIST 613":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_613.csv"))
        elif srm_name == "NIST 613 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_613_GeoReM.csv"))
        elif srm_name == "NIST 614":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_614.csv"))
        elif srm_name == "NIST 614 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_614_GeoReM.csv"))
        elif srm_name == "NIST 615":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_615.csv"))
        elif srm_name == "NIST 615 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_615_GeoReM.csv"))
        elif srm_name == "NIST 616":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_616.csv"))
        elif srm_name == "NIST 616 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_616_GeoReM.csv"))
        elif srm_name == "NIST 617":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_617.csv"))
        elif srm_name == "NIST 617 (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/NIST_617_GeoReM.csv"))
        elif srm_name == "USGS BCR-2G (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/USGS_BCR2G_GeoReM.csv"))
        elif srm_name == "USGS GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/USGS_GSD1G_GeoReM.csv"))
        elif srm_name == "USGS GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/USGS_GSE1G_GeoReM.csv"))
        elif srm_name == "B6":
            data_srm = data.general().importSRM(filename=path+str("/lib/B6.csv"))
        elif srm_name == "Durango Apatite":
            data_srm = data.general().importSRM(filename=path+str("/lib/Durango_Apatite.csv"))
        elif srm_name == "Scapolite 17":
            data_srm = data.general().importSRM(filename=path+str("/lib/Scapolite_17.csv"))
        elif srm_name == "BAM-376":
            data_srm = data.general().importSRM(filename=path+str("/lib/BAM_376.csv"))
        elif srm_name == "BCR-2G":
            data_srm = data.general().importSRM(filename=path+str("/lib/BCR_2G.csv"))
        elif srm_name == "BL-Q":
            data_srm = data.general().importSRM(filename=path+str("/lib/BL_Q.csv"))
        elif srm_name == "Br-Glass":
            data_srm = data.general().importSRM(filename=path+str("/lib/Br_Glass.csv"))
        elif srm_name == "GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/GSD_1G_GeoReM.csv"))
        elif srm_name == "GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=path+str("/lib/GSE_1G_GeoReM.csv"))
        elif srm_name == "GSE-2G":
            data_srm = data.general().importSRM(filename=path+str("/lib/GSE_2G.csv"))
        elif srm_name == "HAL-O":
            data_srm = data.general().importSRM(filename=path+str("/lib/HAL_O.csv"))
        elif srm_name == "K-Br":
            data_srm = data.general().importSRM(filename=path+str("/lib/K_Br.csv"))
        elif srm_name == "MACS-3":
            data_srm = data.general().importSRM(filename=path+str("/lib/MACS_3.csv"))
        elif srm_name == "Po 724":
            data_srm = data.general().importSRM(filename=path+str("/lib/Po_724.csv"))
        elif srm_name == "STDGL-2B2":
            data_srm = data.general().importSRM(filename=path+str("/lib/STDGL_2B2.csv"))
        #
        for item in data_srm:
            srm_dict[srm_name][item[0]] = round(item[1], 4)