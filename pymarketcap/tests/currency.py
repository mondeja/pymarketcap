#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``currency()`` shared method test module."""

from pymarketcap.tests import type_test

def assert_types(res):
    map_types = {
        "symbol":             str,
        "slug":               str,
        "source_code":        (str, type(None)),
        "announcement":       (str, type(None)),
        "explorers":          list,
        "markets_volume_24h": (float, type(None)),
        "price":              (float, type(None)),
        "rank":               (int, type(None)),
        "markets_cap":        (float, type(None)),
        "chats":              list,
        "message_boards":     list,
        "circulating_supply": (float, type(None)),
        "total_supply":       (float, type(None)),
        "max_supply":         (float, type(None)),
        "mineable":           bool,
        "webs":               list,
        "name":               str
    }
    assert isinstance(res, dict)
    for key, value in res.items():
        type_test(map_types, key, value)

def assert_consistence(res):
    keys = list(res.keys())
    assert len(keys) in list(range(14, 17))
    assert "symbol" in keys
    assert "slug" in keys
