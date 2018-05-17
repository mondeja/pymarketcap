#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall
from urllib.request import urlopen

import pytest

from pymarketcap import Pymarketcap
from pymarketcap.tests import restart_if_http_error
from pymarketcap.tests.utils import random_cryptocurrency
from pymarketcap.tests.markets import (
    assert_types,
    assert_consistence
)

pym = Pymarketcap()

@restart_if_http_error
def assert_number_of_markets(res):
    req = urlopen("https://coinmarketcap.com/currencies/%s" % res["website_slug"])
    data = req.read()
    req.close()
    indexes = findall(r'<td class="text-right">(.+)</td>', data.decode())
    assert len(res["markets"]) in [
        int(indexes[-1])+1,
        int(indexes[-1]),
        int(indexes[-1])-1
    ]

def test_without_convert():
    website_slug = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % website_slug, end=" ")
    res = pym.markets(website_slug)
    assert_types(res)
    from pprint import pprint
    pprint(res)
    assert_consistence(res)
    assert_number_of_markets(res)

def test_with_convert():
    website_slug = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % website_slug, end=" ")
    res = pym.markets(website_slug, convert="BTC")
    assert_types(res)
    assert_consistence(res)
    assert_number_of_markets(res)

def test_invalid():
    name = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.markets(name)
    expected_msg = "Any cryptocurrency found matching name == %r." % name
    assert expected_msg in str(excinfo)
