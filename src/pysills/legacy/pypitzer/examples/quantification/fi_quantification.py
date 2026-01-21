# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Pitzer.models import FluidPitzer
import pandas as pd


# columns = [
#     'T',
#     'Na+',
#     'Ca+2',
#     # 'K+',
#     # 'Li+',
#     # 'Mg+2',
#     # 'Sr+2',
#     # 'Cs+',
#     # 'Rb+',
#     'Mn+2',
#     'Zn+2',
#     'Pb+2'
# ]
# df = pd.DataFrame(columns=columns)
#
# def replace_blanks_with_commas(input_string):
#     # replace blank spaces with commas in each row and convert to tuple of floats (or strings)
#     rows = input_string.strip().split('\n')
#     replaced_rows = []
#     for row in rows:
#         row_as_list = []
#         for num in row.split():
#             try:
#                 row_as_list.append(float(num))
#             except ValueError:
#                 row_as_list.append(num)
#         row_as_tuple = tuple(row_as_list)
#         replaced_rows.append(row_as_tuple)
#
#     # output as list of tuples
#     output = replaced_rows
#
#     return output
#
#
# data = """
# -21.90364364	1	0.261712115	0.002102761	0.002044225	0.000300444
# """
# data = replace_blanks_with_commas(data)
#
#
#
# for dt in data:
#     print(dt)
#     species = {
#         'Na+':  dt[1],
#         'Ca+2': dt[2],
#         # 'K+':   dt[3],
#         # 'Li+':  dt[4],
#         # 'Mg+2': dt[5],
#         # 'Sr+2': dt[6],
#         # 'Cs+':  dt[7],
#         # 'Rb+':  dt[8],
#         'Mn+2': dt[3],
#         'Zn+2': dt[4],
#         'Pb+2': dt[5]
#     }
#     fluid = FluidPitzer(
#         x0=(3, 5),
#         species=species,
#         t=dt[0],
#         solids=['H2O(S)']
#     )
#     print(fluid.solids)
#     result = fluid.optimize()
#     if result.success:
#         for key, value in species.items():
#             species[key] = value * result.x[0]
#
#     values_list = list(species.values())
#
#     # create a new DataFrame with the current row data and concatenate it with the existing DataFrame
#     row_data = [dt[0]] + values_list
#     row_df = pd.DataFrame([row_data], columns=columns)
#     df = pd.concat([df, row_df], ignore_index=True)
#
# print(df)
#
# # write the DataFrame to a CSV file
# df.to_csv(r'E:\work\data\low-T\general_result.csv', index=False)

# aqueous species determined in LA-ICP-MS analysis
species = {
    'Na+': 1,
    'K+':  2,
}
fluid = FluidPitzer(
    x0=(3, 3),
    species=species,
    # melting temperature of the last solid
    t=25,
    # the last melting solid
    solids=['KCl']
)

result = fluid.optimize()

print(result)