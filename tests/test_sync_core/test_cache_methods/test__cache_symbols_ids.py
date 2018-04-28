#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for _cache_symbols() private method"""

from pymarketcap import Pymarketcap
from pymarketcap.consts import EXCEPTIONAL_COIN_SLUGS
pym = Pymarketcap()

def test_types():
    res = pym._cache_symbols_ids()
    assert isinstance(res, tuple)
    assert len(res) > 0
    for i, _property in enumerate(res):
        assert isinstance(_property, dict)
        for key, value in _property.items():
            if i == 0:
                assert isinstance(value, str)
            else:
                assert isinstance(value, int)

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
    for original, correct in EXCEPTIONAL_COIN_SLUGS.items():
        assert res[original] == correct
