#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def test_types():
    res = pym._cache_exchanges_ids()

    assert isinstance(res, list)
    for exc in res:
        assert isinstance(exc, list)
        assert isinstance(exc[0], str)
        assert isinstance(exc[1], str)
        assert isinstance(exc[2], int)

def test_consistence():
    res = pym._cache_exchanges_ids()

    assert len(res) > 0

    names = []
    slugs = []
    ids = []
    for exc in res:
        assert len(exc) == 3
        _name, _slug, _id = (exc[0], exc[1], exc[2])
        assert _name not in names
        assert _slug not in slugs
        assert _id not in ids

        names.append(_name)
        slugs.append(_slug)
        ids.append(_id)



