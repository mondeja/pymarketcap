# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
pym = Pymarketcap()

ID = 1
STR_ID = "1"
FLOAT_ID = 1.1

def test_valid_id():
    assert "id" == pym.field_type(ID)

def test_str_id():
    assert "id" == pym.field_type(STR_ID)

def test_float_id():
    assert "id" == pym.field_type(FLOAT_ID)


NAME = "Bitcoin"
MALFORMED_NAME = "BitCoiN"

def test_valid_name():
    assert "name" == pym.field_type(NAME)

def test_malformed_name():
    assert "name" == pym.field_type(MALFORMED_NAME)


SYMBOL = "BTC"
SYMBOL_WITH_NUMBERS = "BTC2"

def test_valid_symbol():
    assert "symbol" == pym.field_type(SYMBOL)

def test_symbol_with_numbers():
    assert "symbol" == pym.field_type(SYMBOL_WITH_NUMBERS)


WEBSITE_SLUG = "bitcoin"

def test_valid_website_slug():
    assert "website_slug" == pym.field_type(WEBSITE_SLUG)
