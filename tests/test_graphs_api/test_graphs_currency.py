#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from random import choice

from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_symbols = list(pym.correspondences.keys())

def teardown_function(function):
    time.sleep(1)

def test_types():
    symbol = choice(all_symbols)
    res = pym.graphs.currency(symbol)
    print("(Currency: %s)" % symbol, end=" ")

    for field, values in res.items():
        assert type(field) == str
        assert type(values) == list
        for timestamp, value in values:
            assert type(timestamp) == int
            assert type(value) in [float, int]

def test_consistence():
    symbol = choice(all_symbols)
    res = pym.graphs.currency(symbol)
    print("(Currency: %s)" % symbol, end=" ")

    assert len(res) in [4, 5]

    fields = [
        "market_cap_by_available_supply",
        "price_btc",
        "price_usd",
        "volume_usd",
        "price_platform",
     ]

    for field, values in res.items():
        assert field in fields
        for timestamp, value in values:
            assert str(timestamp)[-3:] == "000"

