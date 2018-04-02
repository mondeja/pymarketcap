#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice, randint
from datetime import datetime, timedelta

from pymarketcap.tests.graphs import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_symbols = pym.symbols

def test_types():
    symbol = choice(all_symbols)
    res = pym.graphs.currency(symbol)
    print("(Currency: %s)" % symbol, end=" ")

    assert_types(res)

def test_consistence():
    symbol = choice(all_symbols)
    res = pym.graphs.currency(symbol)
    print("(Currency: %s)" % symbol, end=" ")

    assert len(res) in [4, 5]

    fields = [
        "market_cap_by_available_supply",
        "price_btc",
        "price_usd",
        "volume_usd",
        "price_platform",
     ]

    for field, values in res.items():
        assert field in fields

def test_start_end():
    days_ago = timedelta(days=randint(1, 15))
    start = datetime.now() - days_ago
    end = datetime.now()
    symbol = choice(all_symbols)
    print("(Currency: %s | Start: %r)" % (symbol, start), end=" ")
    for startend in [True , False]:
        params = {"start": start, "end": end}
        if not startend:
            params["start"] = None
            params["end"] = None
        res = pym.graphs.currency(choice(pym.symbols), **params)

        # Test types
        assert type(res) == dict

        for key, _list in res.items():
            assert type(_list) == list
            for elem, value in _list:
                assert isinstance(elem, datetime)
                assert type(value) in [int, float]

        # Test consistence
        assert end.day >= res["price_btc"][-1][0].day
        if startend:
            first_day = res["price_usd"][0][0]
            next_day = res["price_usd"][0][0] + timedelta(days=1)
            assert start <= next_day





