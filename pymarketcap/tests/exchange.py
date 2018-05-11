#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``exchange()`` shared method test module."""

from pymarketcap.tests import type_test

def assert_types(res):
    """Type assertions for ``exchange()`` methods attribute."""
    map_types = {
        "currency":       str,
        "pair":           str,
        "volume_24h":     (float, type(None)),
        "price":          float,
        "percent_volume": float,
        "updated":        bool,
        "name":           str,
        "slug":           str
    }
    assert isinstance(res, dict)

    assert isinstance(res["name"], str)
    assert isinstance(res["website_slug"], str)
    assert isinstance(res["id"], int)
    assert isinstance(res["volume"], (float, type(None)))
    assert isinstance(res["social"], dict)

    for key, fields in res["social"].items():
        assert isinstance(key, str)
        for field, data in fields.items():
            assert isinstance(field, str)
            assert isinstance(data, (str, type(None)))

    for market in res["markets"]:
        assert isinstance(market, dict)
        for key, value in market.items():
            type_test(map_types, key, value)

def assert_consistence(res):
    assert res["name"] # len(res["name"]) > 0
    assert res["name"] != None
