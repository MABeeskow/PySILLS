#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

# Name:		data_reduction.py
# Author:	Maximilian A. Beeskow
# Version:	pre-release
# Date:		04.08.2023

#-----------------------------------------------------------------------------------------------------------------------

## MODULES -------------------------------------------------------------------------------------------------------------
import pandas as pd

## CLASSES -------------------------------------------------------------------------------------------------------------
class DataExtraction:
    def __init__(self, filename_long=None):
        self.filename_long = filename_long

    def get_measurements(self, delimiter, skip_header, skip_footer):
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.skip_footer = skip_footer

        dataframe = pd.read_csv(
            self.filename_long, sep=self.delimiter, header=self.skip_header, skipfooter=self.skip_footer,
            engine="python")
        dataframe_blank = dataframe.loc[dataframe.isnull().all(1)]
        if len(dataframe_blank) > 0:
            first_blank_index = dataframe_blank.index[0]
            dataframe = dataframe[:first_blank_index]

        return dataframe

    def get_isotopes(self, dataframe):
        list_names = list(dataframe.columns.values)
        list_names.pop(0)
        list_isotopes = list_names

        return list_isotopes

    def get_times(self, dataframe):
        df_times = dataframe.iloc[:, 0]

        return df_times

class IntensityQuantification:
    def __init__(self, dataframe, internal_standard=None, mode="specific"):
        self.dataframe = dataframe
        self.internal_standard = internal_standard
        self.mode = mode

    def get_intensity(self, interval_bg, interval_min, interval_incl=None):
        if self.mode == "specific":
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

    def get_intensity_ratio(self, isotope):
        if self.mode == "specific":
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Background

            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

class SensitivityQuantification:
    def __init__(self, internal_standard, mode="specific"):
        self.internal_standard = internal_standard
        self.mode = mode

    def get_analytical_sensitivity(self):
        if self.mode == "specific":
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

    def get_normalized_sensitivity(self):
        if self.mode == "specific":
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

    def get_relative_sensitivity_factor(self):
        if self.mode == "specific":
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass
        else:
            # Mineral/Matrix Signal

            # Inclusion Signal
            pass

class CompositionQuantification:
    def __init__(self, internal_standard, mode="specific"):
        self.internal_standard = internal_standard
        self.mode = mode

    def get_composition(self):
        if self.mode == "specific":
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass
        else:
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass

    def get_composition_ratio(self):
        if self.mode == "specific":
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass
        else:
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass

    def get_limit_of_detection(self):
        if self.mode == "specific":
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass
        else:
            # Mineral/Matrix Analysis

            # Fluid Inclusion Analysis

            # Melt Inclusion Analysis
            pass

## TESTING -------------------------------------------------------------------------------------------------------------