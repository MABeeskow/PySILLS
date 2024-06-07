# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description:
# Version: 1.0
# Last Modified: May 7, 2023

import numpy as np


def compute_b_d(x):
    """
    Generate bs and ds.
    :param x: a float.
    :return: two arrays b and d.
    """
    a_i = np.array(
        [1.925154015, -0.060076478, -0.029779077, -0.0072995, 0.000388261, 0.000636875, 3.65836E-05, -4.5037E-05,
         -4.5379E-06, 2.93771E-06, 3.96566E-07, -2.021E-07, -2.52678E-08, 1.35226E-08, 1.22941E-09, -8.21969E-10,
         -5.0847E-11, 4.6333E-11, 1.943E-12, -2.563E-12, -1.0991E-11])
    a_ii = np.array(
        [0.628023321, 0.462762985, 0.150044637, -0.028796058, -0.036552746, -0.001668088, 0.00651984, 0.001130378,
         -0.000887171, -0.000242108, 8.72945E-05, 3.46821E-05, -4.58377E-06, -3.54868E-06, -2.50454E-07, 2.16992E-07,
         8.07796E-08, 4.55856E-09, -6.94476E-09, -2.84926E-09, 2.37816E-10])
    # Region I
    if x <= 1:
        z = 4 * x ** (1 / 5) - 2
        dz_dx = 4 / 5 * x ** (-4 / 5)
        a_k = a_i
    # Region II
    else:
        z = 40 / 9 * x ** (-1 / 10) - 22 / 9
        dz_dx = -40 / 90 * x ** (-11 / 10)
        a_k = a_ii

    # Initialize b and d arrays
    b = np.zeros(23)
    d = np.zeros(23)

    # Compute b and d arrays
    for k in range(20, -1, -1):
        b[k] = z * b[k + 1] - b[k + 2] + a_k[k]
        d[k] = b[k + 1] + z * d[k + 1] - d[k + 2]

    return b[:-2], d[:-2]


def compute_j_jp(x: float) -> dict:
    """
    Computes the values of j_x and j_xp given x.

    Args:
        x (float): The value of x.

    Returns:
        dict: A dictionary containing the values of j_x, j_xp.
    """
    b, d = compute_b_d(x)

    b0 = b[0]
    b2 = b[2]
    d0 = d[0]
    d2 = d[2]

    dz_dx = 0
    if x <= 1:
        dz_dx = (4 / 5) * x ** (-4 / 5)
    elif x >= 1:
        dz_dx = (-40 / 90) * x ** (-11 / 10)

    j_x = (1 / 4) * x - 1 + (1 / 2) * (b0 - b2)
    j_xp = (1 / 4) + (1 / 2) * dz_dx * (d0 - d2)

    return {'j_x': j_x, 'j_xp': j_xp}
