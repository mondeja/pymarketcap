#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
from re import findall
from urllib.request import urlopen

from tqdm import tqdm
import pytest

from pymarketcap.tests.exchange import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap, CoinmarketcapHTTPError
pym = Pymarketcap()

def assert_number_of_markets(res):
    req = urlopen("https://coinmarketcap.com/exchanges/%s/" % res["slug"])
    data = req.read()
    req.close()
    indexes = findall(r'<td class="text-right">(\d+)</td>', data.decode())
    try:
        assert len(res["markets"]) == int(indexes[-1])
    except IndexError:
        if req.getcode() != 200:  # HTTP fail
            pass

def test_types():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.exchange(exc)
    assert_types(res)

def test_consistence():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.exchange(exc)
    assert_consistence(res)
    assert_number_of_markets(res)


def test_convert():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.exchange(exc, convert="BTC")

    assert_types(res)
    assert_consistence(res)

def test_invalid():
    exc = "dabsfgbdsagubfeqbfeyfv"
    with pytest.raises(ValueError) as excinfo:
        pym.exchange(exc)
    assert '%s is not a valid exchange name.' % exc in str(excinfo.value)
