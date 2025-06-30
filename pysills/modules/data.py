#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# data.py
# Maximilian Beeskow
# 30.06.2025
# ----------------------
#
## MODULES
import re, os
import numpy as np
import pandas as pd
import tkinter as tk
from pathlib import Path
#
## TOOLS
#
class Data:
    #
    def __init__(self, filename):
        self.filename = filename
    #
    def import_data_to_pandas(self, skip_header, skip_footer, delimiter=";", names=None):
        #
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.skip_footer = skip_footer
        self.names = names
        #
        dataframe = pd.read_csv(self.filename, sep=self.delimiter, header=self.skip_header, skipfooter=self.skip_footer,
                           names=self.names, engine="python")
        blank_df = dataframe.loc[dataframe.isnull().all(1)]
        if len(blank_df) > 0:
            first_blank_index = blank_df.index[0]
            dataframe = dataframe[:first_blank_index]
        #
        return dataframe
    #
    def import_as_list(self, skip_header=0, skip_footer=0, timestamp=None, delimiter=",", icpms=None):
        f = open(self.filename, 'r')
        imported_data = f.readlines()

        if timestamp != None and icpms != None:
            line_time = imported_data[timestamp]

            if icpms == "Finnigan MAT ELEMENT":
                key_time = re.search(r"(\w+)\,\s+(\w+)\s+(\d+)\,\s+(\d+)\s+(\d+)\:(\d+)\:(\d+)", line_time)
                dict_months = {
                    "January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
                    "July": "07", "August": "08", "September": "09", "October": "10", "November": "11",
                    "December": "12"}
                var_month = dict_months[key_time.group(2)]
                var_day = key_time.group(3)
                var_year = key_time.group(4)
                var_hour = key_time.group(5)
                var_minute = key_time.group(6)
                var_second = key_time.group(7)
                date_file = [str(var_day), str(var_month), str(var_year)]
                time_file = [str(var_hour), str(var_minute), str(var_second)]
                dates = [date_file, date_file]
                times = [time_file, time_file]
            elif icpms in ["Agilent 7900s", "Agilent 8900"]:
                line_time_start = imported_data[2]
                line_time_end = imported_data[-1]

                if "Printed" not in line_time_end:
                    line_time_end = imported_data[-2]

                key_start = re.search(
                    r"Acquired\s+\:\s+(\d+)\/(\d+)\/(\d+)\s+(\d+)\:(\d+)\:(\d+)( AM)?( PM)?( using Batch )(\w+)",
                    line_time_start)
                date_start = ["01", "01", "2000"]
                date_end = ["31", "12", "2000"]
                time_start = ["00", "00", "00"]
                time_end = ["23", "59", "59"]

                if key_start:
                    date_start = [str(key_start.group(1)), str(key_start.group(2)), str(key_start.group(3))]
                    time_start = [str(key_start.group(4)), str(key_start.group(5)), str(key_start.group(6))]

                key_end = re.search(r"\s+Printed:(\d+)\/(\d+)\/(\d+)\s+(\d+)\:(\d+)\:(\d+)(.*)+", line_time_end)

                if key_end:
                    date_end = [str(key_end.group(1)), str(key_end.group(2)), str(key_end.group(3))]
                    time_end = [str(key_end.group(4)), str(key_end.group(5)), str(key_end.group(6))]

                dates = [date_start, date_end]
                times = [time_start, time_end]
            elif icpms in ["Undefined", "Undefined ICP-MS"]:
                date_start = ["01", "01", "2000"]
                date_end = ["31", "12", "2000"]
                time_start = ["00", "00", "00"]
                time_end = ["23", "59", "59"]

                dates = [date_start, date_end]
                times = [time_start, time_end]
        else:
            line_time_start = imported_data[2]
            line_time_end = imported_data[-1]

            if "Printed" not in line_time_end:
                line_time_end = imported_data[-2]

            key_start = re.search(
                r"Acquired\s+\:\s+(\d+)\/(\d+)\/(\d+)\s+(\d+)\:(\d+)\:(\d+)( using Batch )(\w+)",
                line_time_start)

            if key_start:
                date_start = [str(key_start.group(1)), str(key_start.group(2)), str(key_start.group(3))]
                time_start = [str(key_start.group(4)), str(key_start.group(5)), str(key_start.group(6))]

            key_end = re.search(r"\s+Printed:(\d+)\/(\d+)\/(\d+)\s+(\d+)\:(\d+)\:(\d+)(.*)+", line_time_end)

            if key_end:
                date_end = [str(key_end.group(1)), str(key_end.group(2)), str(key_end.group(3))]
                time_end = [str(key_end.group(4)), str(key_end.group(5)), str(key_end.group(6))]

            dates = [date_start, date_end]
            times = [time_start, time_end]

        return dates, times

class Import:

    def __init__(self, filename):
        self.filename = filename

    def import_csv_files(self, rows_header, rows_footer, delimiter=","):
        input_data = np.genfromtxt(fname=self.filename, delimiter=delimiter,
                                   dtype=str, skip_header=rows_header, skip_footer=rows_footer)
        n_rows = len(input_data)
        n_columns = len(input_data[0])
        data = []

        for i in range(n_columns):
            data.append([str(input_data[0][i]), [], str(self.filename)])
        for i in range(n_columns):
            for j in range(1, n_rows):
                data[i][1].append(float(input_data[j][i]))

        return data

class general:

    def __init__(self):
        pass

    def importData(self, filename, delimiter, skipHeader, skipFooter):

        self.filename = filename
        self.delimiter = delimiter
        self.skipHeader = skipHeader
        self.skipFooter = skipFooter

        inputData = np.genfromtxt(self.filename, delimiter=self.delimiter, dtype=str, skip_header=self.skipHeader,
                                  skip_footer=self.skipFooter)
        nLines = len(inputData)
        nRows = len(inputData[0])
        data = []

        for i in range(0, nRows):
            data.append([str(inputData[0][i]), [], str(self.filename)])
        for i in range(0, nRows):
            for j in range(1, nLines):
                data[i][1].append(float(inputData[j][i]))

        return data

    def importSRM(self, filename, delimiter=";", skipHeader=0, skipFooter=0):
        self.filename = filename
        self.delimiter = delimiter
        self.skipHeader = skipHeader
        self.skipFooter = skipFooter

        obj_path = Path(self.filename)
        str_directory = obj_path.parent
        str_filename = obj_path.name

        if "(" in str_filename:
            str_filename_updated = str_filename.replace("(", "")
        else:
            str_filename_updated = str_filename

        if ")" in str_filename:
            str_filename_updated = str_filename.replace(")", "")
        else:
            str_filename_updated = str_filename

        if "-" in str_filename:
            str_filename_updated = str_filename.replace("-", "_")
        else:
            str_filename_updated = str_filename

        self.filename = os.path.join(str_directory, str_filename_updated)

        if "venv_" in self.filename:
            self.filename = self.filename.replace("venv_", "venv-")
        if "site_packages" in self.filename:
            self.filename = self.filename.replace("site_packages", "site-packages")
        if "local_packages" in self.filename:
            self.filename = self.filename.replace("local_packages", "local-packages")

        inputData = np.genfromtxt(self.filename, delimiter=self.delimiter, dtype=str, skip_header=self.skipHeader,
                                  skip_footer=self.skipFooter)
        nLines = len(inputData)
        nRows = len(inputData[0])
        data = []

        for i in range(0, nLines):
            data.append([inputData[i][0], float(inputData[i][1])])

        return data

class Segmentation:
    #
    def __init__(self, input_data):
        self.input_data = input_data
    #
    def find_background(self):
        bg_time = [[], []]
        sgn_time = []
        list_averages = [[], []]
        data_time = self.input_data[0]
        n_timesteps = len(data_time[1])
        data_isotopes = self.input_data[1:]
        n_isotopes = len(data_isotopes)
        n_data = len(data_isotopes[0][1])
        #print("n(isotopes):", n_isotopes)
        #print("n(data):", n_data, n_timesteps)
        #
        condition = False
        position = 0
        for i in range(n_isotopes):
            while condition == False:
                if data_isotopes[i][1][0] == 0.0:
                    position = i
                    list_averages.append(data_isotopes[i][1][0])
                    condition = True
                else:
                    continue
        #
        for i in range(1, n_data):
            data = np.mean(data_isotopes[position][1][:i])
            list_averages[0].append(data)
        for i in range(1, n_data):
            data = np.mean(data_isotopes[position][1][-i:])
            list_averages[1].append(data)
        for i in range(n_data):
            if list_averages[0][i] < 50.0:
                bg_time[0].append(data_time[1][i])
            else:
                break
        for i in range(1, n_data):
            if list_averages[1][i] < 25.0:
                bg_time[1].append(data_time[1][-i])
            else:
                break
        for i in range(len(bg_time[0]), n_data-len(bg_time[1])+1):
            sgn_time.append(data_time[1][i])
        del bg_time[1][-1]
        bg_time[1].reverse()
        #print("Background(1st):")
        #print(bg_time[0])
        #print("Signal:")
        #print(sgn_time)
        #print("Background(2nd):")
        #print(bg_time[1])
        #
        return bg_time, sgn_time
    #
    def select_background(self, start_1=0.0, end_1=10.0, start_2=None, end_2=None):
        bg_time = [[], []]
        positions = [[], []]
        data_time = self.input_data[0]
        n_timesteps = len(data_time[1])
        for i in range(n_timesteps):
            if start_1 <= data_time[1][i] <= end_1:
                bg_time[0].append(data_time[1][i])
                positions[0].append(i)
            elif start_2 != None and end_2 != None and start_2 <= data_time[1][i] <= end_2:
                bg_time[1].append(data_time[1][i])
                positions[1].append(i)
        #print("Background(1st):")
        #print(bg_time[0])
        #print(positions[0])
        #print("Background(2nd):")
        #print(bg_time[1])
        #print(positions[1])
        #
        return bg_time
    #
    def select_signal(self, start=40.0, end=80.0):
        sgn_time = []
        positions = []
        data_time = self.input_data[0]
        n_timesteps = len(data_time[1])
        for i in range(n_timesteps):
            if start <= data_time[1][i] <= end:
                sgn_time.append(data_time[1][i])
                positions.append(i)
        #print("Signal:")
        #print(sgn_time)
        #print(positions)
        #
        return sgn_time
#
class segmentation:
    #
    def __init__(self, inputData, inclusion):
        self.inputData = inputData
        self.inclusion = inclusion

    #
    def segmentData(self):
        #
        nData = len(self.inputData[1][1])
        segments = []
        nIsotopes = len(self.inputData) - 1
        #
        if self.inclusion == True:
            for i in range(0, 5):
                segments.append([])
        else:
            for i in range(0, nIsotopes):
                segments.append([self.inputData[i + 1][0], [], [], []])
            for i in range(0, nIsotopes):
                stepOn = 0
                for j in range(1, nData):
                    delta = self.inputData[1][1][j] - self.inputData[1][1][j - 1]
                    if delta < 1000:
                        stepOn += 1
                        segments[i][1].append(self.inputData[i + 1][1][j - 1])
                    else:
                        stepOn += 1
                        segments[i][1].append(self.inputData[i + 1][1][j - 1])
                        timeLaserOn = self.inputData[0][1][stepOn]
                        break
            # print("Laser on after", timeLaserOn, "s.")
            deltaSignal = []
            for i in range(stepOn, nData):
                deltaSignal.append(self.inputData[1][1][i] - self.inputData[1][1][i - 1])
            # print("deltaSignal:", deltaSignal)
            stepOff = 0
            deltaMeanSignal = []
            for i in range(1, len(deltaSignal)):
                mean = np.mean(deltaSignal[:i])
                deltaMeanSignal.append(mean)
                a = mean / np.mean(deltaMeanSignal[:i])
                # print("mean", mean)
                # print("a", a)
                if a >= 0.1:
                    stepOff += 1
                else:
                    stepOff += 1
                    timeLaserOff = self.inputData[0][1][stepOn + stepOff]
                    break
            # print("Laser off after", timeLaserOff, "s.")
            # print(stepOn, stepOff)
            for i in range(0, nIsotopes):
                for j in range(stepOn, stepOn + stepOff):
                    segments[i][2].append(self.inputData[i + 1][1][j])
            for i in range(0, nIsotopes):
                for j in range(stepOn + stepOff, len(self.inputData[0][1])):
                    segments[i][3].append(self.inputData[i + 1][1][j])
        #
        return segments, stepOn, stepOff

class DataReduction:
    """
    A class that reduces the input data
    """
    #
    def __init__(self, isotopes, signals):
        """
        :param isotopes: list, array - names of the measured isotopes
        :param signals: list, array - measured signal values in cps
        """
        self.isotopes = isotopes
        self.signals = signals
    #
    def calculate_signal_rations(self, internal_standard, signal_indices, treeview):
        results = np.zeros(len(self.isotopes))
        mean_internal = np.mean(self.signals[internal_standard][signal_indices[0]:signal_indices[1]])
        for i in treeview.get_children():
            treeview.delete(i)
        for isotope in self.isotopes:
            value = round(np.mean(self.signals[isotope][signal_indices[0]:signal_indices[1]])/mean_internal, 4)
            treeview.insert("", tk.END, values=[str(isotope)+" / "+str(internal_standard), str(value)])
        #
        return results