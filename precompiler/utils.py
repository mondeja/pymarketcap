#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from urllib.request import urlopen

def GET(url):
    done = False
    count = 0
    while not done:
        try:
            data = urlopen(url)
        except Exception as e:
            print(e)
            count += 1
            if count >= 3:
                break
        else:
            done = True
            response = data.read()
            data.close()
            return response
    print("Check your internet connection before install pymarketcap.")
    sys.exit(1)


def format_list_as_string(_list, items_each_line, left_indent,
                                  indent_first_line=0):
    """Format a list as string"""
    l_formatted = " "*indent_first_line + " ["
    items_each_line_count = 0
    for item in _list:
        l_formatted += '"%s", ' % item
        items_each_line_count += 1
        if items_each_line_count == items_each_line and item != _list[-1]:
            l_formatted = l_formatted[:-1] + "\n" + " "*left_indent
            items_each_line_count = 0
    return l_formatted[:-2] + "]"
