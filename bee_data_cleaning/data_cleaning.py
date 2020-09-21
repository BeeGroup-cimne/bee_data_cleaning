"""This module contains the data cleaning functions to detect the outliers and clean their data."""

import numpy as np
import pandas as pd
from warnings import warn

def _mean_outliers(series, lowq=2.5, highq=97.5):
    hh = series[(float(np.nanpercentile(series, highq)) >= series) & (float(np.nanpercentile(series, lowq)) <= series)]
    return hh.mean()


def _std_outliers(series, lowq=2.5, highq=97.5):
    hh = series[(float(np.nanpercentile(series, highq)) >= series) & (float(np.nanpercentile(series, lowq)) <= series)]
    return hh.std(ddof=0)


def _calculate_znorm(series, mode="global", lowq=2.5, highq=97.5, **kwargs):
    znorm = np.array([np.nan] * len(series))
    if len(series.value_counts(dropna=True).index) > 1:
        # Detect the z-norm outliers
        if mode not in ["rolling", "global"]:
            raise Exception("Not valid mode in detect_znorm_outliers. "
                            "Only 'rolling' or 'global' are available")
        if mode == "global":
            znorm = np.abs((series - _mean_outliers(series, lowq, highq)) / _std_outliers(series, lowq, highq))
        elif mode == "rolling":
            if 'window' in kwargs:
                mean_vals = series.rolling(center=True, window=kwargs['window'], min_periods=1).apply(
                    _mean_outliers, kwargs={'lowq': lowq, 'highq': highq})
                std_vals = series.rolling(center=True, window=kwargs['window'], min_periods=1).apply(
                    _std_outliers, kwargs={'lowq': lowq, 'highq': highq})
                znorm = np.abs((series - mean_vals) / std_vals).as_matrix()
            else:
                raise Exception("Window not specified for 'rolling' mode. Specify a window")
    return znorm


def detect_min_threshold_outliers(series, threshold):
    """Detects the values that are lower than the threshold passed
        series : series, mandatory
            The series where to detect the outliers
        threshold : integer, float, mandatory
            The threshold of the minimum value that will be considered outliers.
    """
    bool_outliers = series < threshold
    return bool_outliers


def detect_znorm_outliers(series, threshold, mode="global", **kwargs):
    """Detects the outliers usin the znorm technique.


        series : series, mandatory
            The series where to detect the outliers
        threshold : integer, float, mandatory
            The threshold of the maximum znorm value to considere as outliers.
        mode: string, mandatory
            Indicate the mode to perform the znorm outlier detection; possible values are:
            'global': considere all the series at once
            'rolling': use a window and slide it through the time series
        window: integer, only when 'rolling'
            The size of the window used when rolling
        lowq: float, default=2.5
            The lower percentile to not considere when performing the mean and std for the znorm
        highq float, default=97.5
            The higher percentile to not considere when performing the mean and std for the znorm

    """
    znorm = _calculate_znorm(series, mode, **kwargs)
    bool_outliers = (znorm > threshold)
    return bool_outliers


def detect_max_threshold_outliers(series, threshold):
    """Detects the values that are higer than the threshold passed
        series : series, mandatory
            The series where to detect the outliers
        threshold : integer, float, mandatory
            The threshold of the maximum value that will be considered outliers.
    """
    bool_outliers = series > threshold
    return bool_outliers


def detect_outliers(series, threshold, method, **kwargs):
    """Deprecated due to its complexity

            Detects all outliers with the different methods by order on the lists
            series : series, mandatory
                The series where to detect the outliers
            threshold : list of integer, float, mandatory
                The threshold of the maximum value that will be considered outliers for each method.
            threshold : list of strings, mandatory
                The threshold of the maximum value that will be considered outliers for each method.
        """
    warn("This function will be deprecated due to its complexity")
    bool_outliers = np.array([False]*len(series))
    for meth, thres in zip(method, threshold):
        if meth == 'znorm':
                bool_outliers_method = detect_znorm_outliers(series, thres, **kwargs)
        elif meth == 'max_threshold':
            bool_outliers_method = detect_max_threshold_outliers(series, thres)
        elif meth == 'min_threshold':
            bool_outliers_method = detect_min_threshold_outliers(series, thres)
        else:
            raise Exception("Specified method not implemented"
                            "Available methods are 'znorm', 'max_threshold', 'min_threshold'")
        bool_outliers = np.logical_or(bool_outliers, bool_outliers_method)
    return bool_outliers


def clean_series(series, bool_outliers):
    """Cleans the series by setting its outliers to 'NaN'

        This function should be used with the results of the the "detect_x" functions, to clean the outliers from the timeseries

        series : series, mandatory
            The series to clean
        bool_outlier : array or series, mandatory
            boolean array or series indicating the outliers as True
    """
    cleaned_series = series.copy()
    cleaned_series[bool_outliers==True] = np.nan
    return cleaned_series


def percentage_of_gaps(series):
    """Returns the percentage of nans found in the series'

        series : series, mandatory
            The series to calculate the percentage of NaN
    """
    try:
        ratio_nans = round((float(series.value_counts(dropna=False)[np.nan]) / float(len(series))) * 100.0, 2)
    except ZeroDivisionError:
        ratio_nans = 0.0

    return ratio_nans


def summary(series, **kwargs):
    """Returns information about the timeseries passed
        "dateStart", "dateEnd", "frequency", "mean", "sd", "min", "max", "p1",
        "p5", "p25", "p50", "p75", "p95", "p99"
        series : series, mandatory
            The series to get the information
        """
    dict_return = {
        "dateStart": min(series.index),
        "dateEnd": max(series.index),
        "frequency": (pd.Series(series.index[1:]) - pd.Series(series.index[:-1])).value_counts().index[0],
        "mean": np.nanmean(np.array(series)),
        "sd": np.nanstd(np.array(series)),
        "min": np.nanmin(np.array(series)),
        "max": np.nanmax(np.array(series)),
        "p1": np.nanpercentile(np.array(series), 1, interpolation='linear'),
        "p5": np.nanpercentile(np.array(series), 5, interpolation='linear'),
        "p25": np.nanpercentile(np.array(series), 25, interpolation='linear'),
        "p50": np.nanpercentile(np.array(series), 50, interpolation='linear'),
        "p75": np.nanpercentile(np.array(series), 75, interpolation='linear'),
        "p95": np.nanpercentile(np.array(series), 95, interpolation='linear'),
        "p99": np.nanpercentile(np.array(series), 99, interpolation='linear')
    }
    dict_return.update(kwargs)