# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description:
# Version: 1.0
# Last Modified: May 7, 2023

from sympy import *

import pprint

pp = pprint.PrettyPrinter(width=41, compact=True)

x, y, z = symbols('x,y,z')

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
                molalities[key] = value.subs({x: x_n, y: y_n})
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
                try:
                    molalities[key] = value.subs({x: x_n, y: y_n, z: z_n})
                except AttributeError:
                    molalities[key] = value
            return molalities, z_n
        x_n = x_n_plus
        y_n = y_n_plus
        z_n = z_n_plus