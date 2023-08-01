#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

# Name:		data_reduction.py
# Author:	Maximilian A. Beeskow
# Version:	pre-release
# Date:		01.08.2023

#-----------------------------------------------------------------------------------------------------------------------

## MODULES -------------------------------------------------------------------------------------------------------------
import pandas as pd

## CLASSES -------------------------------------------------------------------------------------------------------------
class DataExtraction:
    def __init__(self, filename_long):
        self.filename_long = filename_long

    def get_measurements(self, delimiter, skip_header, skip_footer):
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.skip_footer = skip_footer

        df_complete = pd.read_csv(
            self.filename_long, sep=self.delimiter, header=self.skip_header, skipfooter=self.skip_footer,
            engine="python")

        return df_complete

    def get_isotopes(self, dataframe):
        list_names = list(dataframe.columns.values)
        list_names.pop(0)
        list_isotopes = list_names

        return list_isotopes

    def get_times(self, dataframe):
        df_times = dataframe.iloc[:, 0]

        return df_times

class IntensityQuantification:
    def __init__(self, internal_standard):
        self.internal_standard = internal_standard

    def get_intensity(self):
        # Background

        # Matrix Signal

        # Inclusion Signal
        pass

    def get_intensity_ratio(self, internal_standard):
        pass

class SensitivityQuantification:
    def __init__(self, internal_standard):
        self.internal_standard = internal_standard

    def get_analytical_sensitivity(self):
        pass

    def get_normalized_sensitivity(self):
        pass

    def get_relative_sensitivity_factor(self):
        pass

class CompositionQuantification:
    def __init__(self, internal_standard):
        self.internal_standard = internal_standard

    def get_composition(self):
        # Mineral Analysis / Matrix Analysis

        # Fluid Inclusion Analysis

        # Melt Inclusion Analysis
        pass

    def get_composition_ratio(self):
        pass

    def get_limit_of_detection(self):
        pass

## TESTING -------------------------------------------------------------------------------------------------------------