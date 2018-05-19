#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from shlex import split as parse
from subprocess import check_output
from setuptools import setup, find_packages
from setuptools.extension import Extension

def simple_call(command):
    try:
        return check_output(parse(command))
    except Exception as e:
        return 1

def spec_sys_calls(command):
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        command = [command, "sudo %s" % (command)]
    return [command]


def install_cython_via_pip():
    code = 1
    calls = spec_sys_calls("pip3 install Cython")[0]
    for i, command in enumerate(calls):
        code = simple_call(command)
        print(code)
        if i >= len(calls) or code == 0:
            break
    return code


try:
    from Cython.Build import cythonize
except ImportError:   # Cython required
    print("Cython not found. You need to install Cython before pymarketcap.")
    sys.exit(1)

CURR_DIR = os.path.dirname(__file__)
REQ_PATH = os.path.join(CURR_DIR, "requirements.txt")

code = 1
base_call = "pip3 install -r %s" % REQ_PATH
calls = spec_sys_calls(base_call)
for i, command in enumerate(calls):
    code = simple_call(command)
    if i >= len(calls) or code == 0:
        break

if code == 0:
    print("Dependencies installed sucessfully.")
else:
    print("Error installing dependencies, installing pymarketcap anywhere...")


# ===========  Precompiler  ===========
if not "sdist" in sys.argv:
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

# Check if minimum Python3.6
PYTHON_VERSION = sys.version_info
if PYTHON_VERSION < (3,6):
    if PYTHON_VERSION > (3,5):
        if "--quiet" not in sys.argv:
            while True:
                msg = "\nPython version:\n%s\n\nYou need " % sys.version \
                    + "to install almost Python3.6 in order to use " \
                    + "the asynchronous Pymarketcap interface.\n" \
                    + "Install pymarketcap without it anyway? Y/N: "
                cont = str(input(msg)).lower()
                if cont == "n":
                    print("Installation cancelled.")
                    sys.exit(0)
                    break
                elif cont != "y":
                    print("Invalid option.")
                else:
                    print("Installing pymarketcap...")
                    break
    else:
        print("You need almost Python3.5 version to install pymarketcap.")
        sys.exit(1)


# ===========  Cython compilation  ===========

COMPILE_CURL = True

# Windows
if sys.platform.startswith('win32') and "--force-curl" not in sys.argv:
    COMPILE_CURL = False

if "--force-curl" in sys.argv:
    sys.argv.remove("--no-curl")

                          # Building on ReadTheDocs (very crazy):
if "--no-curl" in sys.argv or os.environ.get("READTHEDOCS") == "True":
    COMPILE_CURL = False
    if "--no-curl" in sys.argv:
        sys.argv.remove("--no-curl")

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
    declare_cython_extension("pymarketcap.processer")
]

package_data={"pymarketcap": ["core.pyx", "processer.pyx"]}

if COMPILE_CURL:
    ext_modules.append(
        declare_cython_extension("pymarketcap.curl", libraries=["curl"])
    )
    package_data["pymarketcap"].extend(["curl.pyx", "curl.pxd"])
else:
    core_path = os.path.join(os.path.dirname(__file__),
                             "pymarketcap", "core.pyx")
    with open(core_path, "r") as f:
        content = f.readlines()

    for i, line in enumerate(content):
        if "from pymarketcap.curl import get_to_memory" in line:
            content[i] = line.replace("curl", "url")
            break

    with open(core_path, "w") as f:
        f.writelines(content)

ext_modules = cythonize(ext_modules)


# ===========  Package metadata  ===========

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    LONG_DESC = f.read()

with open(REQ_PATH, "r") as f:
    REQ = [line.strip("\n") for line in f.readlines()]

author, author_email = ("Álvaro Mondéjar Rubio", "mondejar1994@gmail.com")

install = setup(
    name = "pymarketcap",
    version = "4.0.006",
    url = "https://github.com/mondeja/pymarketcap",
    download_url = "https://github.com/mondeja/pymarketcap/archive/master.zip",
    author = author,
    maintainer = author,
    author_email = author_email,
    maintainer_email = author_email,
    platforms=['any'],
    license = "BSD License",
    description = "Python3 API and web scraper for coinmarketcap.com.",
    long_description = LONG_DESC,
    keywords = ["coinmarketcap", "cryptocurrency", "API", "wrapper",
                "scraper", "json", "BTC", "Bitcoin", "C", "Curl", "Cython"],
    install_requires = REQ,
    packages = find_packages(exclude=["precompiler"]),
    ext_modules = ext_modules,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: BSD License",
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
    zip_safe = True,
    provides = ["setup_template_cython"]
)

print(
    "\n%s v%s installation finished succesfully." \
    % (install.get_name().capitalize(), install.get_version())
)
