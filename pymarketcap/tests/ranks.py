#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``ranks()`` synchronous method test module."""

from pymarketcap.tests import type_test

def assert_types(data):
    map_types = {
        "name":           str,
        "website_slug":   str,
        "symbol":         str,
        "volume_24h":     float,
        "price":          float,
        "percent_change": float,
    }
    assert isinstance(data, dict)
    for rank, rdata in data.items():
        assert isinstance(rank, str)
        assert isinstance(rdata, dict)
        for period, pdata in rdata.items():
            assert isinstance(period, str)
            assert isinstance(pdata, list)
            for currency in pdata:
                assert isinstance(currency, dict)
                for key, value in currency.items():
                    type_test(map_types, key, value)