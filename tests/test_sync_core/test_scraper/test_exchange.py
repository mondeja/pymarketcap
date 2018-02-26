#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
from re import findall as re_findall
from urllib.request import urlopen
from urllib.error import HTTPError

from tqdm import tqdm
import pytest

from pymarketcap.tests.exchange import assert_types
from pymarketcap import Pymarketcap, CoinmarketcapHTTPError
pym = Pymarketcap()

def test_types():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.exchange(exc)
    assert_types(res)

def assert_number_of_markets(exc, markets):
    req = urlopen("https://coinmarketcap.com/exchanges/%s/" % exc)
    data = req.read()
    req.close()
    indexes = re_findall(r'<td class="text-right">(\d+)</td>', data.decode())
    assert len(markets) == int(indexes[-1])

def assert_consistence(res, exc):
    assert len(res["name"]) > 0
    assert res["name"] != None
    assert len(res["website"]) > 0
    assert res["website"] != None
    assert_number_of_markets(exc, res["markets"])

def test_consistence():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    assert_types(pym.exchange(exc))


def test_convert():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.exchange(exc, convert="BTC")

    assert_types(res)
    assert_consistence(res, exc)

def test_invalid():
    exc = "dabsfgbdsagubfeqbfeyfv"
    with pytest.raises(ValueError) as excinfo:
        pym.exchange(exc)
    assert '%s is not a valid exchange name.' % exc in str(excinfo.value)
