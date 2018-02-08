#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from random import choice

from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_currencies = list(pym.correspondences.keys())

def teardown_function(function):
    time.sleep(1)

class TypeTester:
    def _source(self, value): assert type(value) == str
    def _pair(self, value): assert type(value) == str
    def _volume_24h(self, value): assert type(value) == float
    def _price(self, value): assert type(value) == float
    def _percent_volume(self, value): assert type(value) == float
    def _updated(self, value): assert type(value) == bool

tt = TypeTester()

def assert_types(res):
    assert type(res) == list
    for source in res:
        assert type(source) == dict
        for key, value in source.items():
            eval("tt._{}({})".format(
                    key,  # Strings need to be "quoted":
                    value if type(value) != str else '"%s"' % value
                ))

def assert_consistence(res):
    for i, source in enumerate(res):
        assert len(source.keys()) == 6
        slash_count = 0
        assert source["pair"].count("/") == 1
        assert source["percent_volume"] <= 100

def test_without_convert():
    symbol = choice(all_currencies)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.markets(symbol)
    assert_types(res)
    assert_consistence(res)

def test_with_convert():
    symbol = choice(all_currencies)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.markets(symbol, convert="BTC")
    assert_types(res)
    assert_consistence(res)
