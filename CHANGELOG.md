## Changelog

### 3.9.0
- All the wrapper rewritten with Cython language.
- The data is obtained and processed by regular expressions instead of parsing the DOM.
- Core functionality of the wrapper rewritten for work with `libcurl` C library through a Cython bridge at compilation time.
- Tests now performed with `pytest` insted of standard library `unittest`.
- `request`, `lxml` and `bs4` dependencies removed, only `cython`, `gcc` and `libcurl` required for compile the code.
- A precompiler added for insert some code and documentation hardcoded before compile the program.
- All the data now is taken from values provided for the code that builds coinmarketcap instead the values displayed in the frontend page, as before. Is possible to select between USD or BTC to returns these in most methods.
- New method `convert()` for convert between currencies using exchange rates values used internally by coinmarketcap.
- New method `tokens()` convering partially https://coinmarketcap.com/tokens/views/all/ endpoint.
- Old method `download_log()` deprecated.

### 3.3.0
- New method `download_logo()` for download images for all coins in coinmarketcap.
- New methods for retrieve info from `graphs` coinmarketcap internal API.
- Some symbols recognition improvements and bugs fixed.

_____________________

Previous versions was minor and progressive changes.

This proyect is originally a fork from https://github.com/barnumbirr/coinmarketcap

