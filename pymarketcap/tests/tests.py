#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from pymarketcap import Pymarketcap
from decimal import Decimal


""" ###########################################
    #########  TESTS CONFIGURATION  ###########
    ###########################################
"""

class ConfigTest:
    """
    Configuration for Pymarketcap tests. 
    """
    COIN = 'BTC'
    COIN_NAME = 'bitcoin'
    EXCHANGE = 'poloniex'

    def __init__(self):
        pass

config = ConfigTest()

""" ###########################################
    ##############  API TESTS  ################
    ###########################################
"""


class TestApiCoinmarketcap(unittest.TestCase):
    """
    Tests for Coinmarketcap Api commands. These will fail in the 
    absence of an internet connection or if Coinmarketcap API goes down.
    """
    def setUp(self):
        self.coinmarketcap = Pymarketcap()

    def test_symbols(self):
        actual = self.coinmarketcap.symbols
        self.assertIs(type(actual), list)
        self.assertEqual(len(actual) > 0, True)
        self.assertIs(type(actual[0]), str)
    
    def test_ticker(self):
        actual = self.coinmarketcap.ticker()
        self.assertIs(type(actual), list)
        self.assertEqual(len(actual) > 0, True)
        for tick in actual:
            self.assertIs(type(tick), dict)

        actual = self.coinmarketcap.ticker(config.COIN)
        self.assertIs(type(actual), dict)

        # With param convert
        actual = self.coinmarketcap.ticker(config.COIN, 
                                           convert="EUR")
        self.assertIs(type(actual), dict)

        actual = self.coinmarketcap.ticker("ETH", 
                                           convert="CNY")
        self.assertIs(type(actual), dict)

    def test_stats(self):
        actual = self.coinmarketcap.stats()

class TestScraperCoinmarketcap(unittest.TestCase):
    """
    Tests for Coinmarketcap Api commands. 
    These will fail in the absence of an internet 
    connection or if Coinmarketcap API goes down.
    """
    def setUp(self):
        self.coinmarketcap = Pymarketcap()

    def test_endpoints(self):
        from requests import get

        endpoints = [
            'currencies/%s/' % config.COIN_NAME,
            'gainers-losers/',
            'currencies/%s/historical-data/'\
                 % config.COIN_NAME,
            'new',
            'exchanges/%s/' % config.EXCHANGE,
            'exchanges/volume/24-hour/all/'
                    ]
        base_url = self.coinmarketcap.web_url

        for e in endpoints:
            _status_code = get(base_url + e).status_code
            self.assertEqual(_status_code, 200)

    def test_markets(self):
        actual = self.coinmarketcap.markets(config.COIN)
        value_types = {'price_usd': Decimal, 
                       '24h_volume_usd': int, 
                       'percent_volume': Decimal, 
                       'pair': str, 
                       'exchange': str}

        self.assertIs(type(actual), list)
        self.assertIs(len(actual) > 0, True)
        for source in actual:
            self.assertIs(type(source), dict)
            for key, value in source.items():
                self.assertIs(type(value), 
                              value_types[key])

    def test_ranks(self):
        temps = ['1h', '24h', '7d']
        queries = ['gainers', 'losers']
        value_types = {'percent_change': Decimal, 
                       '24h_volume_usd': int, 
                       'symbol': str, 
                       'price_usd': Decimal,
                       'name': str}

        actual = self.coinmarketcap.ranks()
        
        self.assertIs(type(actual), dict)
        for q, temp in actual.items():
            self.assertIn(q, queries)
            self.assertIs(type(temp), dict)
            for t, data in temp.items():
                self.assertIn(t, temps)
                self.assertIs(type(data), list)
                self.assertIs(len(data) > 0, True)
                for d in data:
                    self.assertIs(type(d), dict)
                    for key, value in d.items():
                        self.assertIs(type(value), 
                                      value_types[key])

        # Test invalid argument
        with self.assertRaises(AttributeError):
            self.coinmarketcap.ranks('8d')

    def test_historical(self):
        from datetime import datetime
        value_types = {'close': Decimal,
                       'low': Decimal,
                       'usd_volume': int, 
                       'open': Decimal, 
                       'usd_market_cap': int, 
                       'high': Decimal}

        actual = self.coinmarketcap.historical(config.COIN,
                                               20170624, 
                                               20170825)
        self.assertIs(type(actual), list)
        for tick in actual:
            self.assertIs(type(tick), dict)
            for date, data in tick.items():
                self.assertIs(type(date), datetime)
                for key, value in data.items():
                    self.assertIs(type(value),
                                  value_types[key])

    def test_recently(self):
        actual = self.coinmarketcap.recently()
        value_types = {'price_usd': Decimal,
                       'mineable': bool, 
                       'symbol': str, 
                       'usd_market_cap': [str, int], 
                       'circulating_supply': [str, int],
                       'volume_24h_usd': [str, int], 
                       'days_ago': [str, int], 
                       'name': str}
        self.assertIs(type(actual), list)
        for c in actual:
            self.assertIs(type(c), dict)
            for key, value in c.items():
                if type(value_types[key]) is list:
                    self.assertIn(type(value), 
                                  value_types[key])
                else:
                    self.assertIs(type(value), 
                                  value_types[key])

    def test_exchange(self):
        actual = self.coinmarketcap.exchange(config.EXCHANGE)
        value_types = {'market': str, 
                       'price_usd': Decimal,
                       'rank': int, 
                       'volume_24h_usd': int, 
                       'name': str, 
                       'perc_volume': Decimal}

        self.assertIs(type(actual), list)
        for market in actual:
            self.assertIs(type(market), dict)
            for key, value in market.items():
                self.assertIs(type(value), value_types[key])

    def test_exchanges(self):
        actual = self.coinmarketcap.exchanges()
        value_types = {'market': str, 
                       'price_usd': Decimal,
                       'rank': int, 
                       'volume_24h_usd': int, 
                       'name': str, 
                       'perc_volume': Decimal,
                       'perc_change': Decimal}

        self.assertIs(type(actual), list)
        for exch in actual:
            self.assertIs(type(exch), dict)
            for key, value in exch.items():
                if key in ('rank', 'volume_usd'):
                    self.assertIs(type(value), int)
                elif key == 'name':
                    self.assertIs(type(value), str)
                elif key == 'markets':
                    self.assertIs(type(value), list)
                    for m in value:
                        self.assertIs(type(m), dict)
                        for _key, _value in m.items():
                            self.assertIs(type(_value), 
                                          value_types[_key])
    def test_exchange_names(self):
        actual = self.coinmarketcap.exchange_names
        self.assertIs(type(actual), list)


if __name__ == '__main__':
    unittest.main()
