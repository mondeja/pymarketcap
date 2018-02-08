#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for ticker() method"""

import time
from random import choice, randint
from math import ceil

import pytest

from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_symbols = list(pym.correspondences.keys())

def teardown_function():
    time.sleep(3)

class TypeTester:
    def _id(self, value): assert type(value) == str
    def _name(self, value): assert type(value) == str
    def _symbol(self, value):
        int_symbols = [1337, 42, 888, 808, 611, 300]
        _type = str
        if value in int_symbols:
            _type = int
        assert type(value) == _type
    def _rank(self, value): assert type(value) == int
    def _price_usd(self, value): assert type(value) in [float, type(None)]
    def _price_btc(self, value): assert type(value) in [float, type(None)]
    def _24h_volume_usd(self, value): assert type(value) in [float, type(None)]
    def _market_cap_usd(self, value): assert type(value) in [float, int, type(None)]
    def _available_supply(self, value): assert type(value) in [float, int, type(None)]
    def _total_supply(self, value): assert type(value) in [float, int, type(None)]
    def _max_supply(self, value): assert type(value) in [type(None), float, int]
    def _percent_change_1h(self, value): assert type(value) in [float, type(None)]
    def _percent_change_24h(self, value): assert type(value) in [float, type(None)]
    def _percent_change_7d(self, value): assert type(value) in [float, type(None)]
    def _last_updated(self, value): assert type(value) in [int, type(None)]

tt = TypeTester()

class TestWithoutParams:
    def test_types(self):
        res = pym.ticker()
        assert type(res) == list

        for currency in res:
            assert type(currency) == dict
            for key, value in currency.items():
                eval("tt._{}({})".format(
                    key,  # Strings need to be "quoted":
                    value if type(value) != str else '"%s"' % value
                ))

    def test_consistence(self):
        res = pym.ticker()
        assert res[0]["rank"] == 1
        assert res[-1]["rank"] == pym.total_currencies

    def teardown(self):
        time.sleep(3)

class TestWithParams:
    def test_limit(self):
        res = pym.ticker(limit=40)
        assert len(res) == 40
        assert res[0]["rank"] == 1
        res = pym.ticker(limit=385)
        assert len(res) == 385

    def test_currency(self):
        symbol = choice(all_symbols)
        res = pym.ticker(symbol)
        print("(Currency: %s)" % symbol, end=" ")

        # Test types
        assert type(res) == dict
        for key, value in res.items():
            eval("tt._{}({})".format(
                    key,  # Strings need to be 'quoted':
                    value if type(value) != str else '"%s"' % value
                ))

    def test_start(self):
        pos = randint(0, pym.total_currencies - 1)
        res = pym.ticker(start=pos)
        assert res[0]["rank"] == (pos + 1)

    @pytest.mark.skip(reason="ticker_badges property needed but not built yet")
    def test_convert(self):
        for currency in [True, False]:  # With and without currency
            symbol = None
            badge = choice(pym.ticker_badges)
            if currency:
                symbol = choice(all_symbols)
                print("(Currency: %s - Badge: %s)" % (symbol, badge), end=" | ")
            else:
                print("(Badge: %s)" % badge, end=" ")

            res = pym.ticker(currency=symbol, convert=badge)
            keys = res.keys() if currency else res[0].keys()
            badges_in_keys_count = 0
            for key in keys:
                if badge.lower() in key:
                    badges_in_keys_count += 1
            assert badges_in_keys_count == 3

    def teardown(self):
        time.sleep(3)
