#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap

def main():
    cmc = Pymarketcap()

    # Get all currencies ranked by volume
    currencies = cmc.ticker()
    print(currencies)

if __name__ == "__main__":
    main()

