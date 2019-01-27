"""
==========================================
TradeBots
Version: 0.0.1
Math Utility Functions
==========================================

Authors: Connor Sanders and Daniel Pivalizza
"""

import datetime


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


# Function to calculate standard deviation


# Function to calculate moving average