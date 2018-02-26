#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from datetime import datetime, timedelta
from pprint import pprint

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    res = pym.graphs.dominance()

    assert type(res) == dict
    for key, values in res.items():
        assert type(key) == str
        assert type(values) == list
        for tmp, value in values:
            assert isinstance(tmp, datetime)
            assert type(value) in [float, int]

def test_consistence():
    res = pym.graphs.dominance()

    fields = list(res.keys())
    assert "others" in fields

def test_start_end():
    today = datetime.now()
    days_ago = today - timedelta(days=randint(1, 15))

    res = pym.graphs.dominance(start=days_ago)
    key = list(res.keys())[0]
    assert res[key][-1][0].day == today.day
    assert res[key][0][0].day in [days_ago.day,
                                  (days_ago+timedelta(days=1)).day]
