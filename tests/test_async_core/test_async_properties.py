#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

try:
    from pymarketcap import AsyncPymarketcap
except ImportError:
    pass
from pymarketcap import Pymarketcap
from pymarketcap.tests.consts import asyncparms

@pytest.mark.py36
def test_sync_interface(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(**asyncparms) as apym:
            sync_interface = apym.sync
        assert isinstance(sync_interface, Pymarketcap)

    event_loop.run_until_complete(wrapper())
