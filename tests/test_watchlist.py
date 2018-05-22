#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for watchlist() method."""

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_watchlist():
    res = pym.watchlist()
    print(res)
