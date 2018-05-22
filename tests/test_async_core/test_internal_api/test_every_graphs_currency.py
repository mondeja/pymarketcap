#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytest

from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap,
)
from pymarketcap.tests.graphs import assert_types

pym = Pymarketcap()

end = datetime.now().date()
start = end - timedelta(days=1)

graphs_fields = (
    'market_cap_by_available_supply',
    'price_btc',
    'price_usd',
    'volume_usd',
)


async def graphs_currency(**kwargs):
    async with AsyncPymarketcap(debug=True,
                                queue_size=50,
                                consumers=50) as apym:
        currencies = []
        show_msg = True
        async for currency in apym.graphs.every_currency(**kwargs):
            if show_msg:
                print("Testing all responses...")
                show_msg = False
            currencies.append(currency)
        return currencies


@pytest.mark.end2end
def test_every_graphs_currency(event_loop):
    async def wrapper():
        currencies = await graphs_currency()
        assert isinstance(currencies, list)

        for currency in currencies:
            assert_types(currency)

    event_loop.run_until_complete(wrapper())


@pytest.mark.end2end
def test_every_graphs_currency_with_start(event_loop):
    async def wrapper():
        currencies = await graphs_currency(currencies=['bitcoin'], start=start)
        assert isinstance(currencies, list)
        for currency in currencies:
            assert_types(currency)

            for f in graphs_fields:
                assert f in currency

                values = currency[f]
                assert isinstance(values, list)
                assert len(values)

                dt = values[0][0]
                assert isinstance(dt, datetime)
                assert dt.date() == start

    event_loop.run_until_complete(wrapper())


@pytest.mark.end2end
def test_every_graphs_currency_with_end(event_loop):
    async def wrapper():
        currencies = await graphs_currency(currencies=['bitcoin'], end=end)
        assert isinstance(currencies, list)
        for currency in currencies:
            assert_types(currency)

            for f in graphs_fields:
                assert f in currency

                values = currency[f]
                assert isinstance(values, list)
                assert len(values)

                dt = values[-1][0]
                assert isinstance(dt, datetime)
                assert dt.date() == end

    event_loop.run_until_complete(wrapper())


@pytest.mark.end2end
def test_every_graphs_currency_with_start_end(event_loop):
    async def wrapper():
        currencies = await graphs_currency(
            currencies=['bitcoin'],
            start=start,
            end=end
        )
        assert isinstance(currencies, list)
        for currency in currencies:
            assert_types(currency)

            for f in graphs_fields:
                assert f in currency

                values = currency[f]
                assert isinstance(values, list)
                assert len(values)

                dt = values[0][0]
                assert isinstance(dt, datetime)
                assert dt.date() == start

                dt = values[-1][0]
                assert isinstance(dt, datetime)
                assert dt.date() == end

    event_loop.run_until_complete(wrapper())


@pytest.mark.end2end
def test_every_graphs_currency_with_start_end_use_auto_timeframe(event_loop):
    async def wrapper():
        currencies = await graphs_currency(
            currencies=['bitcoin'],
            start=start,
            end=end,
            use_auto_timeframe=True,
        )
        assert isinstance(currencies, list)
        for currency in currencies:
            assert_types(currency)

            for f in graphs_fields:
                assert f in currency

                values = currency[f]
                assert isinstance(values, list)
                assert len(values) > 2

                start_dt = values[0][0]
                assert isinstance(start_dt, datetime)
                assert start_dt.date() == start

                end_dt = values[-1][0]
                assert isinstance(end_dt, datetime)
                assert end_dt.date() == end

                next_dt = values[1][0]
                assert isinstance(next_dt, datetime)
                assert next_dt - start_dt < timedelta(hours=1)

    event_loop.run_until_complete(wrapper())
