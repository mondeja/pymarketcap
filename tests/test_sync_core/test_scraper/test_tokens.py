#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall as re_findall
from urllib.request import urlopen

from pymarketcap.tests.tokens import assert_types
from pymarketcap import Pymarketcap
pym = Pymarketcap()


def test_types():
    res = pym.tokens()
    assert_types(res)


def assert_number_of_tokens(res):
    req = urlopen("https://coinmarketcap.com/tokens/views/all/")
    data = req.read()
    req.close()
    indexes = int(
        re_findall(r'<td class="text-center">\n(\d+)\n</td>', data.decode())[-1]
    )
    assert len(res) in [indexes-1, indexes, indexes+1]


def test_consistence():
    res = pym.tokens()
    assert_number_of_tokens(res)
