# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read the csv file
df = pd.read_csv("E:\\work\\data\\low-T\\error_analysis_s2_4.csv")

# extract the column of interest
Na = df['Na']

# calculate the mean and standard deviation
mean = Na.mean()
std_dev = Na.std(ddof=1) # use Bessel's correction for sample standard deviation

# calculate the 68% confidence interval
lower_bound, upper_bound = mean - std_dev, mean + std_dev
uncertainty = (upper_bound - lower_bound) / 2

# plot the histogram with the confidence interval highlighted
n, bins, patches = plt.hist(Na, bins=30, alpha=0.5, edgecolor='black')
bin_centers = 0.5 * (bins[:-1] + bins[1:])
for patch, left, right in zip(patches, bins[:-1], bins[1:]):
    if left <= lower_bound or right >= upper_bound:
        patch.set_fc('gray')
plt.axvspan(lower_bound, upper_bound, alpha=0.2, color='gray')
plt.title("Na Histogram with 68% Confidence Interval")
plt.xlabel("Na Values")
plt.ylabel("Frequency")

# print the results
print("Mean: {:.2f}".format(mean))
print("Standard Deviation: {:.2f}".format(std_dev))
print("68% Confidence Interval: {:.2f} ± {:.2f}".format(mean, uncertainty))

plt.gcf().canvas.required_interactive_framework = 'TkAgg'
plt.show()
