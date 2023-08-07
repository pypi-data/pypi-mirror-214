"""
Date and time conversions for time-series data.

This module is dedicated to providing reliable conversions between common time-series data representations.
It offers functions that transform {py:class}`pandas.DatetimeIndex` objects into sample times or intervals expressed in
seconds and vice versa.
"""

from datetime import datetime, timedelta
from typing import Union

import numpy as np
import pandas as pd
from pandas import DatetimeIndex

from optool.math import is_monotonic
from optool.uom import UNITS, Quantity


def datetime_index_to_samples(timestamps: DatetimeIndex) -> Quantity:
    """
    Converts a {py:class}`~pandas.DatetimeIndex` to a {py:data}`~optool.uom.Quantity` object representing the sample
    times in seconds.

    :param timestamps: The absolute, monotonic increasing timestamps.
    :return: A quantity object with the sample times in seconds since the first timestamp.
    :raises ValueError: If the timestamps are not {py:attr}`~pandas.Index.is_monotonic_increasing`.
    """
    if not timestamps.is_monotonic_increasing:
        raise ValueError("The timestamps must be monotonic increasing.")
    duration = (timestamps - timestamps[0]).to_pytimedelta()
    sample_times_seconds = np.array([val.total_seconds() for val in duration])
    return Quantity(sample_times_seconds, UNITS.second)


def datetime_index_to_intervals(timestamps: DatetimeIndex) -> Quantity:
    """
    Converts a {py:class}`~pandas.DatetimeIndex` to a {py:data}`~optool.uom.Quantity` object representing the intervals
    between timestamps in seconds.

    :param timestamps: The absolute, monotonic increasing  timestamps.
    :return: A Quantity object with the intervals between the timestamps in seconds.
    :raises ValueError: If the timestamps are not {py:attr}`~pandas.Index.is_monotonic_increasing`.
    """
    if not timestamps.is_monotonic_increasing:
        raise ValueError("The timestamps must be monotonic increasing.")
    intervals_seconds = np.diff(timestamps.astype(np.int64)) / 10**9
    return Quantity(intervals_seconds, UNITS.second)


def samples_to_datetime_index(start: datetime, sample_times: Quantity) -> DatetimeIndex:
    """
    Converts a {py:data}`~optool.uom.Quantity` object representing sample times into a {py:class}`~pandas.DatetimeIndex`
    object.

    :param start: The starting date and time.
    :param sample_times: A quantity object with the sample times in seconds since the start time.
    :return: The absolute timestamps.
    :raises ValueError: If the sample times are not monotonic increasing.
    """
    if not is_monotonic(sample_times, 'ascending', strict=False):
        raise ValueError("The sample times must be monotonic increasing.")
    sample_times_seconds = sample_times.m_as(UNITS.second)
    duration = [timedelta(0, float(second)) for second in sample_times_seconds]
    datetime_values = [start + val for val in duration]
    return pd.DatetimeIndex(datetime_values)


def any_to_intervals(time: Union[Quantity, DatetimeIndex]) -> Quantity:
    """
    Converts a given time input to time intervals.

    - If the input is a {py:class}`~pandas.DatetimeIndex`, time intervals are obtained via
      {py:func}`~datetime_index_to_intervals`.

    - If the input is a {py:class}`~optool.uom.Quantity` and is monotonically increasing, the intervals are simply the
      discrete difference.

    - Otherwise, the input is assumed to be already the time intervals and a copy of the input is returned.

    :param time: The time input to be converted to intervals. It can either be absolute timestamps, time steps, or time
        intervals.
    :return: The intervals derived from the input time.
    :raises ValueError: If the input is a {py:class}`~pandas.DatetimeIndex` but it is not monotonically increasing, or
        the input is not compatible with time, or the magnitude is not a one-dimensional {py:class}`~numpy.ndarray`.
    """
    if isinstance(time, DatetimeIndex):
        return datetime_index_to_intervals(time)
    if not time.is_compatible_with('s'):
        raise ValueError(f"The time array must be compatible with time, but has units {time.u!r}.")
    if not isinstance(time.m, np.ndarray):
        raise ValueError(f"Time must have a magnitude that is a Numpy array, but has type {type(time.m)}.")
    if np.ndim(time.m) != 1:
        raise ValueError(f"Time must have a magnitude that is a one-dimensional array, but have shape {time.m.shape}.")
    if is_monotonic(time, 'ascending', strict=False):
        return Quantity(np.diff(time.m), time.u)
    return time.copy()
