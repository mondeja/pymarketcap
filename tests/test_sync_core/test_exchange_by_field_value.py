# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
from pymarketcap.tests import assert_cryptocurrency_or_exchange_types

pym = Pymarketcap()

NAME = "Poloniex"
WEBSITE_SLUG = "poloniex"


def test_valid_exchange():
    res = pym.exchange_by_field_value("website_slug",
                                      WEBSITE_SLUG)
    assert res["name"] == NAME
    assert res["website_slug"] == WEBSITE_SLUG

    assert_cryptocurrency_or_exchange_types(res)


INVALID_WEBSITE_SLUG = "jishds92327b ugh9 hoGUK"


def test_invalid_exchange():
    res = pym.exchange_by_field_value("website_slug",
                                      INVALID_WEBSITE_SLUG)
    assert res is None
