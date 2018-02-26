#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from datetime import datetime, timedelta

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    res = pym.graphs.global_cap()

    assert type(res) == dict
    for key, values in res.items():
        assert type(key) == str
        assert type(values) == list
        for tmp, value in values:
            assert isinstance(tmp, datetime)
            assert type(value) in [float, int]

def test_consistence():
    res = pym.graphs.global_cap()
    assert len(res) == 2

    fields = list(res.keys())
    for f in ["market_cap_by_available_supply", "volume_usd"]:
        assert f in fields

def test_start_end():
    today = datetime.now()
    days_ago = today - timedelta(days=randint(1, 15))

    res = pym.graphs.global_cap(start=days_ago)
    assert res["market_cap_by_available_supply"][-1][0].day == today.day
    assert res["market_cap_by_available_supply"][0][0].day in \
        [days_ago.day, (days_ago+timedelta(days=1)).day]


