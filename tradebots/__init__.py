"""
==========================================
TradeBots
Version: 0.0.1
Main Module
==========================================

Authors: Connor Sanders
"""

from tradebots.connectors.oanda_connector import OandaConnector
from tradebots.connectors.alpaca_connector import AlpacaConnector


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