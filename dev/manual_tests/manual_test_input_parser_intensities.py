#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		manual_test_input_parser_intensities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		31.01.2026

#-----------------------------------------------

"""
Module: manual_test_input_parser_intensities.py
This file tests if the input parse of the module DataReductionIntensities is working as exptected.
"""

# PACKAGES
from pathlib import Path
import pandas as pd
pd.options.display.float_format = "{:.3f}".format

# MODULES
from pysills.core.intensities.datareduction_intensities import DataReductionIntensities as DRI


# CODE
def run_manual_test(show_full_df=False):
    print("--------------------------")
    print("Manual parser test started")
    print("--------------------------\n")

    root = Path(__file__).resolve().parents[2]
    demo_dir = root/"src"/"pysills"/"legacy"/"lib"/"demo_files"
    filenames = ["demo_ma01.csv", "another_demo_file.xl"]
    dri = DRI(zero_time=True)

    for fname in filenames:
        file_path = demo_dir/fname
        print(f"Testing file: {file_path}")
        df = dri.read_input_data(file_path)
        print(f"  -> shape: {df.shape}")
        print(f"  -> time range: {df.index.min()} – {df.index.max()}")
        print(f"  -> number of isotopes: {df.shape[1]}")
        print(f"  -> first isotopes: {list(df.columns[:5])}")
        print()
        # optional: full output on demand
        if show_full_df:
            print(df, "\n")

        df_ready = dri.prepare_for_reduction(df)
        print(f"  -> shape: {df_ready.shape}")
        print(f"  -> index range: {df_ready.index.min()} – {df_ready.index.max()}")
        tmin = df_ready["time_s"].min()
        tmax = df_ready["time_s"].max()
        print(f"  -> time range: {tmin} – {tmax}")
        print(f"  -> number of isotopes: {df_ready.shape[1] - 1}")
        print(f"  -> first isotopes: {list(df_ready.columns[:5])}")
        print()
        # optional: full output on demand
        if show_full_df:
            print(df_ready, "\n")

        if "demo_ma01.csv" in fname:
            t_0 = 6
            t_1 = 36
            t_2 = 105
            t_3 = 115
            t_4 = 45
            t_5 = 90
            idx_0 = dri.find_index_for_time(df_ready=df_ready, time_value=t_0)
            idx_1 = dri.find_index_for_time(df_ready=df_ready, time_value=t_1)
            idx_2 = dri.find_index_for_time(df_ready=df_ready, time_value=t_2)
            idx_3 = dri.find_index_for_time(df_ready=df_ready, time_value=t_3)
            idx_4 = dri.find_index_for_time(df_ready=df_ready, time_value=t_4)
            idx_5 = dri.find_index_for_time(df_ready=df_ready, time_value=t_5)

            print("Closest measured time value to given value of", t_0, ":  ", idx_0, df_ready["time_s"][idx_0])
            print("Closest measured time value to given value of", t_1, ":  ", idx_1, df_ready["time_s"][idx_1], "\n")

            data_bg1 = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_0, idx_1)])
            print("data_bg1\n", data_bg1, "\n")

            idx_0 = dri.find_index_for_time(df_ready=df_ready, time_value=t_0)
            idx_1 = dri.find_index_for_time(df_ready=df_ready, time_value=t_1)

            print("Closest measured time value to given value of", t_2, ":  ", idx_2, df_ready["time_s"][idx_2])
            print("Closest measured time value to given value of", t_3, ":  ", idx_3, df_ready["time_s"][idx_3], "\n")

            data_bg2 = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_0, idx_1), (idx_2, idx_3)])
            print("data_bg2\n", data_bg2, "\n")

            print("Closest measured time value to given value of", t_4, ":  ", idx_4, df_ready["time_s"][idx_4])
            print("Closest measured time value to given value of", t_5, ":  ", idx_5, df_ready["time_s"][idx_5], "\n")

            data_sig = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_4, idx_5)])
            data_sig_corr = dri.subtract_background(signal=data_sig["mean"], background=data_bg1["mean"])
            sig_corr_std = dri.propagate_background_uncertainty(
                signal_std=data_sig["std"], background_std=data_bg1["std"])
            print("data_sig\n", data_sig, "\n")
            print("data_sig_corr\n", data_sig_corr, "\n")
            print("sig_corr_std\n", sig_corr_std, "\n")
            se_bg1 = dri.compute_standard_error(std=data_bg1["std"], intervals=[(idx_0, idx_1)])
            se_bg2 = dri.compute_standard_error(std=data_bg2["std"], intervals=[(idx_0, idx_1), (idx_2, idx_3)])
            print("se_bg1\n", se_bg1, "\n")
            print("se_bg2\n", se_bg2, "\n")
            rsd_bg1 = dri.compute_rsd(mean=data_bg1["mean"], std=data_bg1["std"])
            rsd_sig = dri.compute_rsd(mean=data_sig["mean"], std=data_sig["std"])
            rsd_sig_corr = dri.compute_rsd(mean=data_sig_corr, std=sig_corr_std)
            print("rsd_bg1\n", rsd_bg1, "\n")
            print("rsd_sig\n", rsd_sig, "\n")
            print("rsd_sig_corr\n", rsd_sig_corr, "\n")

            # Signal intensity ratios
            i_ratios = dri.compute_intensity_ratios(intensities=data_sig_corr, reference_isotope="Si29")
            print("i_ratios\n", i_ratios.map("{:.3e}".format), "\n")

if __name__ == "__main__":
    run_manual_test(show_full_df=True)
