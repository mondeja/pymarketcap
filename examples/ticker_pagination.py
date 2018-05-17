#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example showing how to get all cryptocurrency
USD prices with Coinmarketcap ticker endpoint pagination."""

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def main():
    start = 1
    num_cryptocurrencies = None
    response = {}

    while True:
        cryptocurrencies = pym.ticker(start=start)
        if not num_cryptocurrencies:
            num_cryptocurrencies = \
                cryptocurrencies["metadata"]["num_cryptocurrencies"]
        for _id, currency in cryptocurrencies["data"].items():
            symbol = cryptocurrencies["data"][_id]["symbol"]
            usd_price = cryptocurrencies["data"][_id]["quotes"]["USD"]["price"]
            if usd_price:
                response[symbol] = usd_price
        start += 100
        if start > num_cryptocurrencies:
            break

    assert len(response) <= num_cryptocurrencies
    return response

if __name__ == '__main__':
    response = main()
