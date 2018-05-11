#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``historical()`` shared method test module."""

from datetime import datetime

from pymarketcap.tests import type_test

def assert_types(res):
    map_types = {
        "date":       datetime,
        "open":       float,
        "high":       float,
        "low":        float,
        "close":      (float, type(None)),
        "volume":     (float, type(None)),
        "market_cap": (float, type(None)),
        "name":       str
    }

    assert isinstance(res["history"], list)
    assert isinstance(res["symbol"], str)
    assert isinstance(res["website_slug"], str)
    assert isinstance(res["name"], str)
    assert isinstance(res["id"], int)
    for tick in res["history"]:
        assert isinstance(tick, dict)
        for key, value in tick.items():
            type_test(map_types, key, value)

def assert_consistence(res):
    for i, tick in enumerate(res["history"]):
        assert len(tick.keys()) == 7  # Check number of keys
        if len(res["history"]) > 1:
            if i < len(res["history"])-1:
                assert res["history"][i+1]["date"] < tick["date"]
