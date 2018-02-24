#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from random import choice

from pymarketcap import Pymarketcap
pym = Pymarketcap()

class TypeTester:
    def _date(self, value): assert type(value) == datetime
    def _open(self, value): assert type(value) == float
    def _high(self, value): assert type(value) == float
    def _low(self, value): assert type(value) == float
    def _close(self, value): assert type(value) == float
    def _volume(self, value): assert type(value) == float
    def _market_cap(self, value): assert type(value) == float

tt = TypeTester()

def test_types():
    symbol = choice(pym.coins)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.historical(symbol)
    assert type(res) == list
    for tick in res:
        assert type(tick) == dict
        for key, value in tick.items():
            eval("tt._{}({})".format(
                key,
                value if type(value) != datetime else "value"
            ))

def test_consistence():
    symbol = choice(pym.coins)
    symbol = "TLE"
    print("(Currency: %s)" % symbol, end=" ")
    res = list(pym.historical(symbol))

    # Check dates order
    for i, tick in enumerate(res):
        assert len(tick.keys()) == 7  # Check number of keys
        if i < len(res)-1:
            assert res[i+1]["date"] < tick["date"]
