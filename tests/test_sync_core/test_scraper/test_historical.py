#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import pytest

from pymarketcap import Pymarketcap
from pymarketcap.tests.utils import random_cryptocurrency
from pymarketcap.tests.historical import (
    assert_types,
    assert_consistence
)

pym = Pymarketcap()

def test_types():
    curr = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % curr, end=" ")
    res = pym.historical(curr)
    assert_types(res)

def test_consistence():
    curr = random_cryptocurrency(pym)["website_slug"]
    print('(<currency>["website_slug"] == "%s")' % curr, end=" ")
    res = pym.historical(curr)
    assert_consistence(res)

def test_invalid():
    name = "BDAD)DAAS&/9324423OUVibb"
    with pytest.raises(ValueError) as excinfo:
        res = pym.historical(name)
    expected_msg = "Any cryptocurrency found matching name == %r." % name
    assert expected_msg in str(excinfo)
