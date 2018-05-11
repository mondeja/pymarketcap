#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for stats() method"""

from pymarketcap.tests import type_test
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def assert_types(res, convert=None):
    map_types = {
        "active_cryptocurrencies":          int,
        "active_markets":                   int,
        "bitcoin_percentage_of_market_cap": float,
        "quotes":                           dict,
        "last_updated":                     int,
    }
    quotes_map_types = {
        "total_market_cap": float,
        "total_volume_24h": float
    }

    assert isinstance(res, dict)
    for key, value in res.items():
        type_test(map_types, key, value)

    for key, value in res["quotes"]["USD"].items():
        type_test(quotes_map_types, key, value)

    if convert:
        for key, value in res["quotes"][convert].items():
            type_test(quotes_map_types, key, value)

def test_types():
    res = pym.stats()["data"]
    assert_types(res)

def assert_consistence(res):
    assert len(res) == 5

def test_consistence():
    res = pym.stats()["data"]
    assert_consistence(res)

def test_convert():
    fiat_curr = "EUR"
    res = pym.stats(convert=fiat_curr)["data"]
    assert_types(res, convert=fiat_curr)
    assert_consistence(res)
