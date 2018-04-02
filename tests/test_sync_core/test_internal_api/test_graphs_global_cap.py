#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from datetime import datetime, timedelta

from pymarketcap.tests.graphs import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    res = pym.graphs.global_cap()
    assert_types(res)

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
    possible_days_ago = [
        days_ago.day,
        (days_ago+timedelta(days=1)).day,
        (days_ago-timedelta(days=1)).day
    ]
    possible_days_today = [
        today.day,
        (today-timedelta(days=1)).day,
        (today+timedelta(days=1)).day
    ]
    assert res["market_cap_by_available_supply"][-1][0].day in possible_days_today
    assert res["market_cap_by_available_supply"][0][0].day in possible_days_ago

