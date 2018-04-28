#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep
from random import choice
from urllib.error import HTTPError

import pytest
from tqdm import tqdm

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_consistence():
    print("")
    for size in tqdm([16, 32, 64, 128, 200],
                     desc="Testing currency logo downloads for all sizes"):
        attempts = 20
        while attempts > 0:
            _assert = True
            symbol = choice(pym.symbols)
            tqdm.write("(Currency: %s | Size: %d)" % (symbol, size))
            try:
                res = pym.download_logo(symbol, size=size)
            except ValueError as e:
                print(e)
                attempts -= 1
                _assert = False
                if attempts == 0:
                    break
            else:
                break
        if _assert:
            assert res == "%s_%dx%d.png" % (pym.correspondences[symbol], size, size)
            sleep(.5)

            assert os.path.exists(res)
            os.remove(res)
            assert os.path.exists(res) == False
        if attempts == 0:
            raise AssertionError("0 currency logos downloaded. Check it!")

def test_invalid():
    # Invalid currencies
    with pytest.raises(ValueError) as excinfo:
        pym.download_logo("OADVDOVASDYIV")
    assert "See 'symbols' instance attribute." in str(excinfo)

    # Invalid size
    size = 250
    with pytest.raises(ValueError) as excinfo:
        pym.download_logo("BTC", size=size)
    assert "%dx%d is not a valid size." % (size, size) in str(excinfo)

    # Valid size that doesn't exist for a currency.
    symbol = "BEST"
    size = 200
    with pytest.raises(ValueError) as excinfo:
        pym.download_logo(symbol, size=size)
    assert "currency doesn't allows to be downloaded with size %dx%d." \
        % (size, size) in str(excinfo)
