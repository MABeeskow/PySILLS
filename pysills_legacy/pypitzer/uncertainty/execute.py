# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description:
# Version: 1.0
# Last Modified: May 7, 2023


from sympy import *
from public.icemelting import (clegg_and_brimblecombe, spencer, monnin)
from uncertainty.models import FluidPitzer

from database.solid_data import solids
import pprint
import uncertainty.methods as pm

pp = pprint.PrettyPrinter(width=41, compact=True)

x, z = symbols('x,z')


def newton_raphson(x_n, y_n, inputed_f, r_total, molalities, max_iterators):
    inputed_partial_x = diff(inputed_f, x)
    inputed_partial_y = diff(inputed_f, y)
    tolerance = 10 ** (-6)
    iterate_number = 0

    while iterate_number < max_iterators:
        print("x_{n}: {x_n}; y_{n}: {y_n}".format(n=iterate_number, x_n=float(x_n), y_n=float(y_n)))
        iterate_number += 1
        partial_x = inputed_partial_x.subs({x: x_n, y: y_n}).evalf()
        partial_y = inputed_partial_y.subs({x: x_n, y: y_n}).evalf()
        multiple_num = 1 / (partial_x + partial_y * r_total)
        f = inputed_f.subs({x: x_n, y: y_n}).evalf()
        x_n_plus = x_n - multiple_num * (f + partial_y * (x_n * r_total - y_n))
        y_n_plus = y_n - multiple_num * (r_total * f - partial_x * (x_n * r_total - y_n))

        if abs((x_n_plus - x_n) / x_n) < tolerance and abs((y_n_plus - y_n) / y_n) < tolerance:
            for key, value in molalities.items():
                molalities[key] = value.subs({x: x_n, y: y_n})
            return molalities
        x_n = x_n_plus
        y_n = y_n_plus


def newton_raphson_general(x_n, y_n, f_func, g_func, molalities, max_iterators):
    partial_fx = diff(f_func, x)
    partial_fy = diff(f_func, y)
    partial_gx = diff(g_func, x)
    partial_gy = diff(g_func, y)
    tolerance = 10 ** (-6)
    iterate_number = 0
    while iterate_number < max_iterators:
        print("x_{n}: {x_n}; y_{n}: {y_n}".format(n=iterate_number, x_n=x_n, y_n=y_n))
        iterate_number += 1
        partial_fx = partial_fx.subs({x: x_n, y: y_n}).evalf()
        partial_fy = partial_fy.subs({x: x_n, y: y_n}).evalf()
        partial_gx = partial_gx.subs({x: x_n, y: y_n}).evalf()
        partial_gy = partial_gy.subs({x: x_n, y: y_n}).evalf()
        det_value = partial_fx * partial_gy - partial_fy * partial_gx
        f_value = f_func.subs({x: x_n, y: y_n}).evalf()
        g_value = g_func.subs({x: x_n, y: y_n}).evalf()
        x_n_plus = x_n - (1 / det_value) * (partial_gy * f_value - partial_fy * g_value)
        y_n_plus = y_n - (1 / det_value) * (-partial_gx * f_value + partial_fx * g_value)
        if abs((x_n_plus - x_n) / x_n) < tolerance and abs((y_n_plus - y_n) / y_n) < tolerance:
            for key, value in molalities.items():
                try:
                    molalities[key] = value.subs({x: x_n, y: y_n})
                except AttributeError:
                    molalities[key] = value
            return molalities, y_n
        x_n = x_n_plus
        y_n = y_n_plus


def newton_raphson_three(funcs, x_n, y_n, z_n, molalities, max_iterators):
    f_func = funcs[0]
    g_func = funcs[1]
    h_func = funcs[2]
    a1 = diff(f_func, x)  # partial_fx
    a2 = diff(f_func, y)  # partial_fy
    a3 = diff(f_func, z)  # partial_fz

    b1 = diff(g_func, x)  # partial_gx
    b2 = diff(g_func, y)  # partial_gy
    b3 = diff(g_func, z)  # partial_gz

    c1 = diff(h_func, x)  # partial_hx
    c2 = diff(h_func, y)  # partial_hy
    c3 = diff(h_func, z)  # partial_hz

    tolerance = 10 ** (-6)
    iterate_number = 0
    while iterate_number < max_iterators:
        print("x_{n}: {x_n}; y_{n}: {y_n}; z_{n}: {z_n}".format(n=iterate_number, x_n=x_n, y_n=y_n, z_n=z_n))
        iterate_number += 1
        a1 = a1.subs({x: x_n, y: y_n, z: z_n}).evalf()
        a2 = a2.subs({x: x_n, y: y_n, z: z_n}).evalf()
        a3 = a3.subs({x: x_n, y: y_n, z: z_n}).evalf()
        b1 = b1.subs({x: x_n, y: y_n, z: z_n}).evalf()
        b2 = b2.subs({x: x_n, y: y_n, z: z_n}).evalf()
        b3 = b3.subs({x: x_n, y: y_n, z: z_n}).evalf()
        c1 = c1.subs({x: x_n, y: y_n, z: z_n}).evalf()
        c2 = c2.subs({x: x_n, y: y_n, z: z_n}).evalf()
        c3 = c3.subs({x: x_n, y: y_n, z: z_n}).evalf()

        det_value = a1 * b2 * c3 - a1 * b3 * c2 - a2 * b1 * c3 + a2 * b3 * c1 + a3 * b1 * c2 - a3 * b2 * c1

        f_value = f_func.subs({x: x_n, y: y_n, z: z_n}).evalf()
        g_value = g_func.subs({x: x_n, y: y_n, z: z_n}).evalf()
        h_value = h_func.subs({x: x_n, y: y_n, z: z_n}).evalf()

        x_n_plus = x_n - (1 / det_value) * (
                (b2 * c3 - b3 * c2) * f_value + (-a2 * c3 + a3 * c2) * g_value + (a2 * b3 - a3 * b2) * h_value)
        y_n_plus = y_n - (1 / det_value) * (
                (-b1 * c3 + b3 * c1) * f_value + (a1 * c3 - a3 * c1) * g_value + (-a1 * b3 + a3 * b1) * h_value)
        z_n_plus = z_n - (1 / det_value) * (
                (b1 * c2 - b2 * c1) * f_value + (-a1 * c2 + a2 * c1) * g_value + (a1 * b2 - a2 * b1) * h_value)
        if abs((x_n_plus - x_n) / x_n) < tolerance and abs((y_n_plus - y_n) / y_n) < tolerance and abs(
                (z_n_plus - z_n) / z_n) < tolerance:
            for key, value in molalities.items():
                molalities[key] = value.subs({x: x_n, y: y_n, z: z_n})
            return molalities, z_n
        x_n = x_n_plus
        y_n = y_n_plus
        z_n = z_n_plus


def function_generator(solid, fluid):
    lna_pitzer = fluid.get_water_activity()
    # lnk_potential = 0
    if solid == 'H2O(S)':
        # lnk_ice = clegg_and_brimblecombe(fluid.t)
        # lnk_ice = monnin(fluid.t)
        lnk_ice = spencer(fluid.t)
        f = lnk_ice - lna_pitzer
    else:
        molalities = fluid.get_molalities()

        lnk_potential = pm.get_chemical_potential(solid=solid, temperature=fluid.t)

        print('deltaG:', lnk_potential)

        solid_data = solids[solid]
        print(solid_data)
        lnk_activity = 0
        for species in solid_data.keys():
            # get the stochiometric number of this species first
            sto = solid_data[species]['value']
            if solid_data[species]['type'] == 'cation':
                m_c = molalities[species]
                ln_gamma_c = fluid.get_cation_activity_coefficients(target_cation=species)
                lnk_activity += sto * (
                        ln(m_c) + ln_gamma_c
                )
            elif solid_data[species]['type'] == 'anion':
                m_a = molalities[species]
                ln_gamma_a = fluid.get_anion_activity_coefficients(target_anion=species)
                lnk_activity += sto * (
                        ln(m_a) + ln_gamma_a
                )
            else:
                lnk_activity += sto * lna_pitzer
        f = lnk_potential - lnk_activity
    return f


def invariant_point_input(solid1, solid2, species, t, x_guess, y_guess, max_iterators=100, sulfate=False):
    """
    Calculate the eutectic point between two solid phases.
    :param solid1: [string], the first solid phase.
    :param solid2: [string], the second solid phase.
    :param species: species and corresponding ratios with repect to sodium.
    :param temperature_guess: guess the eutectic temperature, for calculating convenience.
    :param concentration_guess: guess the eutectic concentration of the salt, for calculating convenience.
    :return: eutectic temperature and composition.
    """
    fluid = FluidPitzer(
        t=t,
        dictionary=species,
        database='spencer',
    )

    func_1 = function_generator(solid1, fluid)
    func_2 = function_generator(solid2, fluid)
    return newton_raphson_general(
        x_n=x_guess,
        y_n=y_guess,
        f_func=func_1,
        g_func=func_2,
        molalities=fluid.get_molalities(),
        max_iterators=max_iterators
    )


def invariant_point_input_ternary(solids, molalities, x_n, y_n, z_n):
    """
    Calculate the eutectic point between two solid phases.
    :param solids: a list of solids.
    :param molalities: species and corresponding ratios with repect to sodium.
    :param temperature_guess: guess the eutectic temperature, for calculating convenience.
    :param concentration_guess: guess the eutectic concentration of the salt, for calculating convenience.
    :return: eutectic temperature and composition.
    """
    fluid = FluidPitzer(
        t=z,
        dictionary=molalities,
        database='spencer',

    )
    func_1 = function_generator(solids[0], fluid)
    func_2 = function_generator(solids[1], fluid)
    func_3 = function_generator(solids[2], fluid)
    result = newton_raphson_three(
        funcs=[func_1, func_2, func_3],
        x_n=x_n,
        y_n=y_n,
        z_n=z_n,
        molalities=fluid.get_molalities(),
        max_iterators=100
    )
    return result


def concentration_input(t, species, solid, database='spencer', x_guess=0.01, y_guess=0.01, max_iterators=50,
                        sulfate=False):
    """
    :param t: melting temperature of ice or salts
    :param species: a dictionary, should be in form of {"a species": numeric_ratio,...}.
    :param solid: if the temperature provided is melting temperature of hydrates, then the formula of the hydrate should
    be provided here.
    :param x_guess: guess value of x_n
    :param y_guess: guess value of y_n
    :param database: name of database we will use
    :return:
    """
    print(x_guess, y_guess)
    t_melt = t
    dictionary = species
    fluid = FluidPitzer(
        dictionary=dictionary,
        t=t_melt,
        database=database,
    )
    # print(fluid.get_molalities())

    f_func = function_generator(solid=solid, fluid=fluid)
    g_func = fluid.charge_balance()

    result = newton_raphson_general(
        x_n=x_guess,
        y_n=y_guess,
        f_func=f_func,
        g_func=g_func,
        molalities=fluid.get_molalities(),
        max_iterators=max_iterators
    )
    return result


n = 1
y = symbols('y:' + str(n))
print(y)
v_dict = {
    x: 1.85,  # concentration of Na calculated with the model
    y[0]: 2,
    # y[1]: 0.050009709,
    # y[2]: 0.018006502,
    # y[3]: 0.001333698,
    # y[4]: 0.001159332,
    # y[5]: 0.000121677,
    # y[6]: 0.000139219,
    # y[7]: 0.000423009,
    # y[8]: 0.000329692,
    # y[9]: 2.33738E-05,
    z: 25,
}

u_dict = {
    y[0]: 0.28,
    # y[1]: 0.008029289,
    # y[2]: 0.004282004,
    # y[3]: 0.000493429,
    # y[4]: 0.000567157,
    # y[5]: 1.28302E-05,
    # y[6]: 4.18045E-05,
    # y[7]: 2.47324E-05,
    # y[8]: 0.000122204,
    # y[9]: 2.68774E-06,
    z: 0.2
}

print(u_dict)

fluid = FluidPitzer(
    t=z,
    dictionary={
        'Na+': x,
        'K+': x * y[0],
        # 'Li+': x * y[2],
        # 'Mg+2': x * y[3],
        # 'Sr+2': x * y[4],
        # 'Cs+': x * y[5],
        # 'Rb+': x * y[6],
        # 'Mn+2': x * y[7],
        # 'Zn+2': x * y[8],
        # 'Pb+2': x * y[9],
    },
    database='spencer',
)

# objective function
fun = function_generator('KCl', fluid)

# partial derivative of fun to x,y0,y1,...,z
d_dict = {}
d_dict['d1'] = diff(fun, x)  # partial_fx
d_dict['d2'] = diff(fun, z)  # partial_fz

# partial_fy_i
for i in range(len(v_dict.keys()) - 2):
    d_dict['d{}'.format(i + 3)] = diff(fun, y[i])

# substitute numerical values into partial derivative expressions
for key, value in d_dict.items():
    d_dict[key] = value.subs(v_dict)

# partial to internal standard ∂x/∂z
p_dict = {}
p_dict['p_xz'] = -d_dict['d2'] / d_dict['d1']

# partial to internal standard ∂x/∂y_i, y_i is element/Na ratio
for i in range(len(y)):
    p_dict['p_xy{}'.format(i)] = -d_dict['d{}'.format(i + 3)] / d_dict['d1']

print(p_dict)

import math

sum_v = 0
# uncertainties from element/Na ratios
for i in range(len(y)):
    partial = p_dict['p_xy{}'.format(i)]
    uncertainty = u_dict[y[i]]
    sum_v += (partial * uncertainty) ** 2

# uncertainties from solid melting temperautre
partial_z = p_dict['p_xz']
uncertainty_z = u_dict[z]
sum_v += (partial_z * uncertainty_z) ** 2

# get square root of sum_v
d_x = math.sqrt(sum_v)

print(d_x)
