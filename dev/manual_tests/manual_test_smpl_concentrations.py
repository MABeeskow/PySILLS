#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		manual_test_smpl_concentrations.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		24.02.2026

#-----------------------------------------------

"""
Module: manual_test_smpl_concentrations.py
This file tests if quantification of the sample composition is working as expected.
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
from pysills.core.concentrations.smpl_concentrations import SampleAnalysis as SA
from pysills.core.io.icpms_reader import ICPMSReader


# CODE
def run_manual_test(show_full_df=False):
    print("--------------------------")
    print("Manual test started")
    print("-- mineral analysis")
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

    reference_concentration = 467436.7125
    demo_dir = root/"src"/"pysills"/"legacy"/"lib"/"demo_files"
    filenames_smpl = []
    for counter in range(13):
        if counter < 10:
            filename = "demo_ma0" + str(counter) + ".csv"
        else:
            filename = "demo_ma" + str(counter) + ".csv"
        filenames_smpl.append(filename)
    dri = DRI(zero_time=False)

    files_srm_setup = {
        "demo_ma01.csv": {"BG": [4.8, 37.2], "MAT": [46.2, 87.0]},
        "demo_ma02.csv": {"BG": [4.8, 37.2], "MAT": [46.2, 87.0]},
        "demo_ma03.csv": {"BG": [4.8, 36.9], "MAT": [45.9, 86.7]},
        "demo_ma10.csv": {"BG": [4.8, 36.9], "MAT": [45.9, 87.0]},
        "demo_ma11.csv": {"BG": [4.8, 36.9], "MAT": [45.9, 87.0]},
        "demo_ma12.csv": {"BG": [4.8, 36.9], "MAT": [45.9, 87.0]}}

    files_smpl_setup = {
        "demo_ma04.csv": {"BG": [4.8, 39.9], "MAT": [48.9, 87.6]},
        "demo_ma05.csv": {"BG": [4.8, 40.8], "MAT": [49.8, 88.5]},
        "demo_ma06.csv": {"BG": [4.8, 39.6], "MAT": [48.6, 87.6]},
        "demo_ma07.csv": {"BG": [4.8, 39.9], "MAT": [48.9, 87.9]},
        "demo_ma08.csv": {"BG": [4.8, 39.6], "MAT": [48.6, 87.3]}}

    reader = ICPMSReader()
    filepaths_list = []
    for filename in files_srm_setup.keys():
        file_path = demo_dir/filename
        filepaths_list.append(file_path)
    for filename in files_smpl_setup.keys():
        file_path = demo_dir/filename
        filepaths_list.append(file_path)
    runs = reader.read_many(filepaths_list)
    time_deltas = {}
    for run in runs:
        t_rel = run["t_rel"]
        filename = run["filename"]
        time_deltas[filename] = {"time_delta": t_rel}

    results_srm = {}
    results_smpl = {}
    srm_sensitivities = {}
    for fname, setup_info in files_srm_setup.items():
        file_path = demo_dir/fname
        df = dri.read_input_data(file_path)
        df_ready = dri.prepare_for_reduction(df)

        t_0 = setup_info["BG"][0]
        t_1 = setup_info["BG"][1]
        t_4 = setup_info["MAT"][0]
        t_5 = setup_info["MAT"][1]
        idx_0 = dri.find_index_for_time(df_ready=df_ready, time_value=t_0)
        idx_1 = dri.find_index_for_time(df_ready=df_ready, time_value=t_1)
        idx_4 = dri.find_index_for_time(df_ready=df_ready, time_value=t_4)
        idx_5 = dri.find_index_for_time(df_ready=df_ready, time_value=t_5)

        data_bg1 = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_0, idx_1)])
        data_sig = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_4, idx_5)])
        data_sig_corr = dri.subtract_background(signal=data_sig["mean"], background=data_bg1["mean"])
        i_ratios = dri.compute_intensity_ratios(intensities=data_sig_corr, reference_isotope=ref_isotope)

        isotope_to_element = build_isotope_to_element_mapping(i_ratios.index)
        drs = DRS(isotope_to_element)
        df_sens = drs.calculate_relative_sensitivity(intensity_ratios=i_ratios, concentration_ratios=i_ratios_srm)
        srm_sensitivities[fname] = df_sens
        if show_full_df:
            print("Filename:", fname, "\n")
            print(df_sens, "\n")

    for fname, setup_info in files_smpl_setup.items():
        file_path = demo_dir/fname
        df = dri.read_input_data(file_path)
        df_ready = dri.prepare_for_reduction(df)
        time_delta = time_deltas[fname]["time_delta"]
        df_rsf_drift = drs.calculate_sensitivity_drift(sensitivities_dict=srm_sensitivities, time_info=time_deltas)
        rsf_pred = drs.predict_sensitivities(df_drift=df_rsf_drift, t_probe=time_delta)

        t_0 = setup_info["BG"][0]
        t_1 = setup_info["BG"][1]
        t_4 = setup_info["MAT"][0]
        t_5 = setup_info["MAT"][1]
        idx_0 = dri.find_index_for_time(df_ready=df_ready, time_value=t_0)
        idx_1 = dri.find_index_for_time(df_ready=df_ready, time_value=t_1)
        idx_4 = dri.find_index_for_time(df_ready=df_ready, time_value=t_4)
        idx_5 = dri.find_index_for_time(df_ready=df_ready, time_value=t_5)

        data_bg1 = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_0, idx_1)])
        data_sig = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_4, idx_5)])
        data_sig_corr = dri.subtract_background(signal=data_sig["mean"], background=data_bg1["mean"])
        i_ratios = dri.compute_intensity_ratios(intensities=data_sig_corr, reference_isotope=ref_isotope)
        df_comp = SA(reference_isotope=ref_isotope).compute_concentrations(
            intensity_ratios=i_ratios, sensitivity_values=rsf_pred, reference_concentration=reference_concentration)

        if fname in ["demo_ma04.csv", "demo_ma05.csv", "demo_ma06.csv", "demo_ma07.csv", "demo_ma08.csv"]:
            results_smpl[fname] = {
                "intensities": data_sig_corr, "ratios": i_ratios, "sensitivities": df_sens, "composition": df_comp}
            if show_full_df:
                print("Filename:", fname, "\n")
                print(df_comp)


if __name__ == "__main__":
    run_manual_test(show_full_df=True)