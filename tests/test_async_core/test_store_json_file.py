#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from json import loads
from random import choice

import pytest

from pymarketcap.tests.currency import (
    assert_types,
    assert_consistence
)
from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap
)
pym = Pymarketcap()


WORKDIR="."

def test_every_currency_stored_as_json(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(debug=True,
                                    queue_size=50,
                                    consumers=50,
                                    json=WORKDIR) as apym:
            coins = []
            for i in range(20):
                coins.append(choice(pym.coins))

            async for (currency) in apym.every_currency(coins):
                pass    # Download all files

            for root, dirs, files in os.walk("."):
                for coin in coins:
                    found = False
                    for name in files:
                        if coin in name:
                            found = True   # Coin found

                            with open(name, "r") as f:  # Test responses
                                content = loads(f.read())
                            assert_types(content)
                            assert_consistence(content)

                            os.remove(name)   # Delete file
                            assert os.path.exists(name) == False
                            break
                    assert found == True
                break

    event_loop.run_until_complete(wrapper())
