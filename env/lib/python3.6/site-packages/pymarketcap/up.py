#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Return a dic with all the available currencies
and their symbols correspondences '''
def get_currencies():
        from core import Pymarketcap
        dic = {}
        for currency in Pymarketcap()._up():
            iid = currency.get('id')
            symbol = currency.get('symbol')
            dic[symbol] = iid
        return dic

''' Save the symbols in a temporary .txt file '''
def update_currencies():
    from os import path
    p = path.dirname(path.abspath(__file__))
    try:
        c = open(p + '/tmp/symbols.txt', 'w')
    except IOError:
        from os import mkdir
        mkdir(p + '/tmp')
        c = open(p + '/tmp/symbols.txt', 'w')
    c.write(str(get_currencies()))
    c.close()
