#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for stats() method"""

from time import sleep
from random import choice

from pymarketcap.tests import type_test
from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_badges = list(pym.ticker_badges)
all_badges.remove("USD")

def teardown_function(function):
    sleep(1)

def assert_types(res):
    int_type_fields = [
        "active_assets",
        "active_currencies",
        "active_markets",
        "last_updated",
    ]

    assert isinstance(res, dict)
    for key, value in res.items():
        if key in int_type_fields:
            assert isinstance(value, int)
        else:
            assert isinstance(value, float)

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
