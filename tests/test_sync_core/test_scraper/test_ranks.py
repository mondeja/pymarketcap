#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap.tests import type_test
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def assert_types(data):
    map_types = {
        "name":           str,
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
    assert_types(pym.ranks())

def assert_currencies_order(data):
    # Assert if currencies are in order
    for rank, rdata in data.items():
        for period, pdata in rdata.items():
            for i, currency in enumerate(pdata):
                if i < len(pdata)-1:
                    assert pdata[i+1]["percent_change"] >= currency["percent_change"]

def test_consistence():
    assert_currencies_order(pym.ranks())
