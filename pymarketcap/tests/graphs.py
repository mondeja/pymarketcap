#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""``graphs()`` shared method test module."""

from datetime import datetime

def assert_types(res):
    assert isinstance(res, dict)
    for field, values in res.items():
        if field in ["website_slug", "symbol", "name"]:
            assert isinstance(values, str)
        elif field == "id":
            assert isinstance(values, int)
        else:
            assert isinstance(values, list)
            for tmp, value in values:
                assert isinstance(tmp, datetime)
                assert isinstance(value, (float, int))
