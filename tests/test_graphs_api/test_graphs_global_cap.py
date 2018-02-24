#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
pym = Pymarketcap(cache=False)

def test_types():
    res = pym.graphs.global_cap()

    assert type(res) == dict
    for key, values in res.items():
        assert type(key) == str
        assert type(values) == list
        for timestamp, value in values:
            assert type(timestamp) == int
            assert type(value) in [float, int]

def test_consistence():
    res = pym.graphs.global_cap()
    assert len(res) == 2

    fields = list(res.keys())
    for f in ["market_cap_by_available_supply", "volume_usd"]:
        assert f in fields
