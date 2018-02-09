#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for ticker() method"""

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function():
    time.sleep(1)

class TypeTester:
    def _name(self, value): assert type(value) == str
    def _symbol(self, value): assert type(value) == str
    def _days_ago(self, value): assert type(value) == int
    def _market_cap(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) == float
    def _circulating_supply(self, value): assert type(value) in [float, type(None)]
    def _volume_24h(self, value): assert type(value) in [float, int, type(None)]
    def _percent_change(self, value): assert type(value) in [float, int, type(None)]

tt = TypeTester()

def assert_types(res):
    assert hasattr(res, '__iter__') and not hasattr(res, '__len__')
    for currency in res:
        assert type(currency) == dict
        for key, value in currency.items():
            for key, value in currency.items():
                eval("tt._{}({})".format(
                    key,  # Strings need to be "quoted":
                    value if type(value) != str else '"%s"' % value
                ))

def test_types():
    assert_types(pym.recently())

def test_consistence():
    res = list(pym.recently())

    # Assert days ago in order
    for i, currency in enumerate(res):
        if i < len(res)-1:
            assert res[i+1]["days_ago"] >= currency["days_ago"]


def test_convert():
    res_btc = pym.recently(convert="BTC")

    # Test types
    assert_types(res_btc)

    # Test consistence
    res_usd = pym.recently()
    for curr_btc, curr_usd in zip(res_btc, res_usd):
        for key in curr_btc:
            assert type(curr_btc[key]) == type(curr_usd[key])
