#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap

def main():
    cmc = Pymarketcap()

    # Get all exchanges ranked by volumes
    excs = cmc.exchanges()
    print(excs[0])  # Show first exchange

if __name__ == "__main__":
    main()

