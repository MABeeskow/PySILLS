# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("E:\work\data\low-T\error_analysis2.csv")



# Calculate the mean and standard deviation of the "Na" column
mean = np.mean(df["Na"])
std_dev = np.std(df["Na"], ddof=1)

# Calculate the uncertainty of the mean
uncertainty = std_dev / np.sqrt(len(df["Na"]))

# Print the result
print('mean:', mean)
print('std_dev:', std_dev)
print("Uncertainty of the mean of Na column: ", uncertainty)


# Calculate the range of 1 standard deviation
lower_bound = mean - std_dev
upper_bound = mean + std_dev

# Plot the histogram of the "Na" column
plt.hist(df["Na"], bins=40)

# Highlight the range of 1 standard deviation
plt.axvline(x=lower_bound, color='r', linestyle='--')
plt.axvline(x=upper_bound, color='r', linestyle='--')

# Add labels and title
plt.xlabel("Na")
plt.ylabel("Frequency")
plt.title("Histogram of Na column with 1 std dev range")

# Show the plot
plt.show()