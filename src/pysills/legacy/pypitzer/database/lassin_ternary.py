# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import pandas as pd

pd.set_option('display.precision', 11)

species = {
    ('psi', 'Li+', 'Na+', 'Cl-'): {
        'a1': -0.03575475,
        'a2': 0.065e-3,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
        'a8': 0,
    },
    ('psi', 'Li+', 'K+', 'Cl-'): {
        'a1': 0.388539791,
        'a2': 1.38012743e-3,
        'a3': -1.3143039236e-6,
        'a4': 0,
        'a5': 0,
        'a6': -0.1229797915,
        'a7': 0.0280301705,
        'a8': 0,
    },
    ('psi', 'Na+', 'K+', 'Cl-'): {
        'a1': 1.34211308E-02,
        'a2': 0,
        'a3': -5.10212917e00,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
        'a8': 0,
    },
    ('psi', 'Na+', 'Ca+2', 'Cl-'): {
        'a1': -0.003e0,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
        'a8': 0,
    },
    ('zeta', 'Li+', 'Cl-', 'LiCl0'): {
        'a1': 0,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
        'a8': 0,
    },
    ('zeta', 'K+', 'Cl-', 'LiCl0'): {
        'a1': 1.277846484,
        'a2': 0.769448e-3,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'a6': -0.262633421,
        'a7': 0.068191388,
        'a8': 0,
    },
    ('zeta', 'Na+', 'Cl-', 'LiCl0'): {
        'a1': 0.257865049,
        'a2': -1.495326e-3,
        'a3': 2.22e-6,
        'a4': 0,
        'a5': 0,
        'a6': 0,
        'a7': 0,
        'a8': 0,
    },

}

index = pd.MultiIndex.from_tuples([('pr1', 'pr2', 'pr3', 'pr4')],
                                  names=["parameter", "species1", "species2", "species3"])
df = pd.DataFrame(columns=['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'], index=index)
for key, value in species.items():
    df.loc[key, :] = pd.Series(value)
df.sort_index()

lassin_ternary = df
