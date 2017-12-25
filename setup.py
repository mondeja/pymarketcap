#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup

BASEDIR = os.path.dirname(__file__)

with open(os.path.join(BASEDIR, "requirements.txt")) as f:
    REQ = f.readlines()

with open(os.path.join(BASEDIR, "README.md"), encoding="utf-8") as f:
    DESC = f.read()


setup(
    name = 'pymarketcap',
    version = '3.3.134',
    url = 'https://github.com/mondeja/pymarketcap',
    download_url = 'https://github.com/mondeja/pymarketcap/archive/master.zip',
    author = 'Álvaro Mondéjar',
    author_email = 'mondejar1994@gmail.com',
    license = 'BSD License',
    packages = ['pymarketcap'],
    description = 'Python3 API and web scraper for coinmarketcap.com.',
    long_description = DESC,
    keywords = ['coinmarketcap', 'cryptocurrency', 'API', 'wrapper', 'scraper', 'json', 'BTC', 'Bitcoin'],
    install_requires = REQ,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
