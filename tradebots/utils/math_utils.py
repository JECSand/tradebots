"""
==========================================
TradeBots
Version: 0.0.1
Math Utility Functions
==========================================

Authors: Connor Sanders
"""

import json
import pandas as pd


# Base Interval Mapping Dict
base_interval_scales_mapping = {
    "seconds": 0,
    "minutes": 60,
    "hours": 3600,
    "days": 86400,
    "weeks": 604800,
    "months": 2629800,
    "years": 31556926
}


# Function to calculate the scaled interval factor
def calc_scaled_interval_factor(interval, scale):
    base_scalar = base_interval_scales_mapping[scale]
    if base_scalar == 0:
        return int(interval)
    else:
        return base_scalar * int(interval)


# Function to calculate number of expected observations
def calc_num_of_observations(start, end, interval, scale):
    duration = end - start
    scaled_interval = calc_scaled_interval_factor(interval, scale)
    duration_in_s = duration.total_seconds()
    return [int(divmod(duration_in_s, scaled_interval)[0]), scaled_interval]


# Function to calculate bollinger values
def calc_bollinger_values(candlestick_dicts):
    df = pd.DataFrame(candlestick_dicts)
    df = df.set_index('time')
    return df


# Function to calculate moving average