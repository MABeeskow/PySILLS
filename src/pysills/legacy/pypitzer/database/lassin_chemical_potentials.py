# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd

pd.set_option('display.precision', 11)

solids = {
    "LiCl-H2O": {
        "a1": 36.2702,
        "a2": 0.005655998,
        "a3": 2.696341,
        "a4": -13.2627354,
        "a5": 0,
    },
    "LiCl-2H2O": {
        "a1": 6.1532,
        "a2": -0.0064179,
        "a3": 0,
        "a4": 0,
        "a5": 0,
    },
    "LiCl0": {
        "a1": -3.5869,
        "a2": 0.007566,
        "a3": -1254.4,
        "a4": 0,
        "a5": 0,
    },
    "KCl": {
        "a1": 6.496259873,
        "a2": -0.012323368,
        "a3": -1537.997915,
        "a4": 1.507740146,
        "a5": -42632.32102,
    },
    "NaCl": {
        "a1": -752.24954,
        "a2": -0.11904958,
        "a3": 41385.703,
        "a4": 274.17933,
        "a5": -2480.9109e3,
    },
}

# create database
df = pd.DataFrame(columns=["a1", "a2", "a3", "a4", "a5"])

for key, value in solids.items():
    df.loc[key] = pd.Series(value)

lassin_chemical_potential_db = df
