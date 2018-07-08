#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Warning: use this example with caution,
it will use a lot of your memory."""

import asyncio
from pymarketcap import AsyncPymarketcap

res = []

async def main():
    async with AsyncPymarketcap(queue_size=50, consumers=50) as apym:
        async for currency in apym.every_historical():
            res.append(currency)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print(res[-1])
