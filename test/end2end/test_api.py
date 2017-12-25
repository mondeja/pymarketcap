#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries:
import unittest
from decimal import Decimal
from tqdm import tqdm
from time import time

# Internal modules:
from pymarketcap import Pymarketcap
from pymarketcap import CoinmarketcapCurrencyNotFoundError

from pprint import pprint


class TestApiCoinmarketcapFull(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiCoinmarketcapFull, self).__init__(*args, **kwargs)
        self.coinmarketcap = Pymarketcap()

    def test_ticker(self):
        start = int(time())
        currencies_not_found = []

        value_types = {
            "id": str,
            "name": str,
            "symbol": str,
            "rank": self.coinmarketcap.parse_int,
            "price_usd": self.coinmarketcap.parse_float,
            "price_btc": self.coinmarketcap.parse_float,
            "24h_volume_usd": [self.coinmarketcap.parse_float, type(None)],
            "market_cap_usd": [self.coinmarketcap.parse_float, type(None)], # Some currencies
            "available_supply": [self.coinmarketcap.parse_float, type(None)], # haven"t got
            "total_supply": [self.coinmarketcap.parse_float, type(None)],  # all data available
            "max_supply": [self.coinmarketcap.parse_float, type(None)],
            "percent_change_1h": [self.coinmarketcap.parse_float, type(None)],
            "percent_change_24h": [self.coinmarketcap.parse_float, type(None)],
            "percent_change_7d": [self.coinmarketcap.parse_float, type(None)],
            "last_updated": self.coinmarketcap.parse_int
        }


        for symbol in tqdm(self.coinmarketcap.symbols):
            try:
                tick = self.coinmarketcap.ticker(symbol)
                for key, value in tick.items():
                    print(key, value)
                    if type(value_types[key]) is list:
                        self.assertIn(type(value), value_types[key])
                    else:
                        self.assertIs(type(value), value_types[key])
            except CoinmarketcapCurrencyNotFoundError as error:  # Currency not found?
                currencies_not_found.append(                  # Notify me with all
                	{error.currency: error.url}
                )

        # Display all currencies not found
        print("\nCurrencies not found:")
        pprint(currencies_not_found)

        self.assertEqual(len(currencies_not_found), 0)

        end = time()
        elapsed = end - start

