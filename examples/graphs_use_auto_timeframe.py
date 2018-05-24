#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Warning: use this example with caution,
it will use a lot of your memory."""

import asyncio
from pymarketcap import AsyncPymarketcap
from pprint import pprint
from datetime import datetime, timedelta
res = []

end = datetime.now().date()
start = end - timedelta(days=1)


async def main():
    async with AsyncPymarketcap(queue_size=50, consumers=50, debug=True) as apym:
        async for d in apym.graphs.every_currency(['bitcoin'], start=start, end=end, use_auto_timeframe=True):
            pprint(d)
            print(d.keys())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
