"""
==========================================
TradeBots
Version: 0.0.1
Math Utility Functions
==========================================

Authors: Connor Sanders
"""

import matplotlib.pyplot as plt
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


# Function to calculate number of periods in 20 day span
def calc_num_periods(interval, scale):
    base_scalar = base_interval_scales_mapping[scale]
    day_seconds = base_interval_scales_mapping['days']
    if base_scalar == 0:
        return (day_seconds / int(interval)) * 20
    else:
        return (day_seconds / (base_scalar * int(interval))) * 20


# Function to calculate number of expected observations
def calc_num_of_observations(start, end, interval, scale):
    duration = end - start
    scaled_interval = calc_scaled_interval_factor(interval, scale)
    duration_in_s = duration.total_seconds()
    return [int(divmod(duration_in_s, scaled_interval)[0]), scaled_interval]


# Function to calculate bollinger values
def calc_bollinger_values(candlestick_dicts, interval, time_scale):
    print(candlestick_dicts)
    df = pd.DataFrame(candlestick_dicts)
    if time_scale == 'days':
        df['moving_average'] = df['close'].rolling(window=22).mean()
    else:
        num_periods = int(calc_num_periods(interval, time_scale))
        print(num_periods)
        df['moving_average'] = df['close'].rolling(window=100).mean()
        df['standard_deviation'] = df['close'].rolling(window=100).std()
        df['upper_band'] = df['moving_average'] + (df['standard_deviation'] * 2)
        df['lower_band'] = df['moving_average'] - (df['standard_deviation'] * 2)
    df = df.set_index('time')
    df[['close', 'moving_average', 'upper_band', 'lower_band']].plot(figsize=(24, 12))
    plt.title('30 Day Bollinger Band for Facebook')
    plt.ylabel('Price (USD)')
    plt.show()
    #return df
