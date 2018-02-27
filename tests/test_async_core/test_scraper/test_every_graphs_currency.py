#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap.tests.graphs import assert_types
from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap
)
pym = Pymarketcap()

@pytest.mark.end2end
@pytest.mark.asyncio
async def test_every_graphs_currency(event_loop):
    async with AsyncPymarketcap(debug=True,
                                       queue_size=50,
                                       consumers=50) as apym:
        res = []
        show_msg = True
        async for (currency) in apym.graphs.every_currency():
            if show_msg:
                print("Testing all responses...")
                show_msg = False
            res.append(currency)

            assert_types(currency)

        assert type(res) == list

        # Assert consistence
        assert len(res) < pym.total_currencies + 100
        assert len(res) > pym.total_currencies - 100


