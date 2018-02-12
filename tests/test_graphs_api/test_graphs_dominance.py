#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap(cache=False)

def teardown_function(function):
    time.sleep(1)

def test_types():
    res = pym.graphs.dominance()

    assert type(res) == dict
    for key, values in res.items():
        assert type(key) == str
        assert type(values) == list
        for timestamp, value in values:
            assert type(timestamp) == int
            assert type(value) in [float, int]

def test_consistence():
    res = pym.graphs.dominance()

    fields = list(res.keys())
    assert "others" in fields

