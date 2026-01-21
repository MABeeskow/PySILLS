#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

# Name:		essential_functions.py
# Author:	Maximilian A. Beeskow
# Date:		23.07.2024

#-----------------------------------------------------------------------------------------------------------------------

## MODULES
# external
import re, os, sys, datetime
import tkinter as tk
import numpy as np
import scipy.stats as stats
import tkinter.filedialog as fd
# internal
try:
    from modules import data
    from modules.spike_elimination import two_sided_test_indices, two_sided_test_outliers
except:
    from pysills_legacy.modules import data
    from pysills_legacy.modules.spike_elimination import two_sided_test_indices, two_sided_test_outliers

## CLASSES
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
                key = re.search(r"(\d+\.\d+)" + " - " + r"(\d+\.\d+)", self.var_iw_bg.get())
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
                key = re.search(r"(\d+\.\d+)" + " - " + r"(\d+\.\d+)", self.var_iw_mat.get())
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
                key = re.search(r"(\d+\.\d+)" + " - " + r"(\d+\.\d+)", self.var_iw_sig.get())
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

    def do_grubbs_test2(self, dataset_complete, alpha=0.05, threshold=1000, n_range=3):
        dataset = self.variable

        outlier_indices_pre = two_sided_test_indices(data=dataset, alpha=alpha)
        outlier_values_pre = two_sided_test_outliers(data=dataset, alpha=alpha)
        outlier_indices = []

        for index, value in enumerate(outlier_values_pre):
            if value > threshold:
                outlier_indices.append(outlier_indices_pre[index])

        outlier_indices.sort()

        if len(outlier_indices) > 0:
            print(outlier_indices)

        data_smoothed = []

        for index, value in enumerate(dataset_complete):
            if value > threshold:
                if index in outlier_indices:
                    average_dataset_new = self.determine_surrounded_values(
                        dataset_complete=dataset_complete, index=index)
                    if value in average_dataset_new["All"]:
                        value_corrected = np.min(average_dataset_new["SP"])
                        data_smoothed.append(value_corrected)
                else:
                    data_smoothed.append(value)
            else:
                data_smoothed.append(value)

        return data_smoothed, outlier_indices

    def do_grubbs_test(self, dataset_complete, alpha=0.05, threshold=1000, n_range=3):
        dataset = self.variable

        outlier_indices_pre = two_sided_test_indices(data=dataset, alpha=alpha)
        outlier_indices = outlier_indices_pre
        outlier_indices.sort()

        data_smoothed = dataset_complete.copy()

        for index_outlier in outlier_indices:
            value_outlier = dataset_complete[index_outlier]
            if value_outlier > threshold:
                average_dataset_new = self.determine_surrounded_values(
                    dataset_complete=dataset_complete, index=index_outlier)
                mean = np.mean(average_dataset_new["All"])
                std = np.std(average_dataset_new["All"], ddof=1)
                val_poi = round(abs(value_outlier - mean)/std, 3)
                val_critical = self.calculate_grubbs_critical_value(alpha=alpha, size=len(average_dataset_new["SP"]))
                if val_poi > val_critical:
                    if value_outlier in average_dataset_new["All"]:
                        value_corrected = np.mean(average_dataset_new["SP"])
                        data_smoothed[index_outlier] = round(value_corrected, 2)

        return data_smoothed, outlier_indices

    def calculate_grubbs_critical_value(self, alpha, size):
        t_dist = stats.t.ppf(1 - alpha/(2*size), size - 2)
        numerator = (size - 1)*np.sqrt(np.square(t_dist))
        denominator = np.sqrt(size)*np.sqrt(size - 2 + np.square(t_dist))
        critical_value = numerator/denominator

        return critical_value

    def calculate_grubbs_value(self, dataset_raw):
        std_dev = np.std(dataset_raw, ddof=1)
        avg_y = np.mean(dataset_raw)
        abs_val_minus_avg = abs(np.array(dataset_raw) - avg_y)
        max_of_deviations = max(abs_val_minus_avg)
        max_ind = np.argmax(abs_val_minus_avg)
        Gcal = max_of_deviations/std_dev

        return Gcal, max_ind

    def determine_surrounding_values(self, dataset_complete, index_poi):
        # POI   - Point Of Interest
        # SP    - Surrounding Points
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = dataset_complete[index_poi]
        helper_values["POI"] = val_poi
        n_data = len(dataset_complete)

        if 1 < index_poi and index_poi < n_data - 3:
            val_prev_2 = dataset_complete[index_poi - 2]
            val_prev_1 = dataset_complete[index_poi - 1]
            val_next_1 = dataset_complete[index_poi + 1]
            val_next_2 = dataset_complete[index_poi + 2]
            helper_values["SP"] = [val_prev_2, val_prev_1, val_next_1, val_next_2]
            helper_values["All"] = [val_prev_2, val_prev_1, val_poi, val_next_1, val_next_2]
        elif index_poi == 0:
            val_next_1 = dataset_complete[index_poi + 1]
            val_next_2 = dataset_complete[index_poi + 2]
            helper_values["SP"] = [val_next_1, val_next_2]
            helper_values["All"] = [val_poi, val_next_1, val_next_2]
        elif index_poi == n_data - 1:
            val_prev_2 = dataset_complete[index_poi - 2]
            val_prev_1 = dataset_complete[index_poi - 1]
            helper_values["SP"] = [val_prev_2, val_prev_1]
            helper_values["All"] = [val_prev_2, val_prev_1, val_poi]
        elif index_poi == 1:
            val_prev_1 = dataset_complete[index_poi - 1]
            val_next_1 = dataset_complete[index_poi + 1]
            val_next_2 = dataset_complete[index_poi + 2]
            helper_values["SP"] = [val_prev_1, val_next_1, val_next_2]
            helper_values["All"] = [val_prev_1, val_poi, val_next_1, val_next_2]
        elif index_poi == n_data - 2:
            val_prev_2 = dataset_complete[index_poi - 2]
            val_prev_1 = dataset_complete[index_poi - 1]
            val_next_1 = dataset_complete[index_poi + 1]
            helper_values["SP"] = [val_prev_2, val_prev_1, val_next_1]
            helper_values["All"] = [val_prev_2, val_prev_1, val_poi, val_next_1]

        return helper_values

    def determine_surrounded_values(self, dataset_complete, index, stepsize=4):
        # POI   - Point Of Interest
        # SP    - Surrounding Points
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = dataset_complete[index]
        helper_values["POI"] = val_poi
        helper_values["All"].append(val_poi)
        last_index = len(dataset_complete) - 1

        if index == 0 or index == last_index:
            datapoints = [dataset_complete[1], dataset_complete[2]]
        elif index == last_index:
            datapoints = [dataset_complete[-3], dataset_complete[-2]]
        elif index == 1:
            datapoints = [dataset_complete[0], dataset_complete[2], dataset_complete[3]]
        elif index == last_index - 1:
            datapoints = [dataset_complete[-4], dataset_complete[-3], dataset_complete[-1]]
        else:
            datapoints = [dataset_complete[index - 2], dataset_complete[index - 1], dataset_complete[index + 1],
                          dataset_complete[index + 2]]

        helper_values["SP"].extend(datapoints)
        helper_values["All"].extend(datapoints)

        # for step in range(1, stepsize):
        #     step_before = index - step
        #     step_after = index + step
        #     if step_before >= 0:
        #         helper_values["SP"].append(dataset_complete[step_before])
        #         helper_values["All"].append(dataset_complete[step_before])
        #     if step_after < len(dataset_complete):
        #         helper_values["SP"].append(dataset_complete[step_after])
        #         helper_values["All"].append(dataset_complete[step_after])

        return helper_values

    def find_outlier(self, limit, interval, data_total, isotope, threshold=1000):
        data = self.variable
        n_outl = 0
        indices_outl = []
        data_corrected = []
        helper_interval = np.arange(interval[0], interval[1])

        outlier_indices_pre = two_sided_test_indices(data=data, alpha=limit)
        outlier_values_pre = two_sided_test_outliers(data=data, alpha=limit)

        outlier_indices = []
        for index, value in enumerate(outlier_values_pre):
            if value > threshold:
                outlier_indices.append(outlier_indices_pre[index])
        outlier_indices.sort()
        limit = abs(100 - limit*100)
        helper_outlier = {}

        if len(outlier_indices) > 0:
            for i in outlier_indices:
                if i == 0:
                    data_ref = []
                    data_ref.extend(data[1:3])
                    data_ref = np.min(data_ref)
                elif i == 1:
                    data_ref = []
                    data_ref.extend(data[0:1])
                    data_ref.extend(data[2:4])
                    data_ref = np.min(data_ref)
                elif i >= 2 and i <= len(data)-3:
                    data_ref = []
                    data_ref.extend(data[i-2:i])
                    data_ref.extend(data[i+1:i+3])
                    data_ref = np.min(data_ref)
                elif i == len(data)-2:
                    data_ref = []
                    data_ref.extend(data[i-2:i])
                    data_ref.extend(data[i+1:i+2])
                    data_ref = np.min(data_ref)
                elif i == len(data)-1:
                    data_ref = []
                    data_ref.extend(data[i-2:i])
                    data_ref = np.min(data_ref)

                if isinstance(data, list) or isinstance(data, np.ndarray):
                    data_invest = data[i]
                else:
                    data_invest = data.iloc[i]

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
                        helper_outlier[i] = data_ref
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
                        helper_outlier[i] = data_ref
                    else:
                        data_corrected.append(data_invest)
                else:
                    data_corrected.append(data_invest)

            data_smoothed = np.array(data_total[isotope])

            for index, value_outlier in helper_outlier.items():
                data_smoothed[index] = value_outlier

            data_smoothed.tolist()
        else:
            data_smoothed = np.array(data_total[isotope])
            data_smoothed.tolist()

        return data_smoothed, indices_outl

    def calculate_sensitivity_regression(self, xi_time, var_i, xi_opt):
        xi_time = np.array(xi_time[var_i])
        x = xi_time[:, 0]
        y = xi_time[:, 1]
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0] # m*x + c
        xi_opt[var_i] = [m, c]

class EssentialsSRM:
    def __init__(self):
        var_os = sys.platform
        self.var_os = var_os

    def place_srm_values(self, srm_name, srm_dict):
        path = os.getcwd()
        parent = os.path.dirname(path)
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        path_main = path

        if "/pysills" in path_main:
            path_main = path.replace("/pysills", "")
        elif "/tests" in path_main:
            path_main = path.replace("/tests", "")
        elif "/bin" in path_main:
            path_main = os.path.abspath(__file__)
            path_main = path_main.replace("/modules/essential_functions.py", "")
        elif "Scripts" in path_main:
            path_main = os.path.abspath(__file__)
            path_main = path_main.replace("modules", "")
            path_main = path_main.replace("essential_functions.py", "")
            path_main = path_main[:-1]
        elif "site-packages" in path_main:
            path_main = os.path.abspath(__file__)
            path_main = path_main.replace("modules", "")
            path_main = path_main.replace("essential_functions.py", "")
            path_main = path_main[:-1]

        if "local_packages" in path_main:
            path_main = path_main.replace("local_packages", "local-packages")

        if "site_packages" in path_main:
            path_main = path_main.replace("site_packages", "site-packages")

        list_srm = list(np.array(
            [["NIST 606"], ["NIST 610"], ["NIST 610 (GeoReM)"], ["NIST 610 (Spandler)"], ["NIST 611"],
             ["NIST 611 (GeoReM)"], ["NIST 612"], ["NIST 612 (GeoReM)"], ["NIST 613"], ["NIST 613 (GeoReM)"],
             ["NIST 614"], ["NIST 614 (GeoReM)"], ["NIST 615"], ["NIST 615 (GeoReM)"], ["NIST 616"],
             ["NIST 616 (GeoReM)"], ["NIST 617"], ["NIST 617 (GeoReM)"], ["USGS BCR-2G (GeoReM)"],
             ["USGS GSD-1G (GeoReM)"], ["USGS GSE-1G (GeoReM)"], ["B6"], ["Durango Apatite"], ["Scapolite 17"],
             ["BAM-376"], ["BCR-2G"], ["BL-Q"], ["Br-Glass"], ["GSD-1G (GeoReM)"], ["GSE-1G (GeoReM)"], ["GSE-2G"],
             ["HAL-O"], ["K-Br"], ["MACS-3"], ["Po 724"], ["STDGL-2B2"], ["OU-6 (GeoReM)"]])[:, 0])

        if "pysills" not in path_main:
            path_main = os.path.join(path_main, "pysills")

        if srm_name == "NIST 606":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_606.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 610":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_610.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 610 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_610_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 610 (Spandler)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_610_Spandler.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 611":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_611.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 611 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_611_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 612":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_612.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 612 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_612_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 613":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_613.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 613 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_613_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 614":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_614.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 614 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_614_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 615":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_615.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 615 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_615_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 616":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_616.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 616 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_616_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 617":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_617.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "NIST 617 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "NIST_617_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "USGS BCR-2G (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "USGS_BCR2G_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "USGS GSD-1G (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "USGS_GSD1G_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "USGS GSE-1G (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "USGS_GSE1G_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "B6":
            path_file = os.path.join(path_main, "lib", "srm", "B6.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "Durango Apatite":
            path_file = os.path.join(path_main, "lib", "srm", "Durango_Apatite.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "Scapolite 17":
            path_file = os.path.join(path_main, "lib", "srm", "Scapolite_17.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "BAM-376":
            path_file = os.path.join(path_main, "lib", "srm", "BAM_376.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "BCR-2G":
            path_file = os.path.join(path_main, "lib", "srm", "BCR_2G.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "BL-Q":
            path_file = os.path.join(path_main, "lib", "srm", "BL_Q.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "Br-Glass":
            path_file = os.path.join(path_main, "lib", "srm", "Br_Glass.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "GSD-1G (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "GSD_1G_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "GSE-1G (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "GSE_1G_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "GSE-2G":
            path_file = os.path.join(path_main, "lib", "srm", "GSE_2G.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "HAL-O":
            path_file = os.path.join(path_main, "lib", "srm", "HAL_O.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "K-Br":
            path_file = os.path.join(path_main, "lib", "srm", "K_Br.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "MACS-3":
            path_file = os.path.join(path_main, "lib", "srm", "MACS_3.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "Po 724":
            path_file = os.path.join(path_main, "lib", "srm", "Po_724.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "STDGL-2B2":
            path_file = os.path.join(path_main, "lib", "srm", "STDGL_2B2.csv")
            data_srm = data.general().importSRM(filename=path_file)
        elif srm_name == "OU-6 (GeoReM)":
            path_file = os.path.join(path_main, "lib", "srm", "OU_6_GeoReM.csv")
            data_srm = data.general().importSRM(filename=path_file)
        else:
            srm_name_new = srm_name.replace(" ", "_")
            path_file = os.path.join(path_main, "lib", "srm", srm_name_new)
            data_srm = data.general().importSRM(filename=path_file)

        for item in data_srm:
            srm_dict[srm_name][item[0]] = round(item[1], 4)