#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from pymarketcap import AsyncPymarketcapScraper

async def main():
    async with AsyncPymarketcapScraper() as apym:
        async for currency in apym.every_currency():
            print(currency)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
