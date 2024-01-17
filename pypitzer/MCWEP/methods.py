# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import numpy as np
import pandas as pd
import itertools
from sympy import *

from functools import lru_cache

from database.lassin_binary import lassin_binary
from database.lassin_ternary import lassin_ternary
from database.lassin_chemical_potentials import lassin_chemical_potential_db
from database.solid_data import solids
from public.low_level import find_pair
from public.j_x import compute_j_jp

import functools


# to make dictionary harshable
def hash_dict(func):
    """Transform mutable dictionnary
    Into immutable
    Useful to be compatible with cache
    """

    class HDict(dict):
        def __hash__(self):
            return hash(frozenset(self.items()))

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([HDict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: HDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped


def get_two_ion_db(name):
    database = lassin_binary
    return database


def get_three_ion_db(name):
    database = lassin_ternary
    return database


@hash_dict
@lru_cache(maxsize=None)
def find_parameter_value(pair, dbname, parameter_name, col_name):
    """
    Find values for parameters from database based on ion names.
    :param pair: a tuple of ion pair.
    :param dbname: database name.
    :param parameter_name: the name of the parameter, e.g. 'b0', 'b1' ...
    :param col_name:
    :return:
    """
    database = get_two_ion_db(dbname)

    first_level_df = database.loc[parameter_name]
    ion_pairs = first_level_df.index

    parameter = 0
    for key in ion_pairs:
        if {pair[0], pair[1]} == set(key):
            parameter = first_level_df.loc[key, col_name]

    if isinstance(parameter, pd.Series):
        parameter = parameter.values[0]

    return float(parameter)


def binary_parameters_ready(pair, t):
    """
    Make the A0 - A5 value parameters ready in a dictionary for further selection and calculating
    :param pair: a tuple of ion pair.
    :return: values of parameters.
    """

    dbname = 'lassin'

    database = get_two_ion_db(dbname)

    # get the number of columns
    table_width = len(database.columns)

    parameter_names = ['b0', 'b1', 'b2', 'c_phi', 'theta', 'lambda']
    dic = {}
    for pn in parameter_names:
        for col in database.columns[:table_width]:
            value = find_parameter_value(pair, dbname, pn, col)
            dic[pn + '_' + col] = value
    return dic


def ternary_parameters_ready(pair, t):
    """
    Make parameters ready in a dictionary for further selection and calculating
    :param pair: A tuple a three ions.
    :return: Interaction parameters of this group of ions.
    """

    dbname = 'lassin'

    database = get_three_ion_db(dbname)

    pns = ['psi', 'zeta']
    parameters = {}
    for pn in pns:
        first_level_df = database.loc[pn]
        ion_pairs = first_level_df.index
        col_list = database.columns

        match = find_pair(pair, ion_pairs)
        if match['has']:
            target = match['target']
            for col in col_list:
                parameter = first_level_df.loc[target, col]
                parameters[pn + '_' + col] = parameter
        else:
            for col in col_list:
                parameter = 0
                parameters[pn + '_' + col] = parameter
    return parameters


def chemical_potential_lassin(a1, a2, a3, a4, a5, t):
    log_k = a1 + a2 * t + a3 / t + a4 * np.log10(t) + a5 / (t ** 2)
    return log_k * 2.303


def parameter_cal_lassin(a1, a2, a3, a4, a5, a6, a7, a8, t):
    p = a1 + a2 * t + a3 * t ** 2 + a4 * t ** 3 + a5 / t + a6 * ln(t) + a7 / (t - 263) + a8 / (680 - t)
    return p


def parameter_cal_moller(a1, a2, a3, a4, a5, a6, a7, a8, t):
    p = a1 + a2 * t + a3 / t + a4 * ln(t) + a5 / (t - 263) + a6 * t ** 2 + a7 / (680 - t) + a8 / (t - 227)
    return p


def get_parameter_lassin(name, data, t):
    """
    Choose equation and calculate parameters conveniently.
    :param name: parameter name, can be 'b0', 'b1', 'c', 'theta', 'psi'.
    :param data: a dict contains all the interaction data an ion-pair.
    :param t: temperature of the solution.
    :param method: method used to calculate parameter, default is 'spencer'.
    :return: value of the parameter.
    """
    # print(data)
    a1 = data['{}_a1'.format(name)]
    a2 = data['{}_a2'.format(name)]
    a3 = data['{}_a3'.format(name)]
    a4 = data['{}_a4'.format(name)]
    a5 = data['{}_a5'.format(name)]
    a6 = data['{}_a6'.format(name)]
    a7 = data['{}_a7'.format(name)]
    a8 = data['{}_a8'.format(name)]

    parameter = parameter_cal_lassin(a1, a2, a3, a4, a5, a6, a7, a8, t)

    return parameter


def get_parameter_moller(name, data, t):
    """
    Choose equation and calculate parameters conveniently.
    :param name: parameter name, can be 'b0', 'b1', 'c', 'theta', 'psi'.
    :param data: a dict contains all the interaction data an ion-pair.
    :param t: temperature of the solution.
    :param method: method used to calculate parameter, default is 'spencer'.
    :return: value of the parameter.
    """
    # print(data)
    a1 = data['{}_a1'.format(name)]
    a2 = data['{}_a2'.format(name)]
    a3 = data['{}_a3'.format(name)]
    a4 = data['{}_a4'.format(name)]
    a5 = data['{}_a5'.format(name)]
    a6 = data['{}_a6'.format(name)]
    a7 = data['{}_a7'.format(name)]
    a8 = data['{}_a8'.format(name)]

    parameter = parameter_cal_moller(a1, a2, a3, a4, a5, a6, a7, a8, t)

    return parameter


def get_parameter(pair, name, data, t):
    if 'Li+' in pair or 'LiCl0' in pair:
        return get_parameter_lassin(name, data, t)
    else:
        return get_parameter_moller(name, data, t)


def get_charge_number(ion):
    """
    get the charge number of an ion (str)
    :param ion: ion name, a string with "+" or "-" sign followed by number of charge
    :return: charge number
    """
    if "+" in ion:
        lis = ion.split("+")
        if lis[1]:
            result = lis[1]
        else:
            result = 1
    elif "-" in ion:
        lis = ion.split("-")
        if lis[1]:
            lis[1] = '-' + lis[1]
            result = lis[1]
        else:
            result = -1
    else:
        result = 0
    return int(result)


def is_neutral(ion):
    charge = get_charge_number(ion)
    if charge == 0:
        return True
    return False


def is_cation(ion):
    charge = get_charge_number(ion)
    if charge > 0:
        return True
    return False


def is_anion(ion):
    charge = get_charge_number(ion)
    if charge < 0:
        return True
    return False


def species_type(species):
    """
    Determine whether a species is a cation, anion or neutral species.
    :param species: [string], e.g. "Na+", "Cl-", "H2O".
    :return: type name
    """
    if species.find("+") != -1:
        s_type = 'cation'
    elif species.find("-") != -1:
        s_type = 'anion'
    else:
        s_type = 'neutral'
    return s_type


def salt_type(pair):
    """
    Determine whether a salt is a 2-2 type or not.
    :param ion1: ion1
    :param ion2: ion2
    :return: return True if it is a 2-2 type of salt
    """
    ion1 = pair[0]
    ion2 = pair[1]
    if ion1.find("+") != -1:
        result1 = ion1.split("+")
    else:
        result1 = ion1.split("-")
    if ion2.find("+") != -1:
        result2 = ion2.split("+")
    else:
        result2 = ion2.split("-")
    if result1[1] == '2' and result2[1] == '2':
        return True
    else:
        return False


"""
the Pitzer parameters
"""


def a_phi_moller(t):
    a1 = 3.36901532e-01
    a2 = -6.32100430e-04
    a3 = 9.14252359e00
    a4 = -1.35143986e-02
    a5 = 2.26089488e-03
    a6 = 1.92118597e-06
    a7 = 4.52586464e01
    a8 = 0
    return a1 + a2 * t + a3 / t + a4 * ln(t) + a5 / (t - 263) + a6 * t ** 2 + a7 / (680 - t) + a8 / (t - 227)


def g_func(a):
    result = 2 * (
            1 - (1 + a) * exp(-a)
    ) / a ** 2
    return result


def g_func_prime(a):
    g_prime = -2 * (
            1 - (1 + a + a ** 2 / 2) * exp(-a)
    ) / a ** 2
    return g_prime


def get_beta(parameters, pair, i):
    charge_number1 = get_charge_number(pair[0])
    charge_number2 = get_charge_number(pair[1])

    alpha = 2  # kg^(1/2)⋅mol^(-1/2)
    alpha_1 = 1.4  # kg^(1/2)⋅mol^(-1/2)
    alpha_2 = 12  # kg^(1/2)⋅mol^(-1/2)
    b0 = parameters['b0']
    b1 = parameters['b1']
    b2 = parameters['b2']

    if abs(charge_number1) == 2 and abs(charge_number2) == 2:
        beta_mx = b0 + b1 * g_func(
            alpha_1 * (i ** (1 / 2))
        ) + b2 * g_func(
            alpha_2 * (i ** (1 / 2))
        )
    else:
        beta_mx = b0 + b1 * g_func(
            alpha * i ** (1 / 2)
        )
    return beta_mx


def get_beta_prime(parameters, pair, i):
    charge_number1 = get_charge_number(pair[0])
    charge_number2 = get_charge_number(pair[1])

    alpha = 2  # kg^(1/2)⋅mol^(-1/2)
    alpha_1 = 1.4  # kg^(1/2)⋅mol^(-1/2)
    alpha_2 = 12  # kg^(1/2)⋅mol^(-1/2)
    b0 = parameters['b0']
    b1 = parameters['b1']
    b2 = parameters['b2']

    if abs(charge_number1) == 2 and abs(charge_number2) == 2:
        beta_prime = (
                             b1 * g_func_prime(
                         alpha_1 * (i ** (1 / 2))
                     ) + b2 * g_func_prime(
                         alpha_2 * (i ** (1 / 2))
                     )
                     ) / i
    else:
        beta_prime = b1 * g_func_prime(alpha * i ** (1 / 2)) / i
    return beta_prime


def get_beta_phi(parameters, pair, i):
    charge_number1 = get_charge_number(pair[0])
    charge_number2 = get_charge_number(pair[1])

    alpha = 2  # kg^(1/2)⋅mol^(-1/2)
    alpha_1 = 1.4  # kg^(1/2)⋅mol^(-1/2)
    alpha_2 = 12  # kg^(1/2)⋅mol^(-1/2)

    b0 = parameters['b0']
    b1 = parameters['b1']
    b2 = parameters['b0']

    """for 2-2 type salts"""
    if abs(charge_number1) == 2 and abs(charge_number2) == 2:
        beta_phi = b0 + b1 * exp(-alpha_1 * (i ** (1 / 2))) + b2 * exp(-alpha_2 * (i ** (1 / 2)))
    else:
        """for 1-1, 1-2, 2-1, 3-1, 4-1 type salts"""
        beta_phi = b0 + b1 * exp(-alpha * (i ** (1 / 2)))
    return beta_phi


def get_c(c_phi, z_m, z_x):
    c_mx = c_phi / (2 * (abs(z_m * z_x)) ** 0.5)
    return c_mx


def get_c_gamma(c_phi):
    c_gamma = 3 * c_phi / 2
    return c_gamma


def get_f(a_phi, i):
    """
    :param a_phi: A_phi (Debye-Hukel constant)
    :param i: ionic strength
    :return: expression of "f" function
    """
    b = 1.2
    f = - (4 * i * a_phi / b) * ln(1 + b * i ** (1 / 2))
    return f


def get_f_gamma(a_phi, i):
    """
    :param a_phi:A_phi (Debye-Hukel constant)
    :param i: ionic strength
    :return: the "f^gamma" function in Pitzer's model
    """
    b = 1.2
    f_gamma = - a_phi * (
            i ** (1 / 2) / (1 + b * i ** (1 / 2)) + (2 / b) * ln(
        1 + b * i ** (1 / 2))
    )
    return f_gamma


"""
*** End of the Pitzer parameters dealing *** 
"""


def get_x_mn(z_m: int, z_n: int, a_phi: float, i: float):
    """
    calculate the 'x' value of ions 'm' and 'n'.
    :param z_m: charge number of ion 'm'
    :param z_n: charge number of ion 'n'
    :param a_phi: Avogedral's number of this solution
    :param i: Ionic strength of this solution
    :return: 'x_mn' for calculating the 'J' value
    :reference: [2] p9
    """
    x_mn = 6 * z_m * z_n * a_phi * i ** 0.5
    return x_mn


def get_e_theta(z_m, z_n, a_phi, i):
    """
    :param z_m: charge number of species m
    :param z_n: charge number of species n
    :param a_phi:
    :param i: ionic strength
    :return: e_theta and e_theta_prime
    :reference: [1] p123
    """

    x_mn = get_x_mn(z_m, z_n, a_phi, i)
    x_mm = get_x_mn(z_m, z_m, a_phi, i)
    x_nn = get_x_mn(z_n, z_n, a_phi, i)

    mn = compute_j_jp(x_mn)
    mm = compute_j_jp(x_mm)
    nn = compute_j_jp(x_nn)
    j_mn = mn['j_x']
    j_mn_prime = mn['j_x_prime']
    j_mm = mm['j_x']
    j_mm_prime = mm['j_x_prime']
    j_nn = nn['j_x']
    j_nn_prime = nn['j_x_prime']

    e_theta = (z_m * z_n / (4 * i)) * (j_mn - 0.5 * j_mm - 0.5 * j_nn)
    e_theta_prime = -(e_theta / i) + (z_m * z_n / (8 * i ** 2)) * (
            x_mn * j_mn_prime - 0.5 * x_mm * j_mm_prime - 0.5 * x_nn * j_nn_prime)
    return {
        "e_theta": e_theta,
        "e_theta_prime": e_theta_prime,
    }


@hash_dict
@lru_cache(maxsize=None)
def calculate_ionic_strength(molalities):
    data = molalities
    ions = data.keys()
    sum_value = 0
    for ion in ions:
        charge_number = get_charge_number(ion)
        sum_value += data[ion] * (charge_number ** 2)
    return sum_value / 2


@hash_dict
@lru_cache(maxsize=None)
def calculate_molality(x, species):
    x1 = x[0]
    molalities = {}
    for key, value in species.items():
        molalities[key] = value * x1

    if 'Cl-' not in species.keys():
        sum = 0
        for key, value in molalities.items():
            sum += get_charge_number(key) * value
        molalities['Cl-'] = sum
    return molalities


@hash_dict
@lru_cache(maxsize=None)
def calculate_charge_balance(x, molalities):
    balance = 0
    for species in molalities.keys():
        balance += get_charge_number(species) * molalities[species]
    return balance


@lru_cache(maxsize=None)
def get_chemical_potential(species, t):
    """
    Calculate the standard chemical potential of solids melting reaction.
    the "chemical potential" here actually means "μ/RT".
    :param solid: [string], solid species, e.g. "NaCl"
    :param t: [number], melting temperature of the solid, in Kelvin.
    :return: [number], standard chemical potential of the melting reaction.
    """
    if 'Li' in species:
        data = lassin_chemical_potential_db.loc[species]
        std_chemical_potential = chemical_potential_lassin(
            data['a1'],
            data['a2'],
            data['a3'],
            data['a4'],
            data['a5'],
            t=t
        )
    else:
        data = moller_chemical_potential.loc[species]
        std_chemical_potential = parameter_cal_moller(
            a1=data['a1'],
            a2=data['a2'],
            a3=data['a3'],
            a4=data['a4'],
            a5=data['a5'],
            a6=data['a6'],
            a7=data['a7'],
            a8=data['a8'],
            t=t
        )
    return std_chemical_potential


def get_hydrate_data(solid):
    data = {}
    if solid in solids.keys():
        data = solids[solid]
    return data


@hash_dict
@lru_cache(maxsize=None)
def group_components(components):
    """
    Find groups from components of ions and neutral species
    :param components: consists of cations, anions and neutral species.
    :return: groups
    """
    cations = [c for c in components if '+' in c]
    anions = [a for a in components if '-' in a]
    neutrals = [n for n in components if '+' not in n and '-' not in n]

    cation_anion_pairs = list(itertools.product(cations, anions))
    cation_pairs = list(itertools.combinations(cations, 2)) if len(cations) >= 2 else []
    anion_pairs = list(itertools.combinations(anions, 2)) if len(anions) >= 2 else []
    neutral_pairs = list(itertools.combinations(neutrals, 2))

    neutral_ion_pairs = list(itertools.product(neutrals, cations + anions))

    neutral_cation_anion_pairs = [(a, *b) for a in neutrals for b in cation_anion_pairs]

    return {
        'cations': cations,
        'anions': anions,
        'neutrals': neutrals,
        'cation_anion_pairs': cation_anion_pairs,
        'cation_pairs': cation_pairs,
        'anion_pairs': anion_pairs,
        'neutral_pairs': neutral_pairs,
        'neutral_ion_pairs': neutral_ion_pairs,
        'neutral_cation_anion_pairs': neutral_cation_anion_pairs
    }


"""
Pitzer-model-only methods
"""


@hash_dict
@lru_cache(maxsize=None)
def get_beta_012(rd, t, method):
    b0 = 0
    b1 = 0
    b2 = 0
    if method == 'lassin':
        b0 = get_parameter_lassin(name='b0', data=rd, t=t)
        b1 = get_parameter_lassin(name='b1', data=rd, t=t)
        b2 = get_parameter_lassin(name='b2', data=rd, t=t)
    elif method == 'moller':
        b0 = get_parameter_moller(name='b0', data=rd, t=t)
        b1 = get_parameter_moller(name='b1', data=rd, t=t)
        b2 = get_parameter_moller(name='b2', data=rd, t=t)
    return {
        'b0': b0,
        'b1': b1,
        'b2': b2,
    }


@hash_dict
@lru_cache(maxsize=None)
def beta_calculate(ion_pair, ionic_strength, t):
    rd = binary_parameters_ready(ion_pair, t)
    if 'Li+' in ion_pair or 'LiCl0' in ion_pair:
        method = 'lassin'
    else:
        method = 'moller'

    beta_012 = get_beta_012(rd, t, method=method)

    beta = get_beta(beta_012, ion_pair, ionic_strength)
    return beta


@hash_dict
@lru_cache(maxsize=None)
def beta_phi_calculate(ion_pair, ionic_strength, t):
    rd = binary_parameters_ready(ion_pair, t)
    if 'Li+' in ion_pair or 'LiCl0' in ion_pair:
        method = 'lassin'
    else:
        method = 'moller'
    beta_012 = get_beta_012(rd, t, method=method)

    b_phi = get_beta_phi(beta_012, ion_pair, ionic_strength)

    return b_phi


@hash_dict
@lru_cache(maxsize=None)
def beta_prime_calculate(ion_pair, ionic_strength, t):
    rd = binary_parameters_ready(ion_pair, t)
    if 'Li+' in ion_pair or 'LiCl0' in ion_pair:
        method = 'lassin'
    else:
        method = 'moller'

    beta_012 = get_beta_012(rd, t, method=method)

    b_prime = get_beta_prime(beta_012, ion_pair, ionic_strength)
    return b_prime


@hash_dict
@lru_cache(maxsize=None)
def c_calculate(ion_pair, t, method):
    rd = binary_parameters_ready(ion_pair, t)
    c0 = 0
    if method == 'lassin':
        c0 = get_parameter_lassin(name='c_phi', data=rd, t=t)
    elif method == 'moller':
        c0 = get_parameter_moller(name='c_phi', data=rd, t=t)
    charge_number1 = get_charge_number(ion_pair[0])
    charge_number2 = get_charge_number(ion_pair[1])
    c = get_c(c0, charge_number1, charge_number2)
    return c


@hash_dict
@lru_cache(maxsize=None)
def cc_phi_calculate(ion_pair, a_phi, ionic_strength, t):
    charge_number1 = get_charge_number(ion_pair[0])
    charge_number2 = get_charge_number(ion_pair[1])
    rd = binary_parameters_ready(ion_pair, t)

    if 'Li+' in ion_pair or 'LiCl0' in ion_pair:
        theta = get_parameter_lassin(name='theta', data=rd, t=t)
    else:
        theta = get_parameter_moller(name='theta', data=rd, t=t)
    if charge_number1 != charge_number2:
        e_thetas = get_e_theta(charge_number1, charge_number2, a_phi, ionic_strength)
        e_theta = e_thetas['e_theta']
        e_theta_prime = e_thetas['e_theta_prime']
    else:
        e_theta = 0
        e_theta_prime = 0
    phi = theta + e_theta
    phi_prime = e_theta_prime

    return {
        'phi': phi,
        'phi_prime': phi_prime
    }


@hash_dict
@lru_cache(maxsize=None)
def aa_phi_calculate(ion_pair, a_phi, ionic_strength, t):
    charge_number1 = get_charge_number(ion_pair[0])
    charge_number2 = get_charge_number(ion_pair[1])

    rd = binary_parameters_ready(ion_pair, t)

    if 'Li+' in ion_pair or 'LiCl0' in ion_pair:

        theta = get_parameter_lassin(name='theta', data=rd, t=t)
    else:
        theta = get_parameter_moller(name='theta', data=rd, t=t)
    if charge_number1 != charge_number2:
        e_thetas = get_e_theta(charge_number1, charge_number2, a_phi, ionic_strength)
        e_theta = e_thetas['e_theta']
        e_theta_prime = e_thetas['e_theta_prime']
    else:
        e_theta = 0
        e_theta_prime = 0
    phi = theta + e_theta
    phi_prime = e_theta_prime
    return {
        "phi": phi,
        "phi_prime": phi_prime
    }


"""
Reference
[1] Pitzer K S. Activity coefficients in electrolyte solutions[M]. CRC press, 2018.
[2] Pitzer K S. Thermodynamics of electrolytes. V. Effects of higher-order electrostatic terms[J]. Journal of Solution 
Chemistry, 1975, 4(3): 249-265.
[3] Bradley, Daniel J., and Kenneth S. Pitzer. "Thermodynamics of electrolytes. 12. Dielectric properties of water and 
Debye-Hueckel parameters to 350. degree. C and 1 kbar." Journal of physical chemistry 83.12 (1979): 1599-1603.
[4] Marion GM, Catling DC, Kargel JS. Modeling aqueous ferrous iron chemistry at low temperatures with application to 
Mars. Geochimica et cosmochimica Acta. 2003 Nov 15;67(22):4251-66.
"""
