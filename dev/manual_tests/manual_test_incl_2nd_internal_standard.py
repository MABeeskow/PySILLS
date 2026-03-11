#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		manual_test_incl_2nd_internal_standard.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		11.03.2026

#-----------------------------------------------

"""
Module: manual_test_incl_2nd_internal_standard.py
This file tests if quantification of the sample composition is working as expected.
"""

# PACKAGES
from pathlib import Path

import numpy as np
import pandas as pd
pd.options.display.float_format = "{:.5f}".format

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
    print("-- fluid inclusion analysis")
    print("--------------------------\n")

    root = Path(__file__).resolve().parents[2]
    srm_dir = root/"src"/"pysills"/"legacy"/"lib"/"srm"
    filenames = ["NIST_610_GeoReM.csv", "Scapolite_17.csv"]
    srm = SRM(sep=";")
    ref_isotope_matrix = "Si29"
    ref_isotope_2 = "As75"
    #ref_isotope_2 = "Cl35"
    #ref_isotope_2 = "Li7"
    ref_element = "Na"
    ref_isotope = "Na23"

    df_srm_i_ratios = {}
    df_srm_i = {}
    for fname in filenames:
        file_path = srm_dir/fname
        df_srm = srm.read_input_data(file_path)
        i_ratios_srm = srm.compute_concentration_ratios(df_srm, reference_element=ref_element)
        df_srm_i[fname] = df_srm
        df_srm_i_ratios[fname] = i_ratios_srm

    reference_concentration_mat = 467436.7125
    concentration_incl_is = {"demo_fi05.csv": 19415.2373, "demo_fi06.csv": 19344.7604}      # Na

    # Both internal standards should come from the same standard reference material. In this case, Na, As and Li are
    # all from NIST-610, while Cl comes from Scapolite-17.

    concentration_incl_is2 = {"demo_fi05.csv": 2137.07749, "demo_fi06.csv": 1800.24031}     # As
    #concentration_incl_is2 = {"demo_fi05.csv": 19647.30601, "demo_fi06.csv": 24447.65470}  # Cl
    #concentration_incl_is2 = {"demo_fi05.csv": 95.25327, "demo_fi06.csv": 306.39438}       # Li
    demo_dir = root/"src"/"pysills"/"legacy"/"lib"/"demo_files"
    filenames_smpl = []
    for counter in range(13):
        if counter < 10:
            filename = "demo_fi0" + str(counter) + ".csv"
        else:
            filename = "demo_fi" + str(counter) + ".csv"
        filenames_smpl.append(filename)
    dri = DRI(zero_time=False)

    files_srm_setup = {
        "demo_fi01.csv": {"BG": [1.0, 40.2], "MAT": [46.9, 91.7], "SRM": "NIST_610_GeoReM.csv"},
        "demo_fi02.csv": {"BG": [1.0, 40.2], "MAT": [46.9, 91.0], "SRM": "NIST_610_GeoReM.csv"},
        "demo_fi03.csv": {"BG": [1.0, 39.9], "MAT": [46.4, 91.5], "SRM": "Scapolite_17.csv"},
        "demo_fi04.csv": {"BG": [1.0, 40.8], "MAT": [47.5, 91.4], "SRM": "Scapolite_17.csv"},
        "demo_fi10.csv": {"BG": [1.0, 40.8], "MAT": [47.5, 91.7], "SRM": "NIST_610_GeoReM.csv"},
        "demo_fi11.csv": {"BG": [1.0, 40.2], "MAT": [46.9, 90.7], "SRM": "NIST_610_GeoReM.csv"},
        "demo_fi12.csv": {"BG": [1.8, 40.5], "MAT": [49.4, 89.8], "SRM": "Scapolite_17.csv"},
        "demo_fi13.csv": {"BG": [1.0, 39.9], "MAT": [46.4, 90.7], "SRM": "Scapolite_17.csv"}}

    files_smpl_setup = {
        "demo_fi05.csv": {"BG": [235.9, 296.8], "MAT1": [106.7, 120.4], "MAT2": [134.5, 140.1], "INCL": [121.8, 133.8]},
        "demo_fi06.csv": {"BG": [4.5, 41.9], "MAT1": [85.6, 94.8], "MAT2": [166.7, 176.2], "INCL": [106.4, 156.0]}}

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

    srm_sensitivities_nist610 = {}
    srm_sensitivities_sca17 = {}
    srm_intensities = {}
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
        df_srm_intensities = dri.subtract_background(signal=data_sig["mean"], background=data_bg1["mean"])
        i_ratios = dri.compute_intensity_ratios(intensities=df_srm_intensities, reference_isotope=ref_isotope)

        isotope_to_element = build_isotope_to_element_mapping(i_ratios.index)
        drs = DRS(isotope_to_element)
        srmname = setup_info["SRM"]
        df_sens = drs.calculate_relative_sensitivity(
            intensity_ratios=i_ratios, concentration_ratios=df_srm_i_ratios[srmname])
        if "NIST" in srmname:
            srm_sensitivities_nist610[fname] = df_sens
        else:
            srm_sensitivities_sca17[fname] = df_sens
        srm_intensities[fname] = df_srm_intensities

        #if show_full_df:
        #    print("Filename:", fname, "\n")
        #    print(srm_sensitivities_nist610[fname], "\n")
        #    print(srm_sensitivities_sca17[fname], "\n")

    df_srm_intensities = pd.concat(srm_intensities.values(), axis=1)
    df_srm_intensities = df_srm_intensities.mean(axis=1)

    for fname, setup_info in files_smpl_setup.items():
        reference_concentration_incl = concentration_incl_is[fname]
        reference_concentration_incl_2 = concentration_incl_is2[fname]
        file_path = demo_dir/fname
        df = dri.read_input_data(file_path)
        df_ready = dri.prepare_for_reduction(df)
        time_delta = time_deltas[fname]["time_delta"]
        df_rsf_drift_nist610 = drs.calculate_sensitivity_drift(
            sensitivities_dict=srm_sensitivities_nist610, time_info=time_deltas)
        rsf_pred_nist610 = drs.predict_sensitivities(df_drift=df_rsf_drift_nist610, t_probe=time_delta)
        df_rsf_drift_sca17 = drs.calculate_sensitivity_drift(
            sensitivities_dict=srm_sensitivities_sca17, time_info=time_deltas)
        rsf_pred_sca17 = drs.predict_sensitivities(df_drift=df_rsf_drift_sca17, t_probe=time_delta)

        cols_replace = ["Cl35", "Br81"]
        df_sensitivity_drift = rsf_pred_nist610.copy()
        df_sensitivity_drift[cols_replace] = rsf_pred_sca17[cols_replace]

        t_0 = setup_info["BG"][0]
        t_1 = setup_info["BG"][1]
        t_2 = setup_info["MAT1"][0]
        t_3 = setup_info["MAT1"][1]
        t_4 = setup_info["MAT2"][0]
        t_5 = setup_info["MAT2"][1]
        t_6 = setup_info["INCL"][0]
        t_7 = setup_info["INCL"][1]
        idx_0 = dri.find_index_for_time(df_ready=df_ready, time_value=t_0)
        idx_1 = dri.find_index_for_time(df_ready=df_ready, time_value=t_1)
        idx_2 = dri.find_index_for_time(df_ready=df_ready, time_value=t_2)
        idx_3 = dri.find_index_for_time(df_ready=df_ready, time_value=t_3)
        idx_4 = dri.find_index_for_time(df_ready=df_ready, time_value=t_4)
        idx_5 = dri.find_index_for_time(df_ready=df_ready, time_value=t_5)
        idx_6 = dri.find_index_for_time(df_ready=df_ready, time_value=t_6)
        idx_7 = dri.find_index_for_time(df_ready=df_ready, time_value=t_7)

        data_bg1 = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_0, idx_1)])
        data_sig = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_2, idx_3), (idx_4, idx_5)])
        data_incl = dri.reduce_intervals(df_ready=df_ready, intervals=[(idx_6, idx_7)])

        # matrix quantification
        df_intensities_mat = dri.subtract_background(signal=data_sig["mean"], background=data_bg1["mean"])
        i_ratios = dri.compute_intensity_ratios(intensities=df_intensities_mat, reference_isotope=ref_isotope_matrix)
        df_concentrations_mat = SA(reference_isotope=ref_isotope_matrix).compute_concentrations(
            intensity_ratios=i_ratios, sensitivity_values=df_sensitivity_drift/df_sensitivity_drift[ref_isotope_matrix],
            reference_concentration=reference_concentration_mat)

        df_concentrations_mat = df_concentrations_mat.clip(lower=0.0)

        # inclusion quantification
        df_intensities_mix = dri.subtract_background(signal=data_incl["mean"], background=data_bg1["mean"])

        a = SA(reference_isotope=ref_isotope,
               reference_second_isotope=ref_isotope_2).calculate_mixed_concentration_ratio(
            intensities_mix=df_intensities_mix, sensitivity=df_sensitivity_drift)
        x = SA(reference_isotope=ref_isotope,
               reference_second_isotope=ref_isotope_2).calculate_mass_fraction(
            concentrations_mat=df_concentrations_mat, concentrations_incl={
                ref_isotope_2: reference_concentration_incl_2, ref_isotope: reference_concentration_incl},
            mixed_ratio=a)

        concentration_mix_is = (1 - x)*df_concentrations_mat[ref_isotope] + x*reference_concentration_incl
        i_mix_ratios = dri.compute_intensity_ratios(
            intensities=df_intensities_mix, reference_isotope=ref_isotope)
        df_concentrations_mix = SA(reference_isotope=ref_isotope).compute_concentrations(
            intensity_ratios=i_mix_ratios, sensitivity_values=df_sensitivity_drift,
            reference_concentration=concentration_mix_is)
        df_concentrations_incl_x = SA(reference_isotope=ref_isotope).calculate_inclusion_concentration_using_x(
            concentratios_mix=df_concentrations_mix, concentratios_host=df_concentrations_mat, mass_fraction=x)
        df_intensities_incl_x = dri.calculate_inclusion_intensity_using_x(
            intensities_mix=df_intensities_mix, intensities_mat=df_intensities_mat, mass_fraction=x,
            concentrations_mat=df_concentrations_mat, concentration_mix=df_concentrations_mix,
            sensitivities=df_sensitivity_drift, reference_concentration_incl=reference_concentration_incl,
            reference_isotope=ref_isotope)
        i_incl_ratios = dri.compute_intensity_ratios(intensities=df_intensities_incl_x, reference_isotope=ref_isotope)
        df_concentrations_incl_alt = SA(reference_isotope=ref_isotope).compute_concentrations(
            intensity_ratios=i_incl_ratios, sensitivity_values=df_sensitivity_drift,
            reference_concentration=reference_concentration_incl)

        df_concentrations_incl_x = df_concentrations_incl_x.clip(lower=0.0)
        df_concentrations_incl_alt = df_concentrations_incl_alt.clip(lower=0.0)
        df_concentrations_incl_x = df_concentrations_incl_x.mask(df_concentrations_incl_x > 1000000, 0.0)
        df_concentrations_incl_alt = df_concentrations_incl_alt.mask(df_concentrations_incl_alt > 1000000, 0.0)
        df_concentrations_mix = df_concentrations_mix.clip(lower=0.0)
        df_intensities_incl_x = df_intensities_incl_x.clip(lower=0.0)

        if show_full_df:
            if fname in ["demo_fi05.csv", "demo_fi06.csv"]:
                print("Filename:", fname)
                print("\n-- results: matrix analysis\n")
                print(df_concentrations_mat)
                print(df_sensitivity_drift/df_sensitivity_drift[ref_isotope_matrix])
                print("\n-- results: inclusion analysis")
                print("a", round(a, 5), "x", round(x, 5), "\n")
                print(df_concentrations_incl_x)
                print(df_concentrations_mix)
                print(df_sensitivity_drift)
                print(df_intensities_incl_x)
                print(df_concentrations_incl_alt)
                print(df_concentrations_incl_alt - df_concentrations_incl_x)

if __name__ == "__main__":
    run_manual_test(show_full_df=True)