## Contributing guidelines
- Each new method developed needs to be accompanied with their respective complete unittest as is shown in `tests/` directory.
- Each new pull request needs to be good performed. Plase, don't make a pull request with 4 commits for change a line in the code.

### Testing
You need to install `pytest` for run unittests and `tox` for run tests against different versions:
```
pip3 install -r dev-requirements
```

You can run tests with `pytest` command:
- Run all unittests: `pytest tests`
- Run also end2end tests: `pytest tests --end2end`
- [Run individual tests](https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests):
    + Run API tests: `pytest tests/test_api`
    + Run `historical()` scraper method's consistence:
```
pytest tests/test_scraper/test_historical.py::test_consistence
```

> Also, if your system is Unix, you can use `make` for run tests, install, precompile/restore source code, build and clean the whole directory (see [`Makefile`](https://github.com/mondeja/pymarketcap/blob/master/Makefile)).

### Development progress:

|**Method**|**Developed**|**Documented**|**Tested**|
|:-------------------------|:-:|:-:|:-:|
|**INSTANCE ATTRIBUTES**               |
|`correspondences`         | ✔ | ✔ | ✔ |
|`symbols`                 | ✔ | ✔ | ✔ |
|`coins`                   | ✔ | ✔ | ✔ |
|`total_currencies`        | ✔ | ✔ | ✔ |
|`currencies_to_convert`   | ✔ | ✔ | ✔ |
|`converter_cache`         | ✔ | ✔ | ✔ |
|`exchange_names`          | ✔ | ✔ | ✔ |
|`exchange_slugs`          | ✔ | ✔ | ✔ |
|**PROPERTIES**                        |
|`ticker_badges`           | ✔ | ✔ | ✔ |
|`currency_exchange_rates` | ✔ | ✔ | ✔ |
|**API METHODS**                       |
|`ticker`                  | ✔ | ✔ | ✔ |
|`stats`                   | ✔ | ✔ | ✔ |
|**SCRAPER METHODS**                   |
|`convert`                 | ✔ | ✔ | ✔ |
|`markets`                 | ✔ | ✔ | ✔ |
|`ranks`                   | ✔ | ✔ | ✔ |
|`historical`              | ✔ | ✔ | ✔ |
|`recently`                | ✔ | ✔ | ✔ |
|`exchange`                | ✔ | ✔ | ✔ |
|`exchanges`               | ✔ | ✔ | ✔ |
|`tokens`                  | ✘ | ✘ | ✘ |
|**GRAPHS API METHODS**                |
|`graphs.currency`         | ✔ | ✔ | ✔ |
|`graphs.global_cap`       | ✔ | ✔ | ✔ |
|`graphs.dominance`        | ✔ | ✔ | ✔ |
|**INTERNAL**                          |
|`_is_symbol`              | ✔ | ✔ | ✔ |
|`_cache_symbols`          | ✔ | ✔ | ✔ |


## TODO:
- [ ] Write a benchmarking suite for all methods with and without params.
- [ ] Write documentation and upload to read the docs.
- [ ] Write a live demo for all methods.
- [x] Add `tokens` method covering https://coinmarketcap.com/tokens/views/all/ endpoint.
- [x] Write `CHANGELOG.md`.
- [ ] Write again [`download_logo()` old method](https://github.com/mondeja/pymarketcap/commit/c8848d368435b03c51f1885857255446a1ed8889).

_____________________________

#### How does pymarketcap works in depth?
- Some pieces of code are precompiled before compile with Cython, so if you see missing parts on the source code before install (like the property method `ticker_badges`), understand that they aren't bugs.
- The numerical values returned by the scraper are the real values with which coinmarketcap.com works, not the values displayed on their frontend (see source HTML code of the web).
- Several methods are cached at instantiation time, so they can be obtained later without perform more HTTP requests.