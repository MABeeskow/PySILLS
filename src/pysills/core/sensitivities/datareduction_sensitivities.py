#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		datareduction_sensitivities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: datareduction_sensitivities.py
This module performs the data reduction of the LA-ICP-MS signal intensity input data and calculates the sensitivities.
"""

# PACKAGES
import re
import pandas as pd

# MODULES

# CODE
ISOTOPE_REGEX = re.compile(r"^([A-Z][a-z]?)(\d+)$")


def build_isotope_to_element_mapping(isotopes):
    """
    Build isotope-to-element mapping from isotope labels.

    Parameters
    ----------
    isotopes : iterable of str

    Returns
    -------
    dict
        Mapping isotope -> element
    """
    mapping = {}
    for iso in isotopes:
        m = ISOTOPE_REGEX.match(iso)
        if not m:
            raise ValueError(f"Invalid isotope name: {iso}")
        mapping[iso] = m.group(1)
    return mapping


class DataReductionSensitivities:
    def __init__(self, isotope_to_element):
        self.isotope_to_element = isotope_to_element

    def calculate_relative_sensitivity(self, intensity_ratios, concentration_ratios):
        """
        Compute relative sensitivity factors (RSF).

        Parameters
        ----------
        intensity_ratios : pandas.Series
            Intensity ratios I_x / I_ref indexed by isotope.
        concentration_ratios : pandas.Series
            Concentration ratios C_x / C_ref indexed by element.

        Returns
        -------
        pandas.Series
            RSF values indexed by isotope.
        """
        rsf = {}

        for iso, i_ratio in intensity_ratios.items():
            if iso not in self.isotope_to_element:
                continue  # or raise, je nach gewünschter Striktheit

            elem = self.isotope_to_element[iso]
            if elem not in concentration_ratios.index:
                continue

            c_ratio = concentration_ratios.loc[elem]
            if c_ratio <= 0:
                continue

            rsf[iso] = i_ratio/c_ratio

        return pd.Series(rsf, name="RSF")

    def calculate_analytical_sensitivity(self, df_intensities, df_concentrations):
        result = df_intensities/df_concentrations

        return result