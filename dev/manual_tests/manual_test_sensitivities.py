#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		manual_test_sensitivities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: manual_test_sensitivities.py
This file tests if calculation of the sensitivities is working as expected.
"""

# PACKAGES
from pathlib import Path
import pandas as pd
pd.options.display.float_format = "{:.3f}".format

# MODULES
from pysills.core.sensitivities.datareduction_sensitivities import DataReductionSensitivities as DRS
from pysills.core.intensities.datareduction_intensities import DataReductionIntensities as DRI
from pysills.core.concentrations.srm_concentrations import StandardReferenceMaterial as SRM
from pysills.core.sensitivities.datareduction_sensitivities import build_isotope_to_element_mapping


# CODE
def run_manual_test(show_full_df=False):
    print("--------------------------")
    print("Manual test started")
    print("--------------------------\n")

    root = Path(__file__).resolve().parents[2]
    srm_dir = root/"src"/"pysills"/"legacy"/"lib"/"srm"
    filenames = ["NIST_610_GeoReM.csv"]
    srm = SRM(sep=";")
    ref_element = "Si"
    ref_isotope = "Si29"

    for fname in filenames:
        file_path = srm_dir/fname
        df_srm = srm.read_input_data(file_path)
        i_ratios_srm = srm.compute_concentration_ratios(df_srm, reference_element=ref_element)

    demo_dir = root/"src"/"pysills"/"legacy"/"lib"/"demo_files"
    filenames = ["demo_ma01.csv"]
    dri = DRI(zero_time=True)

    for fname in filenames:
        print("Filename:", fname, "\n")
        file_path = demo_dir/fname
        df = dri.read_input_data(file_path)
        df_ready = dri.prepare_for_reduction(df)

        if "demo_ma01.csv" in fname:
            t_0 = 6
            t_1 = 36
            t_4 = 45
            t_5 = 90
            idx_0 = dri.find_index_for_time(df_ready=df_ready, time_value=t_0)
            idx_1 = dri.find_index_for_time(df_ready=df_ready, time_value=t_1)
            idx_4 = dri.find_index_for_time(df_ready=df_ready, time_value=t_4)
            idx_5 = dri.find_index_for_time(df_ready=df_ready, time_value=t_5)

            data_bg1 = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_0, idx_1)])
            data_sig = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_4, idx_5)])
            data_sig_corr = dri.subtract_background(signal=data_sig["mean"], background=data_bg1["mean"])

            # Signal intensity ratios
            i_ratios = dri.compute_intensity_ratios(intensities=data_sig_corr, reference_isotope=ref_isotope)

    isotope_to_element = build_isotope_to_element_mapping(i_ratios.index)
    drs = DRS(isotope_to_element)

    df_sens = drs.calculate_relative_sensitivity(intensity_ratios=i_ratios, concentration_ratios=i_ratios_srm)
    print("df_sens\n", df_sens.map("{:.3f}".format), "\n")

if __name__ == "__main__":
    run_manual_test(show_full_df=True)