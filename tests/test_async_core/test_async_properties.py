#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap,
)
from pymarketcap.tests.consts import asyncparms


def test_sync_interface(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(**asyncparms) as apym:
            sync_interface = apym.sync
        assert isinstance(sync_interface, Pymarketcap)

    event_loop.run_until_complete(wrapper())
