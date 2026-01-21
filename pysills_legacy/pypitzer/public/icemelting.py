# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description:
# Version: 1.0
# Last Modified: May 7, 2023

import numpy as np
from sympy import *

def monnin(t):
    a = -21.041
    b = 268.52
    c = 3.575
    ln_k = a + b / t + c * ln(t)
    return ln_k


def spencer(t):
    ln_k = 7.875060393E3 + 1.169118490E1 * t - 0.017183789 * t ** 2 + 1.24395543E-5 * t ** 3 - 9.3314790E4 / t - 1.7287461E3 * ln(
        t)
    return ln_k


def goff_gratch(t):
    log_p_ice = 0.876793 * (1 - t / 273.16) - 9.09718 * (273.16 / t - 1) - 3.56654 * np.log10(273.16 / t) + np.log10(
        6.1173)
    log_p_w = -1.3816 * 10 ** (-7) * (10 ** (11.344 * (1 - t / 373.15)) - 1) - 7.90298 * (
            373.15 / t - 1) + 5.02808 * np.log10(373.15 / t) + 8.1328 * 10 ** (-3) * (
                      10 ** (-3.49149 * (373.15 / t - 1)) - 1) + np.log10(1013.25)
    p_ice = np.exp(log_p_ice * 2.303)
    p_w = np.exp(log_p_w * 2.303)
    ln_k = np.log(p_ice / p_w)
    return ln_k


def clegg_and_brimblecombe(t):
    """
    Calculate water activity.
    :param t: temperature, kelvin
    :return:
    """
    k_ice = 1.906354 - 1.880285 * 10 ** (-2) * t + 6.603001 * 10 ** (-5) * t ** 2 - 3.419967 * 10 ** (-8) * t ** 3
    return ln(k_ice)


def ln_clegg_brimblecombe_constant(t):
    """
    :param t: temperature, kelvin
    :return: ln_k
    """
    ln_k = 9.053594 * 10 - 7.215505 * 10 ** (-1) * t + 2.112659 * 10 ** (-3) * t ** 2 - 2.254724 * 10 ** (-6) * t ** 3
    return ln_k


def koop(t):
    lnk = (210368 + 131.438 * t - 3.32373 * 10 ** 6 * t ** (-1) - 41729.1 * np.log(t)) / (t * 8.31446261815324)
    return lnk


def compare_all(t):
    return {
        'monnin': monnin(t),
        'spencer': spencer(t),
        'goff_gratch': goff_gratch(t),
        'clegg_and_brimblecombe': clegg_and_brimblecombe(t),
        'koop': koop(t)
    }


def get_ln_water_activity(t_ice, method=None):
    if method is None:
        method = 'clegg_and_brimblecombe'
    




"""
References:

"""


