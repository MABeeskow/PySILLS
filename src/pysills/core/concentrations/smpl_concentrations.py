#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		smpl_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		11.03.2026

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
    def __init__(self, reference_isotope, reference_second_isotope=None, reference_matrix_only_tracer=None):
        self.reference_isotope = reference_isotope
        self.reference_second_isotope = reference_second_isotope
        self.reference_matrix_only_tracer = reference_matrix_only_tracer

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
        """
        Compute limit of detection, blank and quantification (lod, lob, loq).

        Parameters
        ----------
        intensities : pandas.Series
            Mean intensities, indexed by isotope.
        concentrations : pandas.Series
            Mean concentrations, indexed by isotope.
        n_bg_values : int
            Number of datapoints in (combined) background intervals.
        n_mat_values : int
            Number of datapoints in (combined) sample intervals.
        intensities_bg : pandas.Series
            Mean background intensities, indexed by isotope.
        tau_values : pandas.Series
            Dwell times, indexed by isotope.
        sigma_values : pandas.Series
            Standard deviation intensity values for the background, indexed by isotope.
        mode : str
            Quantification method (Pettke, Longerich).

        Returns
        -------
        lod : pandas.Series
            Limit of detection, indexed by isotope.
        lob : pandas.Series
            Limit of blank, indexed by isotope.
        loq : pandas.Series
            Limit of quantification, indexed by isotope.
        """
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

    def calculate_mixed_concentration_ratio(self, intensities_mix, sensitivity):
        if self.reference_second_isotope is not None:
            intensity_mix_is1 = intensities_mix[self.reference_second_isotope]
            intensity_mix_is2 = intensities_mix[self.reference_isotope]
            sensitivity_is1 = sensitivity[self.reference_second_isotope]
            result = intensity_mix_is1/(intensity_mix_is2*sensitivity_is1)
        elif self.reference_matrix_only_tracer is not None:
            intensity_mix_t = intensities_mix[self.reference_matrix_only_tracer]
            intensity_mix_is = intensities_mix[self.reference_isotope]
            sensitivity_t = sensitivity[self.reference_matrix_only_tracer]
            result = intensity_mix_t/(intensity_mix_is*sensitivity_t)

        return result

    def calculate_mass_fraction(self, concentrations_mat, concentrations_incl, mixed_ratio):
        if self.reference_second_isotope is not None:
            concentration_mat_is1 = concentrations_mat[self.reference_second_isotope]
            concentration_mat_is2 = concentrations_mat[self.reference_isotope]
            concentration_incl_is1 = concentrations_incl[self.reference_second_isotope]
            concentration_incl_is2 = concentrations_incl[self.reference_isotope]
            a = mixed_ratio
            result = (concentration_mat_is1 - a*concentration_mat_is2)/(
                    concentration_mat_is1 - concentration_incl_is1 - a*(concentration_mat_is2 - concentration_incl_is2))
        elif self.reference_matrix_only_tracer is not None:
            concentration_mat_is = concentrations_mat[self.reference_isotope]
            concentration_mat_t = concentrations_mat[self.reference_matrix_only_tracer]
            concentration_incl_is = concentrations_incl[self.reference_isotope]
            concentration_incl_t = concentrations_incl[self.reference_matrix_only_tracer]
            a = mixed_ratio
            result = (concentration_mat_t - a*concentration_mat_is)/(
                    concentration_mat_t - concentration_incl_t - a*(concentration_mat_is - concentration_incl_is))

        return result

    def calculate_inclusion_concentration_using_x(self, concentratios_mix, concentratios_host, mass_fraction):
        x = mass_fraction
        results = (concentratios_mix + (x - 1)*concentratios_host)/x

        return results

    def perform_quantification_by_halter_iterative(self):
        pass

    def perform_quantification_by_halter(self):
        pass

    def perform_quantification_by_borisova(self):
        pass