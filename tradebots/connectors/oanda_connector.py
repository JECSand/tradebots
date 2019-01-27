"""
==========================================
TradeBots
Version: 0.0.1
Oanda Connector Module
==========================================

Authors: Connor Sanders
"""

import sys
import json
import datetime
import tradebots.utils.request_utils as request_utils
import tradebots.utils.math_utils as math_utils
import tradebots.utils.datetime_utils as datetime_utils


# Oanda Scale Mapping
time_scaling_map = {
    'S': 'seconds',
    'M': 'minutes',
    'H': 'hours',
    'D': 'days',
    'W': 'weeks',
    'M1': 'months'
}


# Class that instantiates a new Oanda Connection
class OandaConnector(object):

    # Initialize an Oanda Connection Object
    def __init__(self, secret_token, account_id, symbol, practice):

        # Function that checks if token is valid
        def check_settings(check_account_id, base_url, base_headers, check_type, check_symbol=None):
            if check_type == 'accounts':
                get_url = base_url + '/v3/accounts'
                check_key = 'id'
                check_param = check_account_id
            else:
                get_url = base_url + '/v3/accounts/' + check_account_id + '/instruments'
                check_key = 'name'
                check_param = check_symbol
            try:
                get_req = request_utils.get_request(get_url, base_headers)
                if get_req.code != 200:
                    print('setup error: Token is not recognized by Oanda')
                    sys.exit(1)
                else:
                    res_list = json.loads(get_req.read().decode('utf8')).get(check_type, None)
                    if res_list is not None and len(res_list) > 0:
                        for res_obj in res_list:
                            if res_obj.get(check_key, None) == check_param:
                                return res_obj
                    print(str(check_type) + ' setup error: ' + str(check_param) + ' is not recognized by Oanda')
                    sys.exit(1)
            except:
                print('setup error: Token is not recognized by Oanda')
                sys.exit(1)

        # Object Initialization Variables
        self.practice = practice
        self.base_headers = {"Authorization": 'Bearer ' + str(secret_token)}
        if practice is True:
            self.base_url = 'https://api-fxpractice.oanda.com'
            self.base_streaming_url = 'https://stream-fxpractice.oanda.com/'
        else:
            self.base_url = 'https://api-fxtrade.oanda.com'
            self.base_streaming_url = 'https://stream-fxtrade.oanda.com/'
        self.account_id = account_id
        self.secret_token = secret_token
        check_settings(self.account_id, self.base_url, self.base_headers, 'accounts')
        self.symbol = symbol.replace('/', '_')
        self.symbol_dict = check_settings(self.account_id, self.base_url, self.base_headers, 'instruments', self.symbol)
        self.granularity_meta = {''}

    # Private Static Method to generate historical candle stick req URL
    @staticmethod
    def _generate_candle_stick_url(base_get_url, price, granularity, start, end, smoothed, count):
        i = 0
        if price is not None:
            base_get_url += '?price=' + str(price)
            i += 1
        if granularity is not None:
            if i == 0:
                base_get_url += '?granularity=' + str(granularity)
            else:
                base_get_url += '&granularity=' + str(granularity)
            i += 1
        if count is not None:
            if i == 0:
                base_get_url += '?count=' + str(count)
            else:
                base_get_url += '&count=' + str(count)
            i += 1
        if start is not None:
            if i == 0:
                base_get_url += '?from=' + str(start).replace(':', '%3A')
            else:
                base_get_url += '&from=' + str(start).replace(':', '%3A')
            i += 1
        if end is not None:
            base_get_url += '&to=' + str(end).replace(':', '%3A')
        if smoothed is not None:
            if i == 0:
                base_get_url += '?smoothed=' + str(smoothed)
            else:
                base_get_url += '&smoothed=' + str(smoothed)
        return base_get_url

    # Public Method that returns a dictionary of historical candle stick values
    def historical_candle_sticks(self, price=None, granularity=None, start=None, end=None, smoothed=None, count=None):
        start_dt = datetime.datetime.strptime(start.split('.')[0] + 'Z', '%Y-%m-%dT%H:%M:%SZ')
        end_dt = datetime.datetime.strptime(end.split('.')[0] + 'Z', '%Y-%m-%dT%H:%M:%SZ')
        scale = "".join([i for i in granularity if i.isalpha()])
        interval = "".join([i for i in granularity if i.isdigit()])
        time_scale = time_scaling_map[scale]
        num_observations_data = math_utils.calc_num_of_observations(start_dt, end_dt, interval, time_scale)
        num_observations = num_observations_data[0]
        scaled_interval = num_observations_data[1]
        seconds_per_request = int(scaled_interval * 3000)
        num_of_requests = int(num_observations / 3000)
        date_ranges_list = datetime_utils.generate_dt_range_map(num_of_requests, seconds_per_request, end_dt, start_dt)
        base_get_url = self.base_url + '/v3/instruments/' + self.symbol + '/candles'
        appended_re_candle_data = []
        re_data = {}
        for datetime_list in date_ranges_list:
            c_start = datetime_list[0].isoformat("T") + "Z"
            c_end = datetime_list[1].isoformat("T") + "Z"
            get_url = self._generate_candle_stick_url(base_get_url, price, granularity, c_start, c_end, smoothed, count)
            try:
                get_req = request_utils.get_request(get_url, self.base_headers)
                if get_req:
                    if get_req.code != 200:
                        appended_re_candle_data.append({c_start + ' to ' + c_end: False})
                    else:
                        re_data = json.loads((get_req.read().decode('utf8')))
                        if len(appended_re_candle_data) > 0:
                            appended_re_candle_data += re_data['candles']
                        else:
                            appended_re_candle_data = re_data['candles']
            except:
                appended_re_candle_data.append({c_start + ' to ' + c_end: None})
        re_data['candles'] = appended_re_candle_data
        return re_data

    # Public Method that returns a dictionary of current pricing data
    def current_pricing_data(self):
        get_url = self.base_url + '/v3/accounts/' + self.account_id + '/pricing?instruments=' + self.symbol
        try:
            get_req = request_utils.get_request(get_url, self.base_headers)
            if get_req.code != 200:
                return False
            return json.loads(get_req.read())
        except:
            return False

    # Private Method that formats returned candle stick pricing data
    def _format_candle_stick_data(self, raw_candle_sticks, price='mid'):
        raw_candle_stick_prices = raw_candle_sticks['candles']
        candle_stick_prices = []
        for raw_candle_stick in raw_candle_stick_prices:
            formated_candle_stick_obj = {
                'volume': float(raw_candle_stick['volume']),
                'time': raw_candle_stick['time'],
                'high': float(raw_candle_stick[price].get('h', None)),
                'close': float(raw_candle_stick[price].get('c', None)),
                'open': float(raw_candle_stick[price].get('o', None)),
                'low': float(raw_candle_stick[price].get('l', None)),
            }
            candle_stick_prices.append(formated_candle_stick_obj)
        raw_candle_sticks.update({'candles': candle_stick_prices})
        return raw_candle_sticks

    # Public Method that returns a dictionary of current bollinger band values
    def bollinger_band_data(self, granularity, current=True, start=None, end=None):
        if current is True:
            # get last 20 days worth of candle stick data for submitted granularity; if less than M10, run multiple pulls
            end_dt = datetime.datetime.utcnow()
            start_dt = end_dt - datetime.timedelta(days=22)
            end = end_dt.isoformat("T") + "Z"
            start = start_dt.isoformat("T") + "Z"
            raw_candle_sticks = self.historical_candle_sticks(None, granularity, start, end)
            candle_sticks = self._format_candle_stick_data(raw_candle_sticks)
            #TODO Calculate Bollinger Bands
            return math_utils.calc_bollinger_values(candle_sticks['candles'])
        else:
            pass
        pass

    # Public Method that executes an open trade order
    def open_trade(self):
        pass

    # Public Method that executes a close trade order
    def close_trade(self):
        pass
