#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice

import pytest

from pymarketcap.tests.currency import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    symbol = choice(pym.symbols)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.currency(symbol)
    assert_types(res)

def assert_consistence(res):
    assert res["price"] != None
    assert len(list(res.keys())) in list(range(12, 15))

def test_consistence():
    symbol = choice(pym.symbols)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.currency(symbol)
    assert_consistence(res)

def test_convert():
    symbol = choice(pym.symbols)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.currency(symbol, convert="BTC")

    assert_types(res)
    assert_consistence(res)

def test_invalid():
    symbol = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.currency(symbol)
    assert "See 'symbols' or 'coins' properties" in str(excinfo)

