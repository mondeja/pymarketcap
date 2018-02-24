#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for _cache_symbols() private method"""

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function(function):
    time.sleep(1)

def test_types():
    res = pym._cache_symbols_ids()
    assert type(res) == tuple
    for i, _property in enumerate(res):
        assert type(_property) == dict
        for key, value in _property.items():
            if i == 0:
                assert type(value) == str
            else:
                assert type(value) == int

def test_consistence():
    res = pym.correspondences
    for key, value in res.items():
        assert " " not in value
        for ch in key:
            try:
                assert ch.isupper() or ch.isnumeric() or ch in ["-", "$", "@"]
            except AssertionError:
                assert ch.islower()
        for ch in value:
            assert ch.islower() or ch.isnumeric() or ch in ["-"]
    for original, correct in pym.exceptional_coin_slugs.items():
        assert res[original] == correct
