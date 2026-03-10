#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		icpms_reader.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		10.03.2026

#-----------------------------------------------

"""
Module: icpms_reader.py
This module reads general and file-specific information.
"""

# PACKAGES
import re
import numpy as np
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime, timedelta

# MODULES

# CODE
ISOTOPE_PATTERN = re.compile(r"^[A-Z][a-z]?\d+$")


class ICPMSReader:
    def __init__(self, sep=","):
        self.sep = sep

    def read(self, file_path):
        """
        Read ICP-MS file and return structured content.

        Parameters
        ----------
        file_path : str or Path

        Returns
        -------
        dict
            {
                "data": pandas.DataFrame,
                "timestamp": datetime or None,
                "metadata": dict
            }
        """
        file_path = Path(file_path)
        if file_path.suffix.lower() in [".xls", ".xlsx"]:
            raise ValueError("Binary Excel files are not supported.")

        lines = self._read_lines(file_path)
        timestamp = self._extract_timestamp(lines)
        data_block = self._extract_data_block(lines)
        df = self._to_dataframe(data_block)

        return {"filename": file_path.name, "file_path": str(file_path), "data": df, "timestamp": timestamp}

    def read_many(self, file_paths):
        """
        Read multiple ICP-MS files, sort them chronologically
        and construct a relative time axis.

        Parameters
        ----------
        file_paths : list of str or Path

        Returns
        -------
        list of dict
            Each dict contains:
            {
                "file_name": str,
                "file_path": str,
                "data": pandas.DataFrame,
                "timestamp": datetime,
                "t_rel": float
            }
        """
        runs = []

        # Read all files
        for fp in file_paths:
            content = self.read(fp)
            runs.append(content)

        # Validate timestamps
        for r in runs:
            if r["timestamp"] is None:
                raise ValueError(
                    f"No timestamp found for file {r['file_name']}"
                )

        # Sort chronologically
        runs.sort(key=lambda x: x["timestamp"])
        # Build relative time axis
        t0 = runs[0]["timestamp"]
        for r in runs:
            t_rel = (r["timestamp"] - t0).total_seconds()
            r["t_rel"] = round(t_rel/60)*60

        return runs

    def _read_lines(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]

    def _extract_timestamp(self, lines, mode="end"):
        """
        Extract timestamp from header.

        Parameters
        ----------
        lines : list[str]
            File lines
        mode : str
            "start" -> Acquired timestamp
            "end"   -> Printed timestamp

        Returns
        -------
        datetime or None
        """

        if mode == "start":
            pattern = re.compile(
                r"Acquired\s*:\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})"
            )
            search_lines = lines[:30]

        elif mode == "end":
            pattern = re.compile(
                r"Printed\s*:?\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})"
            )
            search_lines = reversed(lines)

        else:
            raise ValueError("mode must be 'start' or 'end'")

        for line in search_lines:
            match = pattern.search(line)
            if match:
                date_str = match.group(1)
                time_str = match.group(2)

                timestamp = datetime.strptime(
                    f"{date_str} {time_str}",
                    "%d/%m/%Y %H:%M:%S"
                )

                #timestamp = self._round_timestamp(timestamp)

                return timestamp

        return None

    def _round_timestamp(self, ts):
        """
        Round datetime to nearest minute depending on seconds.
        """

        if ts.second >= 30:
            ts = ts + timedelta(minutes=1)

        return ts.replace(second=0, microsecond=0)

    def _is_icp_header(self, line):
        parts = line.split(self.sep)

        if len(parts) < 3:
            return False

        if not parts[0].lower().startswith(("time", "t")):
            return False

        isotope_hits = sum(
            bool(ISOTOPE_PATTERN.match(p))
            for p in parts[1:]
        )

        return isotope_hits >= 1

    def _extract_data_block(self, lines):
        for i, line in enumerate(lines):
            if self._is_icp_header(line):
                header_idx = i
                break
        else:
            raise ValueError("No ICP-MS data header found.")

        data_lines = [lines[header_idx]]

        for line in lines[header_idx + 1:]:
            parts = line.split(self.sep)
            try:
                float(parts[0])
                data_lines.append(line)
            except ValueError:
                break

        return data_lines

    def _to_dataframe(self, data_lines):
        buffer = StringIO("\n".join(data_lines))
        df = pd.read_csv(buffer, sep=self.sep, index_col=0)

        df.index = df.index.astype(float)
        df.index.name = "time_s"

        return df