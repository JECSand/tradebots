"""
==========================================
TradeBots
Version: 0.0.1
Main Module
==========================================

Authors: Connor Sanders and Daniel Pivalizza
"""

from tradebots.connectors.oanda_connector import OandaConnector


# Class that creates a new Bollinger Bot
class BollingerBot(object):

    def __init__(self, trade_platform, secret_token):
        self.trade_platform = trade_platform
        self.secret_token = secret_token
        if trade_platform == 'oanda':
            self.connection = OandaConnector(secret_token)