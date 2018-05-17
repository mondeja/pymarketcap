# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
from pymarketcap.tests import assert_cryptocurrency_or_exchange_types
pym = Pymarketcap()

SYMBOL = "BTC"
NAME = "Bitcoin"
WEBSITE_SLUG = "bitcoin"

def test_valid_cryptocurrency():
    res = pym.cryptocurrency_by_field_value("website_slug",
                                            WEBSITE_SLUG)
    assert res["name"] == NAME
    assert res["symbol"] == SYMBOL
    assert res["website_slug"] == WEBSITE_SLUG

    assert_cryptocurrency_or_exchange_types(res)

INVALID_WEBSITE_SLUG = "hnsdhkfyfd7Fye	ogufgk"

def test_invalid_cryptocurrency():
    res = pym.cryptocurrency_by_field_value("website_slug",
    	                                    INVALID_WEBSITE_SLUG)
    assert res == None
