#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		spike_elimination.py
# Author:	Maximilian A. Beeskow
# Version:	v1.0.64
# Date:		07.02.2025

#-----------------------------------------------

## MODULES
import numpy as np
import scipy.stats as stats
from math import sqrt
from collections import defaultdict
import pandas as pd

## CLASSES
class OutlierDetection:
    def __init__(self, raw_data, alpha, threshold, isotope, dataset_complete):
        self.raw_data = raw_data
        self.alpha = alpha
        self.threshold = threshold
        self.smoothed_data = []
        self.spike_indices = []
        self.isotope = isotope
        self.dataset_complete = dataset_complete

    def calculate_whisker_statistcs(self, helper_values, init=True):
        helper_dataset = helper_values
        val_quartile_first = np.quantile(helper_dataset, 0.25)
        val_quartile_third = np.quantile(helper_dataset, 0.75)
        val_iqr = val_quartile_third - val_quartile_first
        factor = abs(self.alpha + 1)
        val_lower_limit = val_quartile_first - factor*val_iqr
        val_upper_limit = val_quartile_third + factor*val_iqr

        if init == True:
            lower_outliers = [index for index, value in enumerate(helper_dataset) if value < val_lower_limit and
                              value > self.threshold]
            upper_outliers = [index for index, value in enumerate(helper_dataset) if value > val_upper_limit and
                              value > self.threshold]

            outlier_indices = lower_outliers
            outlier_indices.extend(upper_outliers)
            outlier_indices.sort()
        else:
            value_poi = helper_dataset[0]
            print(helper_dataset, helper_dataset[0:])
            val_mean = np.mean(helper_dataset[0:])
            values_sp = helper_dataset[0:]

    def find_outlier(self):
        val_quartile_first = np.quantile(self.dataset_complete, 0.25)
        val_quartile_third = np.quantile(self.dataset_complete, 0.75)
        val_iqr = val_quartile_third - val_quartile_first
        factor = abs(self.alpha + 1)
        val_lower_limit = val_quartile_first - factor*val_iqr
        val_upper_limit = val_quartile_third + factor*val_iqr

        lower_outliers = [index for index, value in enumerate(self.dataset_complete) if value < val_lower_limit and
                          value > self.threshold]
        upper_outliers = [index for index, value in enumerate(self.dataset_complete) if value > val_upper_limit and
                          value > self.threshold]

        data_smoothed = self.dataset_complete.copy()
        outlier_indices = lower_outliers
        outlier_indices.extend(upper_outliers)
        outlier_indices.sort()

        for index in outlier_indices:
            helper_values = self.determine_surrounded_values(var_index=index, stepsize=4)

            if index in lower_outliers:
                corrected_value = np.mean(helper_values["SP"])
            elif index in upper_outliers:
                corrected_value = np.mean(helper_values["SP"])

            data_smoothed[index] = corrected_value

        return data_smoothed, outlier_indices
    def determine_surrounded_values(self, var_index, stepsize=3):
        # POI   - Point Of Interest
        # SP    - Surrounding Points
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.dataset_complete[var_index]
        helper_values["POI"] = val_poi
        helper_values["All"].append(val_poi)

        for step in range(1, stepsize):
            step_before = var_index - step
            step_after = var_index + step
            if step_before >= 0:
                helper_values["SP"].append(self.dataset_complete[step_before])
                helper_values["All"].append(self.dataset_complete[step_before])
            if step_after < len(self.dataset_complete):
                helper_values["SP"].append(self.dataset_complete[step_after])
                helper_values["All"].append(self.dataset_complete[step_after])

        return helper_values

    def extract_surrounding_values(self, index_spike, steps):
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.dataset_complete[index_spike]
        helper_values["POI"] = val_poi

        index_start = max(0, index_spike - steps)
        index_end = min(len(self.dataset_complete), index_spike + (steps + 1))

        helper_values["All"].append(self.dataset_complete[index_start:index_end])
        helper_values["SP"].append((self.dataset_complete[index_start:index_spike] +
                                    self.dataset_complete[index_spike + 1:index_end]))

        return helper_values

    def calculate_grubbs_critical_value(self, size):
        t_dist = stats.t.ppf(1 - self.alpha/(2*size), size - 2)
        numerator = (size - 1)*np.sqrt(np.square(t_dist))
        denominator = np.sqrt(size)*np.sqrt(size - 2 + np.square(t_dist))
        critical_value = numerator/denominator

        return critical_value

class GrubbsTestSILLS:
    def __init__(self, raw_data, alpha, threshold, start_index, dataset_complete):
        self.raw_data = raw_data
        self.alpha = alpha
        self.threshold = threshold
        #self.val_check_7 = 2.097
        #self.val_check_9 = 2.323
        self.smoothed_data = []
        self.spike_indices = []
        self.start_index = start_index
        self.dataset_complete = dataset_complete

    def calculate_grubbs_critical(self, N, alpha=0.01):
        df = N - 2
        t_val = stats.t.ppf(1 - (alpha/(2*N)), df)
        grubbs_val = (N - 1)/(N**0.5)*((t_val**2)/(df + t_val**2))**0.5
        return grubbs_val

    def outlier_elimination_zsore(self): # outlier_elimination_zsore
        data = self.raw_data
        z_scores = np.abs(stats.zscore(data))
        zscore_threshold = 2
        helper_data = {}

        for index, value in enumerate(self.raw_data):
            if value > self.threshold:
                if z_scores[index] > zscore_threshold:
                    self.spike_indices.append(index + self.start_index)
                    surrounding_6 = self.extract_surrounding_values(index_spike=index, steps=4)
                    mean_5 = np.mean(surrounding_6["SP"])
                    helper_data[index + self.start_index] = mean_5

        for index, value in enumerate(self.dataset_complete):
            if index in self.spike_indices:
                self.smoothed_data.append(helper_data[index])
            else:
                self.smoothed_data.append(value)

        return self.smoothed_data, self.spike_indices

    def determine_outlier(self):
        N_low = 7
        N_high = 9
        G_comp_7 = round(self.calculate_grubbs_critical(N=N_low), 3)
        G_comp_9 = round(self.calculate_grubbs_critical(N=N_high), 3)
        helper_data = {}

        for index, value in enumerate(self.raw_data):
            if value > self.threshold:
                surrounding_7 = self.extract_surrounding_values(index_spike=index, steps=N_low)
                surrounding_9 = self.extract_surrounding_values(index_spike=index, steps=N_high)

                mean_6 = np.mean(surrounding_7["SP"])
                mean_7 = np.mean(surrounding_7["All"])
                std_7 = np.std(surrounding_7["All"], ddof=1)
                mean_9 = np.mean(surrounding_9["All"])
                std_9 = np.std(surrounding_9["All"], ddof=1)

                if np.abs(value - mean_7)/std_7 > G_comp_7 and np.abs(value - mean_9)/std_9 > G_comp_9:
                    val_corr = mean_6
                    self.spike_indices.append(index + self.start_index)
                    helper_data[index + self.start_index] = val_corr

        for index, value in enumerate(self.dataset_complete):
            if index in self.spike_indices:
                self.smoothed_data.append(helper_data[index])
            else:
                self.smoothed_data.append(value)

        return self.smoothed_data, self.spike_indices

    def determine_outlier2(self):
        helper_data = {}
        for index, value in enumerate(self.raw_data):
            if value >= self.threshold:
                surrounding_3 = self.determine_surrounded_values(index=index, stepsize=3)
                surrounding_4 = self.determine_surrounded_values(index=index, stepsize=4)

                mean_3 = np.mean(surrounding_3["All"])
                std_3 = np.std(surrounding_3["All"], ddof=1)
                mean_4 = np.mean(surrounding_4["All"])
                std_4 = np.std(surrounding_4["All"], ddof=1)

                if std_3 > 0:
                    val_poi_3 = round(abs(value - mean_3)/std_3, 3)
                else:
                    val_poi_3 = np.nan

                if std_4 > 0:
                    val_poi_4 = round(abs(value - mean_4)/std_4, 3)
                else:
                    val_poi_4 = np.nan

                val_crit_3 = round(self.calculate_grubbs_critical_value(size=len(surrounding_3["All"])), 3)
                val_crit_4 = round(self.calculate_grubbs_critical_value(size=len(surrounding_4["All"])), 3)

                if val_poi_3 > val_crit_3 and val_poi_4 > val_crit_4:
                    val_corr = np.mean(surrounding_3["SP"])
                    self.spike_indices.append(index + self.start_index)
                    helper_data[index + self.start_index] = val_corr

        for index, value in enumerate(self.dataset_complete):
            if index in self.spike_indices:
                self.smoothed_data.append(helper_data[index])
            else:
                self.smoothed_data.append(value)

        return self.smoothed_data, self.spike_indices

    def extract_surrounding_values(self, index_spike, steps):
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.dataset_complete[index_spike]
        helper_values["POI"] = val_poi

        index_start = max(0, index_spike - steps)
        index_end = min(len(self.dataset_complete), index_spike + (steps + 1))

        helper_values["All"].append(self.dataset_complete[index_start:index_end])
        helper_values["SP"].append((self.dataset_complete[index_start:index_spike] +
                                    self.dataset_complete[index_spike + 1:index_end]))

        return helper_values

    def determine_surrounded_values(self, index, stepsize=4):
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.raw_data[index]
        helper_values["POI"] = val_poi
        helper_values["All"].append(val_poi)

        for step in range(1, stepsize):
            step_before = index - step
            step_after = index + step
            if step_before >= 0:
                helper_values["SP"].append(self.raw_data[step_before])
                helper_values["All"].append(self.raw_data[step_before])
            if step_after < len(self.raw_data):
                helper_values["SP"].append(self.raw_data[step_after])
                helper_values["All"].append(self.raw_data[step_after])

        return helper_values

    def calculate_grubbs_critical_value(self, size):
        t_dist = stats.t.ppf(1 - self.alpha/(2*size), size - 2)
        numerator = (size - 1)*np.sqrt(np.square(t_dist))
        denominator = np.sqrt(size)*np.sqrt(size - 2 + np.square(t_dist))
        critical_value = numerator/denominator

        return critical_value

class GrubbsTest:
    def __init__(self, raw_data, alpha, threshold, start_index, dataset_complete):
        self.raw_data = raw_data
        self.alpha = alpha
        self.threshold = threshold
        self.smoothed_data = []
        self.spike_indices = []
        self.start_index = start_index
        self.dataset_complete = dataset_complete

    def determine_outlier(self):
        helper_data = {}
        for index, value in enumerate(self.raw_data):
            if value >= self.threshold:
                surrounding_3 = self.determine_surrounded_values(index=index, stepsize=3)
                surrounding_4 = self.determine_surrounded_values(index=index, stepsize=4)
                val_poi_3, index_poi_3 = self.calculate_grubbs_value()
                val_poi_3 = round(val_poi_3, 3)
                val_crit_3 = round(self.calculate_grubbs_critical_value(size=len(surrounding_3["All"])), 3)
                val_poi_4, index_poi_4 = self.calculate_grubbs_value()
                val_poi_4 = round(val_poi_4, 3)
                val_crit_4 = round(self.calculate_grubbs_critical_value(size=len(surrounding_4["All"])), 3)

                if val_poi_3 > val_crit_3 and val_poi_4 > val_crit_4:
                    val_corr = np.mean(surrounding_3["SP"])
                    self.spike_indices.append(index + self.start_index)
                    helper_data[index + self.start_index] = val_corr

        for index, value in enumerate(self.dataset_complete):
            if index in self.spike_indices:
                self.smoothed_data.append(helper_data[index])
            else:
                self.smoothed_data.append(value)

        return self.smoothed_data, self.spike_indices

    def determine_surrounded_values(self, index, stepsize=4):
        helper_values = {"POI": 0, "SP": [], "All": []}
        val_poi = self.raw_data[index]
        helper_values["POI"] = val_poi
        helper_values["All"].append(val_poi)

        for step in range(1, stepsize):
            step_before = index - step
            step_after = index + step
            if step_before >= 0:
                helper_values["SP"].append(self.raw_data[step_before])
                helper_values["All"].append(self.raw_data[step_before])
            if step_after < len(self.raw_data):
                helper_values["SP"].append(self.raw_data[step_after])
                helper_values["All"].append(self.raw_data[step_after])

        return helper_values

    def calculate_grubbs_critical_value(self, size):
        t_dist = stats.t.ppf(1 - self.alpha/(2*size), size - 2)
        numerator = (size - 1)*np.sqrt(np.square(t_dist))
        denominator = np.sqrt(size)*np.sqrt(size - 2 + np.square(t_dist))
        critical_value = numerator/denominator

        return critical_value

    def calculate_grubbs_value(self):
        std_dev = np.std(self.raw_data, ddof=1)
        avg_y = np.mean(self.raw_data)
        abs_val_minus_avg = abs(np.array(self.raw_data) - avg_y)
        max_of_deviations = max(abs_val_minus_avg)
        max_ind = np.argmax(abs_val_minus_avg)
        Gcal = max_of_deviations/std_dev

        return Gcal, max_ind


__all__ = ['two_sided_test_indices',
           'two_sided_test_outliers',
           'TwoSidedGrubbsTest',
           'OutputType']


DEFAULT_ALPHA = 0.95


# Test output types
class OutputType:
    DATA = 0  # Output data without outliers
    OUTLIERS = 1  # Output outliers
    INDICES = 2  # Output outlier indices


class GrubbsTestAlternative(object):
    def __init__(self, data):
        self.original_data = data

    def _copy_data(self):
        if isinstance(self.original_data, np.ndarray):
            return self.original_data
        elif pd is not None and isinstance(self.original_data, pd.Series):
            return self.original_data
        elif isinstance(self.original_data, list):
            return np.array(self.original_data)
        else:
            raise TypeError('Unsupported data format')

    def _delete_item(self, data, index):
        if pd is not None and isinstance(data, pd.Series):
            return data.drop(index)
        elif isinstance(data, np.ndarray):
            return np.delete(data, index)
        else:
            raise TypeError('Unsupported data format')

    def _get_indices(self, values):
        last_seen = defaultdict(lambda: 0)
        data = list(self.original_data)
        indices = list()
        for value in values:
            start = last_seen[value]
            index = data.index(value, start)
            indices.append(index)
            last_seen[value] = index + 1
        return indices

    def _get_g_test(self, data, alpha):
        """Compute a significant value score following these steps, being alpha
        the requested significance level:

        1. Find the upper critical value of the t-distribution with n-2
           degrees of freedom and a significance level of alpha/2n
           (for two-sided tests) or alpha/n (for one-sided tests).

        2. Use this t value to find the score with the following formula:
           ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))

        :param numpy.array data: data set
        :param float alpha: significance level
        :return: G_test score
        """
        n = len(data)
        significance_level = self._get_t_significance_level(alpha, n)
        t = stats.t.isf(significance_level, n-2)
        return ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))

    def _test_once(self, data, alpha):
        """Perform one iteration of the Smirnov-Grubbs test.

        :param numpy.array data: data set
        :param float alpha: significance level
        :return: the index of the outlier if one if found; None otherwise
        """
        target_index, value = self._target(data)
        var_std = data.std()
        if var_std > 0:
            g = value/var_std
        else:
            g = 0
        g_test = self._get_g_test(data, alpha)
        return target_index if g > g_test else None

    def run(self, alpha=DEFAULT_ALPHA, output_type=OutputType.DATA):
        """Run the Smirnov-Grubbs test to remove outliers in the given data set.

        :param float alpha: significance level
        :param int output_type: test output type (from OutputType class values)
        :return: depending on the value of output_type, the data set without
        outliers (DATA), the outliers themselves (OUTLIERS) or the indices of
        the outliers in the original data set (INDICES)
        """
        data = self._copy_data()
        outliers = list()

        while True:
            outlier_index = self._test_once(data, alpha)
            if outlier_index is None:
                break
            outlier = data[outlier_index]
            outliers.append(outlier)
            data = self._delete_item(data, outlier_index)

        return_value = data
        if output_type == OutputType.OUTLIERS:
            return_value = outliers
        elif output_type == OutputType.INDICES:
            return_value = self._get_indices(outliers)
        return return_value

    def _target(self, data):
        raise NotImplementedError

    def _get_t_significance_level(self, alpha):
        raise NotImplementedError

class TwoSidedGrubbsTest(GrubbsTestAlternative):
    def _target(self, data):
        """Compute the index of the farthest value from the sample mean and its
        distance.

        :param numpy.array data: data set
        :return int, float: the index of the element and its distance to the
        mean
        """
        relative_values = abs(data - data.mean())
        index = relative_values.argmax()
        value = relative_values[index]
        return index, value

    def _get_t_significance_level(self, alpha, n):
        return alpha/(2*n)

def _test(test_class, data, alpha, output_type):
    return test_class(data).run(alpha, output_type=output_type)

def _two_sided_test(data, alpha, output_type):
    return _test(TwoSidedGrubbsTest, data, alpha, output_type)

def two_sided_test_indices(data, alpha=DEFAULT_ALPHA):
    #alpha = 1 - alpha
    return _two_sided_test(data, alpha, OutputType.INDICES)

def two_sided_test_outliers(data, alpha=DEFAULT_ALPHA):
    return _two_sided_test(data, alpha, OutputType.OUTLIERS)