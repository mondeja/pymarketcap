#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
from urllib.error import HTTPError

from tqdm import tqdm
import pytest

from pymarketcap.tests.exchange import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap, CoinmarketcapHTTPError
pym = Pymarketcap()

def test_types():
    exc = choice(pym.exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.exchange(exc)
    assert_types(res)

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
