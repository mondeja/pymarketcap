#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from re import findall as re_findall
from urllib.request import urlopen

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function(function):
    time.sleep(1.5)

class TypeTester:
    def _name(self, value): assert type(value) == str
    def _web(self, value): assert type(value) == str
    def _pair(self, value): assert type(value) == str
    def _volume(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) == float
    def _perc_volume(self, value): assert type(value) == float

tt = TypeTester()

def assert_types(res):
    assert type(res) == list
    for exc in res:
        assert type(exc) == dict
        assert type(exc["name"]) == str
        assert type(exc["markets"]) == list
        for market in exc["markets"]:
            for key, value in market.items():
                assert type(key) == str
                eval("tt._{}({})".format(
                    key,
                    value if type(value) != str else '"%s"' % value
                ))

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
    assert_consistence(pym.exchanges())

def test_convert():
    assert_types(pym.exchanges(convert="BTC"))
    assert_consistence(pym.exchanges(convert="BTC"))
