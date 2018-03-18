#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``historical()`` shared method test module."""

from datetime import datetime

def assert_types(res):
    type_tester = {
        "date":       datetime,
        "open":       float,
        "high":       float,
        "low":        float,
        "close":      [float, type(None)],
        "volume":     [float, type(None)],
        "market_cap": [float, type(None)],
        "name":       str
    }

    assert isinstance(res["history"], list)
    assert isinstance(res["symbol"], str)
    assert isinstance(res["slug"], str)
    for tick in res["history"]:
        assert isinstance(tick, dict)
        for key, value in tick.items():
            assert isinstance(value, type_tester[key])

def assert_consistence(res):
    for i, tick in enumerate(res["history"]):
        assert len(tick.keys()) == 7  # Check number of keys
        if len(res["history"]) > 1:
            if i < len(res["history"])-1:
                assert res["history"][i+1]["date"] < tick["date"]
