"""
==========================================
TradeBots
Version: 0.0.1
DateTime Utility Functions
==========================================

Authors: Connor Sanders
"""
import datetime


# Function to calculate datetime map
def generate_dt_range_map(num_of_requests, seconds_per_request, end_dt, start_dt):
    date_time_ranges = []
    i = 0
    cur_start = start_dt
    while i < num_of_requests:
        cur_end = cur_start + datetime.timedelta(0, seconds_per_request)
        i += 1
        if i < num_of_requests:
            cur_time_range_list = [cur_start, cur_end]
        else:
            cur_time_range_list = [cur_start, end_dt]
        date_time_ranges.append(cur_time_range_list)
        cur_start = cur_end + datetime.timedelta(0, int(seconds_per_request / 3000))
    return date_time_ranges
