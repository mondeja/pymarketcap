#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Shared interfaces tests modules."""

def type_test(type_tester, key, value):
    try:
        assert isinstance(value, type_tester[key])
    except AssertionError as err:
        print("Key: %s\nValue: %r\n" % (key, value))
        raise err
