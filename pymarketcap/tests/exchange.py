#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``exchange()`` shared method test module."""

def assert_types(res):
    """Type assertions for ``exchange()`` methods attribute."""
    type_tester = {
        "currency":       str,
        "pair":           str,
        "volume_24h":     [float, type(None)],
        "price":          float,
        "percent_volume": float,
        "updated":        bool,
        "name":           str,
        "slug":           str
    }
    assert isinstance(res, dict)

    assert isinstance(res["name"], str)
    assert isinstance(res["website"], str)
    assert isinstance(res["volume"], [float, type(None)])
    assert isinstance(res["social"], dict)

    for key, fields in res["social"].items():
        assert isinstance(key, str)
        for field, data in fields.items():
            assert isinstance(field, str)
            assert isinstance(data, [str, type(None)])

    for market in res["markets"]:
        assert isinstance(market, dict)
        for key, value in market.items():
            assert isinstance(value, type_tester[key])

def assert_consistence(res):
    assert len(res["name"]) > 0
    assert res["name"] != None
    assert len(res["website"]) > 0
    assert res["website"] != None
