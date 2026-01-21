import numpy as np
import pandas as pd
import itertools
from sympy import *
from scipy import integrate

from database.marion_binary import marion_binary
from database.marion_ternary import marion_ternary
from database.lassin_binary import lassin_binary
from database.spencer_revised_binary import spencer_binary
from database.spencer_revised_ternary import spencer_ternary
from database.spencer_revised_chemical_potential import spencer_chemical_potential_db
from database.marion_chemical_potential import marion_chemical_potential_db
from database.lassin_chemical_potential import lassin_chemical_potential_db
from database.solid_data import solids
from public.low_level import find_pair


def get_two_ion_db(name):
    name = name.lower()
    database = None
    if name == 'spencer':
        database = spencer_binary
    elif name == 'marion':
        database = marion_binary
    elif name == 'lassin':
        database = lassin_binary
    return database


def get_three_ion_db(name):
    name = name.lower()
    database = None
    if name == 'spencer':
        database = spencer_ternary
    elif name == 'marion':
        database = marion_ternary
    return database


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

    # determine which database to use when needed.
    if 'Fe+2' in pair:
        dbname = 'marion'
    else:
        dbname = 'spencer'

    database = get_two_ion_db(dbname)

    # get the number of columns
    table_width = len(database.columns)

    parameter_names = ['b0', 'b1', 'b2', 'c_phi', 'theta']
    dic = {}
    for pn in parameter_names:
        for col in database.columns[:table_width]:
            value = find_parameter_value(pair, dbname, pn, col)
            dic[pn + '_' + col] = value
    return dic


def ternary_parameters_ready_spencer(pair,t):
    """
    Make parameters ready in a dictionary for further selection and calculating
    :param pair: A tuple a three ions.
    :return: Interaction parameters of this group of ions.
    """

    if 'Fe+2' in pair:
        dbname = 'marion'
    else:
        dbname = 'spencer'

    database = get_three_ion_db(dbname)
    pns = ['psi', ]
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


def parameter_cal_holmes(a1, a2, a3, a4, a5, a6, t):
    t_r = 298.15
    parameter = a1 + a2 * (1 / t - 1 / t_r) + a3 * np.log(t / t_r) + a4 * (t - t_r) + a5 * (t ** 2 - t_r ** 2) + a6 * np.log(
        t - 260)
    return parameter


def parameter_cal_spencer(a1, a2, a3, a4, a5, a6, t):
    parameter = a1 + a2 * t + a3 * t ** 2 + a4 * t ** 3 + a5 / t + a6 * np.log(t)
    return parameter


def parameter_cal_moller(a1, a2, a3, a4, a5, a6, a7, a8, t):
    parameter = a1 + a2 * t + a3 / t + a4 * np.log(t) + a5 / (t - 263) + a6 * t ** 2 + a7 / (680 - t) + a8 / (t - 227)
    return parameter


def parameter_cal_appelo(a1, a2, a3, a4, a5, a6, t):
    tr = 298.15
    parameter = a1 + a2 * (1 / t - 1 / tr) + a3 * np.log(t / tr) + a4 * (t - tr) + a5 * (t ** 2 - tr ** 2) + a6 * (
            1 / (t ** 2) - 1 / (tr ** 2))
    return parameter


def parameter_cal_marion(a1, a2, a3, a4, a5, a6, a7, t):
    # reference: [4]
    parameter = a1 + a2 * t + a3 * t ** 2 + a4 * t ** 3 + a5 / t + a6 * np.log(t) + a7 / (t ** 2)
    return parameter


def parameter_cal_marion_kargel(a1, a2, a3, a4, a5, a6, a7, a8, t):
    return a1 + a2 * t + a3 * t ** 2 + a4 * t ** 3 + a5 / t + a6 * np.log(t) +a7/(t**2) + a8 * t ** 4

print(
    parameter_cal_marion_kargel(
    a1=-1.4816780e2,
    a2=8.933802e-1,
    a3=-2.332199e-3,
    a4=2.146860e-6,
    a5=0,
    a6=0,
    a7=0,
    a8=0,
    t=298.16,
))
def chemical_potential_lassin(a1, a2, a3, a4, a5, t):
    ln_k = a1 + a2 * t + a3 / t + a4 * np.log(t) + a5 / (t ** 2)
    return ln_k


def parameter_cal_lassin(a1, a2, a3, a4, a5, a6, a7, a8, t):
    p = a1 + a2 * t + a3 * t ** 2 + a4 * t ** 3 + a5 / t + a6 * np.log(t) + a7 / (t - 263) + a8 / (680 - t)
    return p


def get_parameter(name, data, t, method='spencer'):
    """
    Choose equation and calculate parameters conveniently.
    :param name: parameter name, can be 'b0', 'b1', 'c', 'theta', 'psi'.
    :param data: a dict contains all the interaction data an ion-pair.
    :param t: temperature of the solution.
    :param method: method used to calculate parameter, default is 'spencer'.
    :return: value of the parameter.
    """
    a1 = data['{}_a1'.format(name)]
    a2 = data['{}_a2'.format(name)]
    a3 = data['{}_a3'.format(name)]
    a4 = data['{}_a4'.format(name)]
    a5 = data['{}_a5'.format(name)]
    a6 = data['{}_a6'.format(name)]

    parameter = 0
    if method == 'spencer':
        parameter = parameter_cal_spencer(a1, a2, a3, a4, a5, a6, t)
    elif method == 'holmes':
        parameter = parameter_cal_holmes(a1, a2, a3, a4, a5, a6, t)
    elif method == 'marion':
        a7 = data['{}_a7'.format(name)]
        parameter = parameter_cal_marion(a1, a2, a3, a4, a5, a6, a7, t)
    return parameter


def get_charge_number(ion):
    """
    get the charge number of an ion (str)
    :param ion: ion name, a string with "+" or "-" sign followed by number of charge, or a neutral species name
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
        # assume neutral species like NaCl, CaCO3, etc. have a charge of 0
        result = 0
    return int(result)


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
    a_phi = parameter_cal_moller(a1, a2, a3, a4, a5, a6, a7, a8, t)
    return a_phi


def a_phi_spencer(t):
    """
    Calculate the A_phi (Debye-Hukel constant) according to the temperature
    :param t: temperature of solution, Calvin(K)
    :return: value of a_phi
    :reference:
    """
    a1 = 8.66836498e1
    a2 = 8.48795942e-2
    a3 = -8.88785150e-5
    a4 = 4.88096393e-8
    a5 = -1.32731477e3
    a6 = -1.76460172e1
    a_phi = parameter_cal_spencer(a1, a2, a3, a4, a5, a6, t)
    return a_phi


def g_func(a):
    result = 2 * (
            1 - (1 + a) * np.exp(-a)
    ) / a ** 2
    return result


def g_func_prime(a):
    g_prime = -2 * (
            1 - (1 + a + a ** 2 / 2) * np.exp(-a)
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

    # if 'Fe+2' in pair or 'Fe+3' in pair:
    #     alpha_1 = 2
    #     alpha_2 = 1
    #     beta_mx = b0 + b1 * g_func(
    #         alpha_1 * (i ** (1 / 2))
    #     ) + b2 * g_func(
    #         alpha_2 * (i ** (1 / 2))
    #     )
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

    # if 'Fe+2' in pair or 'Fe+3' in pair:
    #     alpha_1 = 2
    #     alpha_2 = 1
    #     beta_prime = (
    #                          b1 * g_func_prime(
    #                      alpha_1 * (i ** (1 / 2))
    #                  ) + b2 * g_func_prime(
    #                      alpha_2 * (i ** (1 / 2))
    #                  )
    #                  ) / i
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
    # if 'Fe+2' in pair or 'is' in pair:
    #     alpha_1 = 2
    #     alpha_2 = 1
    #     beta_phi = b0 + b1 * exp(-alpha_1 * (i ** (1 / 2))) + b2 * exp(-alpha_2 * (i ** (1 / 2)))
    if abs(charge_number1) == 2 and abs(charge_number2) == 2:
        beta_phi = b0 + b1 * np.exp(-alpha_1 * (i ** (1 / 2))) + b2 * np.exp(-alpha_2 * (i ** (1 / 2)))
    else:
        """for 1-1, 1-2, 2-1, 3-1, 4-1 type salts"""
        beta_phi = b0 + b1 * np.exp(-alpha * (i ** (1 / 2)))
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
    f = - (4 * i * a_phi / b) * np.log(1 + b * i ** (1 / 2))
    return f


def get_f_gamma(a_phi, i):
    """
    :param a_phi:A_phi (Debye-Hukel constant)
    :param i: ionic strength
    :return: the "f^gamma" function in Pitzer's model
    """
    b = 1.2
    f_gamma = - a_phi * (
            i ** (1 / 2) / (1 + b * i ** (1 / 2)) + (2 / b) * np.log(
        1 + b * i ** (1 / 2))
    )
    return f_gamma


"""
*** End of the Pitzer parameters dealing *** 
"""


def a_phi_calculating(t=298.15):
    """
    Calculate the A_phi (Debye-Hukel constant) according to the temperature
    :param t: temperature of solution, degree celcius
    :return: value of a_phi
    :reference: [1] p297
    """
    if t <= 273:
        a_phi = 0.13422 * (0.0368329 * t - 14.62718 * np.log(t) - 1530.1474 / t + 80.40631)
        return a_phi
    elif 273 < t <= 373:
        a_phi = 0.13422 * (4.1725332 - 0.1481291 * t ** (1 / 2) + 1.5188505 * 10 ** (-5) * t ** 2 - 1.8016317 * 10 ** (
            -8) * t ** 3 + 9.3816144 * 10 ** (-10) * t ** 3.5)
        return a_phi


def sym_phi_calculation(theta0, theta1, i):
    alpha = 2
    phi_mn = theta0 + (2 * theta1 / (alpha * i)) * (1 - (1 + alpha * i ** 0.5) * np.exp(-alpha * i ** 0.5))
    return phi_mn


def dialectric_constant(t, p):
    """
    calculate the dialectric constant of a solution.
    :param t: temperature of solution
    :param p: pressure of the solution
    :return: dialectric constant (epsilon)
    :reference: [1] P130
    """

    u1 = 3.4279e2
    u2 = -5.0866e-3
    u3 = 9.4690e-7
    u4 = -2.0525
    u5 = 3.1159e3
    u6 = -1.8289e2
    u7 = -8.0325e3
    u8 = 4.2142e6
    u9 = 2.1417

    epsilon1000 = u1 * np.exp(u2 * t + u3 * t ** 2)
    c = u4 + u5 / (u6 + t)
    b = u7 + u8 / t + u9 * t
    epsilon = epsilon1000 + c * np.log((b + p) / (b + 1000))
    return epsilon


def get_x_mn(z_m, z_n, a_phi, i):
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

import time
def get_j(a):
    """
    Calculate the value of J(x) and J'(X) with 'x' already known.
    :param a: result calculated from function 'get_x_mn()'
    :return: values of J(x) and J'(x)
    """
    start_time = time.time()  # Start the timer

    # j_x
    func1 = lambda b: (1 / a) * ((1 - np.exp(-(a / b) * np.exp(-b))) * b ** 2)
    func_int1 = integrate.quad(func1, 0, np.inf)[0]
    j_x = (1 / 4) * a - 1 + func_int1

    # j_x_prime
    func2 = lambda b: (1 / a) * np.exp(-a / b * np.exp(-b) - b) * b
    func_int2 = integrate.quad(func2, 0, np.inf)[0]
    j_x_prime = (1 / 4) - (func_int1 / a) + func_int2

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    return {
        'j_x': j_x,
        'j_x_prime': j_x_prime,
        'elapsed_time': elapsed_time
    }


def get_j_symbol(x):
    """
    To avoid ambiguity, here we use "a" and "b" to replace the variable "x" and "y" in the original equations.
    :param x: the x value.
    :return: expressions of function J(x) and J'(x) as a dict.
    """

    b = symbols('b')
    a = x
    # j_x
    func1 = (1 / a) * ((1 - np.exp(-(a / b) * np.exp(-b))) * b ** 2)
    func_int1 = Integral(func1, (b, 0, oo))
    j_x = (1 / 4) * a - 1 + func_int1
    # j_x = j_x.subs(a, a)

    # j_x_prime
    func2 = (1 / a) * np.exp(-a / b * np.exp(-b) - b) * b
    func_int2 = Integral(func2, (b, 0, oo))
    j_x_prime = (1 / 4) - (func_int1 / a) + func_int2

    return {
        'j_x': j_x,
        'j_x_prime': j_x_prime
    }


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
    mn = get_j_symbol(x_mn)
    mm = get_j_symbol(x_mm)
    nn = get_j_symbol(x_nn)
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


def get_chemical_potential(solid, temperature):
    """
    Calculate the standard chemical potential of solids melting reaction.
    the "chemical potential" here actually means "μ/RT".
    :param solid: [string], solid species, e.g. "NaCl"
    :param temperature: [number], melting temperature of the solid, in Kelvin.
    :return: [number], standard chemical potential of the melting reaction.
    """
    std_chemical_potential = 0
    if 'Fe' in solid:
        data = marion_chemical_potential_db.loc[solid]
        std_chemical_potential = parameter_cal_marion(
            data['a1'],
            data['a2'],
            data['a3'],
            data['a4'],
            data['a5'],
            data['a6'],
            data['a7'],
            temperature
        )
    elif solid == 'LiCl0':
        data = lassin_chemical_potential_db.loc[solid]
        std_chemical_potential = chemical_potential_lassin(
            data['a1'],
            data['a2'],
            data['a3'],
            data['a4'],
            data['a5'],
            temperature
        )
    else:
        if solid in spencer_chemical_potential_db.index:
            data = spencer_chemical_potential_db.loc[solid]
            std_chemical_potential = parameter_cal_spencer(
                data['a1'],
                data['a2'],
                data['a3'],
                data['a4'],
                data['a5'],
                data['a6'],
                temperature
            )
    return std_chemical_potential
# print(get_chemical_potential('H2O(S)',273.16))

def get_hydrate_data(solid):
    data = {}
    if solid in solids.keys():
        data = solids[solid]
    return data


def group_components(components):
    """
    Find groups from components of ions and neutral species
    :param components: consists of cations, anions and neutral species.
    :return: groups
    """
    cations = []
    anions = []
    neutrals = []
    cation_pairs = []
    anion_pairs = []
    neutral_pairs = []
    for i in components:
        if '+' in i:
            cations.append(i)
        elif '-' in i:
            anions.append(i)
        else:
            neutrals.append(i)

    ions = cations + anions

    cation_anion_pairs = [(a, b) for a in cations for b in anions]
    if len(cations) >= 2:
        cation_pairs = list(itertools.combinations(cations, 2))
    if len(anions) >= 2:
        anion_pairs = list(itertools.combinations(anions, 2))
    neutral_ion_pairs = [(a, b) for a in neutrals for b in ions]
    return {
        'cations': cations,
        'anions': anions,
        'neutrals': neutrals,
        'cation_anion_pairs': cation_anion_pairs,
        'cation_pairs': cation_pairs,
        'anion_pairs': anion_pairs,
        'neutral_pairs': neutral_pairs,
        'neutral_ion_pairs':neutral_ion_pairs
    }


"""
Pitzer-model-only methods
"""


def get_ionic_strength(data):
    """
    For calculating ionic strength, can be molality based or mole fraction based.
    :param data: a dictionary, contains species and their molalities or mole fractions,e.g. {'Na+':0.1, ...}.
    :return: ionic strength.
    """
    ions = data.keys()
    sum_value = 0
    for ion in ions:
        charge_number = get_charge_number(ion)
        sum_value += data[ion] * (charge_number ** 2)
    return sum_value / 2


def get_beta_012(rd, t, method):
    b0 = get_parameter(name='b0', data=rd, t=t, method=method)
    b1 = get_parameter(name='b1', data=rd, t=t, method=method)
    b2 = get_parameter(name='b2', data=rd, t=t, method=method)
    return {
        'b0': b0,
        'b1': b1,
        'b2': b2,
    }


def beta_calculate(ion_pair, ionic_strength, t):
    rd = binary_parameters_ready(ion_pair,t)

    # if contains 'Fe+2' data will be read from different database.
    if 'Fe+2' in ion_pair:
        beta_012 = get_beta_012(rd, t, 'marion')
    elif 'Li+' in ion_pair or 'Cs+' in ion_pair:
        beta_012 = get_beta_012(rd, t, 'holmes')
    else:
        beta_012 = get_beta_012(rd, t, 'spencer')

    beta = get_beta(beta_012, ion_pair, ionic_strength)
    return beta


def beta_phi_calculate(ion_pair, ionic_strength, t):
    rd = binary_parameters_ready(ion_pair,t)
    if 'Fe+2' in ion_pair:
        beta_012 = get_beta_012(rd, t, 'marion')
    elif 'Li+' in ion_pair or 'Cs+' in ion_pair:
        beta_012 = get_beta_012(rd, t, 'holmes')
    else:
        beta_012 = get_beta_012(rd, t, 'spencer')

    b_phi = get_beta_phi(beta_012, ion_pair, ionic_strength)

    return b_phi


def beta_prime_calculate(ion_pair, ionic_strength, t):
    rd = binary_parameters_ready(ion_pair, t)

    if 'Fe+2' in ion_pair:
        beta_012 = get_beta_012(rd, t, 'marion')
    elif 'Li+' in ion_pair or 'Cs+' in ion_pair:
        beta_012 = get_beta_012(rd, t, 'holmes')
    else:
        beta_012 = get_beta_012(rd, t, 'spencer')
    b_prime = get_beta_prime(beta_012, ion_pair, ionic_strength)
    return b_prime


def c_calculate(ion_pair, t):
    rd = binary_parameters_ready(ion_pair, t)
    if 'Fe+2' in ion_pair:
        c0 = get_parameter(name='c_phi', data=rd, t=t, method='marion')
    elif 'Li+' in ion_pair or 'Cs+' in ion_pair:
        c0 = get_parameter(name='c_phi', data=rd, t=t, method='holmes')
    else:
        c0 = get_parameter(name='c_phi', data=rd, t=t, method='spencer')
    charge_number1 = get_charge_number(ion_pair[0])
    charge_number2 = get_charge_number(ion_pair[1])
    c = get_c(c0, charge_number1, charge_number2)
    return c

def lambda_calculate(pair,t):
    pass


def cc_phi_calculate(ion_pair, a_phi, ionic_strength, t):
    charge_number1 = get_charge_number(ion_pair[0])
    charge_number2 = get_charge_number(ion_pair[1])
    rd = binary_parameters_ready(ion_pair,t)
    theta = get_parameter(name='theta', data=rd, t=t)
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


def aa_phi_calculate(ion_pair, a_phi, ionic_strength, t):
    charge_number1 = get_charge_number(ion_pair[0])
    charge_number2 = get_charge_number(ion_pair[1])

    rd = binary_parameters_ready(ion_pair,t)
    theta = get_parameter(name='theta', data=rd, t=t)

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


def water_dielectric_constant(t, p):
    """
    Calculate the dielectric constant of water.
    reference:[3]
    :param t: temperature of the water, in Kelvin.
    :param p: pressure, in bar.
    :return: dielectric constant.
    """
    u1 = 3.4279E2
    u2 = -5.0866E-3
    u3 = 9.4690E-7
    u4 = -2.0525
    u5 = 3.1159E3
    u6 = -1.8289E2
    u7 = -8.0325E3
    u8 = 4.2142E6
    u9 = 2.1417

    d_1000 = u1 * np.exp(u2 * t + u3 * t ** 2)
    c = u4 + u5 / (u6 + t)
    b = u7 + u8 / t + u9 * t

    d = d_1000 + c * np.log((b + p) / (b + 1000))
    return d


"""
------------------------------------------------------------------------------------------------------------------------
"""

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
