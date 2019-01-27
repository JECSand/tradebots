"""
==========================================
TradeBots
Version: 0.0.1
Connectors Test Module
==========================================

Authors: Connor Sanders
"""

from tradebots import BollingerBot


# Test Connection here
api_token = 'YOURTOKENHERE'
acct_id = 'YOURACCOUNTHERE'
symb = 'EUR_USD'
new_bollinger_bot = BollingerBot('oanda', api_token, acct_id, symb)


def check_candle_sticks():
    print('candle stick dict')
    candle_sticks_dict = new_bollinger_bot.candle_sticks(price='B', start='2019-01-03T21:48:55.000000000Z',
                                                         granularity='M10', end='2019-01-23T21:59:55.000000000Z')
    candle_sticks = candle_sticks_dict['candles']
    i = 0
    for candle_stick in candle_sticks:
        i += 1
        print(i)
        print(candle_stick.get('time', None))


def check_bollinger_bands():
    print('bollinger band check')
    granularity = 'S30'
    bolinger_bands = new_bollinger_bot.bollinger_bands(granularity)
    print(bolinger_bands)


check_bollinger_bands()