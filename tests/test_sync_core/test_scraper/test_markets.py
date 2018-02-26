#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
import pytest

from pymarketcap.tests.markets import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()


def test_without_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.markets(coin)
    assert_types(res)
    assert_consistence(res)

def test_with_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.markets(coin, convert="BTC")
    assert_types(res)
    assert_consistence(res)

def test_invalid():
    symbol = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.markets(symbol)
    assert "See 'symbols' or 'coins' properties" in str(excinfo)
