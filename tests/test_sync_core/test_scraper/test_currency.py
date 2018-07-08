#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap.tests.utils import random_cryptocurrency
from pymarketcap.tests.currency import (
    assert_types,
    assert_consistence
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    website_slug = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % website_slug, end=" ")
    res = pym.currency(website_slug)
    assert_types(res)

def test_consistence():
    website_slug = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % website_slug, end=" ")
    res = pym.currency(website_slug)
    assert_consistence(res)

def test_convert():
    website_slug = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % website_slug, end=" ")
    res = pym.currency(website_slug, convert="BTC")

    assert_types(res)
    assert_consistence(res)

def test_invalid():
    name = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.currency(name)
    expected_msg = "Any cryptocurrency found matching name == %r." % name
    assert expected_msg in str(excinfo)
