#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.extension import Extension
try:
    from Cython.Build import cythonize
except ImportError:   # Cython required
    print("Cython not found. You need to install Cython before pymarketcap.")
    sys.exit(1)

# Precompiler
from precompiler import run_builder, run_unbuilder

source = os.path.join(os.getcwd(), "pymarketcap", "core.pyx")
built = run_builder(source)
if not built:
    if run_unbuilder():
        if run_builder(source):
            pass
        else:
            print("Error building pymarketcap.")
            sys.exit(1)
    else:
        print("Error building pymarketcap.")
        sys.exit(1)


LONG_DESC = "pymarketcap is library for retrieve data from www.coinmarketcap.com" \
          + " API and website. Consist of a cythonized scraper and API wrapper built" \
          + " with curl C library. Actually, on works in Python>=3.5."

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    REQ = f.readlines()

def declare_cython_extension(ext_name, libraries=None):
    """Declare a Cython extension module for setuptools.

    Args:
        ext_name (str):
            Absolute module name, e.g. use `mylibrary.mypackage.mymodule`
            for the Cython source file `mylibrary/mypackage/mymodule.pyx`.
        libraries (list):
            Libraries needed to build the extension.

    Returns (object):
        Extension object that can be passed to ``setuptools.setup``.
    """
    ext_path = ext_name.replace(".", os.path.sep) + ".pyx"

    return Extension(ext_name, [ext_path], libraries=libraries)

ext_modules = [
    declare_cython_extension("pymarketcap.core"),
    declare_cython_extension("pymarketcap.curl", libraries=["curl"])
]

try:
    ext_modules = cythonize(ext_modules)

    setup(
        name="pymarketcap",
        version = "3.9.009",
        url = "https://github.com/mondeja/pymarketcap",
        download_url = "https://github.com/mondeja/pymarketcap/archive/master.zip",
        author = "Álvaro Mondéjar",
        author_email = "mondejar1994@gmail.com",
        license = "BSD License",
        description = "Python3 API and web scraper for coinmarketcap.com.",
        long_description = LONG_DESC,
        keywords = ["coinmarketcap", "cryptocurrency", "API", "wrapper",
                    "scraper", "json", "BTC", "Bitcoin", "C", "Curl", "Cython"],
        install_requires = REQ,
        setup_requires = ["cython"],
        packages = find_packages(exclude=["precompiler"]),
        ext_modules=ext_modules,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Financial and Insurance Industry",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Office/Business",
            "Topic :: Office/Business :: Financial",
            "Topic :: Office/Business :: Financial :: Accounting",
            "Topic :: Office/Business :: Financial :: Investment",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        zip_safe = False,
        package_data={'pymarketcap': ['*.pxd', '*.pyx']},
        provides = ["setup_template_cython"],
    )
except Exception as e:
    print("INSTALL ERROR: %s" % e)
    run_unbuilder()
