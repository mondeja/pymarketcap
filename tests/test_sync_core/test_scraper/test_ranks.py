#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap.tests import type_test
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def assert_types(data):
    map_types = {
        "name":           str,
        "slug":           str,
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

def test_types():
    res = pym.ranks()
    assert_types(res)

def test_consistence():
    res = pym.ranks()

    # Check if a currency is repeated
    for rank, rdata in res.items():
        assert rank in ["gainers", "losers"]
        for period, pdata in rdata.items():
            assert period in ["1h", "24h", "7d"]

