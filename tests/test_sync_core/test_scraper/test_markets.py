#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
from re import findall
from urllib.request import urlopen

import pytest

from pymarketcap.tests.markets import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def assert_number_of_markets(res):
    req = urlopen("https://coinmarketcap.com/currencies/%s" % res["slug"])
    data = req.read()
    req.close()
    indexes = findall(r'<td class="text-right">(.+)</td>', data.decode())
    assert len(res["markets"]) == int(indexes[-1])

def test_without_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.markets(coin)
    assert_types(res)
    assert_consistence(res)
    assert_number_of_markets(res)

def test_with_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.markets(coin, convert="BTC")
    assert_types(res)
    assert_consistence(res)
    assert_number_of_markets(res)

def test_invalid():
    symbol = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.markets(symbol)
    assert "See 'symbols' or 'coins' properties" in str(excinfo)
