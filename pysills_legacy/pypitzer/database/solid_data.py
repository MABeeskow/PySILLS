# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

solids = {
    'H2O(S)': {
        'H2O': {
            'value': 1,
            'type': 'neutral'
        },
    },
    'NaCl': {
        'Na+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 0,
            'type': 'neutral'
        },
    },
    'NaCl-2H2O': {
        'Na+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 2,
            'type': 'neutral'
        },
    },
    'KCl': {
        'K+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 0,
            'type': 'neutral'
        },
    },
    'CaCl2-6H2O': {
        'Ca+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 6,
            'type': 'neutral'
        },
    },
    'MgCl2-6H2O': {
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 6,
            'type': 'neutral'
        },
    },
    'MgCl2-8H2O': {
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 8,
            'type': 'neutral'
        },
    },
    'MgCl2-12H2O': {
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 12,
            'type': 'neutral'
        },
    },
    'Na2SO4-10H2O': {
        'Na+': {
            'value': 2,
            'type': 'cation'
        },
        'SO4-2': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 10,
            'type': 'neutral'
        },
    },
    'Na2SO4': {
        'Na+': {
            'value': 2,
            'type': 'cation'
        },
        'SO4-2': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 0,
            'type': 'neutral'
        },
    },
    'MgSO4-6H2O': {
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'SO4-2': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 6,
            'type': 'neutral'
        },
    },
    'MgSO4-7H2O': {
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'SO4-2': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 7,
            'type': 'neutral'
        },
    },
    'K2SO4': {
        'K+': {
            'value': 2,
            'type': 'cation'
        },
        'SO4-2': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 0,
            'type': 'neutral'
        },
    },
    'K2Mg(SO4)2-6H2O': {
        'K+': {
            'value': 2,
            'type': 'cation'
        },
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'SO4-2': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 6,
            'type': 'neutral'
        },
    },
    'KCl-MgCl2-6H2O': {
        'K+': {
            'value': 1,
            'type': 'cation'
        },
        'Mg+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 3,
            'type': 'anion'
        },
        'H2O': {
            'value': 6,
            'type': 'neutral'
        },
    },
    'CaMg2Cl6-12H2O': {
        'Ca+2': {
            'value': 1,
            'type': 'cation'
        },
        'Mg+2': {
            'value': 2,
            'type': 'cation'
        },
        'Cl-': {
            'value': 6,
            'type': 'anion'
        },
        'H2O': {
            'value': 12,
            'type': 'neutral'
        },
    },
    'LiCl-5H2O': {
        'Li+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 5,
            'type': 'neutral'
        },
    },
    'LiCl-3H2O': {
        'Li+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 3,
            'type': 'neutral'
        },
    },
    'LiCl-2H2O': {
        'Li+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 2,
            'type': 'neutral'
        },
    },
    'LiCl-H2O': {
        'Li+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 1,
            'type': 'neutral'
        },
    },
    'LiCl0': {
        'Li+': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 1,
            'type': 'anion'
        },
        'H2O': {
            'value': 0,
            'type': 'neutral'
        },
    },
    'FeCl2-4H2O': {
        'Fe+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 4,
            'type': 'neutral'
        },
    },
    'FeCl2-6H2O': {
        'Fe+2': {
            'value': 1,
            'type': 'cation'
        },
        'Cl-': {
            'value': 2,
            'type': 'anion'
        },
        'H2O': {
            'value': 6,
            'type': 'neutral'
        },
    },
    '2KCl-FeCl2-2H2O': {
        'Fe+2': {
            'value': 1,
            'type': 'cation'
        },
        'K+': {
            'value': 2,
            'type': 'cation'
        },
        'Cl-': {
            'value': 4,
            'type': 'anion'
        },
        'H2O': {
            'value': 2,
            'type': 'neutral'
        },
    },
}
