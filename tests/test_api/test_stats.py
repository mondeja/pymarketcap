#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for stats() method"""

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function(function):
    time.sleep(3)

def test_types():
    res = pym.stats()
    assert type(res) == dict
    assert len(res) == 7
    for key, value in res.items():
        assert type(key) == str
        assert type(value) in (float, int)

def test_keys():
    res = pym.stats()
    target_keys = (
        "active_assets",
        "active_currencies",
        "total_24h_volume_usd",
        "bitcoin_percentage_of_market_cap",
        "active_markets",
        "total_market_cap_usd"
    )
    for key in target_keys:
        assert key in res.keys()


