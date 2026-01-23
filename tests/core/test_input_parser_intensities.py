#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		test_input_parser_intensities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: test_input_parser_intensities.py
This file tests if the input parse of the module DataReductionIntensities is working as exptected.
"""

# PACKAGES
import re
import pytest
from pathlib import Path

# MODULES
from pysills.core.intensities.datareduction_intensities import DataReductionIntensities as DRI

# CODE
DIRECTORY_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("filename", [
    "demo_ma01.csv",
    "another_demo_file.xl",
])
def test_intensity_parsing(filename):
    demo_file_path = (DIRECTORY_ROOT/"src"/"pysills"/"legacy"/"lib"/"demo_files"/filename)

    parser = DRI()
    df = parser.read_input_data(demo_file_path)

    assert not df.empty
    assert df.index.name == "time_s"
    assert df.index.dtype.kind in ("f", "i")
    assert df.shape[1] > 1
    assert all(re.fullmatch(r"[A-Z][a-z]?\d+", c) for c in df.columns)
    assert df.index.is_monotonic_increasing


@pytest.mark.parametrize("filename", [
    "demo_ma01.csv",
    "another_demo_file.xl",
])
def test_prepare_for_reduction(filename):
    demo_file_path = (
        DIRECTORY_ROOT / "src" / "pysills" / "legacy" / "lib" / "demo_files" / filename
    )

    parser = DRI()
    df = parser.read_input_data(demo_file_path)
    df_ready = parser.prepare_for_reduction(df)

    assert "time_s" in df_ready.columns
    assert df_ready.index.dtype.kind == "i"
    assert df_ready["time_s"].dtype.kind in ("f", "i")
    assert df_ready.shape[1] > 2

    isotope_cols = df_ready.columns.drop("time_s")
    assert all(re.fullmatch(r"[A-Z][a-z]?\d+", c) for c in isotope_cols)
