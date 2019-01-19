"""
==========================================
TradeBots
Version: 0.0.1
Alpaca Connector Module
==========================================

Authors: Connor Sanders and Daniel Pivalizza
"""

import sys


# Class that instantiates a new Alpaca Connection
class AlpacaConnector(object):

    # Initialize an Alpaca Connection
    def __init__(self, secret_token, symbol):

        # Function that checks if token is valid
        def check_token(secret_token):
            if secret_token:
                # Write code here
                return secret_token
            print('Token is not recognized by Alpaca')
            sys.exit(1)

        # Function that check if symbol is valid upon bot instantiation
        def check_symbol(symbol):
            if symbol:
                # Write code here
                return symbol
            print('Alpaca Connector does not recognize the symbol, ' + str(symbol))
            sys.exit(1)

        self.secret_token = check_token(secret_token)
        self.symbol = check_symbol(symbol)

    # Public Method that returns a dictionary of current candle stick values
    def current_candle_sticks(self):
        pass

    # Public Method that returns a dictionary of current bollinger band values
    def bollinger_bands(self):
        pass

    # Public Method that executes an open trade order
    def open_trade(self):
        pass

    # Public Method that executes a close trade order
    def close_trade(self):
        pass
