<h1>pymarketcap</h1>

[![Build Status](https://travis-ci.org/mondeja/pymarketcap.svg?branch=master)](https://travis-ci.org/mondeja/pymarketcap) [![PyPI](https://img.shields.io/pypi/v/pymarketcap.svg)](https://pypi.python.org/pypi/pymarketcap) [![PyPI](https://img.shields.io/pypi/pyversions/pymarketcap.svg)](https://pypi.python.org/pypi/pymarketcap)

**pymarketcap** is library for retrieve data from [coinmarketcap](http://coinmarketcap.com/) API and website. Consist of a cythonized scraper and API wrapper built with curl C library. Actually, only works in Python≥3.5.

```diff
+ New version 3.9.0
- Some breaking changes have been introduced since 3.9.0 version. The old version (3.3.158) is still hosted at Pypi and will be there for a short period of time but won't be longer supported. Please, update to the new version, is faster, more accurate and has new features!
```

## Install

### Dependencies
You need to install [`cython`](http://cython.readthedocs.io/en/latest/src/quickstart/install.html), `gcc` compiler and [libcurl](https://curl.haxx.se/docs/install.html).

### Commands
```
pip3 install https://github.com/mondeja/pymarketcap/archive/master.zip
```

or install from source:

```
git clone https://github.com/mondeja/pymarketcap.git
cd pymarketcap
pip3 install -r requirements.txt
python setup.py install
```

## Documentation
All methods are currently only self explained in doctrings.

### [Testing and contributing](https://github.com/mondeja/pymarketcap/blob/master/CONTRIBUTING.md)

### [Changelog](https://github.com/mondeja/pymarketcap/blob/master/CHANGELOG.md)

_____________________________

### [License](https://github.com/mondeja/pymarketcap/blob/master/LICENSE.txt)

### Support
- Issue Tracker: https://github.com/mondeja/pymarketcap/issues
- If you want contact me → mondejar1994@gmail.com

_____________________________

#### Buy me a coffee?

If you feel like buying me a coffee (or a beer?), donations are welcome:

```
BTC: 1LnPPp7nEF7fHNMtHvVaEFNaHmPKji1uCo
BCH: qp40gr5y9usdyqh62hac7umvcqe5n2nc9vpff4der5
ETH: 0x3284674cC02d18395a00546ee77DBdaA391Aec23
LTC: LXSXiczN1ZYyf3WoeawraL7G1d31vVWgXK
STEEM: @mondeja
```
