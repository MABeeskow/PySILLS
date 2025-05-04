# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd

pd.set_option('display.precision', 11)
compounds = {
    "LiCl0": {
        'a1': -3.5869,
        'a2': 0.007566,
        'a3': -1254.4,
        'a4': 0,
        'a5': 0,
    },
    "LiCl-2H2O": {
        'a1': 6.1532,
        'a2': -0.0064179,
        'a3': 0,
        'a4': 0,
        'a5': 0,
    },
    "LiCl-H2O": {
        'a1': 36.2702,
        'a2': 0.005655998,
        'a3': 2.696341,
        'a4': -13.2627354,
        'a5': 0,
    },
    "3LiOH-LiCl": {
        'a1': 9.269,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
    },
    "LiOH-LiCl": {
        'a1': 6.593,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
    },
    "LiOH-3LiCl": {
        'a1': 17.95,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
    },
}

# create database
df = pd.DataFrame(columns=['a1', 'a2', 'a3', 'a4', 'a5'])

for key, value in compounds.items():
    df.loc[key] = pd.Series(value)

lassin_chemical_potential_db = df
