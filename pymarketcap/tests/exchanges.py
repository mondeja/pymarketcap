#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``exchanges()`` shared method test module."""

from pymarketcap.tests import type_test

def assert_types(res):
    map_types = {
        "name":           str,
        "web":            str,
        "pair":           str,
        "volume":         (float, type(None)),
        "price":          float,
        "percent_volume": float
    }

    assert isinstance(res, list)
    for exc in res:
        assert isinstance(exc, dict)
        assert isinstance(exc["name"], str)
        assert isinstance(exc["markets"], list)
        for market in exc["markets"]:
            for key, value in market.items():
                type_test(map_types, key, value)
