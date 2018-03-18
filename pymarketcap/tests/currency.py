#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``currency()`` shared method test module."""

def assert_types(res):
    type_tester = {
        "symbol":                   str,
        "slug":                     str,
        "source_code":              [str, type(None)],
        "announcement":             [str, type(None)],
        "explorers":                list,
        "total_markets_volume_24h": [float, type(None)],
        "price":                    [float, type(None)],
        "rank":                     list,
        "total_markets_cap":        [float, type(None)],
        "chats":                    list,
        "message_boards":           list,
        "circulating_supply":       [float, type(None)],
        "total_supply":             [float, type(None)],
        "max_supply":               [float, type(None)],
        "mineable":                 bool,
        "webs":                     list,
        "name":                     str
    }
    assert isinstance(res, dict)
    for key, value in res.items():
        assert isinstance(value, type_tester[key])

def assert_consistence(res):
    keys = list(res.keys())
    assert len(keys) in list(range(14, 17))
    assert "symbol" in keys
    assert "slug" in keys
