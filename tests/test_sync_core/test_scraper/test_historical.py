#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from random import choice

import pytest

from pymarketcap.tests.historical import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.historical(coin)
    assert_types(res)


def test_consistence():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.historical(coin)
    assert_consistence(res)

def test_invalid():
    symbol = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.historical(symbol)
    assert "See 'symbols' or 'coins' properties" in str(excinfo)
