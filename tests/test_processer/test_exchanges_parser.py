#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
pym = Pymarketcap()

exchanges = pym.exchanges()

def assert_any_field_in_response(field, readable_field):
    found = False
    for exc in exchanges:
        value = exc[field]

        if isinstance(value, list):
            found = True
            for market in value:
                for _key, _value in market.items():
                    if _value == None:
                        found = False
                        break
                if found == False:
                    break
        elif isinstance(value, str):
            if value != "":
                found = True
        elif value == None:
            continue
        else:
            msg = "Case not anticipated. 'type(value) == %r'"
            raise NotImplementedError(msg % type(value))
    try:
        assert found == True
    except AssertionError as err:
        print("Any %s found searching all currencies." % readable_field \
              + "Check 'processer:exchanges()' function.")
        raise err

def test_name():
    assert_any_field_in_response("name", "exchange name")

def test_markets():
    assert_any_field_in_response("markets", "market")