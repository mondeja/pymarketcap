#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for ticker() method"""

from pymarketcap.tests import type_test
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def assert_types(res):
    map_types = {
        "name":               str,
        "symbol":             str,
        "added":              str,
        "market_cap":         (float, type(None)),
        "price":              float,
        "circulating_supply": (float, type(None)),
        "volume_24h":         (float, type(None)),
        "percent_change":     (float, type(None)),
    }

    assert isinstance(res, list)
    assert len(res) > 0
    for currency in res:
        assert isinstance(currency, dict)
        for key, value in currency.items():
                type_test(map_types, key, value)

def test_types():
    res = pym.recently()
    assert_types(res)

def test_convert():
    res_btc = pym.recently(convert="BTC")

    # Test types
    assert_types(res_btc)

    # Test consistence
    res_usd = pym.recently()
    for curr_btc, curr_usd in zip(res_btc, res_usd):
        for key in curr_btc:
            assert type(curr_btc[key]) == type(curr_usd[key])
