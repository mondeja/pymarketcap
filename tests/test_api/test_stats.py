#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for stats() method"""

import time
from random import choice

from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_badges = list(pym.ticker_badges)

class TypeTester:
    def _active_assets(self, value): assert type(value) == int
    def _active_currencies(self, value): assert type(value) == int
    def _active_markets(self, value): assert type(value) == int
    def _bitcoin_percentage_of_market_cap(self, value): assert type(value) == float
    def _last_updated(self, value): assert type(value) == int
    def _total_24h_volume_usd(self, value): assert type(value) == float
    def _total_market_cap_usd(self, value): assert type(value) == float

tt = TypeTester()

def teardown_function(function):
    time.sleep(1)

def assert_types(res):
    assert type(res) == dict
    for key, value in res.items():
        assert type(key) == str
        if "_%s" % key in dir(tt):
            eval("tt._{}({})".format(key, value))
        else:
            assert type(value) == float

def test_types():
    res = pym.stats()
    assert_types(res)

def assert_consistence(res, with_convert=False):
    if with_convert:
        assert len(res) == 9
    else:
        assert len(res) == 7

def test_consistence():
    res = pym.stats()
    assert_consistence(res)

def test_convert():
    badge = choice(all_badges)
    res = pym.stats(convert=badge)

    keys_with_badge = 0
    for key in res:
        if badge.lower() in key:
            keys_with_badge += 1
    assert keys_with_badge == 2

    assert_types(res)
    assert_consistence(res, with_convert=True)
