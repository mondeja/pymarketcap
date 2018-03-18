#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for ticker() method"""

from time import sleep
from random import choice, randint

from pymarketcap.tests import type_test
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function():
    sleep(1)

def assert_types(res):
    map_types = {
        "id":                   str,
        "name":                 str,
        "symbol":               str,
        "rank":                 int,
        "price_usd":            (float, type(None)),
        "price_btc":            (float, type(None)),
        "24h_volume_usd":        (float, type(None)),
        "market_cap_usd":       (float, int, type(None)),
        "available_supply":     (float, int, type(None)),
        "total_supply":         (float, int, type(None)),
        "max_supply":           (float, int, type(None)),
        "percent_change_1h":    (float, type(None)),
        "percent_change_24h":   (float, type(None)),
        "percent_change_7d":    (float, type(None)),
        "last_updated":         (int, type(None))
    }
    assert isinstance(res, (list, dict))

    for key, value in res.items():
        if key in map_types:
            type_test(map_types, key, value)
        else:
            assert isinstance(value, (float, int, type(None)))


def test_consistence():
    res = pym.ticker()
    assert res[0]["rank"] == 1
    assert res[-1]["rank"] == pym.total_currencies

def test_limit():
    res = pym.ticker(limit=40)
    assert len(res) == 40
    assert res[0]["rank"] == 1
    res = pym.ticker(limit=385)
    assert len(res) == 385

def test_name():
    symbol = choice(pym.symbols)
    res = pym.ticker(symbol)
    print("(Symbol: %s)" % symbol, end=" ")

    assert_types(res)

def test_start():
    pos = randint(0, pym.total_currencies - 1)
    res = pym.ticker(start=pos)
    assert res[0]["rank"] == (pos + 1)

def test_convert():
    for currency in [True, False]:  # With and without currency
        symbol = None
        badge = choice(pym.ticker_badges)
        if currency:
            symbol = choice(pym.symbols)
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

        if currency:
            assert_types(res)
