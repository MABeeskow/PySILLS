#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		incl_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		12.03.2026

#-----------------------------------------------

"""
Module: incl_concentrations.py
This module performs the compositional analysis of the sample input files.
"""

# PACKAGES
import numpy as np
import pandas as pd

# MODULES

# CODE


class InclusionAnalysis:
    def __init__(self, reference_isotope, matrix_only_tracer=None, second_reference_isotope=None):
        self.reference_isotope = reference_isotope
        self.matrix_only_tracer = reference_isotope
        self.second_reference_isotope = reference_isotope

    def determine_mixed_concentration_ratio(self, intensities_mixed, sensitivities):
        var_is1 = self.second_reference_isotope
        var_is2 = self.reference_isotope
        a = intensities_mixed[var_is1]/intensities_mixed[var_is2]*sensitivities[var_is1]

        return a

    def determine_mass_fraction(self, concentrations_matrix, concentrations_inclusion, mixed_concentration_ratio):
        var_is1 = self.second_reference_isotope
        var_is2 = self.reference_isotope
        a = mixed_concentration_ratio
        x = (concentrations_matrix[var_is1] - a*concentrations_matrix[var_is2])/(
                concentrations_matrix[var_is1] - concentrations_inclusion[var_is1] - a*(
                concentrations_matrix[var_is2] - concentrations_inclusion[var_is2]))

        return x

    def determine_mixed_concentration_second_internal_standard(
            self, concentrations_matrix, concentrations_inclusion, mass_fraction):
        var_is2 = self.reference_isotope
        x = mass_fraction
        concentration_is2 = (1 - x)*concentrations_matrix[var_is2] + x*concentrations_inclusion[var_is2]

        return concentration_is2

    def determine_mixed_concentrations(self, intensities_mixed, concentration_mixed_is2, sensitivities):
        var_is2 = self.reference_isotope
        concentrations_mixed = (intensities_mixed*concentration_mixed_is2)/(intensities_mixed[var_is2]*sensitivities)

        return concentrations_mixed

    def determine_inclusion_concentrations(self, concentrations_matrix, concentrations_mixed, mass_fraction):
        x = mass_fraction
        concentration_inclusion = concentrations_mixed/x - (1 - x)/x*concentrations_matrix

        return concentration_inclusion

    def determine_concentrations_halter(self, intensities_srm, concentrations_srm, intensities_incl, rsf):
        concentrations_smpl = (concentrations_srm*intensities_incl*rsf)/intensities_srm

        return concentrations_smpl

    def determine_inclusion_concentrations_halter(self, concentrations_mat, concentrations_mixed, x):
        concentrations_incl = concentrations_mat - (concentrations_mat - concentrations_mixed)/x

        return concentrations_incl

    def determine_mass_fraction_halter(self, concentrations_mat_is, concentrations_mix_is, concentrations_incl_is):
        x = (concentrations_mat_is - concentrations_mix_is)/(concentrations_mat_is - concentrations_incl_is)

        return x
