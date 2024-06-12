# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Load the CSV file
data = pd.read_csv(r'E:\work\data\low-T\error_analysis.csv')

# Extract the data columns
RK = data['RK']
Tm = data['Tm']
mNa = data['mNa']

# Plot the histograms
fig, axs = plt.subplots(1, 3, figsize=(10, 4))

axs[0].hist(RK, color='blue')
axs[0].set_xlabel('RK')
axs[0].set_ylabel('Count')

axs[1].hist(Tm, color='green')
axs[1].set_xlabel('Tm')
axs[1].set_ylabel('Count')

axs[2].hist(mNa, color='red')
axs[2].set_xlabel('mNa')
axs[2].set_ylabel('Count')

# Calculate the 68% confidence interval for mNa
conf_int = stats.norm.interval(0.68, loc=np.mean(mNa), scale=np.std(mNa) / np.sqrt(len(mNa)))

print(conf_int)
# Calculate the uncertainty as half of the range of the confidence interval
uncertainty = (conf_int[1] - conf_int[0]) / 2

# Plot the confidence interval
axs[2].axvspan(conf_int[0], conf_int[1], alpha=0.5, color='grey')

# Show the plot
plt.show()

plt.savefig(r'E:\work\plots\error histogram.pdf', format='pdf')
mNa_mean = np.mean(mNa)

# Print the mean and uncertainty as x ± δx
print('Mean mNa: {:.3f} ± {:.3f}'.format(mNa_mean, uncertainty))
# Save the figure to a PDF file
