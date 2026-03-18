#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		smpl_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		17.03.2026

#-----------------------------------------------

"""
Module: smpl_concentrations.py
This module performs the compositional analysis of the sample input files.
"""

# PACKAGES
import re
import numpy as np
import pandas as pd

# MODULES

# CODE
_chemistry_data = {
    "O": 15.999, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974, "K": 39.098, "Ca": 40.078,
    "Ti": 47.867, "Cr": 51.996, "Mn": 54.938, "Fe": 55.845, "Ga": 69.723, "Ge": 72.630, "Zr": 91.224,
    "Ba": 137.33, "B": 10.81, "Ag": 107.87, "As": 74.922, "Li": 6.94, "Rb": 85.468, "Cs": 132.91, "Sr": 87.62,
    "Sc": 44.956, "Y": 88.906, "Hf": 178.49, "V": 50.942, "Nb": 92.906, "Ta": 180.95, "Mo": 95.962, "W": 183.84,
    "Tc": 98.906, "Re": 186.21, "Ru": 101.07, "Os": 190.23, "Co": 58.933, "Rh": 102.91, "Ir": 192.22,
    "Ni": 58.693, "Pd": 106.42, "Pt": 195.08, "Cu": 63.546, "Au": 196.97, "Zn": 65.38, "Cd": 112.41,
    "Hg": 200.59, "In": 114.82, "Tl": 204.38, "C": 12.011, "Sn": 118.71, "Pb": 207.2, "N": 14.007, "Sb": 121.76,
    "Bi": 208.98, "S": 32.06, "Se": 78.96, "Te": 127.60, "Po": 209.98, "Cl": 35.45, "Br": 79.904, "I": 126.90,
    "At": 210.99, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24, "Pm": 146.92, "Sm": 150.36,
    "Eu": 151.96, "Gd": 157.25, "Tb": 158.93, "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93,
    "Yb": 173.05, "Lu": 174.97, "Ac": 227.03, "Th": 232.04, "Pa": 231.04, "U": 238.05, "Be": 9.0122,
    "F": 18.998, "H": 1.008}
_chemistry_data_oxides = {
    "SiO2": 60.083, "Al2O3": 101.961, "Fe2O3": 159.687, "FeO": 71.844, "Na2O": 61.979, "TiO2": 79.865,
    "MnO": 70.937, "Mn2O3": 157.873, "SnO": 134.709, "Li2O": 29.879, "Ga2O3": 187.443, "B2O3": 69.617,
    "BeO": 25.0112, "GeO2": 104.628, "CaO": 56.077, "Rb2O": 186.935, "AgO": 123.869, "As2O3": 197.841,
    "Au2O": 409.939, "BaO": 153.32, "Br2O": 175.807, "Cl2O": 86.899, "Cs2O": 281.819, "CuO": 79.545,
    "PbO": 223.199, "SO3": 80.057, "Sb2O3": 291.517, "SrO": 103.619, "WO3": 231.837, "ZnO": 81.379,
    "MgO": 40.304, "K2O": 55.097, "SnO2": 150.708, "Ag2O": 231.739, "Bi2O5": 497.955, "CO2": 44.009,
    "CdO": 128.409, "Ce2O3": 328.237, "CeO2": 172.118, "CoO": 74.932, "Cr2O3": 151.989, "Dy2O3": 372.997,
    "Er2O3": 382.517, "Eu2O3": 351.917, "Gd2O3": 362.497, "HfO2": 404.977, "HgO": 216.589, "Ho2O3": 377.857,
    "In2O3": 277.637, "IrO": 208.219, "La2O3": 325.817, "Lu2O3": 397.937, "MnO2": 86.936, "MoO3": 143.959,
    "N2O5": 108.009, "Nb2O5": 265.807, "Nd2O3": 336.477, "NiO": 74.692, "OsO": 206.229, "P2O5": 141.943,
    "PbO2": 239.198, "PdO": 122.419, "Pr2O3": 329.817, "Pr6O11": 1021.449, "PtO": 211.079, "ReO": 202.209,
    "RhO": 118.909, "RuO": 117.069, "SO4": 96.056, "Sb2O5": 323.515, "Sc2O3": 137.909, "SeO3": 126.957,
    "Sm2O3": 348.717, "Ta2O5": 441.895, "Tb2O3": 365.857, "Tb4O7": 747.713, "TeO3": 175.597, "ThO2": 264.038,
    "Tl2O3": 456.757, "Tm2O3": 385.857, "UO2": 270.048, "UO3": 286.047, "U3O8": 842.142, "V2O5": 181.879,
    "Y2O3": 225.809, "Yb2O3": 394.097, "ZrO2": 123.222, "I2O4": 317.796, "I2O5": 333.795, "I4O9": 651.591,
    "I2O": 269.799, "Ni2O3": 165.383, "Co2O3": 165.863, "CrO": 67.995, "H2O": 18.015, "SO2": 64.058, "Au2O3": 441.937}

_conversion_factors = {
    "SiO2": (_chemistry_data["Si"]/_chemistry_data_oxides["SiO2"])**(-1),
    "Al2O3": (2*_chemistry_data["Al"]/_chemistry_data_oxides["Al2O3"])**(-1),
    "Fe2O3": (2*_chemistry_data["Fe"]/_chemistry_data_oxides["Fe2O3"])**(-1),
    "FeO": (_chemistry_data["Fe"]/_chemistry_data_oxides["FeO"])**(-1),
    "Na2O": (2*_chemistry_data["Na"]/_chemistry_data_oxides["Na2O"])**(-1),
    "TiO2": (_chemistry_data["Ti"]/_chemistry_data_oxides["TiO2"])**(-1),
    "MnO": (_chemistry_data["Mn"]/_chemistry_data_oxides["MnO"])**(-1),
    "Mn2O3": (2*_chemistry_data["Mn"]/_chemistry_data_oxides["Mn2O3"])**(-1),
    "SnO": (_chemistry_data["Sn"]/_chemistry_data_oxides["SnO"])**(-1),
    "Li2O": (2*_chemistry_data["Li"]/_chemistry_data_oxides["Li2O"])**(-1),
    "Ga2O3": (2*_chemistry_data["Ga"]/_chemistry_data_oxides["Ga2O3"])**(-1),
    "B2O3": (2*_chemistry_data["B"]/_chemistry_data_oxides["B2O3"])**(-1),
    "BeO": (_chemistry_data["Be"]/_chemistry_data_oxides["BeO"])**(-1),
    "GeO2": (_chemistry_data["Ge"]/_chemistry_data_oxides["GeO2"])**(-1),
    "CaO": (_chemistry_data["Ca"]/_chemistry_data_oxides["CaO"])**(-1),
    "Rb2O": (2*_chemistry_data["Rb"]/_chemistry_data_oxides["Rb2O"])**(-1),
    "AgO": (_chemistry_data["Ag"]/_chemistry_data_oxides["AgO"])**(-1),
    "As2O3": (2*_chemistry_data["As"]/_chemistry_data_oxides["As2O3"])**(-1),
    "Au2O": (2*_chemistry_data["Au"]/_chemistry_data_oxides["Au2O"])**(-1),
    "Au2O3": (2*_chemistry_data["Au"]/_chemistry_data_oxides["Au2O3"])**(-1),
    "BaO": (_chemistry_data["Ba"]/_chemistry_data_oxides["BaO"])**(-1),
    "Br2O": (2*_chemistry_data["Br"]/_chemistry_data_oxides["Br2O"])**(-1),
    "Cl2O": (2*_chemistry_data["Cl"]/_chemistry_data_oxides["Cl2O"])**(-1),
    "Cs2O": (2*_chemistry_data["Cs"]/_chemistry_data_oxides["Cs2O"])**(-1),
    "CuO": (_chemistry_data["Cu"]/_chemistry_data_oxides["CuO"])**(-1),
    "PbO": (_chemistry_data["Pb"]/_chemistry_data_oxides["PbO"])**(-1),
    "SO3": (_chemistry_data["S"]/_chemistry_data_oxides["SO3"])**(-1),
    "Sb2O3": (2*_chemistry_data["Sb"]/_chemistry_data_oxides["Sb2O3"])**(-1),
    "SrO": (_chemistry_data["Sr"]/_chemistry_data_oxides["SrO"])**(-1),
    "WO3": (_chemistry_data["W"]/_chemistry_data_oxides["WO3"])**(-1),
    "ZnO": (_chemistry_data["Zn"]/_chemistry_data_oxides["ZnO"])**(-1),
    "MgO": (_chemistry_data["Mg"]/_chemistry_data_oxides["MgO"])**(-1),
    "K2O": (2*_chemistry_data["K"]/_chemistry_data_oxides["K2O"])**(-1),
    "SnO2": (_chemistry_data["Sn"]/_chemistry_data_oxides["SnO2"])**(-1),
    "Ag2O": (2*_chemistry_data["Ag"]/_chemistry_data_oxides["Ag2O"])**(-1),
    "Bi2O5": (2*_chemistry_data["Bi"]/_chemistry_data_oxides["Bi2O5"])**(-1),
    "CO2": (_chemistry_data["C"]/_chemistry_data_oxides["CO2"])**(-1),
    "CdO": (_chemistry_data["Cd"]/_chemistry_data_oxides["CdO"])**(-1),
    "Ce2O3": (2*_chemistry_data["Ce"]/_chemistry_data_oxides["Ce2O3"])**(-1),
    "CeO2": (_chemistry_data["Ce"]/_chemistry_data_oxides["CeO2"])**(-1),
    "CoO": (_chemistry_data["Co"]/_chemistry_data_oxides["CoO"])**(-1),
    "CrO": (_chemistry_data["Cr"]/_chemistry_data_oxides["CrO"])**(-1),
    "Cr2O3": (2*_chemistry_data["Cr"]/_chemistry_data_oxides["Cr2O3"])**(-1),
    "Dy2O3": (2*_chemistry_data["Dy"]/_chemistry_data_oxides["Dy2O3"])**(-1),
    "Er2O3": (2*_chemistry_data["Er"]/_chemistry_data_oxides["Er2O3"])**(-1),
    "Eu2O3": (2*_chemistry_data["Eu"]/_chemistry_data_oxides["Eu2O3"])**(-1),
    "Gd2O3": (2*_chemistry_data["Gd"]/_chemistry_data_oxides["Gd2O3"])**(-1),
    "HfO2": (_chemistry_data["Hf"]/_chemistry_data_oxides["HfO2"])**(-1),
    "HgO": (_chemistry_data["Hg"]/_chemistry_data_oxides["HgO"])**(-1),
    "Ho2O3": (2*_chemistry_data["Ho"]/_chemistry_data_oxides["Ho2O3"])**(-1),
    "In2O3": (2*_chemistry_data["In"]/_chemistry_data_oxides["In2O3"])**(-1),
    "IrO": (_chemistry_data["Ir"]/_chemistry_data_oxides["IrO"])**(-1),
    "La2O3": (2*_chemistry_data["La"]/_chemistry_data_oxides["La2O3"])**(-1),
    "Lu2O3": (2*_chemistry_data["Lu"]/_chemistry_data_oxides["Lu2O3"])**(-1),
    "MnO2": (_chemistry_data["Mn"]/_chemistry_data_oxides["MnO2"])**(-1),
    "MoO3": (_chemistry_data["Mo"]/_chemistry_data_oxides["MoO3"])**(-1),
    "N2O5": (2*_chemistry_data["N"]/_chemistry_data_oxides["N2O5"])**(-1),
    "Nb2O5": (2*_chemistry_data["Nb"]/_chemistry_data_oxides["Nb2O5"])**(-1),
    "Nd2O3": (2*_chemistry_data["Nd"]/_chemistry_data_oxides["Nd2O3"])**(-1),
    "NiO": (_chemistry_data["Ni"]/_chemistry_data_oxides["NiO"])**(-1),
    "OsO": (_chemistry_data["Os"]/_chemistry_data_oxides["OsO"])**(-1),
    "P2O5": (2*_chemistry_data["P"]/_chemistry_data_oxides["P2O5"])**(-1),
    "PbO2": (_chemistry_data["Pb"]/_chemistry_data_oxides["PbO2"])**(-1),
    "PdO": (_chemistry_data["Pd"]/_chemistry_data_oxides["PdO"])**(-1),
    "Pr2O3": (2*_chemistry_data["Pr"]/_chemistry_data_oxides["Pr2O3"])**(-1),
    "Pr6O11": (6*_chemistry_data["Pr"]/_chemistry_data_oxides["Pr6O11"])**(-1),
    "PtO": (_chemistry_data["Pt"]/_chemistry_data_oxides["PtO"])**(-1),
    "ReO": (_chemistry_data["Re"]/_chemistry_data_oxides["ReO"])**(-1),
    "RhO": (_chemistry_data["Rh"]/_chemistry_data_oxides["RhO"])**(-1),
    "RuO": (_chemistry_data["Ru"]/_chemistry_data_oxides["RuO"])**(-1),
    "SO4": (_chemistry_data["S"]/_chemistry_data_oxides["SO4"])**(-1),
    "Sb2O5": (2*_chemistry_data["Sb"]/_chemistry_data_oxides["Sb2O5"])**(-1),
    "Sc2O3": (2*_chemistry_data["Sc"]/_chemistry_data_oxides["Sc2O3"])**(-1),
    "SeO3": (_chemistry_data["Se"]/_chemistry_data_oxides["SeO3"])**(-1),
    "Sm2O3": (2*_chemistry_data["Sm"]/_chemistry_data_oxides["Sm2O3"])**(-1),
    "Ta2O5": (2*_chemistry_data["Ta"]/_chemistry_data_oxides["Ta2O5"])**(-1),
    "Tb2O3": (2*_chemistry_data["Tb"]/_chemistry_data_oxides["Tb2O3"])**(-1),
    "Tb4O7": (4*_chemistry_data["Tb"]/_chemistry_data_oxides["Tb4O7"])**(-1),
    "TeO3": (_chemistry_data["Te"]/_chemistry_data_oxides["TeO3"])**(-1),
    "ThO2": (_chemistry_data["Th"]/_chemistry_data_oxides["ThO2"])**(-1),
    "Tl2O3": (2*_chemistry_data["Tl"]/_chemistry_data_oxides["Tl2O3"])**(-1),
    "Tm2O3": (2*_chemistry_data["Tm"]/_chemistry_data_oxides["Tm2O3"])**(-1),
    "UO2": (_chemistry_data["U"]/_chemistry_data_oxides["UO2"])**(-1),
    "UO3": (_chemistry_data["U"]/_chemistry_data_oxides["UO3"])**(-1),
    "U3O8": (3*_chemistry_data["U"]/_chemistry_data_oxides["U3O8"])**(-1),
    "V2O5": (2*_chemistry_data["V"]/_chemistry_data_oxides["V2O5"])**(-1),
    "Y2O3": (2*_chemistry_data["Y"]/_chemistry_data_oxides["Y2O3"])**(-1),
    "Yb2O3": (2*_chemistry_data["Yb"]/_chemistry_data_oxides["Yb2O3"])**(-1),
    "ZrO2": (_chemistry_data["Zr"]/_chemistry_data_oxides["ZrO2"])**(-1),
    "I2O4": (2*_chemistry_data["I"]/_chemistry_data_oxides["I2O4"])**(-1),
    "I2O5": (2*_chemistry_data["I"]/_chemistry_data_oxides["I2O5"])**(-1),
    "I4O9": (4*_chemistry_data["I"]/_chemistry_data_oxides["I4O9"])**(-1),
    "I2O": (2*_chemistry_data["I"]/_chemistry_data_oxides["I2O"])**(-1),
    "Co2O3": (2*_chemistry_data["Co"]/_chemistry_data_oxides["Co2O3"])**(-1),
    "Ni2O3": (2*_chemistry_data["Ni"]/_chemistry_data_oxides["Ni2O3"])**(-1),
    "H2O": (2*_chemistry_data["H"]/_chemistry_data_oxides["H2O"])**(-1),
    "SO2": (_chemistry_data["S"]/_chemistry_data_oxides["SO2"])**(-1)}
_chemistry_oxides_sorted = {
    "H": ["H2O"], "Li": ["Li2O"], "Be": ["BeO"], "B": ["B2O3"], "C": ["CO", "CO2"],
    "N": ["NO", "N2O3", "NO2", "N2O5"], "Na": ["Na2O"], "Mg": ["MgO"], "Al": ["Al2O3"], "Si": ["SiO2"],
    "P": ["P2O3", "P2O5"], "S": ["SO", "SO2", "SO3"], "Cl": ["Cl2O", "ClO2", "Cl2O3", "Cl2O5", "Cl2O7"],
    "K": ["K2O"], "Ca": ["CaO"], "Sc": ["Sc2O3"], "Ti": ["Ti2O3", "TiO2"], "V": ["VO", "V2O3", "VO2", "V2O5"],
    "Cr": ["CrO", "Cr2O3", "CrO3"], "Mn": ["MnO", "Mn2O3", "MnO2", "MnO3", "Mn2O7"],
    "Fe": ["FeO", "Fe2O3", "FeO3"], "Co": ["CoO", "Co2O3"], "Ni": ["NiO", "Ni2O3"], "Cu": ["Cu2O", "CuO"],
    "Zn": ["ZnO"], "Ga": ["Ga2O3"], "Ge": ["GeO2"], "As": ["As2O3", "As2O5"], "Se": ["SeO2", "SiO3"],
    "Br": ["Br2O", "Br2O3", "Br2O5", "Br2O7"], "Kr": ["KrO"], "Rb": ["Rb2O"], "Sr": ["SrO"], "Y": ["Y2O3"],
    "Zr": ["ZrO2"], "Nb": ["Nb2O3", "Nb2O5"], "Mo": ["MoO", "Mo2O3", "MoO2", "Mo2O5", "MoO3"], "Tc": ["Tc2O7"],
    "Ru": ["RuO", "Ru2O3", "RuO2", "RuO3", "RuO4"], "Rh": ["Rh2O", "RhO", "Rh2O3", "RhO2", "Rh2O5"],
    "Pd": ["PdO", "PdO2"], "Ag": ["Ag2O", "AgO"], "Cd": ["CdO"], "In": ["In2O3"], "Sn": ["SnO", "SnO2"],
    "Sb": ["Sb2O3", "Sb2O5"], "Te": ["TeO2", "TeO3"], "I": ["I2O", "I2O4", "I2O5", "I4O9"],
    "Xe": ["XeO", "XeO2", "XeO3"], "Cs": ["Cs2O"], "Ba": ["BaO"], "La": ["La2O3"], "Ce": ["Ce2O3", "CeO2"],
    "Pr": ["Pr2O3", "PrO2"], "Nd": ["Nd2O3"], "Pm": ["Pm2O3"], "Sm": ["SmO", "Sm2O3"], "Eu": ["EuO", "Eu2O3"],
    "Gd": ["Gd2O3"], "Tb": ["Tb2O3", "TbO2"], "Dy": ["Dy2O3"], "Ho": ["Ho2O3"], "Er": ["Er2O3"],
    "Tm": ["TmO", "Tm2O3"], "Yb": ["YbO", "Yb2O3"], "Lu": ["Lu2O3"], "Hf": ["HfO2"], "Ta": ["Ta2O5"],
    "W": ["WO", "WO2O3", "WO2", "W2O5", "WO3"], "Re": ["ReO", "ReO2", "ReO3", "Re2O7"],
    "Os": ["OsO", "Os2O3", "OsO2", "OsO3", "OsO4"], "Ir": ["Ir2O", "IrO", "Ir2O3", "IrO2", "IrO3"],
    "Pt": ["PtO", "PtO2"], "Au": ["Au2O", "Au2O3"], "Hg": ["Hg2O", "HgO"], "Tl": ["Tl2O", "Tl2O3"],
    "Pb": ["PbO", "PbO2"], "Bi": ["Bi2O3", "B2O5"], "Po": ["PoO", "PoO2", "PoO3"],
    "At": ["At2O", "At2O3", "At2O5", "At2O7"], "Rn": ["RnO"], "Fr": ["Fr2O"], "Ra": ["RaO"], "Ac": ["Ac2O3"],
    "Th": ["ThO2"], "Pa": ["PaO2", "Pa2O5"], "U": ["U2O3", "UO2", "U2O5", "UO3"],
    "Np": ["Np2O3", "NpO2", "Np2O5", "NpO3"], "Pu": ["Pu2O3", "PuO2", "Pu2O5", "PuO3"],
    "Am": ["Am2O3", "AmO2", "Am2O5", "AmO3"], "Cm": ["Cm2O3", "CmO2"], "Bk": ["Bk2O3", "BkO2"],
    "Cf": ["Cf2O3", "CfO2"], "Es": ["Es2O3"], "Fm": ["Fm2O3"], "Md": ["Md2O3"], "No": ["NoO", "No2O3"],
    "Lr": ["Lr2O3"]}

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
        """
        Calculates the 1-sigma concentration. "sig" represents the specific signal contribution (e.g., matrix, mixed,
        inclusion)

        Parameters
        ----------
        intensities_bg : pandas.Series
            Mean background intensities, indexed by isotope.
        intensities_sig : str
            Mean sample intensities, indexed by isotope.
        tau_values : str
            Dwell times, indexed by isotope.
        ref_concentration_sig : str
            Sample concentration of the reference isotope.
        ref_intensity_sig : str
            Sample intensity of the reference isotope.
        sensitivity_sig : str
            Normalized/relative sample sensitivity, indexed by isotope.

        Returns
        -------
        results : pandas.Series
            1-sigma concentration, indexed by isotope.
        """
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

    def determine_mass_fraction_volume(self, volume_incl, rho_incl, volume_mat, rho_mat):
        x = (volume_incl*rho_incl)/(volume_mat*rho_mat + volume_incl*rho_incl)

        return x

    def determine_mass_fraction_geometric(self, a, b, radius, rho_mat, rho_incl, c=None):
        if c is not None:
            volume = 4/3*np.pi*a*b*c
            upper_term = volume*rho_incl
            lower_term = (2*np.pi*c*radius**2 - volume)*rho_mat + upper_term
            x = upper_term/lower_term
        else:
            area = 4/3*np.pi*a*b
            upper_term = area*rho_incl
            lower_term = (2*np.pi*radius**2 - area)*rho_mat + upper_term
            x = upper_term/lower_term

        return x

    def calculate_inclusion_concentration_using_x(self, concentratios_mix, concentratios_host, mass_fraction):
        x = mass_fraction
        results = (concentratios_mix + (x - 1)*concentratios_host)/x
        return results

    def perform_quantification_by_halter_iterative(self):
        pass

    def perform_quantification_by_halter(self):
        pass

    def calculate_inclusion_concentration_by_borisova(
            self, concentrations_mat_t, rho_mat, rho_incl, radius_mat, radius_incl, sensitivities, k):
        results = (concentrations_mat_t*(rho_mat/rho_incl)*(1/sensitivities)*k*(1.5*(radius_mat/radius_incl)**2 - 1))

        return results

    def calculate_apparent_concentrations(self, concentrations_srm, intensities_smpl, intensities_srm):
        results = concentrations_srm*intensities_smpl/intensities_srm
        return results

    def convert_element_concentrations_to_oxide_concentrations(
            self, concentrations_apparent, accept_unphysical_values=False):
        list_isotopes = concentrations_apparent.index.tolist()
        list_elements = []
        conversion_factors = {}
        for isotope in list_isotopes:
            key_element = re.search(r"(\D+)(\d+)", isotope)
            element = key_element.group(1)
            list_elements.append(element)
            list_oxides = _chemistry_oxides_sorted[element]
            for oxide in list_oxides:
                if element in ["P", "S", "Cl", "Ti", "Mn", "Fe", "Cu", "Ge", "As", "Br", "W", "Au"]:
                    if oxide in ["P2O5", "SO3", "Cl2O", "TiO2", "MnO", "Fe2O3", "CuO", "GeO2", "As2O3", "Br2O", "WO3",
                                 "Au2O3"]:
                        factor = _conversion_factors[oxide]
                        conversion_factors[isotope] = factor
                else:
                    factor = _conversion_factors[oxide]
                    conversion_factors[isotope] = factor

        df_conversion_factors = pd.Series(conversion_factors, index=list_isotopes)
        df_concentrations_oxides = concentrations_apparent*df_conversion_factors
        rsf = 10**6/df_concentrations_oxides.sum()
        concentrations = concentrations_apparent*rsf
        if accept_unphysical_values:
            concentrations = concentrations.clip(lower=0.0)
            concentrations = concentrations.mask(concentrations > 1000000, 0.0)

        return concentrations

    def calculate_inclusion_concentrations_by_normalizing_oxides_using_salinity(
            self, concentrations_apparent, salinity, dissolved_volatiles=1.0, accept_unphysical_values=False):
        list_isotopes = concentrations_apparent.index.tolist()
        list_elements = []
        conversion_factors = {}
        for isotope in list_isotopes:
            key_element = re.search(r"(\D+)(\d+)", isotope)
            element = key_element.group(1)
            list_elements.append(element)
            list_oxides = _chemistry_oxides_sorted[element]
            for oxide in list_oxides:
                if element in ["P", "S", "Cl", "Ti", "Mn", "Fe", "Cu", "Ge", "As", "Br", "W", "Au"]:
                    if oxide in ["P2O5", "SO3", "Cl2O", "TiO2", "MnO", "Fe2O3", "CuO", "GeO2", "As2O3", "Br2O", "WO3",
                                 "Au2O3"]:
                        factor = _conversion_factors[oxide]
                        conversion_factors[isotope] = factor
                else:
                    factor = _conversion_factors[oxide]
                    conversion_factors[isotope] = factor

        df_conversion_factors = pd.Series(conversion_factors, index=list_isotopes)
        df_concentrations_oxides = concentrations_apparent*df_conversion_factors
        rsf = (salinity*dissolved_volatiles)*10**6/df_concentrations_oxides.sum()
        concentrations = concentrations_apparent*rsf
        if accept_unphysical_values:
            concentrations = concentrations.clip(lower=0.0)
            concentrations = concentrations.mask(concentrations > 1000000, 0.0)

        return concentrations