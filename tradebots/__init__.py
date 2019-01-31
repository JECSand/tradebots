"""
==========================================
TradeBots
Version: 0.0.1
Main Module
==========================================

Authors: Connor Sanders
"""

import numpy as np
from tradebots.connectors.oanda_connector import OandaConnector
from tradebots.connectors.alpaca_connector import AlpacaConnector
from tradebots.neutralnetworks.neural_network import NeuralNetwork


# Class that creates a new Bollinger Bot
class BollingerBot(object):

    def __init__(self, trade_platform, secret_token, account_id, symbol, practice=True):
        self.trade_platform = trade_platform
        self.secret_token = secret_token
        self.account_id = account_id
        self.symbol = symbol
        self.practice = practice
        if trade_platform == 'oanda':
            self.connection = OandaConnector(self.secret_token, self.account_id, self.symbol, self.practice)
        elif trade_platform == 'alpaca':
            self.connection = AlpacaConnector(self.secret_token, self.symbol)

    def current_price(self):
        return self.connection.current_pricing_data()

    def candle_sticks(self, price=None, granularity=None, start=None, end=None, smoothed=None, count=None):
        return self.connection.historical_candle_sticks(price, granularity, start, end, smoothed, count)

    def bollinger_bands(self, granularity, current=True, start=None, end=None):
        return self.connection.bollinger_band_data(granularity, current, start, end)

    def train_bot(self, granularity):
        bollinger_band_data = self.bollinger_bands(granularity)
        #print(bollinger_band_data)
        data_array = bollinger_band_data.values.T.tolist()
        data_array2 = bollinger_band_data.values.tolist()

        #print(data_array)
        #data_matrix = [list(l) for l in zip(*bollinger_band_data.values)]
        check_data_inputs = []
        i = 0
        for data in data_array2:
            cur_list = [data[1], data[4], data[5], data[6], data[7], data[8], data[9], data[10]]
            #print(cur_list)
            check_data_inputs.append(cur_list)
        # all variables except dates and prices
        # All close prices
        result_data = []
        for res_data in data_array[1]:
            result_data.append([res_data])
        data_results = np.array(result_data)
        data_inputs = np.array(check_data_inputs)
        print(data_results)
        print(data_inputs)
        nn = NeuralNetwork(data_inputs, data_results)
        for c in range(1500):
            nn.feedforward()
            nn.backprop()
        print(nn.output)
        return nn
