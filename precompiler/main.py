#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pymarketcap installation precompiler."""

import os
from precompiler.builder import Builder

def run_builder(source):
    print("Precompiling pymarketcap source code...")
    builder = Builder(source)

    build_funcs = [
        "ticker_badges",
        "unskip_tests"
    ]

    try:
        for func in build_funcs:
            builder.build(func)
    except Exception as e:
        print("Error precompiling pymarketcap source code.")
        return False

    print("Pymarketcap source code precompiled successfully.")
    return True

def run_unbuilder():
    print("Restoring pymarketcap source code...")
    builder = Builder()
    try:
        response = builder.unbuild()
    except Exception as e:
        print("Error restoring pymarketcap source code.")
        return False
    print("Pymarketcap source code restored successfully.")
    return response
