#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``tokens()`` synchronous method test module."""

from pymarketcap.tests import type_test

def assert_types(data):
    map_types = {
        "name":               str,
        "symbol":             str,
        "platform":           (str, type(None)),
        "market_cap":         (float, type(None)),
        "price":              (float, type(None)),
        "circulating_supply": (float, type(None)),
        "volume_24h":         (float, type(None))
    }
    for currency in data:
        for key, value in currency.items():
            type_test(map_types, key, value)
