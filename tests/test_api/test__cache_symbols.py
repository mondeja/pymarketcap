#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for _cache_symbols() private method"""

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function(function):
    time.sleep(3)

def test_types():
    res = pym._cache_symbols()
    assert type(res) == dict
    for key, value in res.items():
        assert type(value) == str

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
