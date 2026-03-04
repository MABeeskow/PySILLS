#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		smpl_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		04.03.2026

#-----------------------------------------------

"""
Module: smpl_concentrations.py
This module performs the compositional analysis of the sample input files.
"""

# PACKAGES
import numpy as np
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

    def compute_concentration_ratios(self, concentrations, reference_isotope):
        """
        Compute concentration ratios C_x / C_ref.

        Parameters
        ----------
        concentrations : pandas.Series
            Mean concentrations indexed by isotope.
        reference_isotope : str
            Isotope used as reference (e.g. 'Si29').

        Returns
        -------
        pandas.Series
            Concentration ratios indexed by isotope.
        """
        if reference_isotope not in concentrations.index:
            raise ValueError(f"Reference isotope '{reference_isotope}' not found")

        conc_ref = concentrations.loc[reference_isotope]
        if conc_ref <= 0:
            raise ValueError("Reference intensity must be positive")

        ratios = concentrations/conc_ref
        ratios.name = f"C/C_{reference_isotope}"

        return ratios

    def compute_limit_of_detection(
            self, intensities, concentrations, n_bg_values, n_mat_values, intensities_bg=None, tau_values=None,
            sigma_values=None, mode="Pettke"):
        if mode == "Pettke":
            lod = (3.29*(intensities_bg*tau_values*n_mat_values*(1 + n_mat_values/n_bg_values))**(0.5) +
                            2.71)/(n_mat_values*tau_values)*(concentrations/intensities)
            a = 3.29/3.3
            b = 1/3.29
        elif mode == "Longerich":
            lod = (3*sigma_values*concentrations)/(intensities)*(1/n_bg_values + 1/n_mat_values)**(0.5)
            a = 3.0/3.3
            b = 1/3.0

        lob = 1.65*a*b*lod
        loq = 10*a*b*lod

        results = pd.DataFrame({"LoB": lob, "LoD": lod, "LoQ": loq})

        return results

    def calculate_1_sigma_concentration(
            self, intensities_bg, intensities_sig, tau_values, ref_concentration_sig, ref_intensity_sig,
            sensitivity_sig):
        var_intensities_bg = intensities_bg["mean"]
        var_length_bg = intensities_bg["length"]
        var_intensities_sig = intensities_sig["mean"]
        var_length_sig = intensities_sig["length"]

        sigma_bg = np.sqrt(var_intensities_bg/(var_length_bg*tau_values))
        sigma_sig = np.sqrt(var_intensities_sig/(var_length_sig*tau_values))
        sigma = np.sqrt(sigma_bg**2 + sigma_sig**2)
        results = (ref_concentration_sig/(ref_intensity_sig*sensitivity_sig))*sigma

        return results

    def perform_quantification_by_halter_iterative(self):
        pass

    def perform_quantification_by_halter(self):
        pass

    def perform_quantification_by_borisova(self):
        pass