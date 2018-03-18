#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test wrapper properties"""

from pymarketcap.consts import INVALID_COINS
from pymarketcap import Pymarketcap
pym = Pymarketcap()


###   API METHOD CACHERS   ###

def test_correspondences():
    res = pym.correspondences

    # Test types
    assert type(res) == dict
    for key, value in res.items():
        assert type(key) == str
        assert type(value) == str

    # Test consistence
    assert res == pym._cache_symbols_ids()[0]

def test_ids_correspondences():
    res = pym.ids_correspondences

    # Test types
    assert type(res) == dict
    for key, value in res.items():
        assert type(key) == str
        assert type(value) == int

    # Test consistence
    assert res == pym._cache_symbols_ids()[1]

def test_symbols():
    res = pym.symbols

    # Test types
    assert type(res) == list

    # Test consistence
    assert len(res) > 0

def test_coins():
    res = pym.coins

    # Test types
    assert type(res) == list
    for coin in res:
        assert type(coin) == str

    # Test consistence
    for invalid_coin in INVALID_COINS:
        assert invalid_coin not in res
    assert len(res) > 0

def test_total_currencies():
    # Test types
    res = pym.total_currencies
    assert type(res) == int

    # Test consistence
    assert res == len(pym.ticker())


###   WEB SCRAPER METHOD CACHERS   ###

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
    assert len(res) == len(pym.__exchange_names_slugs())

def test_exchange_slugs():
    # Test types
    res = pym.exchange_slugs
    assert type(res) == list
    for exc in res:
        assert type(exc) == str

    # Test consistence
    assert len(res) > 0
    assert len(res) == len(pym.__exchange_names_slugs())
