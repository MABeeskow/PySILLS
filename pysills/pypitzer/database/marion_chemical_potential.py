# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd

pd.set_option('display.precision', 11)
compounds = {
    # O2(g) <-> O2(aq)
    "O2(g)": {
        'a1': 2.98399e-1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -5.59617e3,
        'a6': 0,
        'a7': 1.049668e6,
    },
    # 2H2O(1)  <->  2H2(g) + O2(g)
    "H2O(g)": {
        'a1': 3.92869e1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -6.87562e4,
        'a6': 0,
        'a7': 0,
    },
    # Fe2+ + H2O <-> FeOH+ + H+
    "Fe+2 + H2O": {
        'a1': 3.93e-1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -6.6392e3,
        'a6': 0,
        'a7': 0,
    },
    # FeCO3(0) <-> Fe2+ + CO3-2
    "FeCO3(0)": {
        'a1': -1.46641e1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 1.36517e3,
        'a6': 0,
        'a7': 0,
    },
    "FeCl2-4H2O": {
        'a1': -4.594879e0,
        'a2': 1.45731e-1,
        'a3': -3.461353e-4,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
    },
    # "FeCl2-4H2O": {
    #     'a1': 6.97, # Christov, 2005
    #     'a2': 0,
    #     'a3': 0,
    #     'a4': 0,
    #     'a5': 0,
    #     'a6': 0,
    #     'a7': 0,
    # },
    "FeCl2-6H2O": {
        'a1': -3.607762e2,
        'a2': 4.61798e0,
        'a3': -1.886403e-2,
        'a4': 2.525105e-5,
        'a5': 0,
        'a6': 0,
        'a7': 0,
    },
    "FeSO4-H2O": {
        'a1': 6.324332e0,
        'a2': -2.7915e-2,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
    },
    "FeSO4-7H2O": {
        'a1': 2.096187e1,
        'a2': -2.343349e-1,
        'a3': 4.92807e-4,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
    },
    "FeCO3": {
        'a1': -2.9654e1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 1.24845e3,
        'a6': 0,
        'a7': 0,
    },
    # 4Fe2+ + 10H2O + O2(g) <-> 4Fe(OH)3 + 8H+
    "Fe(OH)3": {
        'a1': -8.786e0,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 1.04807e4,
        'a6': 0,
        'a7': 0,
    },
    '2KCl-FeCl2-2H2O': {
        'a1': 10.109,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
    },

}

# create database
df = pd.DataFrame(columns=['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'])

for key, value in compounds.items():
    df.loc[key] = pd.Series(value)

marion_chemical_potential_db = df
