<h1>pymarketcap</h1>

[![PyPi Version](http://img.shields.io/pypi/v/pymarketcap.svg)](https://pypi.python.org/pypi/pymarketcap/)

**pymarketcap** is an APACHE licensed library for retrieve information from [coinmarketcap](http://coinmarketcap.com/) API and web. Consist of a parser built on BeautifulSoup and a API wrapper. If you only want the API wrapper, go to [here](https://github.com/mondeja/coinmarketcap-api).

## Installation:

You need to install BeautifulSoup before:

    $ pip install bs4

From source use

    $ python setup.py install

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
