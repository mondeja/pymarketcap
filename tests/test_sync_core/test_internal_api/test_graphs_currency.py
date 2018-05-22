#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from random import randint

from pymarketcap import Pymarketcap
from pymarketcap.tests.graphs import assert_types
from pymarketcap.tests.utils import random_cryptocurrency

pym = Pymarketcap()


def test_types():
    curr = random_cryptocurrency(pym)["website_slug"]
    res = pym.graphs.currency(curr)
    print('(<currency>["website_slug"] == "%s")' % curr, end=" ")

    assert_types(res)


def test_consistence():
    curr = random_cryptocurrency(pym)["website_slug"]
    res = pym.graphs.currency(curr)
    print('(<currency>["website_slug"] == "%s")' % curr, end=" ")

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
    curr = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == %s | Start: %r | End: %r)' % (
    curr, start, end),
          end=" ")
    for startend in [True, False]:
        params = {"start": start, "end": end}
        if not startend:
            params["start"], params["end"] = (None, None)
        res = pym.graphs.currency(curr, **params)

        # Test types
        assert isinstance(res, dict)

        for key, _list in res.items():
            assert isinstance(_list, list)
            for elem, value in _list:
                assert isinstance(elem, datetime)
                assert type(value) in [int, float]

        # Test consistence
        if end.day > 2:
            assert end.day >= res["price_btc"][-1][0].day
        if startend:
            first_day = res["price_usd"][0][0]
            next_day = res["price_usd"][0][0] + timedelta(days=1)
            assert start <= next_day
