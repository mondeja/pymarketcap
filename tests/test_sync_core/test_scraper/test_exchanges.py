#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall as re_findall
from urllib.request import urlopen

from pymarketcap.tests import (
    type_test,
    restart_if_http_error
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def assert_types(res):
    map_types = {
        "name":           str,
        "web":            str,
        "pair":           str,
        "volume":         (float, type(None)),
        "price":          float,
        "percent_volume": float
    }

    assert isinstance(res, list)
    for exc in res:
        assert isinstance(exc, dict)
        assert isinstance(exc["name"], str)
        assert isinstance(exc["markets"], list)
        for market in exc["markets"]:
            for key, value in market.items():
                type_test(map_types, key, value)

@restart_if_http_error
def assert_number_of_exchanges(res):
    req = urlopen("https://coinmarketcap.com/exchanges/volume/24-hour/all/")
    data = req.read()
    req.close()
    indexes = re_findall(r'"volume-header">(\d+)\.', data.decode())
    assert len(res) == int(indexes[-1])

def assert_consistence(res):
    assert_number_of_exchanges(res)
    for exc in res:
        for market in exc["markets"]:
            assert market["pair"].count("/") == 1

def test_types():
    assert_types(pym.exchanges())

def test_consistence():
    res = pym.exchanges()
    assert_consistence(res)

def test_convert():
    assert_types(pym.exchanges(convert="BTC"))
    assert_consistence(pym.exchanges(convert="BTC"))
