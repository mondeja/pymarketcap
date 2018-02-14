#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test wrapper properties"""

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function(function):
    time.sleep(1)


###   API METHODS   ###

def test_correspondences():
    # Test consistence
    assert pym.correspondences == pym._cache_symbols()

def test_symbols():
    res = pym.symbols

    # Test types
    assert type(res) == list

    # Test consistence
    assert res == sorted(list(pym.correspondences.keys()))
    assert len(res) > 0

def test_coins():
    res = pym.coins

    # Test types
    assert type(res) == list
    for coin in res:
        assert type(coin) == str

    # Test consistence
    assert res == sorted(list(pym.correspondences.values()))
    assert len(res) > 0

def test_total_currencies():
    # Test types
    res = pym.total_currencies
    assert type(res) == int

    # Test consistence
    assert res == len(pym.ticker())


###   WEB SCRAPER METHODS   ###

def test_currency_exchange_rates():
    # Test types
    res = pym.currency_exchange_rates
    for key, value in res.items():
        assert type(key) == str
        assert type(value) == float

    # Test consistence
    ctc = pym.currencies_to_convert
    for symbol in list(res.keys()):
        assert symbol in ctc

def test_currencies_to_convert():
    # Test types
    currencies = pym.currencies_to_convert
    assert type(currencies) == list
    for curr in currencies:
        assert type(curr) == str

    # Test consistence
    assert len(currencies) > 0

def test_exchange_names():
    # Test types
    res = pym.exchange_names
    assert type(res) == list
    assert len(res) > 0
    for exc in res:
        assert type(exc) == str

    # Test consistence
    assert len(res) > 0
    assert len(res) == len(pym.__exchange_names())

def test_exchange_slugs():
    # Test types
    res = pym.exchange_slugs
    assert type(res) == list
    for exc in res:
        assert type(exc) == str

    # Test consistence
    assert len(res) > 0
    assert len(res) == len(pym.__exchange_slugs())
