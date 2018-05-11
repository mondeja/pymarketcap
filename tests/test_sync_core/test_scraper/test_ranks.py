#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap.tests.ranks import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    res = pym.ranks()
    assert_types(res)

def test_consistence():
    res = pym.ranks()

    # Check if a currency is repeated
    for rank, rdata in res.items():
        assert rank in ["gainers", "losers"]
        for period, pdata in rdata.items():
            assert period in ["1h", "24h", "7d"]

