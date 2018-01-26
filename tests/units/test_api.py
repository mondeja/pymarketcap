#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries:
import unittest
from decimal import Decimal
import time

# Internal modules:
from config import ConfigTest
from pymarketcap import Pymarketcap


""" ##############  API TESTS  ################ """

class TestApiCoinmarketcap(unittest.TestCase):
    """
    Tests for Coinmarketcap Api commands. These will fail in the
    absence of an internet connection or if Coinmarketcap API goes down.
    """
    def __init__(self, *args, **kwargs):
        super(TestApiCoinmarketcap, self).__init__(*args, **kwargs)
        self.coinmarketcap = Pymarketcap()
        self.config = ConfigTest()

    def tearDown(self):
        # Prevent TooManyRequestsError
        time.sleep(.25)

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

        actual = self.coinmarketcap.ticker(self.config.COIN)
        self.assertIs(type(actual), dict)

        # With param convert
        actual = self.coinmarketcap.ticker(self.config.COIN,
                                           convert="EUR")
        self.assertIs(type(actual), dict)

        actual = self.coinmarketcap.ticker("ETH",
                                           convert="CNY")
        self.assertIs(type(actual), dict)

    def test_stats(self):
        actual = self.coinmarketcap.stats()
