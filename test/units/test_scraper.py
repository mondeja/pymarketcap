#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries:
import unittest
from decimal import Decimal

# Internal modules:
from config import ConfigTest
from pymarketcap import Pymarketcap


""" ############  SCRAPER TESTS  ############## """

class TestScraperCoinmarketcap(unittest.TestCase):
    """
    Tests for Coinmarketcap Api commands.
    These will fail in the absence of an internet
    connection or if coinmarketcap.com goes down.
    """
    def __init__(self, *args, **kwargs):
        super(TestScraperCoinmarketcap, self).__init__(*args, **kwargs)
        self.coinmarketcap = Pymarketcap()
        self.config = ConfigTest()

    def test_endpoints(self):
        from requests import get

        endpoints = [
            'currencies/%s/' % self.config.COIN_NAME,
            'gainers-losers/',
            'currencies/%s/historical-data/'\
                 % self.config.COIN_NAME,
            'new',
            'exchanges/%s/' % self.config.EXCHANGE,
            'exchanges/volume/24-hour/all/'
                    ]
        base_url = self.coinmarketcap.web_url

        for e in endpoints:
            _status_code = get(base_url + e).status_code
            self.assertEqual(_status_code, 200)

    def test_markets(self):
        actual = self.coinmarketcap.markets(self.config.COIN)
        value_types = {'price_usd': Decimal,
                       '24h_volume_usd': int,
                       'percent_volume': Decimal,
                       'pair': str,
                       'exchange': str,
                       'updated': bool}

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
                       'high': Decimal,
                       'date': datetime}

        actual = self.coinmarketcap.historical(self.config.COIN,
                                               datetime(2017, 9, 30),
                                               datetime(2017, 10, 10))
        self.assertIs(type(actual), list)
        for tick in actual:
            self.assertIs(type(tick), dict)
            for key, value in tick.items():
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
                       'name': str,
                       }
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
        actual = self.coinmarketcap.exchange(self.config.EXCHANGE)
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

    def _assert_graphs_data_structure(self, data):
        self.assertIs(type(data), dict)

        for key, value in data.items():
            self.assertIs(type(value), list)
            for timestamp in value:
                self.assertIs(type(timestamp), list)
                for _value in timestamp:
                    self.assertIn(type(_value), (float, int))

    def test_graphs_currency(self):
        actual = self.coinmarketcap.graphs.currency(self.config.COIN)
        self._assert_graphs_data_structure(actual)

    def test_graphs_global_cap(self):
        actual = self.coinmarketcap.graphs.global_cap(bitcoin=True)
        self._assert_graphs_data_structure(actual)

    def test_graphs_dominance(self):
        actual = self.coinmarketcap.graphs.dominance()
        self._assert_graphs_data_structure(actual)