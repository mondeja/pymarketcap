#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'pymarketcap',
    version = '3.2.0',
    url = 'https://github.com/mondeja/pymarketcap',
    download_url = 'https://github.com/mondeja/pymarketcap/archive/master.zip',
    author = 'Álvaro Mondéjar <mondejar1994@gmail.com>',
    author_email = 'mondejar1994@gmail.com',
    license = 'Apache v2.0 License',
    packages = ['pymarketcap'],
    description = 'Python3 API and web scraper for coinmarketcap.com.',
    long_description = open('README.md','r').read(),
    keywords = ['coinmarketcap', 'cryptocurrency', 'API', 'wrapper', 'scraper', 'json', 'BTC', 'Bitcoin'],
)
