#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

def assert_types(res):
    assert type(res) == dict
    for field, values in res.items():
        if field in ["slug", "symbol"]:
            assert type(values) == str
        else:
	        assert type(values) == list
	        for tmp, value in values:
	            assert isinstance(tmp, datetime)
	            assert type(value) in [float, int]