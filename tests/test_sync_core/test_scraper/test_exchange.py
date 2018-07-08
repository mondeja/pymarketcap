#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall
from urllib.request import urlopen

import pytest

from pymarketcap.tests import restart_if_http_error
from pymarketcap.tests.utils import random_exchange
from pymarketcap.tests.exchange import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

@restart_if_http_error
def assert_number_of_markets(res):
    req = urlopen("https://coinmarketcap.com/exchanges/%s/" % res["website_slug"])
    data = req.read()
    req.close()
    indexes = findall(r'<td class="text-right">(\d+)</td>', data.decode())
    assert len(res["markets"]) == int(indexes[-1])

def test_types():
    exc = random_exchange(pym)["website_slug"]
    print('(<exchange>["website_slug"] == "%s")' % exc, end=" ")
    res = pym.exchange(exc)
    assert_types(res)

def test_consistence():
    exc = random_exchange(pym)["website_slug"]
    print('(<exchange>["website_slug"] == "%s")' % exc, end=" ")
    res = pym.exchange(exc)
    assert_consistence(res)
    assert_number_of_markets(res)

def test_convert():
    exc = random_exchange(pym)["website_slug"]
    print('(<exchange>["website_slug"] == "%s")' % exc, end=" ")
    res = pym.exchange(exc, convert="BTC")

    assert_types(res)
    assert_consistence(res)

def test_invalid():
    exc = "dabsfgbdsagubfeqbfeyfv"
    with pytest.raises(ValueError) as excinfo:
        pym.exchange(exc)
    expected_msg = "Any exchange found matching website_slug == %r" % exc
    assert expected_msg in str(excinfo.value)
