#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		srm_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: srm_concentrations.py
This module performs the data import from the standard reference material (srm) input files.
"""

# PACKAGES
import pandas as pd
from pathlib import Path

# MODULES

# CODE


class StandardReferenceMaterial:
    def __init__(self, sep=","):
        self.sep = sep

    def read_input_data(self, file_path):
        """
        Load SRM concentrations from a CSV file.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Path to the SRM CSV file.

        Returns
        -------
        pandas.DataFrame
        """
        suffix = Path(file_path).suffix.lower()
        if suffix in [".xls", ".xlsx"]:
            raise ValueError("Binary Excel files are not supported by this parser")

        file_path = Path(file_path)
        df = pd.read_csv(file_path, sep=self.sep, header=None, names=["Element", "Concentration"])

        if df.empty:
            raise ValueError("SRM file is empty")

        if df.shape[1] != 2:
            raise ValueError("SRM file must contain exactly two columns")

        df["Element"] = df["Element"].str.strip()
        df["Element"] = df["Element"].str.capitalize()
        df["Concentration"] = pd.to_numeric(df["Concentration"], errors="coerce")

        return df

    def compute_concentration_ratios(self, df_srm, reference_element):
        """
        Compute concentration ratios C_x / C_ref for a standard reference material.

        Parameters
        ----------
        df_srm : pandas.DataFrame
            SRM concentrations with columns ['Element', 'Concentration'].
        reference_element : str
            Element used as reference (e.g. 'Si').

        Returns
        -------
        pandas.Series
            Concentration ratios indexed by element symbol.
        """
        df = df_srm.set_index("Element", drop=True)
        reference_element = reference_element.strip().capitalize()
        if reference_element not in df.index:
            raise ValueError(f"Reference element '{reference_element}' not found in SRM")

        c_ref = df.loc[reference_element, "Concentration"]

        if c_ref <= 0:
            raise ValueError("Reference concentration must be positive")

        ratios = df["Concentration"]/c_ref
        ratios.name = f"C/C_{reference_element}"

        return ratios