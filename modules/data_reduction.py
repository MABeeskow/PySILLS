#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

# Name:		data_reduction.py
# Author:	Maximilian A. Beeskow
# Version:	pre-release
# Date:		13.09.2023

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
            engine="python")
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
    def __init__(self, dataframe, internal_standard=None, mode="specific"):
        self.dataframe = dataframe
        self.internal_standard = internal_standard
        self.mode = mode

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

    def get_intensity(self, interval_bg, interval_min, interval_incl=None):
        if self.mode == "specific":
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

    def get_intensity_ratio(self, isotope):
        if self.mode == "specific":
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

class SensitivityQuantification:
    def __init__(self, internal_standard, mode="specific"):
        self.internal_standard = internal_standard
        self.mode = mode

    def get_analytical_sensitivity(self):
        if self.mode == "specific":
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

    def get_normalized_sensitivity(self):
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

## TESTING -------------------------------------------------------------------------------------------------------------