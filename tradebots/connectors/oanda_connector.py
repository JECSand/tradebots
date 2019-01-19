"""
==========================================
TradeBots
Version: 0.0.1
Oanda Connector Module
==========================================

Authors: Connor Sanders and Daniel Pivalizza
"""


# Class that instantiates a new Oanda Connection
class OandaConnector(object):

    def __init__(self, secret_token):
        self.secret_token = secret_token