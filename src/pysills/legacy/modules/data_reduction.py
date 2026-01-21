#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

# Name:		data_reduction.py
# Author:	Maximilian A. Beeskow
# Version:	v1.0.77
# Date:		16.05.2025

#-----------------------------------------------------------------------------------------------------------------------

## MODULES -------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import os, time

## CLASSES -------------------------------------------------------------------------------------------------------------
class DataExtraction:
    def __init__(self, filename_long=None):
        self.filename_long = filename_long

    def find_header(self):
        file_content = open(self.filename_long[0])
        found_delimiter = False
        common_header_elements = ["Time", "Li7", "Na23", "Mg24", "Si29", "S32", "Cl35", "K39", "Ca44"]
        set_common = set(common_header_elements)
        for index, line in enumerate(file_content):
            if len(line) > 100 and found_delimiter == False:
                var_delimiter = self.get_delimiter(var_str=line)
                index_header = index
                line_header = line
                possible_header_elements = line_header.split(var_delimiter)
                if "\n" in possible_header_elements[-1]:
                    possible_header_elements[-1] = possible_header_elements[-1].replace("\n", "")
                set_possible = set(possible_header_elements)
                set_intersection = list(set_common & set_possible)
                if len(set_intersection) > 0:
                    found_delimiter = True
            else:
                set_intersection = []
            if len(set_intersection) > 0:
                break

        return index_header, possible_header_elements, var_delimiter

    def get_delimiter(self, var_str):
        possible_delimiter = [",", ";", " "]
        n_str = len(var_str)
        condition = False
        while condition == False:
            for delimiter in possible_delimiter:
                for element in var_str.split(delimiter):
                    n_element = len(element)
                    if n_element != n_str:
                        delimiter_working = delimiter
                        condition = True
                    if condition == True:
                        break
                if condition == True:
                    break

        return delimiter_working

    def find_dataset_end(self, var_delimiter, var_index_header):
        file_content = open(self.filename_long[0])
        last_data_line = 0
        for index, line in enumerate(file_content):
            if index > var_index_header:
                line_elements = line.split(var_delimiter)
                if len(line_elements) > 0:
                    if len(line_elements) > 2:
                        last_data_line = index
                    else:
                        break
                else:
                    break

        return last_data_line

    def get_file_creation_time(self, var_delimiter, meta_data=False):
        if meta_data == False:
            file_content = open(self.filename_long[0])
            common_date_keys = [
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Mon", "Tue", "Wed",
                "Thu", "Fri", "Sat", "Sun", "Acquired", "Printed", "Created", "January", "February", "March", "April",
                "May", "June", "July", "August", "September", "October", "November", "December"]
            set_common = set(common_date_keys)
            for index, line in enumerate(file_content):
                if len(line) < 100:
                    line_elements = line.split(var_delimiter)
                    if "\n" in line_elements[-1]:
                        line_elements[-1] = line_elements[-1].replace("\n", "")
                    set_possible = set(line_elements)
                    set_intersection = list(set_common & set_possible)
                    if len(set_intersection) > 0:
                        break
                    else:
                        for common_key in common_date_keys:
                            if common_key in line_elements:
                                print(common_key)
        else:
            path = self.filename_long[0]
            time_creation = os.stat(path).st_birthtime
            time_creation_converted = time.ctime(time_creation)
            t_obj = time.strptime(time_creation_converted)
            t_stamp = time.strftime("%H:%M:%S", t_obj)

        return line_elements

    def get_measurements(self, delimiter, skip_header, skip_footer):
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.skip_footer = skip_footer

        dataframe = pd.read_csv(
            self.filename_long, sep=self.delimiter, header=self.skip_header, skipfooter=self.skip_footer,
            engine="python", encoding="latin1")
        dataframe_blank = dataframe.loc[dataframe.isnull().all(1)]

        if len(dataframe_blank) > 0:
            first_blank_index = dataframe_blank.index[0]
            dataframe = dataframe[:first_blank_index]
        var_columns = dataframe.columns

        for column in var_columns:
            dataframe[column] = dataframe[column].astype(float)

        return dataframe

    def get_isotopes(self, dataframe):
        list_names = list(dataframe.columns.values)
        list_names.pop(0)
        list_isotopes = list_names

        return list_isotopes

    def get_times(self, dataframe):
        df_times = dataframe.iloc[:, 0]

        return df_times

class IntensityQuantification:
    def __init__(self, dataframe, internal_standard=None, mode="specific", project_type="MA", results_container=None):
        self.dataframe = dataframe
        self.internal_standard = internal_standard
        self.mode = mode
        self.project_type = project_type
        self.results_container = results_container

    def prepare_calculation_intervals(self, interval_bg=None, interval_mat=None, interval_incl=None):
        if interval_bg != None:
            condensed_interval = self.combine_all_intervals(interval_set=interval_bg)
        elif interval_mat != None:
            condensed_interval = self.combine_all_intervals(interval_set=interval_mat)
        elif interval_incl != None:
            condensed_interval = self.combine_all_intervals(interval_set=interval_incl)

        return condensed_interval

    def check_if_intervals_isolated(self, intervals_list_01, intervals_list_02=None):
        helper_isolated = []
        helper_overlapped = []
        if intervals_list_02 == None:
            intervals_list_02 = intervals_list_01
        for index_01, interval_01 in enumerate(intervals_list_01):
            for index_02, interval_02 in enumerate(intervals_list_02):
                if interval_02 != interval_01:
                    set_01 = set(range(interval_01[0], interval_01[1]))
                    set_02 = set(range(interval_02[0], interval_02[1]))
                    set_intersection = list(set_01 & set_02)
                    if len(set_intersection) > 0:
                        print("Overlap between:", interval_01, interval_02)
                    else:
                        print("No overlap between:", interval_01, interval_02)

    def combine_all_intervals(self, interval_set):
        condensed_intervals = {}
        if len(interval_set) > 1:
            helper_intervals = []
            for key, item in interval_set.items():
                helper_intervals.append(item["Indices"])
            helper_intervals.sort()
            for index, interval in enumerate(helper_intervals):
                indices_interval = list(range(interval[0], interval[1] + 1))
                if index == 0:
                    all_indices = indices_interval
                all_indices = sorted(np.unique(all_indices + indices_interval))
            all_indices = np.array(all_indices)
            diff_indices = []
            for index, value in enumerate(all_indices):
                if index == 0:
                    diff_indices.append(1)
                else:
                    diff_indices.append(value - all_indices[index - 1])
            indices_jump = [index for index, value in enumerate(diff_indices) if value != 1]
            if len(indices_jump) > 0:
                if len(indices_jump) > 1:
                    for index, value in enumerate(indices_jump):
                        if index == 0:
                            condensed_intervals[index + 1] = [all_indices[0], all_indices[value - 1]]
                            next_start = all_indices[value]
                        else:
                            if index == len(indices_jump) - 1:
                                condensed_intervals[index + 1] = [next_start, all_indices[value - 1]]
                                condensed_intervals[index + 2] = [all_indices[value], all_indices[-1]]
                            else:
                                condensed_intervals[index + 1] = [next_start, all_indices[value - 1]]
                                condensed_intervals[index + 2] = [all_indices[value - 1], all_indices[value]]
                                next_start = all_indices[value]
                else:
                    condensed_intervals[1] = [all_indices[0], all_indices[indices_jump[0] - 1]]
                    condensed_intervals[2] = [all_indices[indices_jump[0]], all_indices[-1]]
            else:
                condensed_intervals[1] = [all_indices[0], all_indices[-1]]
        else:
            for key, item in interval_set.items():
                condensed_intervals[key] = item["Indices"]

        return condensed_intervals

    def get_intensity(self, interval_bg=None, interval_min=None, interval_incl=None, data_key="Data RAW",
                      average_type="arithmetic mean", stack_intervals=False):
        """ Collects the signal intensities from all defined calculation intervals.
        -------
        Parameters
        interval_bg : dict
            Dictionary that contains the defined intervals for the background signal.
        interval_min : dict
            Dictionary that contains the defined intervals for the mineral/matrix signal.
        interval_incl : dict
            Dictionary that contains the defined intervals for the inclusion signal.
        data_key : str
            It specifies if the raw or smoothed data have to be considered.
        average_type : str
            It specifies if the arithmetic mean or the median has to be used.
        stack_intervals : boolean
            It defines if the interval dataset has to be stacked or averaged.
        -------
        Returns
        helper_results : dict
            Dictionary that contains the results.
        -------
        """
        if self.project_type == "MA":
            list_focus = ["BG", "MAT"]
        else:
            list_focus = ["BG", "MAT", "INCL"]

        if data_key == "Data SMOOTHED":
            data_key = "Data IMPROVED"

        helper_results = {}

        for isotope in self.dataframe.keys():
            if self.project_type == "MA":
                helper_results[isotope] = {
                    "uncorrected": {"BG": 0, "MAT": 0, "1 SIGMA BG": 0, "1 SIGMA MAT": 0},
                    "corrected": {"BG": 0, "MAT": 0, "1 SIGMA BG": 0, "1 SIGMA MAT": 0}}
            else:
                helper_results[isotope] = {
                    "uncorrected": {"BG": 0, "MAT": 0, "INCL": 0, "1 SIGMA BG": 0, "1 SIGMA MAT": 0, "1 SIGMA INCL": 0},
                    "corrected": {"BG": 0, "MAT": 0, "INCL": 0, "MIX": 0, "1 SIGMA BG": 0, "1 SIGMA MAT": 0,
                                  "1 SIGMA INCL": 0, "1 SIGMA MIX": 0}}

            for focus in list_focus:
                if focus == "BG":
                    # Background
                    helper_bg = []
                    helper_bg_2 = []
                    helper_bg_sigma = []
                    helper_bg_parts = []
                    for index, interval in interval_bg.items():
                        start_index = interval[0]
                        end_index = interval[1] + 1
                        dataset = self.dataframe[isotope][data_key][start_index:end_index]
                        helper_bg_2.extend(dataset)

                        if stack_intervals == False:
                            if average_type == "arithmetic mean":
                                helper_bg.append(np.mean(dataset))
                            else:
                                helper_bg.append(np.median(dataset))
                            helper_bg_sigma.append(np.std(dataset, ddof=1)/np.sqrt(len(dataset)))
                        else:
                            helper_bg.extend(dataset)

                    n_dataset = len(helper_bg_2)
                    if n_dataset % 2 == 0:
                        n_1st_half = int(len(helper_bg_2)/2)
                    else:
                        n_1st_half = int(round(len(helper_bg_2)/2 + 0.5, 0))

                    if average_type == "arithmetic mean":
                        dataset_1st_half = round(np.mean(helper_bg_2[:n_1st_half]), 4)
                        dataset_2nd_half = round(np.mean(helper_bg_2[n_1st_half:]), 4)
                    else:
                        dataset_1st_half = round(np.median(helper_bg_2[:n_1st_half]), 4)
                        dataset_2nd_half = round(np.median(helper_bg_2[n_1st_half:]), 4)

                    if dataset_2nd_half > 0:
                        parallelism_factor = round(dataset_1st_half/dataset_2nd_half, 4)
                    else:
                        parallelism_factor = np.nan

                    if stack_intervals == True:
                        helper_bg_sigma.append(np.std(helper_bg, ddof=1)/np.sqrt(len(helper_bg)))

                    if average_type == "arithmetic mean":
                        result_bg = np.mean(helper_bg_2)
                        result_bg_1sigma = np.mean(np.std(helper_bg_2, ddof=1)/np.sqrt(len(helper_bg_2)))
                        results_bg_sigma = np.std(helper_bg_2, ddof=1)
                    else:
                        result_bg = np.median(helper_bg_2)
                        result_bg_1sigma = np.median(np.std(helper_bg_2, ddof=1)/np.sqrt(len(helper_bg_2)))
                        results_bg_sigma = np.std(helper_bg_2, ddof=1)

                    helper_results[isotope]["uncorrected"]["BG"] = result_bg
                    helper_results[isotope]["uncorrected"]["1 SIGMA BG"] = result_bg_1sigma
                    helper_results[isotope]["corrected"]["BG"] = result_bg - result_bg
                    helper_results[isotope]["corrected"]["1 SIGMA BG"] = result_bg_1sigma - result_bg_1sigma
                    self.results_container["BG"][isotope] = result_bg
                    self.results_container["BG SIGMA"][isotope] = results_bg_sigma
                    self.results_container["N BG"][isotope] = len(helper_bg_2)
                    self.results_container["Parallelism BG"][isotope] = [dataset_1st_half, dataset_2nd_half]
                elif focus == "MAT":
                    # Mineral/Matrix Signal
                    helper_mat = []
                    helper_mat_sigma = []
                    helper_mat_2 = []
                    for index, interval in interval_min.items():
                        start_index = interval[0]
                        end_index = interval[1] + 1
                        dataset = self.dataframe[isotope][data_key][start_index:end_index]
                        helper_mat_2.extend(dataset)

                        if stack_intervals == False:
                            if average_type == "arithmetic mean":
                                helper_mat.append(np.mean(dataset))
                            else:
                                helper_mat.append(np.median(dataset))
                            helper_mat_sigma.append(np.std(dataset, ddof=1)/np.sqrt(len(dataset)))
                            helper_mat_sigma.append(np.std(dataset, ddof=1)/np.sqrt(len(dataset)))
                        else:
                            helper_mat.extend(dataset)

                    n_dataset = len(helper_mat_2)
                    if n_dataset % 2 == 0:
                        n_1st_half = int(len(helper_mat_2)/2)
                    else:
                        n_1st_half = int(round(len(helper_mat_2)/2 + 0.5, 0))

                    if average_type == "arithmetic mean":
                        dataset_1st_half = round(np.mean(helper_mat_2[:n_1st_half]), 4)
                        dataset_2nd_half = round(np.mean(helper_mat_2[n_1st_half:]), 4)
                    else:
                        dataset_1st_half = round(np.median(helper_mat_2[:n_1st_half]), 4)
                        dataset_2nd_half = round(np.median(helper_mat_2[n_1st_half:]), 4)

                    if dataset_2nd_half > 0:
                        parallelism_factor = round(dataset_1st_half/dataset_2nd_half, 4)
                    else:
                        parallelism_factor = np.nan

                    if stack_intervals == True:
                        helper_mat_sigma.append(np.std(helper_mat, ddof=1)/np.sqrt(len(helper_mat)))

                    if average_type == "arithmetic mean":
                        result_mat = np.mean(helper_mat_2)
                        result_mat_1sigma = np.mean(np.std(helper_mat_2, ddof=1)/np.sqrt(len(helper_mat_2)))
                        results_mat_sigma = np.std(helper_mat_2, ddof=1)
                    else:
                        result_mat = np.median(helper_mat_2)
                        result_mat_1sigma = np.median(np.std(helper_mat_2, ddof=1)/np.sqrt(len(helper_mat_2)))
                        results_mat_sigma = np.std(helper_mat_2, ddof=1)

                    helper_results[isotope]["uncorrected"]["MAT"] = result_mat
                    helper_results[isotope]["uncorrected"]["1 SIGMA MAT"] = result_mat_1sigma
                    helper_results[isotope]["corrected"]["MAT"] = result_mat - result_bg
                    helper_results[isotope]["corrected"]["1 SIGMA MAT"] = result_mat_1sigma - result_bg_1sigma
                    self.results_container["MAT"][isotope] = result_mat
                    self.results_container["1 SIGMA MAT"][isotope] = result_mat_1sigma
                    self.results_container["MAT SIGMA"][isotope] = results_mat_sigma
                    self.results_container["N MAT"][isotope] = len(helper_mat_2)
                    self.results_container["Parallelism MAT"][isotope] = [dataset_1st_half, dataset_2nd_half]
                elif focus == "INCL":
                    # Inclusion Signal
                    helper_incl = []
                    helper_incl_2 = []
                    helper_incl_sigma = []
                    for index, interval in interval_incl.items():
                        start_index = interval[0]
                        end_index = interval[1] + 1
                        dataset = self.dataframe[isotope][data_key][start_index:end_index]
                        helper_incl_2.extend(dataset)

                        if stack_intervals == False:
                            if average_type == "arithmetic mean":
                                helper_incl.append(np.mean(dataset))
                            else:
                                helper_incl.append(np.median(dataset))
                            helper_incl_sigma.append(np.std(dataset, ddof=1)/np.sqrt(len(dataset)))
                        else:
                            helper_incl.extend(dataset)

                    n_dataset = len(helper_incl_2)
                    if n_dataset % 2 == 0:
                        n_1st_half = int(len(helper_incl_2)/2)
                    else:
                        n_1st_half = int(round(len(helper_incl_2)/2 + 0.5, 0))

                    if average_type == "arithmetic mean":
                        dataset_1st_half = round(np.mean(helper_incl_2[:n_1st_half]), 4)
                        dataset_2nd_half = round(np.mean(helper_incl_2[n_1st_half:]), 4)
                    else:
                        dataset_1st_half = round(np.median(helper_incl_2[:n_1st_half]), 4)
                        dataset_2nd_half = round(np.median(helper_incl_2[n_1st_half:]), 4)

                    if dataset_2nd_half > 0:
                        parallelism_factor = round(dataset_1st_half/dataset_2nd_half, 4)
                    else:
                        parallelism_factor = np.nan

                    if stack_intervals == True:
                        helper_incl_sigma.append(np.std(helper_incl, ddof=1)/np.sqrt(len(helper_incl)))

                    if average_type == "arithmetic mean":
                        result_incl = np.mean(helper_incl_2)
                        result_incl_1sigma = np.mean(np.std(helper_incl_2, ddof=1)/np.sqrt(len(helper_incl_2)))
                        results_incl_sigma = np.std(helper_incl_2, ddof=1)
                    else:
                        result_incl = np.median(helper_incl_2)
                        result_incl_1sigma = np.median(np.std(helper_incl_2, ddof=1)/np.sqrt(len(helper_incl_2)))
                        results_incl_sigma = np.std(helper_incl_2, ddof=1)

                    helper_results[isotope]["uncorrected"]["INCL"] = result_incl
                    helper_results[isotope]["uncorrected"]["1 SIGMA INCL"] = result_incl_1sigma
                    helper_results[isotope]["corrected"]["MIX"] = result_incl - result_bg
                    helper_results[isotope]["corrected"]["1 SIGMA MIX"] = result_incl_1sigma - result_bg_1sigma
                    self.results_container["INCL"][isotope] = result_incl
                    self.results_container["1 SIGMA INCL"][isotope] = result_incl_1sigma
                    self.results_container["INCL SIGMA"][isotope] = results_incl_sigma
                    self.results_container["N INCL"][isotope] = len(helper_incl_2)
                    self.results_container["Parallelism INCL"][isotope] = [dataset_1st_half, dataset_2nd_half]

            # for key, item in helper_results[isotope].items():
            #     print(key, item)

        return self.results_container

    def get_intensity_corrected(self, data_container, data_container_ratio=None, isotope_is=None, mode=None,
                                isotope_t=None):
        """ Calculates the background- and partially also matrix-corrected signal intensities.
        -------
        Parameters
        data_container : dict
            Dictionary that contains the previously extracted signal intensities.
        mode : int
            It defines which quantification method has to be used.
        isotope_t : str
            It defines the special isotope that is needed for the quantification.
        -------
        Returns
        helper_results : dict
            Dictionary that contains the results.
        -------
        """
        if self.project_type == "MA":
            list_focus = ["MAT"]
        else:
            list_focus = ["MAT", "INCL"]

        for isotope in data_container["BG"].keys():
            if isotope.isdigit():
                pass
            else:
                intensity_bg_i = data_container["BG"][isotope]
                for focus in list_focus:
                    if focus == "MAT":
                        intensity_sig2_i = data_container[focus][isotope]
                        if None in [intensity_sig2_i, intensity_bg_i]:
                            value_mat_i = None
                        else:
                            value_mat_i = intensity_sig2_i - intensity_bg_i

                        if value_mat_i != None:
                            if value_mat_i > 0:
                                result_mat_i = value_mat_i
                            else:
                                result_mat_i = 0.0
                        else:
                            result_mat_i = np.nan

                        self.results_container["BG"][isotope] = 0.0
                        self.results_container[focus][isotope] = result_mat_i
                    elif focus == "INCL":
                        intensity_sig2_i = data_container["MAT"][isotope]
                        intensity_sig3_i = data_container[focus][isotope]
                        intensity_mix_i = intensity_sig3_i - intensity_bg_i
                        intensity_mat_i = intensity_sig2_i - intensity_bg_i

                        if isotope_t != None:
                            intensity_bg_t = data_container["BG"][isotope_t]
                            intensity_sig2_t = data_container["MAT"][isotope_t]
                            intensity_sig3_t = data_container[focus][isotope_t]
                            intensity_mat_t = intensity_sig2_t - intensity_bg_t

                        if intensity_mix_i > 0:
                            intensity_mix_i = intensity_mix_i
                        else:
                            intensity_mix_i = 0.0

                        if intensity_mat_i > 0:
                            intensity_mat_i = intensity_mat_i
                        else:
                            intensity_mat_i = 0.0

                        if isotope_t != None:
                            if intensity_mat_t > 0:
                                intensity_mat_t = intensity_mat_t
                            else:
                                intensity_mat_t = 0.0

                        if mode == 0:   # Heinrich et al. (2003)
                            intensity_mix_t = intensity_sig3_t - intensity_bg_t
                            value_incl_i = intensity_mix_i - intensity_mix_t*(intensity_mat_i/intensity_mat_t)
                        elif mode == 1: # "SILLS (without R)"
                            intensity_incl_mat_t = intensity_sig3_t - intensity_bg_t
                            intensity_incl_mat_i = (intensity_incl_mat_t/intensity_mat_t)*intensity_mat_i
                            value_incl_i = intensity_mix_i - intensity_incl_mat_i
                        elif mode == 2: # "SILLS (with R)"
                            intensity_incl_mat_t = intensity_sig3_t - intensity_bg_t
                            intensity_incl_mat_i = (intensity_incl_mat_t/intensity_mat_t)*intensity_mat_i
                            if intensity_mat_i > 0:
                                factor_r = intensity_incl_mat_i/intensity_mat_i
                            else:
                                factor_r = 0.0
                            value_incl_i = intensity_mix_i - factor_r*intensity_mat_i
                        elif mode == 3: # "Theory"
                            intensity_incl_mat_t = intensity_sig3_t - intensity_bg_t
                            intensity_incl_mat_i = (intensity_incl_mat_t/intensity_mat_t)*intensity_mat_i
                            value_incl_i = intensity_sig3_i - intensity_bg_i - intensity_incl_mat_i

                        if value_incl_i > 0:
                            result_incl_i = value_incl_i
                        else:
                            result_incl_i = 0.0

                        self.results_container[focus][isotope] = result_incl_i

                        if "MIX" not in self.results_container:
                            self.results_container["MIX"] = {}

                        if isotope not in self.results_container["MIX"]:
                            self.results_container["MIX"][isotope] = intensity_mix_i

                        if "MAT-INCL" not in self.results_container:
                            self.results_container["MAT-INCL"] = {}

                        if isotope not in self.results_container["MAT-INCL"]:
                            try:
                                self.results_container["MAT-INCL"][isotope] = intensity_incl_mat_i
                            except:
                                intensity_incl_mat_i = intensity_sig3_i - result_incl_i - intensity_bg_i
                                self.results_container["MAT-INCL"][isotope] = intensity_incl_mat_i

        return self.results_container

    def get_averaged_intensities(self, data_container, average_type="arithmetic mean"):
        """ Calculates the intensity average (arithmetic mean or median) for all isotopes.
        -------
        Parameters
        data_container : dict
            Dictionary that contains the previously extracted signal intensities.
        average_type : str
            It defines which average has to be used for the quantification.
        -------
        Returns
        helper_results : dict
            Dictionary that contains the results.
        -------
        """
        helper_results = {}
        for filename, item in data_container.items():
            if type(item) == dict:
                for isotope in item["MAT"].keys():
                    if isotope not in helper_results:
                        helper_results[isotope] = []

                    intensity_mat_i = item["MAT"][isotope]
                    helper_results[isotope].append(intensity_mat_i)

        for isotope, item in helper_results.items():
            if isotope.isdigit():
                pass
            else:
                if average_type == "arithmetic mean":
                    result_i = np.mean(item)
                elif average_type == "median":
                    result_i = np.median(item)

                self.results_container[isotope] = result_i

        return self.results_container

    def get_intensity_ratio(self, data_container, dict_is, filename_short=None, datatype=None):
        """ Calculates the intensity ratio for all isotopes.
        -------
        Parameters
        data_container : dict
            Dictionary that contains the previously extracted signal intensities.
        dict_is : dict
            Dictionary that contains information about the internal standard of every file.
        filename_short : str
            Short version of the file of interest (only needed for 'Quick Results' mode).
        datatype : str
            It specifies the data type (only needed for the final 'Results' mode).
        -------
        Returns
        -------
        """
        if self.project_type == "MA":
            list_focus = ["MAT"]
        else:
            list_focus = ["MAT", "INCL"]

        if filename_short != None:
            if filename_short in dict_is["STD"]:
                isotope_is = dict_is["STD"][filename_short]
                for focus in ["MAT"]:
                    value_is = data_container[filename_short][focus][isotope_is]
                    for isotope, value in data_container[filename_short][focus].items():
                        if value_is > 0:
                            result_i = value/value_is
                        else:
                            result_i = np.nan

                        self.results_container[filename_short][focus][isotope] = result_i
            elif filename_short in dict_is["SMPL"]:
                #isotope_is = dict_is["SMPL"][filename_short]
                for focus in list_focus:
                    if focus in dict_is["SMPL"][filename_short]:
                        isotope_is = dict_is["SMPL"][filename_short][focus]
                    else:
                        isotope_is = dict_is["SMPL"][filename_short]

                    value_is = data_container[filename_short][focus][isotope_is]
                    for isotope, value in data_container[filename_short][focus].items():
                        if value_is > 0:
                            result_i = value/value_is
                        else:
                            result_i = np.nan

                        self.results_container[filename_short][focus][isotope] = result_i
            else:
                print("File", filename_short, "was not found!")
        else:
            for filetype in ["STD", "SMPL"]:
                for filename_short, isotope_is in dict_is[filetype].items():
                    if filetype == "STD":
                        list_focus = ["MAT"]
                    else:
                        if self.project_type == "MA":
                            list_focus = ["MAT"]
                        else:
                            list_focus = ["MAT", "INCL"]

                    for focus in list_focus:
                        value_is = data_container[filetype][datatype][filename_short][focus][isotope_is]
                        if value_is != None:
                            for isotope, value in data_container[filetype][datatype][filename_short][focus].items():
                                if value_is > 0:
                                    result_i = value/value_is
                                else:
                                    result_i = np.nan

                                self.results_container[filetype][datatype][filename_short][focus][isotope] = result_i

        return self.results_container

class SensitivityQuantification:
    def __init__(self, dataframe_01, dataframe_02, mode="specific", project_type="MA", results_container=None):
        self.dataframe_01 = dataframe_01
        self.dataframe_02 = dataframe_02
        self.mode = mode
        self.project_type = project_type
        self.results_container = results_container

    def get_normalized_sensitivity(self, filename_short=None, filetype=None, datatype=None, data_sensitivity=None,
                                   dict_is=None):
        """ Calculates the normalized sensitivity for all isotopes.
        -------
        Parameters
        filename_short : str
            Short version of the file of interest (only needed for 'Quick Results' mode).
        filetype : str
            File type (e.g. STD) (only needed for 'Quick Results' mode).
        datatype : str
            Data type (e.g. RAW) (only needed for 'Final Results' mode).
        data_sensitivity : dict
            It contains the analytical sensitivity data.
        dict_is : dict
            It contains information about the internal standard.
        -------
        Returns
        -------
        """
        if filename_short != None:
            if filetype == "STD":
                for isotope, intensity_i in self.dataframe_01["MAT"].items():
                    concentration_i = self.dataframe_02["MAT"][isotope]

                    if intensity_i != None and concentration_i > 0:
                        result_i = intensity_i/concentration_i
                    else:
                        result_i = 0.0

                    self.results_container[filename_short]["MAT"][isotope] = result_i
            else:
                str_is = dict_is[filetype][filename_short]
                intensity_is = self.dataframe_01["MAT"][str_is]
                concentration_is = self.dataframe_02["MAT"][str_is]
                for isotope, intensity_i in self.dataframe_01["MAT"].items():
                    sensitivity_i = data_sensitivity["MAT"][isotope]

                    if concentration_is > 0:
                        result_i = (sensitivity_i*intensity_is)/concentration_is
                    else:
                        result_i = 0.0

                    self.results_container[filename_short]["MAT"][isotope] = result_i
        else:
            for filetype in ["STD", "SMPL"]:
                if filetype == "STD":
                    for filename_short, dataset_01 in self.dataframe_01[filetype][datatype].items():
                        if type(dataset_01) == dict:
                            for isotope, intensity_i in dataset_01["MAT"].items():
                                concentration_i = self.dataframe_02[filetype][datatype][filename_short]["MAT"][isotope]

                                if intensity_i != None and concentration_i > 0:
                                    result_i = intensity_i/concentration_i
                                else:
                                    result_i = 0.0

                                self.results_container[filetype][datatype][filename_short]["MAT"][isotope] = result_i
                else:
                    for filename_short, dataset_01 in self.dataframe_01[filetype][datatype].items():
                        str_is = dict_is[filetype][filename_short]
                        intensity_is = self.dataframe_01[filetype][datatype][filename_short]["MAT"][str_is]
                        concentration_is = self.dataframe_02[filetype][datatype][filename_short]["MAT"][str_is]
                        for isotope, intensity_i in dataset_01["MAT"].items():
                            sensitivity_i = data_sensitivity[filetype][datatype][filename_short]["MAT"][isotope]

                            if concentration_is != None:
                                if concentration_is > 0:
                                    result_i = (sensitivity_i*intensity_is)/concentration_is
                                else:
                                    result_i = np.nan
                            else:
                                result_i = np.nan

                            self.results_container[filetype][datatype][filename_short]["MAT"][isotope] = result_i

        return self.results_container

    def get_analytical_sensitivity(self):
        if self.mode == "specific":
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

    def get_relative_sensitivity_factor(self):
        if self.mode == "specific":
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

class CompositionQuantification:
    def __init__(self, internal_standard, mode="specific"):
        self.internal_standard = internal_standard
        self.mode = mode

    def get_composition(self):
        if self.mode == "specific":
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass
        else:
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass

    def get_composition_ratio(self):
        if self.mode == "specific":
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass
        else:
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass

    def get_limit_of_detection(self):
        if self.mode == "specific":
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass
        else:
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass

class LinearRegression:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values

    def calculate_linar_regression(self):
            mean_x = np.mean(self.x_values)
            mean_y = np.mean(self.y_values)
            helper_xy = 0
            helper_x2 = 0
            n = len(self.x_values)

            for index, x_value in enumerate(self.x_values):
                y_value = self.y_values[index]
                helper_xy += x_value*y_value
                helper_x2 += x_value**2

            upper_term = helper_xy - n*mean_x*mean_y
            lower_term = helper_x2 - n*mean_x**2
            b = upper_term/lower_term
            a = mean_y - b*mean_x

            return a, b

## TESTING -------------------------------------------------------------------------------------------------------------