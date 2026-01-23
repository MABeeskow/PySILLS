#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		datareduction_intensities.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		23.01.2026

#-----------------------------------------------

"""
Module: datareduction_intensities.py
This module performs the data reduction of the LA-ICP-MS signal intensity input data.
"""

# PACKAGES
import re
import numpy as np
import pandas as pd
from io import StringIO
from pathlib import Path

# MODULES

# CODE
ISOTOPE_PATTERN = re.compile(r"^[A-Z][a-z]?\d+$")


def _read_raw_lines(file_path):
    """Read non-empty lines from a text-based input file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def _is_icp_header(line, sep=","):
    """Check whether a line represents a valid ICP-MS data header."""
    parts = line.split(sep)

    if len(parts) < 3:
        return False
    if not parts[0].lower().startswith(("time", "t")):
        return False

    isotope_hits = sum(bool(ISOTOPE_PATTERN.match(p)) for p in parts[1:])

    return isotope_hits >= 1


def _extract_data_block(lines, sep=","):
    """Extract the contiguous ICP-MS data block starting from the header line."""
    for i, line in enumerate(lines):
        if _is_icp_header(line, sep):
            header_idx = i
            break
    else:
        raise ValueError("Kein ICP-MS Datenheader gefunden")

    data_lines = [lines[header_idx]]  # Header
    for line in lines[header_idx + 1:]:
        parts = line.split(sep)
        try:
            float(parts[0])
            data_lines.append(line)
        except ValueError:
            break  # Datenblock endet

    return data_lines


def _to_dataframe(data_lines, sep=","):
    """Convert extracted data lines into a pandas DataFrame."""
    buffer = StringIO("\n".join(data_lines))
    return pd.read_csv(buffer, sep=sep, index_col=0)

def _count_points(intervals):
    return sum(e - s + 1 for s, e in intervals)

class DataReductionIntensities:
    def __init__(self, sep=",", time_s="time_s"):
        """
        Initialize the intensity data reduction handler.

        Parameters
        ----------
        sep : str, optional
            Column separator used in input files.
        time_s : str, optional
            Name of the time column used in reduction-ready data.
        """
        self.sep = sep
        self.time_s = time_s

    def read_input_data(self, file_path):
        """
        Parse a raw LA-ICP-MS input file and return the signal intensity data.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Path to a text-based ICP-MS data file.

        Returns
        -------
        pandas.DataFrame
            Parsed intensity data with time as index and isotopes as columns.

        Raises
        ------
        ValueError
            If a binary Excel file is provided or no valid data block is found.
        """
        suffix = Path(file_path).suffix.lower()
        if suffix in [".xls", ".xlsx"]:
            raise ValueError("Binary Excel files are not supported by this parser")

        lines = _read_raw_lines(file_path)
        data_block = _extract_data_block(lines, sep=self.sep)
        df = _to_dataframe(data_block, sep=self.sep)
        df.index = df.index.astype(float)
        df.index.name = self.time_s

        return df

    def prepare_for_reduction(self, df):
        """
        Prepare a parsed intensity DataFrame for index-based data reduction.

        This converts the time index into an explicit column and resets the
        DataFrame index to a RangeIndex for optimal performance.

        Parameters
        ----------
        df : pandas.DataFrame
            Parsed intensity DataFrame with time as index.

        Returns
        -------
        pandas.DataFrame
            Reduction-ready DataFrame with a RangeIndex and a 'time_s' column.
        """
        df_ready = df.copy()
        # Assign time data
        df_ready.insert(0, self.time_s, df.index.to_numpy())
        df_ready.reset_index(drop=True, inplace=True)
        # Assign data types
        df_ready[self.time_s] = df_ready[self.time_s].astype(float)
        df_ready.iloc[:, 1:] = df_ready.iloc[:, 1:].astype(float)

        return df_ready

    def reduce_intervals(self, df_ready, intervals, statistics=("mean", "std")):
        """
        Reduce signal intensities over one or multiple index-based intervals.

        Parameters
        ----------
        df_ready : pandas.DataFrame
            Reduction-ready DataFrame with a RangeIndex and a time column
            (e.g. 'time_s') followed by isotopic intensity columns.
        intervals : list of tuple[int, int]
            List of inclusive index intervals [(start, end), ...].
            All intervals are merged into a single data block prior to reduction.
        statistics : tuple of {"mean", "std", "sum", "median"}, optional
            Statistics to compute for the merged data block.
            Default is ("mean", "std"), where standard deviation is calculated
            with ddof=1.

        Returns
        -------
        pandas.Series
            Reduced intensities for each isotope, indexed by isotope name.

        Raises
        ------
        ValueError
            If no intervals are provided, intervals are invalid,
            or the statistic is unsupported.
        """
        if not intervals:
            raise ValueError("No intervals provided")

        funcs = {
            "mean": np.nanmean,
            "sum": np.nansum,
            "median": np.nanmedian,
            "std": lambda x, axis=0: np.nanstd(x, axis=axis, ddof=1),
        }

        for stat in statistics:
            if stat not in funcs:
                raise ValueError(f"Unknown statistic: {stat}")

        values = df_ready.iloc[:, 1:].to_numpy()
        blocks = [values[s:e + 1] for s, e in intervals]
        data = np.vstack(blocks)
        result = {stat: funcs[stat](data, axis=0) for stat in statistics}

        return {stat: pd.Series(vals, index=df_ready.columns[1:]) for stat, vals in result.items()}

    def find_index_for_time(self, df_ready, time_value):
        """
        Find the index corresponding to the closest time value to the given time.

        Parameters
        ----------
        df_ready : pandas.DataFrame
            Reduction-ready DataFrame containing a time column.
        time_value : float
            Target time (in seconds).

        Returns
        -------
        int
            Index of the closest time approx. equal to time_value.

        Raises
        ------
        ValueError
            If the time_value is outside the available time range.
        """
        times = df_ready["time_s"].to_numpy()

        idx = np.searchsorted(times, time_value)

        if idx == 0:
            return 0
        if idx == len(times):
            return len(times) - 1

        before = idx - 1
        after = idx

        if abs(times[after] - time_value) < abs(times[before] - time_value):
            return after
        else:
            return before

    def subtract_background(self, signal, background):
        """
        Subtract background intensities from signal intensities.

        Parameters
        ----------
        signal : pandas.Series
            Mean signal intensities per isotope.
        background : pandas.Series
            Mean background intensities per isotope.

        Returns
        -------
        pandas.Series
            Background-corrected signal intensities per isotope.
        """
        if not signal.index.equals(background.index):
            raise ValueError("Signal and background isotopes do not match")

        return signal - background

    def propagate_background_uncertainty(self, signal_std, background_std):
        """
        Propagate uncertainties for background-corrected signal intensities.

        Parameters
        ----------
        signal_std : pandas.Series
            Standard deviation of the signal intensities per isotope.
        background_std : pandas.Series
            Standard deviation of the background intensities per isotope.

        Returns
        -------
        pandas.Series
            Propagated standard deviation of background-corrected intensities.
        """
        if not signal_std.index.equals(background_std.index):
            raise ValueError("Signal and background isotopes do not match")

        return np.sqrt(signal_std**2 + background_std**2)

    def compute_standard_error(self, std, intervals):
        """
        Compute the standard error of the mean.

        Parameters
        ----------
        std : pandas.Series
            Standard deviation per isotope.
        intervals : list of tuple[int, int]
            List of inclusive index intervals [(start, end), ...].
            All intervals are merged into a single data block prior to reduction.

        Returns
        -------
        pandas.Series
            Standard error per isotope.
        """
        n = _count_points(intervals=intervals)
        if n <= 0:
            raise ValueError("n must be positive")

        return std/np.sqrt(n)

    def compute_rsd(self, mean, std, percent=True):
        """
        Compute relative standard deviation (RSD).

        Parameters
        ----------
        mean : pandas.Series
            Mean intensity per isotope.
        std : pandas.Series
            Standard deviation per isotope.
        percent : bool, optional
            If True, return RSD in percent.

        Returns
        -------
        pandas.Series
            Relative standard deviation.
        """
        rsd = std/mean
        if percent:
            rsd *= 100.0
        return rsd

    def compute_intensity_ratios(self, intensities, reference_isotope):
        """
        Compute intensity ratios I_x / I_ref.

        Parameters
        ----------
        intensities : pandas.Series
            Background-corrected mean intensities indexed by isotope.
        reference_isotope : str
            Isotope used as reference (e.g. 'Si29').

        Returns
        -------
        pandas.Series
            Intensity ratios indexed by isotope.
        """
        if reference_isotope not in intensities.index:
            raise ValueError(f"Reference isotope '{reference_isotope}' not found")

        i_ref = intensities.loc[reference_isotope]

        if i_ref <= 0:
            raise ValueError("Reference intensity must be positive")

        ratios = intensities/i_ref
        ratios.name = f"I/I_{reference_isotope}"

        return ratios