#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice

import pytest

from pymarketcap.tests.currency import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.currency(coin)
    assert_types(res)

def test_consistence():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.currency(coin)
    assert_consistence(res)

def test_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.currency(coin, convert="BTC")

    assert_types(res)
    assert_consistence(res)

def test_invalid():
    symbol = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.currency(symbol)
    assert "See 'symbols' or 'coins' properties" in str(excinfo)

