#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		manual_test_input_parser_intensities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: manual_test_input_parser_intensities.py
This file tests if the input parse of the module DataReductionIntensities is working as exptected.
"""

# PACKAGES
from pathlib import Path

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
    parser = DRI()

    for fname in filenames:
        file_path = demo_dir/fname
        print(f"Testing file: {file_path}")
        df = parser.read_input_data(file_path)
        print(f"  -> shape: {df.shape}")
        print(f"  -> time range: {df.index.min()} – {df.index.max()}")
        print(f"  -> number of isotopes: {df.shape[1]}")
        print(f"  -> first isotopes: {list(df.columns[:5])}")
        print()
        # optional: full output on demand
        if show_full_df:
            print(df, "\n")

        df_ready = parser.prepare_for_reduction(df)
        print(f"  -> shape: {df_ready.shape}")
        print(f"  -> index range: {df_ready.index.min()} – {df_ready.index.max()}")
        print(f"  -> time range: "
              f"{df_ready["time_s"].min()} – {df_ready["time_s"].max()}")
        print(f"  -> number of isotopes: {df_ready.shape[1] - 1}")
        print(f"  -> first isotopes: {list(df_ready.columns[:5])}")
        print()
        # optional: full output on demand
        if show_full_df:
            print(df_ready, "\n")

        if "demo_ma01.csv" in fname:
            data_bg = DRI().reduce_intervals(df_ready=df_ready, intervals=[(19, 125)])
            print("data_bg", data_bg, "\n")
            data_bg = DRI().reduce_intervals(df_ready=df_ready, intervals=[(19, 125), (346, 392)])
            print("data_bg", data_bg, "\n")


if __name__ == "__main__":
    run_manual_test(show_full_df=True)
