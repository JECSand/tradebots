"""
==========================================
TradeBots
Version: 0.0.1
Math Utility Functions
==========================================

Authors: Connor Sanders
"""

import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np


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


# Function to calculate stock's RSI
def calc_rsi(price):
    avg_gain = price[price > 0].sum() / n
    avg_loss = -price[price < 0].sum() / n
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def calc_rsi_values(candlestick_dicts, n=14):
    df = pd.DataFrame(candlestick_dicts)
    df['rsi'] = (df['close'] - df['close'].shift(1)).fillna(0)
    return pd.rolling_apply(df, n, calc_rsi)


# Function to calculate bollinger values
def calc_bollinger_values(candlestick_dicts, interval, time_scale):
    #print(candlestick_dicts)
    df = pd.DataFrame(candlestick_dicts)
    if time_scale == 'days':
        df['moving_average'] = df['close'].rolling(window=45).mean()
    else:
        num_periods = int(calc_num_periods(interval, time_scale))
        print(num_periods)
        delta = df.close.diff()
        up_days = delta.copy()
        up_days[delta <= 0] = 0.0
        down_days = abs(delta.copy())
        down_days[delta > 0] = 0.0
        RS_up = up_days.rolling(window=17).mean()
        RS_down = down_days.rolling(window=17).mean()
        df['rsi'] = 100 - 100 / (1 + RS_up / RS_down)
        df['moving_average'] = df['close'].rolling(window=200).mean()
        df['standard_deviation'] = df['close'].rolling(window=200).std()
        df['upper_band'] = df['moving_average'] + (df['standard_deviation'] * 2)
        df['lower_band'] = df['moving_average'] - (df['standard_deviation'] * 2)
        df['band_diff'] = df['upper_band'] - df['lower_band']
    df = df.set_index('time')
    #df[['close', 'moving_average', 'upper_band', 'lower_band']].plot(figsize=(24, 12))
    #plt.title('30 Day Bollinger Band Chart')
    #plt.ylabel('Price (USD)')
    #plt.show()
    return df.dropna()


# Function that calculates a
def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


# Function that calculates the derivative of a sigmoid
def sigmoid_derivative(x):
    return x * (1.0 - x)
