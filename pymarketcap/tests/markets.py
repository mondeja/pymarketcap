#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``markets()`` synchronous method test module."""

from pymarketcap.tests import type_test

def assert_types(res):
    map_types = {
        "source":         str,
        "pair":           str,
        "volume_24h":     float,
        "price":          float,
        "percent_volume": float,
        "updated":        bool,
        "markets":        list,
        "symbol":         str,
        "website_slug":   str,
        "id":             int
    }

    for source in res["markets"]:
        assert isinstance(source, dict)
        for key, value in source.items():
            type_test(map_types, key, value)

def assert_consistence(res):
    for source in res["markets"]:
        assert len(source.keys()) == 6
        assert source["pair"].count("/") == 1
        assert source["percent_volume"] <= 100
