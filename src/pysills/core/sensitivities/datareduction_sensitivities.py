#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		datareduction_sensitivities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		12.03.2026

#-----------------------------------------------

"""
Module: datareduction_sensitivities.py
This module performs the data reduction of the LA-ICP-MS signal intensity input data and calculates the sensitivities.
"""

# PACKAGES
import re
import numpy as np
import pandas as pd

# MODULES

# CODE
ISOTOPE_REGEX = re.compile(r"^([A-Z][a-z]?)(\d+)$")


def extract_element(iso: str) -> str:
    return re.findall(r"[A-Za-z]+", iso)[0]

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

    def calculate_sensitivity_drift(self, sensitivities_dict, time_info):
        """
        Calculate linear drift of RSF per isotope.

        Parameters
        ----------
        sensitivities_dict : dict
            file_name -> pandas.Series (RSF values)

        time_info : dict
            file_name -> {"path": ..., "time_delta": float}

        Returns
        -------
        pandas.DataFrame
            Index = isotope
            Columns = ["intercept", "slope"]
        """
        # Build RSF matrix
        df = pd.DataFrame(sensitivities_dict).T
        # Extract time axis aligned with df index
        times = []
        for fname in df.index:
            if fname not in time_info:
                raise ValueError(f"No time information for file {fname}")
            times.append(time_info[fname]["time_delta"])

        t = np.array(times, dtype=float)
        if len(t) < 2:
            raise ValueError("At least two SRM time points required for drift calculation.")

        # Design matrix
        A = np.vstack([np.ones_like(t), t]).T
        results = []
        for isotope in df.columns:
            y = df[isotope].to_numpy(dtype=float)
            mask = np.isfinite(y)
            if mask.sum() < 2:
                results.append((isotope, np.nan, np.nan))
                continue

            A_valid = A[mask]
            y_valid = y[mask]
            coeffs, _, _, _ = np.linalg.lstsq(A_valid, y_valid, rcond=None)
            intercept = float(coeffs[0])
            slope = float(coeffs[1])
            results.append((isotope, intercept, slope))

        df_drift = pd.DataFrame(
            results,
            columns=["isotope", "intercept", "slope"]
        ).set_index("isotope")

        return df_drift

    def predict_sensitivities(self, df_drift, t_probe):
        """
        Parameters
        ----------
        df_drift : DataFrame
            Index = isotope
            Columns = ["intercept", "slope"]

        t_probe : float

        Returns
        -------
        pandas.Series
            RSF per isotope at time t_probe
        """
        rsf = df_drift["intercept"] + df_drift["slope"]*t_probe
        rsf.name = "RSF"
        return rsf

    def calculate_normalized_sensitivity(self, df_intensities, df_concentrations):
        result = df_intensities/df_concentrations

        return result

    def calculate_relative_sensitivity_factor(
            self, df_srm_intensities, df_srm_concentrations, df_is_intensity, df_is_concentration, df_sensitivity):
        elements = df_srm_intensities.index.map(lambda x: re.findall(r"[A-Za-z]+", x)[0])
        df_srm_concentrations = (df_srm_concentrations.set_index("Element")["Concentration"].astype(float))
        conc_iso = pd.Series(elements, index=df_srm_intensities.index).map(df_srm_concentrations)
        mask = (conc_iso.notna() & (conc_iso > 0) & (df_srm_intensities > 0) & (df_is_concentration > 0))
        rsf = pd.Series(np.nan, index=df_srm_intensities.index)
        rsf[mask] = (df_sensitivity[mask]*(conc_iso[mask]/df_srm_intensities[mask])*
                     (df_is_intensity/df_is_concentration))

        return rsf.rename("RSF")

    def determine_rsf_is(self, intensity_srm_is, concentration_srm_is, intensity_smpl_is, concentration_smpl_is):
        rsf = (concentration_srm_is*intensity_smpl_is)/(concentration_smpl_is*intensity_srm_is)

        return rsf
