#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		smpl_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		24.02.2026

#-----------------------------------------------

"""
Module: smpl_concentrations.py
This module performs the compositional analysis of the sample input files.
"""

# PACKAGES
import pandas as pd

# MODULES

# CODE


class SampleAnalysis:
    def __init__(self, reference_isotope):
        self.reference_isotope = reference_isotope

    def compute_concentrations(self, intensity_ratios, sensitivity_values, reference_concentration):
        """
        Compute sample concentrations from intensity ratios and RSF.

        Parameters
        ----------
        intensity_ratios : pandas.Series
            I_x / I_ref (background corrected)
        sensitivity_values : pandas.Series
            relative sensitivity values with respect to the reference isotope

        Returns
        -------
        pandas.Series
            Concentrations per isotope
        """
        concentrations = {}

        for iso, i_ratio in intensity_ratios.items():
            if iso not in sensitivity_values.index:
                continue

            rsf_val = sensitivity_values.loc[iso]
            if rsf_val <= 0:
                continue

            concentrations[iso] = (float(i_ratio)*float(reference_concentration)/float(rsf_val))

        return pd.Series(concentrations, name="Concentration")

    def compute_concentration_ratios(self, df_smpl, reference_element):
        pass

    def compute_limit_of_detection(self, df_smpl):
        pass