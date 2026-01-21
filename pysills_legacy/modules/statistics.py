#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# statistics.py
# Maximilian Beeskow
# 07.08.2021
# ----------------------
#
## MODULES
import numpy as np
import pandas as pd
from outliers import smirnov_grubbs as grubbs
import re
import matplotlib.pyplot as plt
from scipy import stats
#
## TOOLS
#
class statisticalAnalysis:
    #
    def __init__(self, data):
        self.data = data
    #
    def analyzeSensitivities(self, reference):
        # Input data
        xi = self.data
        self.reference = reference
        #
        #print("")
        #print("Statistical analysis of the sensitivity calculation (EXTERNAL STANDARD):")
        xiData = []
        for i in range(0, len(xi[0])):
            xiData.append([xi[0][i][0], [xi[0][i][2][0], xi[1][i][2][0], xi[2][i][2][0], xi[3][i][2][0]], [xi[0][i][2][1], xi[1][i][2][1], xi[2][i][2][1], xi[3][i][2][1]]])
        for i in range(0, len(xiData)):
           print(xiData[i][0], ":", "mean =", np.mean(xiData[i][1]), "std =", np.std(xiData[i][1], ddof=1), round(100*np.std(xiData[i][1], ddof=1)/np.mean(xiData[i][1]), 2), "%")
        print("")
        #
        data = []
        #
        for i in range(0, len(xiData)):
            data.append([xiData[i][0], np.mean(xiData[i][1]), np.std(xiData[i][1], ddof=1), self.reference])
        #
        return data
    #
    def analyze_xi(self, reference, isotopes):
        # Input data
        xi = self.data
        self.isotopes = isotopes
        self.reference = reference
        #
        #print("")
        #print("Statistical analysis of the sensitivity calculation (EXTERNAL STANDARD):")
        all_xi = [[self.isotopes[i], []] for i in range(len(self.isotopes))]
        for i in range(len(self.data[0])):
            for j in range(len(self.data)):
                all_xi[i][1].append(self.data[j][i])
                print(self.data[j][i])
        for i in range(len(all_xi)):
           print(all_xi[i][0], ":", "mean =", np.mean(all_xi[i][1]), "std =", np.std(all_xi[i][1], ddof=1), round(100*np.std(all_xi[i][1], ddof=1)/np.mean(all_xi[i][1]), 2), "%")
        print("")
        #
        data_raw = []
        for i in range(len(all_xi)):
            data_raw.append(pd.Series(all_xi[i][1]))
        df = pd.concat(data_raw, axis=1)
        df.columns = self.isotopes
        print(df)
        print(df.describe())
        data = []
        #
        for i in range(0, len(all_xi)):
            data.append([all_xi[i][0], np.mean(all_xi[i][1]), np.std(all_xi[i][1], ddof=1), self.reference])
        print(data)
        #
        return data, df
    #
    def analyzeConcentrations(self):
        # Input data
        inputC = self.data
        #
        list_meanC = []
        list_stdC = []
        for i in range(0, len(inputC[0])):
            list_meanC.append([inputC[0][i][0], []])
            list_stdC.append([inputC[0][i][0], []])
        for i in range(0, len(inputC)):
            for j in range(0, len(inputC[0])):
                if inputC[i][j][0] == list_meanC[j][0]:
                    list_meanC[j][1].append(inputC[i][j][2][0])
                    list_stdC[j][1].append(inputC[i][j][2][1])
        #print("")
        #print("Statistical analysis of the concentration calculation (SAMPLE):")
        #print("Number of measurements:", len(inputC))
        dataC = []
        for i in range(0, len(inputC[0])):
            dataC.append([inputC[0][i][0], [inputC[0][i][2][0], inputC[1][i][2][0]], [inputC[0][i][2][1], inputC[1][i][2][1]]])
        #for i in range(0, len(dataC)):
        #    print(dataC[i][0], ":", "mean =", round(np.mean(dataC[i][1]),2), "std =", round(np.mean(dataC[i][2]),2), round(100*np.mean(dataC[i][2])/np.mean(dataC[i][1]),2), "%")
        #print("")
        #
        data = []
        #
        for i in range(0, len(dataC)):
            data.append([dataC[i][0], np.mean(dataC[i][1]), np.std(dataC[i][1], ddof=1)])
        #
        return data

class SimpleStatistics:
    #
    def __init__(self, input_data):
        self.input_data = self.input_data
    #
    def convert_data_to_dataframe(self):
        pass


class Segmentation:
    #
    def __init__(self, data_input, isotopes):
        self.data_input = data_input
        self.isotopes = isotopes
    #
    def find_background_segments(self, isotope, threshold=200):
        indices = np.where(self.data_input > threshold)[0]
        print(isotope)
        # print("Mean(intensity) BG 1:", np.mean(self.data_input[0:indices[0]]))
        # print("Mean(intensity) BG 2:", np.mean(self.data_input[indices[-1]+1:-1]))
        limits_bg1 = [0, indices[0]]
        limits_bg2 = [indices[-1]+1, len(self.data_input)-1]
        # print(limits_bg1)
        # print(limits_bg2)
        #
        return [limits_bg1, limits_bg2]
    #
    def calculate_change(self, bg1_end, bg2_start):
        data = self.data_input[bg1_end:bg2_start].values
        change = np.around(np.array([(data[i]-data[i-1])/(data[i-1])*100 for i in range(1, len(data))]), 2)
        change = np.insert(change, 0, 0, axis=0)
        print(change)

class OutlierAnalysis:
    #
    def __init__(self, data_input):
        self.data_input = data_input
    #
    def grubbs_test_two_sided(self, alpha=0.05):
        """
        Performs a two-sided outlier test after Grubbs
        :param alpha: level of significance
        :return data_output: data array without outliers
        """
        data_output = grubbs.test(data=self.data_input, alpha=alpha)
        outliers = grubbs.max_test_outliers(data=self.data_input, alpha=.05)
        outlier_indices = grubbs.max_test_indices(data=self.data_input, alpha=.05)
        print("Outliers:", outliers)
        print("Indices:", outlier_indices)
        #
        return data_output
    #
    def find_outliers(self, limits_bg1, limits_sig, limits_bg2, threshold=1000):
        data_bg1 = self.data_input[limits_bg1[0]:limits_bg1[1]]
        data_sig = self.data_input[limits_sig[0]:limits_sig[1]]
        data_bg2 = self.data_input[limits_bg2[0]:limits_bg2[1]]

        filtered_bg1 = data_bg1[data_bg1 >= threshold]
        print("Filtered background:", filtered_bg1)

