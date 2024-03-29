# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd

pd.set_option('display.precision', 11)
solids = {
    'CaSO4(AQ)': {
        'a1': -1.47477745e01,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 3.2640946e03,
        'a6': 0
    },
    'MgSO4(AQ)': {
        'a1': 3.65283115e02,
        'a2': -7.1578257e-01,
        'a3': 0,
        'a4': 0,
        'a5': -4.48753391e04,
        'a6': 0
    },
    'H2O(l)': {
        'a1': -1.4816780e2,
        'a2': 8.933802e-1,
        'a3': -2.332199e-3,
        'a4': 2.146860e-6,
        'a5': 0,
        'a6': 0,
    },
    'H2O(S)': {
        'a1': 7.875060393e03,
        'a2': 1.169118490e01,
        'a3': -1.7183789e-02,
        'a4': 1.24395543e-05,
        'a5': -9.3314790e04,
        'a6': -1.7287461e03
    },
    'NaCl': {
        'a1': 9.14839001e3,
        'a2': 8.22348745e0,
        'a3': -8.1288759e-3,
        'a4': 3.95552403e-6,
        'a5': -1.54040868e5,
        'a6': -1.83624247e3,
    },
    'NaCl-2H2O': {
        'a1': -1.2222551e04,
        'a2': -9.8806459e00,
        'a3': 8.46685083e-03,
        'a4': -3.4459117e-06,
        'a5': 2.09823965e05,
        'a6': 2.42328528e03,
    },
    'KCl': {
        'a1': -1.62917341e3,
        'a2': -1.51940390e0,
        'a3': 1.45249679e-3,
        'a4': -6.9427505e-7,
        'a5': 2.26012743e4,
        'a6': 3.33075506e2,
    },
    'CaCl2-6H2O': {
        'a1': 1.42290062e05,
        'a2': 1.61973105e02,
        'a3': -1.95332071e-01,
        'a4': 1.17636119e-04,
        'a5': -2.04059847e06,
        'a6': -2.97464810e04,
    },
    'MgCl2-6H2O': {
        'a1': 7.52225099e02,
        'a2': 1.17584653e-01,
        'a3': 0,
        'a4': 0,
        'a5': -2.43223909e04,
        'a6': -1.21990076e02,
    },
    'MgCl2-8H2O': {
        'a1': 2.27801976e03,
        'a2': 6.49361616e-01,
        'a3': 0,
        'a4': 0,
        'a5': -6.23075123e04,
        'a6': -3.95438891e02,
    },
    'MgCl2-12H2O': {
        'a1': 2.55008896e05,
        'a2': 2.44532240e02,
        'a3': -2.48807876e-01,
        'a4': 1.22425236e-04,
        'a5': -4.02988342e06,
        'a6': -5.18668604e04,
    },
    'KCl-MgCl2-6H2O': {
        'a1': -4.45702171e01,
        'a2': 2.32023790e-01,
        'a3': -7.14935692e-04,
        'a4': 5.32658215e-07,
        'a5': -4.24817923e03,
        'a6': 8.59110245e00,
    },
    '2KCl-FeCl2-2H2O': {
        'a1': 12.97,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    'CaCl2-2MgCl2-12H2O': {
        'a1': 8.03777918e01,
        'a2': -1.388069e-1,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    'Na2SO4-10H2O': {
        'a1': -0.4633773e2,
        'a2': 0.1753075,
        'a3': -0.9822103e-4,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    # 'Na2SO4-10H2O': {
    #     'a1': 8.44728050e04,
    #     'a2': 7.68443387e01,
    #     'a3': -7.4825816e-02,
    #     'a4': 3.51806085e-05,
    #     'a5': -1.3881852e06,
    #     'a6': -1.7026778e04,
    # },
    # "Na2SO4": {
    #     'a1': -0.1238537e1,
    #     'a2': 0.1929792e-2,
    #     'a3': 0,
    #     'a4': 0,
    #     'a5': 0,
    #     'a6': 0,
    # },
    "Na2SO4": {
        'a1': -3.9635632e03,
        'a2': -5.8114490e00,
        'a3': 7.59799462e-03,
        'a4': -4.6571737e-06,
        'a5': 3.93454893e04,
        'a6': 8.79598423e02,
    },
    "MgSO4-6H2O": {
        'a1': -0.57876e1,
        'a2': 0.68509e-2,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    "MgSO4-7H2O": {
        'a1': 0.3956e1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -0.24710e4,
        'a6': 0
    },
    "MgSO4-12H2O": {
        'a1': -0.2958180e2,
        'a2': 0.8851618e-1,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    "CaSO4": {
        'a1': -0.7822042e2,
        'a2': 0.6908174e0,
        'a3': -0.2246589e-2,
        'a4': 0.2344988e-5,
        'a5': 0,
        'a6': 0,
    },
    "CaSO4·2H2O": {
        'a1': -0.9107165e2,
        'a2': 0.7584271e0,
        'a3': -0.2370863e-2,
        'a4': 0.2456876e-5,
        'a5': 0,
        'a6': 0,
    },
    "(K,Na)3Na(SO4)2": {
        'a1': -0.6207986e2,
        'a2': 0.1527005e0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    "Na2Mg(SO4)2-4H2O": {
        'a1': -0.79121e1,
        'a2': 0.8220223e-2,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    "K2SO4": {
        'a1': 0.6500e1,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -0.31573e4,
        'a6': 0,
    },
    "K2Mg(SO4)2-6H2O": {
        'a1': -0.8661262e2,
        'a2': 0.470966e0,
        'a3': -0.7186864e-3,
        'a4': 0,
        'a5': 0,
        'a6': 0,
    },
    "LiCl-5H2O": {
        'a1': 13.9346,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -1684.852,
        'a6': 0,
    },
    "LiCl-3H2O": {
        'a1': 11.58593,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -720.9875,
        'a6': 0,
    },
    "LiCl-2H2O": {
        'a1': 8.482008,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -436.1729,
        'a6': 0,
    },
    "LiCl-H2O": {
        'a1': 410.8374,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -1.606861e04,
        'a6': -60.5503,
    },
    "LiCl": {
        'a1': 252.0552,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': -7.44290e03,
        'a6': -37.39279,
    }
}

# create database
df = pd.DataFrame(columns=['a1', 'a2', 'a3', 'a4', 'a5', 'a6'])

for key, value in solids.items():
    df.loc[key] = pd.Series(value)

spencer_chemical_potential_db = df