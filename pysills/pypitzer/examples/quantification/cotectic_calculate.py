# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023


import sys
import os
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Pitzer.model2 import FluidPitzer

# shape = (0, 2)
# result_array = np.empty(shape, dtype=np.float64)
# ts =[
# -20
# ]
# for t in ts:
#     fluid = FluidPitzer(
#         x0=(3, 1),
#         species=['Na+', 'Ca+2'],
#         t=t + 273.16,
#         solids=['NaCl-2H2O', 'H2O(S)'],
#     )
#     print(fluid.get_molalities([1,2]))
#     result = fluid.optimize()
#     if result.success:
#         print(result.x)
#         result_array = np.append(result_array, [result.x], axis=0)
# print(result_array)


fluid = FluidPitzer(
        x0=(3, 1),
        species=['Na+', 'Ca+2'],
        t=-22 + 273.16,
        solids=['NaCl-2H2O', 'H2O(S)'],
    )

print(fluid.optimize())