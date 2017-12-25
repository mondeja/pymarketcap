<h1>pymarketcap</h1>

[![Build Status](https://travis-ci.org/mondeja/pymarketcap.svg?branch=master)](https://travis-ci.org/mondeja/pymarketcap) [![PyPI](https://img.shields.io/pypi/v/pymarketcap.svg)](https://pypi.python.org/pypi/pymarketcap)

**pymarketcap** is library for retrieve data from [coinmarketcap](http://coinmarketcap.com/) API and website. Consist of a scraper built on BeautifulSoup and an API wrapper powered by requests. Only works in Python3.

## Install

```
pip install pymarketcap
```

or install from source:

```
git clone https://github.com/mondeja/pymarketcap.git
cd pymarketcap
pip install -r requirements.txt
python setup.py install
```

## Documentation
All methods are self explained in doctrings. Also, you can see all available methods in action at [wiki page](https://github.com/mondeja/pymarketcap/wiki).

## Testing
```
pip3 install -r dev-requirements.txt
```

- All tests with benchmarking: `python3 test/test.py --with-timer -v`

> Benchmarking results for all unittests will be stored in `test/benchmarking.json`

- API unittests without benchmarking: `cd tests && nosetests units/test_api.py -v`
- Scraper unittest with benchmarking: `cd tests && nosetests units/test_scraper.py --with-timer -v`
- End to end API tests (takes a long time): `cd tests && python3 end2end/test_api.py`

You can see last online builds with tests at [TravisCI](https://travis-ci.org/mondeja/pymarketcap).


## Contribute

- Issue Tracker: https://github.com/mondeja/pymarketcap/issues
- Source Code: https://github.com/mondeja/pymarketcap

### Development progress:

|**Method**|**Developed**|**Documented**|**Tested**|
|:-------------------------|:-:|:-:|:-:|
|**API COMMANDS**                      |
|`symbols`                 | ✔ | ✔ | ✔ |
|`ticker`                  | ✔ | ✔ | ✔ |
|`stats`                   | ✔ | ✔ | ✔ |
|**SCRAPER COMMANDS**                  |
|`markets`                 | ✔ | ✔ | ✔ |
|`ranks`                   | ✔ | ✔ | ✔ |
|`historical`              | ✔ | ✔ | ✔ |
|`recently`                | ✔ | ✔ | ✔ |
|`exchange`                | ✔ | ✔ | ✔ |
|`exchanges`               | ✔ | ✔ | ✔ |
|`exchange_names`          | ✔ | ✔ | ✔ |
|`graphs.currency`         | ✔ | ✔ | ✔ |
|`graphs.global_cap`       | ✔ | ✔ | ✔ |
|`graphs.dominance`        | ✔ | ✔ | ✔ |
|`assets`                  | ✘ | ✘ | ✘ |

## Support

If you are having issues, please let me know (mondejar1994@gmail.com).


## License

Copyright (c) 2017 Álvaro Mondéjar Rubio <mondejar1994@gmail.com>.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation, advertising
materials, and other materials related to such distribution and use
acknowledge that the software was developed by Álvaro Mondéjar Rubio. The
name of the Álvaro Mondéjar Rubio may not be used to endorse or promote
products derived from this software without specific prior written
permission.

THIS SOFTWARE IS PROVIDED “AS IS” AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

### Buy me a coffee?

If you feel like buying me a coffee (or a beer?), donations are welcome:

```
BTC : 1LfUF4AcvH7Wd1wTc7Mmqobj4AypUbpvN5
ETH : 0x7428fE875226880DaD222c726F6340eec42Db567
STEEM: @mondeja
```
