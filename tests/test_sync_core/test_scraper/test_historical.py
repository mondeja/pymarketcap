#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from random import choice

import pytest

from pymarketcap.tests.historical import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    symbol = choice(pym.coins)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.historical(symbol)
    assert_types(res)

def test_consistence():
    symbol = choice(pym.coins)
    symbol = "TLE"
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.historical(symbol)

    # Check dates order
    for i, tick in enumerate(res["history"]):
        assert len(tick.keys()) == 7  # Check number of keys
        if i < len(res)-1:
            assert res["history"][i+1]["date"] < tick["date"]

def test_invalid():
    symbol = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.historical(symbol)
    assert "See 'symbols' or 'coins' properties" in str(excinfo)
