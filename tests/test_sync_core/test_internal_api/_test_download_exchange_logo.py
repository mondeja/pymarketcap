#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep
from random import choice

import pytest
from tqdm import tqdm

from pymarketcap import Pymarketcap
pym = Pymarketcap()

exchange_names = pym.exchange_names
exchange_slugs = pym.exchange_slugs

def assert_consistence(res):
    assert len(res) > 0
    assert isinstance(res, str)
    assert os.path.exists(res)
    os.remove(res)
    assert os.path.exists(res) == False

def test_consistence():
    print("")
    for size in tqdm([16, 32, 64, 128, 200],
                     desc="Testing exchange logo downloads for all sizes"):
        attempts = 20
        while attempts > 0:
            _assert = True
            exc = choice(exchange_slugs)
            tqdm.write("(Exchange: %s | Size: %d)" % (exc, size))
            try:
                res = pym.download_exchange_logo(exc, size=size)
            except ValueError as e:
                print(e)
                attempts -= 1
                _assert = False
                if attempts == 0:
                    break
            else:
                break
        if _assert:
            assert res == "%s_%dx%d.png" % (exc, size, size)
            sleep(.5)

            assert os.path.exists(res)
            os.remove(res)
            assert os.path.exists(res) == False
        if attempts == 0:
            raise AssertionError("0 exchange logos downloaded. Check it!")

def test_invalid():
    # Invalid exchange
    exc = "PIDBASDVBHB934VHJ"

    with pytest.raises(ValueError) as excinfo:
        pym.download_exchange_logo(exc)
    assert "Exchange %s not found." % exc in str(excinfo)

    # Invalid size
    exc = choice(exchange_names)
    size = 47365
    print("(Exchange: %s)" % exc, end=" ")
    with pytest.raises(ValueError) as excinfo:
        pym.download_exchange_logo(exc, size=size)
    assert "%dx%d is not a valid size." % (size, size) in str(excinfo)

def test_download_passing_name():
    exc = choice(exchange_names)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.download_exchange_logo(exc)
    assert_consistence(res)

def test_download_passing_slug():
    exc = choice(exchange_slugs)
    print("(Exchange: %s)" % exc, end=" ")
    res = pym.download_exchange_logo(exc)
    assert_consistence(res)

