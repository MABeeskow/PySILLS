# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description:
# Version: 1.0
# Last Modified: May 7, 2023

from sympy import *


def find_pair(x, pairs):
    """
    :param x: a tuple
    :param pairs: a list of tuples
    :return: a dict contains a boolean value and the match (if there is).
    """
    pair_length = len(pairs)
    i = 0
    has = False
    target = ''
    while i < pair_length:
        pair = pairs[i]
        if set(x) == set(pair):
            has = True
            target = pair
        i += 1
    return {
        "has": has,
        "target": target
    }


x = symbols('x')


def newton_raphson(x_n, eq, eq_prime, max_iterators):
    tolerance = 10 ** (-6)
    iterate_number = 0

    while iterate_number < max_iterators:
        print("x_{n}: {x_n}".format(n=iterate_number, x_n=float(x_n)))
        iterate_number += 1
        f = eq.subs({x: x_n}).evalf()
        f_prime = eq_prime.subs({x: x_n}).evalf()
        x_n_plus = x_n - f / f_prime

        if abs((x_n_plus - x_n) / x_n) < tolerance:
            return x_n
        x_n = x_n_plus


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


def type_of_species(ion):
    """
    determine the type of a ion (string).
    :param ion:
    :return: 0-neutral, 1-cation, -1-anion
    """
    type_value = 0

    charge = get_charge_number(ion)
    if charge == 0:
        type_value = 0
    if charge > 0:
        type_value = 1
    if charge < 0:
        type_value = -1
    return type_value
