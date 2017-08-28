<h1>pymarketcap</h1>

[![PyPi Version](http://img.shields.io/pypi/v/pymarketcap.svg)](https://pypi.python.org/pypi/pymarketcap/)

**pymarketcap** is an APACHE licensed library for retrieve information from [coinmarketcap](http://coinmarketcap.com/) API and web. Consist of a scraper built on BeautifulSoup and an API wrapper. Only tested in Python3.

## Installation:

You need to install BeautifulSoup and requests before:

    $ pip3 install bs4
    $ pip3 install requests

From source use

    $ git clone https://github.com/mondeja/pymarketcap.git
    $ cd pymarketcap
    $ python3 setup.py install

## Documentation:

### API methods

- **`GET /v1/ticker/`**
- **`GET /v1/ticker/currency`**

```python
>>> from pymarketcap import *       # Only contains the class Pymarketcap
>>> coinmarketcap = Pymarketcap()
>>> coinmarketcap.ticker(<currency>)
# <currency> can be passed through 'ethereum' or 'ETH' and returns in json

>>> coinmarketcap.ticker('ETH')
>>> coinmarketcap.ticker('ethereum')

# Add VERBOSE=True or V=True for a string response, like this:
>>> coinmarketcap.ticker('STEEM', V=True)

# This is for receive all the currencies in a string
>>> coinmarketcap.ticker(VERBOSE=True)

# This is for convert the price in response
# (Only works if you pass a currency)
>>> coinmarketcap.ticker('NXT', convert='EUR') 

# This is for limit the amount of currencies:
# (Only works if you don't pass a currency)
>>> coinmarketcap.ticker(limit=10)

[
  {
    id: "bitcoin",
    name: "Bitcoin",
    symbol: "BTC",
    rank: 1,
    price_usd: 448.66,
    24h_volume_usd: 84396000,
    market_cap_usd: 6946212888,
    available_supply: 15482200,
    total_supply: 15482200,
    percent_change_1h: 0.47,
    percent_change_24h: -1.61,
    percent_change_7d: 1.25
  },
  {
    id: "ethereum",
    name: "Ethereum",
    symbol: "ETH",
    rank: 2,
    price_usd: 7.28,
    24h_volume_usd: 13419600,
    market_cap_usd: 578917949,
    available_supply: 79512085,
    total_supply: 79512085,
    percent_change_1h: 0.21,
    percent_change_24h: -6.51,
    percent_change_7d: -14.64
  },

  ...
]			
```


- **`GET /v1/global/`**

```python
>>> coinmarketcap.stats(VERBOSE=True)
{
  total_market_cap_usd: 8280726727,
  total_24h_volume_usd: 108644044,
  bitcoin_percentage_of_market_cap: 81.77,
  active_currencies: 690,
  active_assets: 57,
  active_markets: 1902
}		
```


### Web Parser methods

#### [Currency markets](http://coinmarketcap.com/currencies/<currency>/#markets)

- **`GET http://coinmarketcap.com/currencies/<currency>/#markets`**


```python
>>> coinmarketcap.markets('ETH', V=True)

[
  {
    "pair": "ETH/BTC", 
    "source": "Poloniex", 
    "percent_volume": 29.72, 
    "price_usd": 49.07, 
    "24h_volume_usd": 35779900
  }, 
  {
    "pair": "ETH/USD", 
    "source": "GDAX", 
    "percent_volume": 8.22, 
    "price_usd": 49.99, 
    "24h_volume_usd": 9897980
  }, 
  {
    "pair": "ETH/USD", 
    "source": "Bitfinex", 
    "percent_volume": 7.98, 
    "price_usd": 49.45, 
    "24h_volume_usd": 9606490
  }, 

 ...
]
```


#### [Global ranks](http://www.coinmarketcap.com/gainers-losers/)

- **`GET http://www.coinmarketcap.com/gainers-losers/`**

```python
>>> coinmarketcap.ranks(V=True)

{
  "losers": {
    "1h": [
      {
        "24h_volume_usd": 15219, 
        "symbol": "XEN", 
        "price_usd": 0.327427, 
        "percent_change": -24.28, 
        "name": "Xenixcoin"
      }, 
      {
        "24h_volume_usd": 818024, 
        "symbol": "PINK", 
        "price_usd": 0.002168, 
        "percent_change": -18.3, 
        "name": "PinkCoin"
      },
      ...

# You can pass '7d', '24h', '1h', 'gainers' and 'losers' for filter responses:
coinmarketcap.ranks('gainers', '1h', V=True)

{
  "1h": [
    {
      "24h_volume_usd": 62719, 
      "symbol": "NOBL", 
      "price_usd": 0.00024, 
      "percent_change": 18.99, 
      "name": "NobleCoin"
    }, 
    {
      "24h_volume_usd": 22355, 
      "symbol": "RDD", 
      "price_usd": 5.5e-05, 
      "percent_change": 17.72, 
      "name": "ReddCoin"
    }, 
    {
      "24h_volume_usd": 12723, 
      "symbol": "BOLI", 
      "price_usd": 0.003156, 
      "percent_change": 15.83, 
      "name": "Bolivarcoin"
    }, 
...
```

#### [Historical data](https://coinmarketcap.com/currencies/bitcoin/historical-data/)

- **`GET https://coinmarketcap.com/currencies/<currency>/historical-data/?start=<start_time>&end=<end_time>`**

```python
>>> coinmarketcap.historical('STEEM', 20170131, 20170825)

# First argument is the currency. Second and third are start and end 
#       times for retrieve the data in the form yearmonthday

[
  {datetime.datetime(2017, 8, 25, 0, 0): {'low': 1.26, 
                                         'usd_market_cap': 306485000, 
                                         'open': 1.28, 
                                         'high': 1.37, 
                                         'close': 1.37, 
                                         'usd_volume': 1456350}
                                         }, 
  {datetime.datetime(2017, 8, 24, 0, 0): {'low': 1.2, 
                                         'usd_market_cap': 295147000, 
                                         'open': 1.23, 
                                         'high': 1.33, 
                                         'close': 1.28, 
                                         'usd_volume': 1958180}
                                         }, 
  {datetime.datetime(2017, 8, 23, 0, 0): {'low': 1.19, 
                                         'usd_market_cap': 289363000, 
                                         'open': 1.21, 
                                         'high': 1.31, 
                                         'close': 1.24, 
                                         'usd_volume': 2415700}
                                         }, 
  ...
]

```

#### [Recently added](https://coinmarketcap.com/new/)

- **`GET https://coinmarketcap.com/new/`**

```python
>>> coinmarketcap.recently()


[
  {'days_ago': 1, 
  'price_usd': 0.150346, 
  'market_cap': '?', 
  'volume_24h_usd': 9154, 
  'name': 'AdCoin', 
  'symbol': 'ACC', 
  'mineable': False, 
  'circulating_supply': '?'}, 
  
  {'days_ago': 2, 
  'price_usd': 0.029002, 
  'market_cap': '?', 
  'volume_24h_usd': 13658, 
  'name': 'OX Fina', 
  'symbol': 'OX', 
  'mineable': True, 
  'circulating_supply': '?'},
  
  {'days_ago': 2, 
  'price_usd': 4.3e-05, 
  'market_cap': '?', 
  'volume_24h_usd': 4945, 
  'name': 'Protean', 
  'symbol': 'PRN', 
  'mineable': True, 
  'circulating_supply': '?'},
  
  ...
]

```


#### [Exchange](https://coinmarketcap.com/exchanges/poloniex/)

- **`GET https://coinmarketcap.com/exchanges/<exchange>/`**

```python
>>> coinmarketcap.exchange('poloniex')


[
  {'perc_volume': 32.08, 
  'price_usd': 136.66, 
  'name': 'Monero', 
  'volume_24h_usd': 124742000, 
  'market': 'XMR/BTC', 
  'volume_rank': 1}, 
  
  {'perc_volume': 8.17, 
  'price_usd': 328.77, 
  'name': 'Ethereum', 
  'volume_24h_usd': 31765800, 
  'market': 'ETH/BTC', 
  'volume_rank': 2},
  
  {'perc_volume': 7.94, 
  'price_usd': 0.210747, 
  'name': 'Ripple', 
  'volume_24h_usd': 30864200, 
  'market': 'XRP/BTC', 
  'volume_rank': 3},
  
  ...
]
```


#### [Exchanges](https://coinmarketcap.com/exchanges/volume/24-hour/all/)

- **`GET https://coinmarketcap.com/exchanges/volume/24-hour/all/`**

```python
>>> coinmarketcap.exchanges(limit=3)

# Admits an argument for limit the amount of exchanges (default == 50)

[
  {'rank': 1, 
  'markets': [
               {'rank': 1, 
               'price_usd': 377.74, 
               'volume_24h_usd': 134254000, 
               'perc_change': 30.56, 
               'market': 'DASH/KRW'}, 
               
               {'rank': 2, 
               'price_usd': 0.21399, 
               'volume_24h_usd': 80827100, 
               'perc_change': 18.4, 
               'market': 'XRP/KRW'}, 
               
               {'rank': 3, 
               'price_usd': 333.56, 
               'volume_24h_usd': 75882000, 
               'perc_change': 17.27, 
               'market': 'ETH/KRW'}, 
               
               {'rank': 4, 
               'price_usd': 633.5, 
               'volume_24h_usd': 62741200, 
               'perc_change': 14.28, 
               'market': 'BCH/KRW'}, 
               
               {'rank': 5, 
               'price_usd': 4353.8, 
               'volume_24h_usd': 40231500, 
               'perc_change': 9.16, 
               'market': 'BTC/KRW'}, 
               
               {'rank': 6, 
               'price_usd': 51.61, 
               'volume_24h_usd': 31873700, 
               'perc_change': 7.26, 
               'market': 'LTC/KRW'}, 
               
               {'rank': 7, 
               'price_usd': 15.35, 
               'volume_24h_usd': 13454900, 
               'perc_change': 3.06, 
               'market': 'ETC/KRW'}, 
             ], 
   'volume_usd': 439264400, 
   'name': 'bithumb'},
 ...
]

```


## License:

```
  Apache v2.0 License
  Copyright 2017 Álvaro Mondéjar

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

```

## Buy me a coffee?

If you feel like buying me a coffee (or a beer?), donations are welcome:

```
BTC : 1LfUF4AcvH7Wd1wTc7Mmqobj4AypUbpvN5
ETH : 0x7428fE875226880DaD222c726F6340eec42Db567
STEEM: @mondeja
```
