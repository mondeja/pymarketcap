#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Shared interfaces tests modules."""

def type_test(map_types, key, value):
    try:
        assert isinstance(value, map_types[key])
    except AssertionError as err:
        print("Key: %s\nValue: %r\n" % (key, value))
        raise err
