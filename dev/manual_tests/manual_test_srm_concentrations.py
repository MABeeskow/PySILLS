#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		manual_test_srm_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: manual_test_srm_concentrations.py
This file tests if the input from the srm files is working as expected.
"""

# PACKAGES
from pathlib import Path
import pandas as pd
pd.options.display.float_format = "{:.3f}".format

# MODULES
from pysills.core.concentrations.srm_concentrations import StandardReferenceMaterial as SRM


# CODE
def run_manual_test(show_full_df=False):
    print("--------------------------")
    print("Manual parser test started")
    print("--------------------------\n")

    root = Path(__file__).resolve().parents[2]
    srm_dir = root/"src"/"pysills"/"legacy"/"lib"/"srm"
    filenames = ["B6.csv", "NIST_610_GeoReM.csv"]
    srm = SRM(sep=";")

    for fname in filenames:
        file_path = srm_dir/fname
        print(f"Testing file: {file_path}")
        df = srm.read_input_data(file_path)
        print(f"  -> shape: {df.shape}")
        print(f"  -> index range: {df.index.min()} – {df.index.max()}")
        print(f"  -> first elements: {df.iloc[:5, 0].tolist()}")
        if show_full_df:
            print(df, "\n")

        ref_element = "Si"
        ratios = srm.compute_concentration_ratios(df, reference_element=ref_element)
        print("Reference element:", ref_element)
        print(f"  -> shape: {ratios.shape}")
        print(f"  -> index range: {ratios.index.min()} – {ratios.index.max()}")
        if show_full_df:
            print(ratios.map("{:.3e}".format), "\n")

if __name__ == "__main__":
    run_manual_test(show_full_df=True)