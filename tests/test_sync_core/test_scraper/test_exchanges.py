#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall as re_findall
from urllib.request import urlopen

from pymarketcap.tests import restart_if_http_error
from pymarketcap.tests.exchanges import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()


@restart_if_http_error
def assert_number_of_exchanges(res):
    req = urlopen("https://coinmarketcap.com/exchanges/volume/24-hour/all/")
    data = req.read()
    req.close()
    indexes = re_findall(r'"volume-header">(\d+)\.', data.decode())
    assert len(res) == int(indexes[-1])

def assert_consistence(res):
    assert len(res) > 0
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
