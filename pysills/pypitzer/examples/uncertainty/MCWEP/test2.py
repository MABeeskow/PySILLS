# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read the csv file
df = pd.read_csv("E:\\work\\data\\low-T\\error_analysis.csv")

# extract the columns of interest
RK = df['RK']
Tm = df['Tm']
mNa = df['mNa']

# plot the histograms
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
axs[0].hist(RK, alpha=0.5, edgecolor='black', bins=np.linspace(RK.min(), RK.max(), 30))
axs[0].set_title("RK")
axs[1].hist(Tm, alpha=0.5, edgecolor='black', bins=np.linspace(Tm.min(), Tm.max(), 30))
axs[1].set_title("Tm")
axs[2].hist(mNa, alpha=0.5, edgecolor='black', bins=np.linspace(mNa.min(), mNa.max(), 30))
axs[2].set_title("mNa")

# find the 95% confidence interval for the last histogram
n, bins, patches = axs[2].hist(mNa, alpha=0.5, edgecolor='black', bins=np.linspace(mNa.min(), mNa.max(), 30))
bin_centers = 0.5 * (bins[:-1] + bins[1:])
cdf = np.cumsum(n)
cdf = cdf / cdf[-1]
lower_bound = np.interp(0.05, cdf, bin_centers)
upper_bound = np.interp(0.95, cdf, bin_centers)
conf_interval = (lower_bound, upper_bound)
print("95% confidence interval for mNa histogram:", conf_interval)

# add a transparent gray rectangle to represent the 95% confidence interval in the last histogram
for patch, left, right in zip(patches, bins[:-1], bins[1:]):
    if left <= lower_bound or right >= upper_bound:
        patch.set_alpha(0.5)
        patch.set_fc('gray')

# save the plot to pdf
plt.tight_layout()
plt.savefig("E:\\work\\plots\\error_histogram.pdf")
plt.show()