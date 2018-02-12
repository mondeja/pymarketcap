#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

from precompiler import recopiler
from precompiler.utils import format_list_as_string

class Builder:
    """Parser and compiler of the source code of the wrapper
    to create it programatically.

    Args:
        source (str, optional): Path to source file where make changes.
            As default cymarketcap/src/core.pyx
    """
    def __init__(self, source=os.path.join(os.getcwd(), "pymarketcap", "core.pyx")):
        self.source = source
        self.test_sources = {
            "test_ticker": os.path.join(os.getcwd(), "tests", "test_api", "test_ticker.py")
        }

    ###   MAIN BUILDER METHODS   ###

    def build(self, func):
        """Run the compiler for build a piece of code.

        Args:
            func (str): Select the func to use for build.

        """
        return eval('self.%s()' % func)

    def read_source(self):
        """Read source file and returns their content."""
        with open(self.source, "r") as f:
            content = f.read()
        return content

    def write_source(self, content):
        """Reaplce content of source file.

        Args:
            content (str): New content to write on source file.
        """
        with open(self.source, "w") as f:
            f.write(content)

    # ==========================================================

    ###   BUILDS METHODS   ###

    def ticker_badges(self):
        # Get badges from coinmarketcap docs
        badges = recopiler.get_badges_list()

        def return_ticker_badges(stream, badges):
            # Get source
            searcher = re.compile(r"\s{4}def ticker_badges.*return\n^$",
            	                  re.MULTILINE | re.DOTALL)
            original_func = searcher.search(stream).group()[:-1]

            badges_formatted = format_list_as_string(badges, 8, 16)

            # Write badges as return of ticker_badges function
            output_func = original_func + badges_formatted
            return stream.replace(original_func, output_func)

        stream = return_ticker_badges(self.read_source(), badges)

        def ticker__doc__badges(stream, badges):
            """Write badges list on ticker __doc__"""
            badges_formatted = format_list_as_string(badges, 8, 20,
                                                     indent_first_line=18)
            stream = stream.replace("next badges:", "next badges:\n%s" % badges_formatted)
            return stream

        result = ticker__doc__badges(stream, badges)

        # Save result on source file
        self.write_source(result)

    def currency_exchange_rates(self):
        # Get currencies from coinmarketcap.com main page
        currencies = recopiler.get_currency_exchange_rates_list()

        def currency_exchange_rates__doc__(stream, currencies):
            searcher = re.compile(r"\s{4}def currency_exchange_rates.*next currencies:\n",
                              re.MULTILINE | re.DOTALL)

            original_func = searcher.search(stream).group()[:-1]

            # Format currencies list to indented list as string
            currs_formatted = format_list_as_string(currencies, 6, 13, 11)

            # Write currencies for exchange rates in currency_exchange_rates.__doc__
            output_func = original_func + "\n" + currs_formatted
            return stream.replace(original_func, output_func)

        result = currency_exchange_rates__doc__(self.read_source(), currencies)

        # Save result on source file
        self.write_source(result)

    def unskip_tests(self):
        source = self.test_sources["test_ticker"]
        with open(source, "r") as f:
            content = f.readlines()

        result = []
        for line in content:
            if "@pytest.mark.skip" in line and "ticker_badges" in line:
                continue
            result.append(line)

        with open(source, "w") as f:
            f.writelines(result)

    # ===========================================================================

    def unbuild(self):
        """Restaure original state of the code"""
        def return_ticker_badges(stream):
            searcher = re.compile(r"def ticker_badges.+\n.+\n.+return(\s.+\n.+\n.+\n.+)")
            original_func = searcher.search(stream).group(1)
            return stream.replace(original_func, "", 1)

        def ticker__doc__badges(stream):
            searcher = re.compile(r"next badges:(\n.+\n.+\n.+\n.+)")
            original_func = searcher.search(stream).group(1)
            return stream.replace(original_func, "", 1)

        def currency_exchange_rates__doc__(stream):
            searcher = re.compile(r"next currencies:(\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+)")
            original_func = searcher.search(stream).group(1)
            return stream.replace(original_func, "", 1)

        stream = currency_exchange_rates__doc__(
            ticker__doc__badges(
                return_ticker_badges(self.read_source())
            )
        )
        self.write_source(stream)

        def reskip_tests(stream):
            func_name_string = " "*4 + "def test_convert(self):"
            skip_string = " "*4 \
                + '@pytest.mark.skip(reason="ticker_badges property needed but not built yet")\n'
            return stream.replace(func_name_string,
                                  skip_string + func_name_string)

        source = self.test_sources["test_ticker"]
        with open(source, "r") as f:
            stream = f.read()

        with open(source, "w") as f:
            f.write(reskip_tests(stream))

        return True

